# Samsara "Trips and Stops" Report — Build Plan V2

## Architecture Decision

**Phase 1 (Build Now)**: Pure Retool — Samsara REST API called directly from Retool queries. No Python, no Supabase. Deliverable is an importable Retool app JSON file.

**Phase 2 (Upgrade Later)**: Add Supabase + Trigger.dev or Prefect for scheduled sync. The core JS transformer code is **zero-rework** — only the query data sources change.

---

## Why NOT Webhooks or Historical Locations API

- **GeofenceEntry/Exit webhooks**: Real-time push events only — they fire NOW when vehicles cross boundaries. Useless for querying past trip data on demand. Skip.
- **Historical Locations API** (GPS breadcrumbs): Not needed — the Trips API already provides start/end addresses per trip. Historical Locations only adds value if you need sub-trip GPS tracking.
- **The three endpoints you actually need**: Trips + Idling Events + Addresses.

---

## Target Report Layout (from verizon time on site report.png)

**Header**: Vehicle name | Driver name

**Per date section** (grouped by local date):
1. `start_header` row — "Starting from: [address]" (red if matches saved address)
2. `trip` rows — Start Time | Distance+Duration | Stop Location | Arrival Time | Idle Duration | Stop Duration
   - Stop Location: red `[address]` if matches saved Samsara address, plain text otherwise
   - Last trip of day: Stop Duration = `--`
3. `total` row — `MM/DD/YYYY | Total | X miles in Yh Zm | — | total idle | total stops | N stops`

---

## Phase 1: Pure Retool — What Gets Built

### Retool App Components

| Component | Type | Purpose |
|-----------|------|---------|
| `vehicleSelect` | Select | Choose vehicle to report on |
| `datePicker` | Date Range Picker | Choose start/end date |
| `btnRun` | Button | Triggers report fetch |
| `txtHeader` | Text | Shows "Vehicle Name — Driver Name" |
| `tblReport` | Table | Main report table, grouped by `trip_date` |

### Samsara REST API Resource (user creates once)
- Resource name: `Samsara`
- Base URL: `https://api.samsara.com`
- Auth header: `Authorization: Bearer {{samsara_api_key}}`
- Store API key in Retool Environment Secrets

### Four Queries

**`qGetVehicles`** (runs on page load):
```
GET /fleet/vehicles
```

**`qGetAddresses`** (runs on page load):
```
GET /addresses
```

**`qGetTrips`** (runs on btnRun click):
```
GET /v1/fleet/trips
vehicleId: {{ vehicleSelect.value }}
startMs:   {{ datePicker.startDate.getTime() }}   ← epoch milliseconds (v1 API)
endMs:     {{ datePicker.endDate.getTime() }}
```

**`qGetIdlingEvents`** (runs on btnRun click):
```
GET /fleet/idlingEvents
vehicleIds: {{ vehicleSelect.value }}
startTime:  {{ datePicker.startDate.toISOString() }}   ← ISO 8601 (v2 API)
endTime:    {{ datePicker.endDate.toISOString() }}
```

### JS Transformer: `transformReportData`

Full transformer code (paste into Retool transformer or embedded in app JSON):

