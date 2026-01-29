# Hotel Search App V2 - Setup Instructions

## Overview

This version uses the **Booking.com API** for real-time hotel pricing, availability, and direct booking links.

## Prerequisites

- Retool account (self-hosted or cloud)
- RapidAPI account with valid API key

---

## Step 1: RapidAPI Setup

### 1.1 Create RapidAPI Account
1. Go to [rapidapi.com](https://rapidapi.com)
2. Sign up or log in

### 1.2 Subscribe to Required APIs

**Booking.com API** (for hotel search with real pricing):
1. Navigate to [Booking.com API](https://rapidapi.com/DataCrawler/api/booking-com15)
2. Click "Subscribe" and select a plan
3. Free tier: ~500 requests/month
4. **This provides**: Real-time prices, availability, booking links, review scores

**Forward Reverse Geocoding API** (for address lookup):
1. Navigate to [Forward Reverse Geocoding API](https://rapidapi.com/GeocodeSupport/api/forward-reverse-geocoding)
2. Click "Subscribe" and select a plan (Free tier available)

### 1.3 Get Your API Key
1. Go to RapidAPI Dashboard
2. Click on any subscribed API
3. Copy your `X-RapidAPI-Key` from the code snippets section
4. This single key works for all your subscribed APIs

---

## Step 2: Retool Resource Configuration

### 2.1 Create Geocoding Resource

1. In Retool, go to **Resources** → **Create new**
2. Select **REST API**
3. Configure:
   - **Name**: `RapidAPI_Geocoding`
   - **Base URL**: `https://forward-reverse-geocoding.p.rapidapi.com`
   - **Headers**:
     | Key | Value |
     |-----|-------|
     | X-RapidAPI-Key | `<your-api-key>` |
     | X-RapidAPI-Host | `forward-reverse-geocoding.p.rapidapi.com` |
4. Click **Create resource**

### 2.2 Create Booking.com Resource (NEW)

1. Go to **Resources** → **Create new**
2. Select **REST API**
3. Configure:
   - **Name**: `RapidAPI_Booking`
   - **Base URL**: `https://booking-com15.p.rapidapi.com`
   - **Headers**:
     | Key | Value |
     |-----|-------|
     | X-RapidAPI-Key | `<your-api-key>` |
     | X-RapidAPI-Host | `booking-com15.p.rapidapi.com` |
4. Click **Create resource**

---

## Step 3: Environment Variable (Recommended)

Instead of hardcoding your API key in resources, use a Retool secret:

1. Go to **Settings** → **Secrets** (or **Config vars** in some versions)
2. Create a new secret:
   - **Name**: `RAPIDAPI_KEY`
   - **Value**: `<your-api-key>`
3. In your resources, reference it as: `{{ retoolContext.configVars.RAPIDAPI_KEY }}`

---

## Step 4: Import the App

1. In Retool, go to **Apps** → **Create new** → **From JSON/file**
2. Upload `hotel-search-v2.json`
3. Click **Import**

---

## Step 5: Connect Resources to Queries

After import, verify the queries are connected to the correct resources:

1. Open the imported app in edit mode
2. Click on `geocodeAddress` query in the left panel
3. Ensure **Resource** is set to `RapidAPI_Geocoding`
4. Click on `searchHotels` query
5. Ensure **Resource** is set to `RapidAPI_Booking` (not RapidAPI_Hotels)

---

## Step 6: Test the App

1. Enter a test address: `Times Square, New York, NY`
2. Select search radius: `10 miles`
3. Pick check-in date (tomorrow or later)
4. Pick check-out date (after check-in)
5. Set max price (optional): `$300`
6. Select minimum stars: `3★`
7. Click **Search Hotels**

### Expected Results (V2 with Booking.com):
- Loading spinner appears on button and table
- Success notification shows results count
- **Real prices** appear (not synthetic $80, $95, etc.)
- **Distance in miles** from your search location
- **Review scores** from actual guest reviews
- Click "Book Now" → Opens **real Booking.com reservation page**
- Click any row → Details modal with actual hotel info

---

## What's Different in V2

| Feature | V1 (Hotels4) | V2 (Booking.com) |
|---------|--------------|------------------|
| Prices | Fake/synthetic | Real-time actual prices |
| Availability | Always "available" | Real availability status |
| Booking Links | Empty or placeholder | Direct Booking.com URLs |
| Distance | Not calculated | Accurate miles from search point |
| Review Scores | Random/null | Actual guest review scores |
| Star Ratings | Cycled 2-5 | Real hotel classification |

---

## Troubleshooting

### "Location Not Found" Error
- Verify the address format (include city, state/country)
- Check geocoding API subscription is active
- Test API directly in RapidAPI dashboard

### "Search Failed" Error
- Verify Booking.com API subscription is active
- Check API key is correct in resource headers
- Ensure dates are valid (check-out after check-in, both in future)
- Review browser console for detailed error

### No Results Returned
- Expand search radius (try 25 miles)
- Lower minimum star rating to 1
- Remove max price filter
- Try a major city (New York, London, Paris)
- Check dates are not too far in the future (some APIs limit to ~1 year)

### Distance Shows 0 or Incorrect
- Ensure geocodeAddress query ran successfully first
- Check `geocodeAddress.data[0].lat` has a value in debugger
- Verify the transformer has the Haversine distance function

### Booking Links Don't Work
- Verify hotel_id is being returned from API
- Check the bookingLink field in `filteredHotelsTransformer.value`
- Links format: `https://www.booking.com/hotel/{hotel_id}.html`

---

## API Rate Limits

| API | Free Tier | Recommendation |
|-----|-----------|----------------|
| Booking.com | ~500 requests/month | Cache results, use debouncing |
| Geocoding | ~1000 requests/month | Cache address lookups |

For production use, consider upgrading to paid plans.

---

## Customization Options

### Modify Search Parameters
Edit `searchHotels` query URL to adjust:
- `adults`: Number of adults per room (default: 2)
- `room_qty`: Number of rooms (default: 1)
- `units`: `metric` or `imperial`
- `currency_code`: USD, EUR, GBP, etc.

### Available Booking.com API Endpoints
- `/v1/hotels/searchHotelsByCoordinates` - Search by lat/lng (current)
- `/v1/hotels/searchDestination` - Search by city/region name
- `/v1/hotels/getHotelDetails` - Get full hotel info
- `/v1/hotels/getHotelPhotos` - Get photo gallery

### Transformer Customization
The `filteredHotelsTransformer` function handles:
- Distance calculation (Haversine formula)
- Field mapping from Booking.com response
- Filtering by stars, radius, price
- Sorting by distance

Modify this function to change filtering logic or add new computed fields.

---

## Files in This Package

| File | Purpose |
|------|---------|
| `hotel-search-v2.json` | Import into Retool (uses Booking.com API) |
| `hotelappv2.json` | Original export (uses Hotels4 API) |
| `hotel-search-instructions.md` | This setup guide |
| `modify_retool_app.py` | Script used to generate v2 from original |

---

## Support

- **Retool Docs**: https://docs.retool.com
- **Booking.com API Docs**: https://rapidapi.com/DataCrawler/api/booking-com15
- **RapidAPI Support**: https://rapidapi.com/support
