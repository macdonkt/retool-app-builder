# Hotel Search App V3 - Setup Instructions

This document provides step-by-step instructions for importing and configuring the Hotel Search app with Google Geocoding and Booking.com APIs.

## Prerequisites

- Retool account with permissions to create resources and import apps
- Google Cloud account with Geocoding API enabled
- RapidAPI account with Booking.com API subscription

---

## Step 1: Obtain API Keys

### Google Geocoding API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Library**
4. Search for "Geocoding API" and enable it
5. Go to **APIs & Services** → **Credentials**
6. Click **Create Credentials** → **API Key**
7. Copy the API key
8. (Recommended) Restrict the key to Geocoding API only

### Booking.com RapidAPI Key

1. Go to [RapidAPI - Booking.com API](https://rapidapi.com/tipsters/api/booking-com15)
2. Subscribe to a plan (free tier available)
3. Copy your `X-RapidAPI-Key` from the API dashboard

---

## Step 2: Create Retool Resources

### Resource 1: Google_Geocoding

1. In Retool, go to **Resources** → **Create New**
2. Select **REST API**
3. Configure:

| Field | Value |
|-------|-------|
| **Name** | `Google_Geocoding` |
| **Base URL** | `https://maps.googleapis.com/maps/api/geocode` |
| **Headers** | None required |

4. Click **Create Resource**

### Resource 2: RapidAPI_Booking

1. In Retool, go to **Resources** → **Create New**
2. Select **REST API**
3. Configure:

| Field | Value |
|-------|-------|
| **Name** | `RapidAPI_Booking` |
| **Base URL** | `https://booking-com15.p.rapidapi.com` |

4. Add Headers:

| Header | Value |
|--------|-------|
| `x-rapidapi-host` | `booking-com15.p.rapidapi.com` |
| `x-rapidapi-key` | `[YOUR_RAPIDAPI_KEY]` |

5. Click **Create Resource**

---

## Step 3: Update App JSON with API Key

Before importing, update the Google API key in the JSON file:

1. Open `hotel-search-v3-booking.json` in a text editor
2. Find and replace:
   ```
   YOUR_GOOGLE_API_KEY
   ```
   with your actual Google Geocoding API key

3. Save the file

---

## Step 4: Import the App

1. In Retool, go to **Apps** → **Create New** → **From JSON/ZIP**
2. Upload `hotel-search-v3-booking.json`
3. Click **Import**
4. Open the imported app

---

## Step 5: Verify Query Configurations

After import, verify each query is connected to the correct resource:

### geocodeAddress Query
- **Resource**: `Google_Geocoding`
- **Method**: GET
- **Endpoint**: `/json?address={{ encodeURIComponent(addressInput.value) }}&key=[API_KEY]`

### searchHotels Query
- **Resource**: `RapidAPI_Booking`
- **Method**: GET
- **Endpoint**: `/v1/hotels/searchHotelsByCoordinates?latitude=...&longitude=...`

### getHotelDetails Query
- **Resource**: `RapidAPI_Booking`
- **Method**: GET
- **Endpoint**: `/api/v1/hotels/getHotelDetails?hotel_id=...`

### getRoomList Query
- **Resource**: `RapidAPI_Booking`
- **Method**: GET
- **Endpoint**: `/api/v1/hotels/getRoomList?hotel_id=...`

---

## Step 6: Test the App

### Test 1: Geocoding
1. Enter an address in the search field (e.g., "Times Square, New York")
2. Click Search
3. Verify coordinates are returned (check geocodeAddress query results)

### Test 2: Hotel Search
1. After geocoding succeeds, verify hotel results appear in the table
2. Check that map markers are displayed
3. Verify statistics cards show correct data

### Test 3: Hotel Details
1. Click on a hotel row in the table
2. Verify the detail modal opens
3. Check that hotel information is displayed correctly

### Test 4: Error Handling
1. Enter an invalid address (e.g., "asdfasdfasdf")
2. Verify error notification appears
3. Check that the app handles empty results gracefully

---

## Troubleshooting

### "Resource not found" Error
- Ensure resource names match exactly: `Google_Geocoding` and `RapidAPI_Booking`
- Check that resources are created in the correct Retool environment

### No Hotels Returned
- Verify the geocoding query returns valid coordinates
- Check RapidAPI subscription is active
- Verify the Booking.com API key is correct

### Map Not Displaying Markers
- Check that `mapMarkersTransformer` is returning valid lat/lng values
- Verify the map component is bound to `{{ mapMarkersTransformer.value }}`

### CORS Errors
- Retool handles CORS for REST API resources automatically
- If issues persist, check resource configuration

---

## API Rate Limits

### Google Geocoding API
- Free tier: $200/month credit (~40,000 requests)
- Rate limit: 50 requests per second

### Booking.com API (RapidAPI)
- Varies by plan
- Free tier typically includes 100-500 requests/month
- Check your RapidAPI dashboard for current limits

---

## App Features

### Pages
1. **Search** - Main hotel search with filters
2. **Favorites** - Saved favorite hotels
3. **Compare** - Side-by-side hotel comparison

### Components
- Address search with autocomplete-friendly geocoding
- Interactive map with hotel markers
- Filterable hotel table
- Statistics cards (avg price, best rating, total results)
- Hotel detail modal with room availability

### Filters
- Star rating (minimum)
- Distance radius (miles)
- Maximum price

---

## Data Flow

```
User Input (Address)
       ↓
geocodeAddress (Google API)
       ↓ Returns: { lat, lng }
       ↓
searchHotels (Booking.com API)
       ↓ Returns: Hotel list
       ↓
filteredHotelsTransformer
       ↓ Normalizes & filters data
       ↓
┌──────────┼──────────┐
↓          ↓          ↓
Table    Map      Stats
         ↓
    Row Select
         ↓
getHotelDetails + getRoomList
         ↓
   Detail Modal
```

---

## Customization

### Change Default Location
In `searchHotels` query, update the fallback coordinates:
```javascript
latitude={{ geocodeAddress.data.results[0]?.geometry.location.lat || 40.7128 }}
longitude={{ geocodeAddress.data.results[0]?.geometry.location.lng || -74.006 }}
```

### Change Currency
In `searchHotels`, `getHotelDetails`, and `getRoomList` queries, update:
```
currency_code=USD
```
to your preferred currency (EUR, GBP, etc.)

### Change Language
Update `languagecode` parameter in queries:
```
languagecode=en-us
```
Options: en-us, en-gb, de, fr, es, it, etc.

---

## Support

- **Retool Documentation**: https://docs.retool.com
- **Google Geocoding API**: https://developers.google.com/maps/documentation/geocoding
- **Booking.com API (RapidAPI)**: https://rapidapi.com/tipsters/api/booking-com15