```javascript
// ─── CONFIG — change this to match your fleet's timezone ───────────────────
const FLEET_TIMEZONE = 'America/New_York';
// ───────────────────────────────────────────────────────────────────────────

// ─── Helpers ───────────────────────────────────────────────────────────────

function formatDuration(totalSeconds) {
  if (totalSeconds == null) return '--';
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  if (h > 0) return `${h}h ${String(m).padStart(2,'0')}m`;
  return `${String(m).padStart(2,'0')}m ${String(s).padStart(2,'0')}s`;
}

function haversineMeters(lat1, lon1, lat2, lon2) {
  const R = 6_371_000;
  const toRad = d => d * Math.PI / 180;
  const dLat = toRad(lat2 - lat1), dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat/2)**2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function findMatchingAddress(lat, lon, addressRaw, savedAddresses) {
  for (const addr of savedAddresses) {
    if (addr.latitude && addr.longitude) {
      const dist = haversineMeters(lat, lon, addr.latitude, addr.longitude);
      if (dist <= (addr.radius_meters || 200)) return addr;
    }
  }
  const raw = (addressRaw || '').toLowerCase().trim();
  return savedAddresses.find(a => (a.formatted_address || '').toLowerCase().trim() === raw) || null;
}

function toLocalDateString(epochMs) {
  return new Date(epochMs).toLocaleDateString('en-US', {
    timeZone: FLEET_TIMEZONE, year: 'numeric', month: '2-digit', day: '2-digit'
  });
}

function toLocalTimeString(epochMs) {
  return new Date(epochMs).toLocaleTimeString('en-US', {
    timeZone: FLEET_TIMEZONE, hour: 'numeric', minute: '2-digit', hour12: true
  });
}

// ─── Normalize Samsara API responses ───────────────────────────────────────

const trips = (qGetTrips.data.trips || []).map(t => ({
  id:                 t.id,
  start_time_ms:      t.startMs,
  end_time_ms:        t.endMs,
  distance_meters:    t.distanceMeters,
  start_address_raw:  t.startAddress,
  end_address_raw:    t.endAddress,
  start_lat:          t.startCoordinates?.latitude,
  start_lng:          t.startCoordinates?.longitude,
  end_lat:            t.endCoordinates?.latitude,
  end_lng:            t.endCoordinates?.longitude,
  driver_id:          t.driverId,
}));

const idling = (qGetIdlingEvents.data.data || []).map(e => ({
  start_time_ms:    new Date(e.startTime).getTime(),
  end_time_ms:      new Date(e.endTime).getTime(),
  duration_seconds: e.durationMs ? Math.floor(e.durationMs / 1000) : 0,
}));

const addresses = (qGetAddresses.data.data || []).map(a => ({
  id:                a.id,
  name:              a.name,
  formatted_address: a.formattedAddress,
  latitude:          a.latitude,
  longitude:         a.longitude,
  radius_meters:     a.geofence?.circle?.radius || 200,
}));

// ─── Core logic ────────────────────────────────────────────────────────────

function getIdleForTrip(trip) {
  return idling
    .filter(e => e.start_time_ms >= trip.start_time_ms && e.start_time_ms <= trip.end_time_ms)
    .reduce((sum, e) => sum + e.duration_seconds, 0);
}

const sorted = [...trips].sort((a, b) => a.start_time_ms - b.start_time_ms);

const byDate = {};
for (const trip of sorted) {
  const d = toLocalDateString(trip.start_time_ms);
  (byDate[d] = byDate[d] || []).push(trip);
}

const rows = [];

for (const [dateStr, dayTrips] of Object.entries(byDate).sort()) {
  let dayMiles = 0, dayDriveSecs = 0, dayIdleSecs = 0, dayStopSecs = 0;

  // Starting from row
  const first = dayTrips[0];
  const startMatch = findMatchingAddress(first.start_lat, first.start_lng, first.start_address_raw, addresses);
  rows.push({
    row_type: 'start_header',
    trip_date: dateStr,
    stop_location_raw: first.start_address_raw,
    stop_is_geofence: !!startMatch,
    stop_geofence_name: startMatch?.name || null,
  });

  // Trip rows
  for (let i = 0; i < dayTrips.length; i++) {
    const trip = dayTrips[i];
    const next = dayTrips[i + 1] || null;
    const driveSecs     = Math.round((trip.end_time_ms - trip.start_time_ms) / 1000);
    const distMiles     = parseFloat((trip.distance_meters / 1609.344).toFixed(2));
    const idleSecs      = getIdleForTrip(trip);
    const stopSecs      = next ? Math.max(0, Math.round((next.start_time_ms - trip.end_time_ms) / 1000)) : null;
    const endMatch      = findMatchingAddress(trip.end_lat, trip.end_lng, trip.end_address_raw, addresses);

    dayMiles     += distMiles;
    dayDriveSecs += driveSecs;
    dayIdleSecs  += idleSecs;
    if (stopSecs != null) dayStopSecs += stopSecs;

    rows.push({
      row_type:               'trip',
      trip_date:              dateStr,
      trip_id:                trip.id,
      start_time_display:     toLocalTimeString(trip.start_time_ms),
      distance_miles:         distMiles,
      drive_duration_display: formatDuration(driveSecs),
      stop_location_raw:      trip.end_address_raw,
      stop_is_geofence:       !!endMatch,
      stop_geofence_name:     endMatch?.name || null,
      arrival_time_display:   toLocalTimeString(trip.end_time_ms),
      idle_duration_display:  formatDuration(idleSecs),
      stop_duration_display:  stopSecs != null ? formatDuration(stopSecs) : '--',
    });
  }

  // Daily totals row
  rows.push({
    row_type:               'total',
    trip_date:              dateStr,
    stop_count:             dayTrips.length,
    distance_miles:         parseFloat(dayMiles.toFixed(2)),
    idle_duration_display:  formatDuration(dayIdleSecs),
    stop_duration_display:  formatDuration(dayStopSecs),
    totals_label:           `${parseFloat(dayMiles.toFixed(2))} miles in ${formatDuration(dayDriveSecs)}`,
  });
}

return rows;
```

### Table Column Expressions

**Start Time column** (mapped value):
```javascript
{{ currentRow.row_type !== 'total' && currentRow.row_type !== 'start_header' ? currentRow.start_time_display : '' }}
```

**Distance / Duration column** (mapped value):
```javascript
{{ currentRow.row_type === 'total' ? currentRow.totals_label : currentRow.distance_miles + ' mi  •  ' + currentRow.drive_duration_display }}
```
Color expression: `{{ currentRow.row_type === 'trip' ? '#e6820e' : 'inherit' }}`

