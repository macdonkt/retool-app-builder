# Retool Setup Instructions — Samsara Trips Report

## Step 1: Create the Samsara REST API Resource

Do this **once** in Retool before importing the app.

1. Go to **Resources** in the Retool left sidebar
2. Click **Create new** → **REST API**
3. Configure:
   - **Name**: `Samsara` ← must match exactly (the JSON references this name)
   - **Base URL**: `https://api.samsara.com`
   - Under **Headers**, add one header:
     - Key: `Authorization`
     - Value: `Bearer YOUR_API_KEY_HERE`
4. Click **Save**

> To get your Samsara API key: Samsara Dashboard → Settings → API Tokens → Create Token

---

## Step 2: Import the App

1. In Retool, click **Create new app**
2. Choose **Import from JSON**
3. Upload `samsara_trips_report.json`
4. The app will appear with all queries and components pre-configured

---

## Step 3: Set Your Fleet Timezone

Open the `transformReportData` transformer (in the Query panel, left side) and change **line 2**:

```javascript
const FLEET_TIMEZONE = 'America/New_York';  // ← change this
```

Common US timezone strings:
- `'America/New_York'` — Eastern
- `'America/Chicago'` — Central
- `'America/Denver'` — Mountain
- `'America/Los_Angeles'` — Pacific

This controls how dates are grouped (so a 11:30 PM UTC trip shows under the correct local date) and how times display in the report.

---

## Step 4: Run the Report

1. Select a vehicle from the **Vehicle** dropdown (populates from Samsara on page load)
2. Set a **Date Range** with the date picker
3. Click **Run Report**

The report fetches trips and idling events from Samsara, then the transformer builds the table rows.

---

## If the Import Doesn't Load Correctly

Retool's JSON schema can vary between versions. If some queries or columns don't load after import, use the code below to manually configure them.

### Manual Query Setup

Create these 4 queries in Retool using the Samsara REST resource:

| Query name | Method | Path | Trigger |
|---|---|---|---|
| `qGetVehicles` | GET | `/fleet/vehicles` | On page load |
| `qGetAddresses` | GET | `/addresses` | On page load |
| `qGetTrips` | GET | `/v1/fleet/trips` | Manual |
| `qGetIdlingEvents` | GET | `/fleet/idlingEvents` | Manual |

**`qGetTrips` query parameters:**
```
vehicleId  =  {{ vehicleSelect.value }}
startMs    =  {{ datePicker.startDate ? new Date(datePicker.startDate).getTime() : '' }}
endMs      =  {{ datePicker.endDate ? new Date(datePicker.endDate).getTime() : '' }}
```

**`qGetIdlingEvents` query parameters:**
```
vehicleIds  =  {{ vehicleSelect.value }}
startTime   =  {{ datePicker.startDate ? new Date(datePicker.startDate).toISOString() : '' }}
endTime     =  {{ datePicker.endDate ? new Date(datePicker.endDate).toISOString() : '' }}
```

Create a **Transformer** named `transformReportData` and paste in the full transformer code from [Samsara Retool Report Build Plan V2.md](Samsara%20Retool%20Report%20Build%20Plan%20V2.md).

### Manual Table Column Config

Create a **Table** component connected to `{{ transformReportData.data }}` with these columns:

| Column title | Mapped value expression | Notes |
|---|---|---|
| START TIME | `{{ currentRow.row_type !== 'total' && currentRow.row_type !== 'start_header' ? currentRow.start_time_display : '' }}` | |
| DISTANCE (MILES) / DURATION | `{{ currentRow.row_type === 'total' ? currentRow.totals_label : currentRow.row_type === 'start_header' ? '' : currentRow.distance_miles + ' mi  •  ' + currentRow.drive_duration_display }}` | Color: `{{ currentRow.row_type === 'trip' ? '#e6820e' : 'inherit' }}` |
| STOP LOCATION | *(HTML column — see code below)* | Enable HTML rendering |
| ARRIVAL TIME | `{{ currentRow.row_type === 'trip' ? currentRow.arrival_time_display : '' }}` | |
| IDLE DURATION | `{{ currentRow.idle_duration_display \|\| '' }}` | |
| STOP DURATION | `{{ currentRow.stop_duration_display \|\| '' }}` | |

**Stop Location HTML expression:**
```javascript
{{
  (function() {
    var row = currentRow;
    if (row.row_type === 'start_header') {
      var addr = row.stop_is_geofence
        ? '<span style="color:red">[' + row.stop_location_raw + ']</span><br/>' + row.stop_location_raw
        : (row.stop_location_raw || '');
      return '<span style="font-style:italic">Starting from:</span> ' + addr;
    }
    if (row.row_type === 'total') {
      return '<strong>Total — ' + row.stop_count + ' stops</strong>';
    }
    if (row.stop_is_geofence) {
      return '<span style="color:red">[' + row.stop_location_raw + ']</span><br/>' + row.stop_location_raw;
    }
    return row.stop_location_raw || '';
  })()
}}
```

**Row background color** (in table's "Row color" property):
```javascript
{{ currentRow.row_type === 'total' ? '#f0f0f0' : currentRow.row_type === 'start_header' ? '#f9f9f9' : '#ffffff' }}
```

**Group rows by**: `trip_date`

---

## Troubleshooting

**"vehicleSelect is not defined" in qGetTrips**: The query ran before the vehicle dropdown loaded. Set `qGetTrips` trigger to **Manual** (not On page load).

**All idling durations show 0**: The Samsara idling events API may return `durationMs` in a different field. Open `qGetIdlingEvents`, check the raw response, and update the transformer line:
```javascript
duration_seconds: e.durationMs ? Math.floor(e.durationMs / 1000) : 0,
```
to use whatever field name appears in the response.

**Stop locations not showing red brackets**: The addresses endpoint returned no data, or the geofence radius is too small. Check `qGetAddresses.data` has results. Default radius fallback is 200 meters — adjust in the transformer:
```javascript
radius_meters: (a.geofence && a.geofence.circle) ? a.geofence.circle.radius : 200,
//                                                                              ↑ increase if needed
```

**Dates grouping incorrectly (trips on wrong day)**: Change `FLEET_TIMEZONE` in the transformer to match your fleet's actual timezone.

**Empty report after clicking Run**: Check that both `qGetTrips` and `qGetIdlingEvents` completed successfully (green check in query panel). If trips returned data but `transformReportData` is empty, open the transformer and check the browser console for errors.
