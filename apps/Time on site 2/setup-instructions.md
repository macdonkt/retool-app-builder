# Samsara Trips & Stops Report — Setup Instructions

## Import the App

1. In Retool, click **Create new** → **Import an app**
2. Upload `samsara_trips_report.json`
3. Name the app (e.g., "Trips & Stops Report")

---

## Step 1: Create the Samsara REST API Resource

Do this once in **Retool → Resources → Create new resource**:

| Setting | Value |
|---------|-------|
| Resource type | REST API |
| Name | `Samsara` ← must be exactly this |
| Base URL | `https://api.samsara.com` |
| Header key | `Authorization` |
| Header value | `Bearer YOUR_API_KEY` |

Replace `YOUR_API_KEY` with your Samsara API token.

**Alternative (recommended):** Store the key in Retool Environment Secrets as `SAMSARA_API_KEY` and set the header value to `Bearer {{ secret.SAMSARA_API_KEY }}`.

---

## Step 2: Set Your Fleet Timezone

Open the app editor and find the **`transformReportData`** JavaScript query.

Change line 1:
```javascript
const FLEET_TIMEZONE = 'America/New_York';
```

Common values:
- `'America/New_York'` — Eastern
- `'America/Chicago'` — Central
- `'America/Denver'` — Mountain
- `'America/Los_Angeles'` — Pacific

---

## Using the App

1. **Select vehicles** — pick one or more from the multi-select dropdown
2. **Pick date range** — select start and end dates
3. **Click Run Report** — fetches trips, idling events, and address data

### Report Layout

Each vehicle's section shows:
- **Vehicle header row** — Name (VIN) — Driver: Name (blue tint)
- **Starting from** row — first location of the day (gray tint)
- **Trip rows** — start time, distance/duration (orange), stop location, arrival time, idle, stop duration
- **Daily total row** — mileage, drive time summary, totals (gray)

Geofence locations (matching saved Samsara addresses) appear in **red brackets**.

---

## Troubleshooting

**Vehicles don't load on page open**
- Check that the `Samsara` resource exists with correct base URL and auth header

**"No vehicles selected" warning**
- Select at least one vehicle from the dropdown before clicking Run Report

**Report shows no data**
- Verify the date range has trips for the selected vehicle(s)
- Check Samsara API key has read access to `/v1/fleet/trips` and `/fleet/idlingEvents`

**Addresses not showing in red**
- Addresses must be saved in Samsara (fleet → Addresses) to match
- The transformer matches by GPS radius (default 200m) then falls back to exact address string match