**Stop Location column** (custom HTML):
```javascript
if (currentRow.row_type === 'start_header') {
  const a = currentRow.stop_is_geofence
    ? `<span style="color:red">[${currentRow.stop_location_raw}]</span><br/>${currentRow.stop_location_raw}`
    : (currentRow.stop_location_raw || '');
  return `<span style="font-style:italic">Starting from:</span> ${a}`;
}
if (currentRow.row_type === 'total') {
  return `<strong>Total — ${currentRow.stop_count} stops</strong>`;
}
if (currentRow.stop_is_geofence) {
  return `<span style="color:red">[${currentRow.stop_location_raw}]</span><br/>${currentRow.stop_location_raw}`;
}
return currentRow.stop_location_raw || '';
```

**Arrival Time column**: `{{ currentRow.arrival_time_display || '' }}`

**Idle Duration column**: `{{ currentRow.idle_duration_display || '' }}`

**Stop Duration column**: `{{ currentRow.stop_duration_display || '' }}`

**Row background color** (table row color expression):
```javascript
{{ currentRow.row_type === 'total' ? '#f0f0f0' : currentRow.row_type === 'start_header' ? '#f9f9f9' : 'white' }}
```

---

## Deliverable File

**`samsara_trips_report.json`** — complete importable Retool app

Encodes: all 4 queries, JS transformer, table with all column config, HTML rendering, row colors, filter bar components.

Import via: **Retool → Create App → Import from JSON**

### After Import — Two Things to Configure

1. **Create Samsara REST API resource** (one time, in Retool's Resources panel):
   - Resource type: REST API
   - Name: `Samsara`
   - Base URL: `https://api.samsara.com`
   - Header: `Authorization` = `Bearer YOUR_API_KEY`

2. **Set timezone** in the transformer (line 2 of `transformReportData`):
   ```javascript
   const FLEET_TIMEZONE = 'America/New_York'; // ← change this
   ```

**Note on JSON compatibility**: Retool's import JSON schema evolves between versions. The file is written to current best knowledge. If a query or component doesn't load correctly after import, the individual code/expression snippets above can be copy-pasted manually into the relevant Retool panels.

---

## Phase 2 Upgrade Path

### What changes (in Retool)
1. Add Supabase PostgreSQL resource
2. Replace `qGetTrips`, `qGetIdlingEvents`, `qGetAddresses` with Supabase SQL queries (same field names in output)

### What is zero rework
- `transformReportData` JS transformer — identical, no changes
- All table columns, expressions, row styling
- All filter bar components

### ETL job (Trigger.dev or Prefect) — nightly sync
1. Fetch Samsara vehicles, drivers, addresses → upsert Supabase
2. For each vehicle: fetch yesterday's trips → upsert, run address matching, populate `end_address_id`
3. Fetch yesterday's idling events → upsert, link to parent trips by time overlap

### Phase 2 Supabase queries (replace the REST API calls)
```sql
-- qGetTrips
SELECT id,
       EXTRACT(EPOCH FROM start_time)*1000 AS start_time_ms,
       EXTRACT(EPOCH FROM end_time)*1000   AS end_time_ms,
       distance_meters, start_address_raw, end_address_raw,
       start_lat, start_lng, end_lat, end_lng, driver_id
FROM trips
WHERE vehicle_id = {{ vehicleSelect.value }}
  AND trip_date BETWEEN {{ datePicker.startDate }} AND {{ datePicker.endDate }}
ORDER BY start_time;

-- qGetIdlingEvents
SELECT trip_id,
       SUM(EXTRACT(EPOCH FROM (end_time - start_time))::int) AS duration_seconds,
       MIN(EXTRACT(EPOCH FROM start_time)*1000)::bigint       AS start_time_ms
FROM idling_events
WHERE vehicle_id = {{ vehicleSelect.value }}
  AND start_time BETWEEN {{ datePicker.startDate }} AND {{ datePicker.endDate }}
GROUP BY trip_id;

-- qGetAddresses (unchanged — same query works for Supabase)
SELECT id, name, formatted_address, latitude, longitude, radius_meters FROM addresses;
```

---

## Key Edge Cases

| Issue | Handled by |
|-------|-----------|
| Multiple idling events per trip | `filter + reduce` in `getIdleForTrip()` |
| Last trip stop duration = `--` | `next === null` → `stopSecs = null` → `'--'` |
| Historical geofence matching | `findMatchingAddress`: haversine distance + radius, string fallback |
| Timezone date grouping | `toLocalDateString()` uses `FLEET_TIMEZONE` |
| No driver assigned | `driver_id: null` passes through; display "Unassigned" in header |
| v1 trips API uses epoch ms | Explicit mapping: `t.startMs`, `t.endMs` |
| v2 idling API uses ISO 8601 | Explicit mapping: `new Date(e.startTime).getTime()` |
| Large date range (>2 weeks) | Slower in Phase 1 (direct API); fixed by Supabase cache in Phase 2 |
| Samsara API pagination | Add `after` cursor loop if paginated response detected |
