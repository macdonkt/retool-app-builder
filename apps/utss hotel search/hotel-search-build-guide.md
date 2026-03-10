# Hotel Search App - Manual Build Guide

Since Retool uses Transit encoding for JSON exports (not plain JSON), here's a step-by-step guide to build the app directly in Retool UI.

---

## Step 1: Create New App

1. In Retool, click **Create new** → **App**
2. Name it: `Hotel Search`
3. Choose **Desktop** layout

---

## Step 2: Set Up Resources (if not done already)

See `hotel-search-instructions.md` for RapidAPI resource setup.

---

## Step 3: Build the Search Form

### 3.1 Add Page Title
1. Drag **Text** component to canvas
2. Set **Value**: `Hotel Search`
3. Set **Size**: `Heading 1`

### 3.2 Add Address Input
1. Drag **Text Input** below the title
2. **ID**: `addressInput`
3. **Label**: `Address`
4. **Placeholder**: `Enter full address (e.g., 123 Main St, New York, NY)`

### 3.3 Add Radius Dropdown
1. Drag **Select** next to address input
2. **ID**: `radiusSelect`
3. **Label**: `Search Radius`
4. **Values**:
   ```
   [5, 10, 15, 20, 25]
   ```
5. **Labels**:
   ```
   ["5 miles", "10 miles", "15 miles", "20 miles", "25 miles"]
   ```
6. **Default value**: `10`

### 3.4 Add Check-in Date Picker
1. Drag **Date** component
2. **ID**: `checkInDate`
3. **Label**: `Check-in Date`
4. **Min date**: `{{ moment().format('YYYY-MM-DD') }}`

### 3.5 Add Check-out Date Picker
1. Drag another **Date** component
2. **ID**: `checkOutDate`
3. **Label**: `Check-out Date`
4. **Min date**: `{{ moment(checkInDate.value).add(1, 'days').format('YYYY-MM-DD') }}`

### 3.6 Add Max Price Input
1. Drag **Number Input**
2. **ID**: `maxPriceInput`
3. **Label**: `Max Nightly Price`
4. **Prefix**: `$`
5. **Step**: `10`
6. **Placeholder**: `No limit`

### 3.7 Add Star Rating Selector
1. Drag **Button Group**
2. **ID**: `starRatingSelector`
3. **Label**: `Minimum Stars`
4. **Values**: `[1, 2, 3, 4, 5]`
5. **Labels**: `["1★", "2★", "3★", "4★", "5★"]`
6. **Default value**: `1`

### 3.8 Add Search Button
1. Drag **Button**
2. **ID**: `searchButton`
3. **Text**: `Search Hotels`
4. **Loading**: `{{ geocodeAddress.isFetching || searchHotels.isFetching }}`
5. **Disabled**: `{{ !addressInput.value || !checkInDate.value || !checkOutDate.value }}`

---

## Step 4: Create Queries

### 4.1 Geocode Address Query

1. In left panel, click **+** next to Queries
2. Select **Resource query** → choose `RapidAPI_Geocoding`
3. **Name**: `geocodeAddress`
4. **Method**: `GET`
5. **URL path**: `/v1/search`
6. **URL parameters**:
   | Key | Value |
   |-----|-------|
   | q | `{{ addressInput.value }}` |
   | format | `json` |
   | limit | `1` |
7. **Run settings**: Uncheck "Run query on page load"
8. **Enable transformer** and paste:
```javascript
const result = data && data[0];
if (result) {
  return {
    lat: parseFloat(result.lat),
    lon: parseFloat(result.lon),
    displayName: result.display_name
  };
}
return null;
```

9. **Add success event handler**:
   - Event: `Success`
   - Action: `Trigger query`
   - Query: `searchHotels`
   - Only run if: `{{ geocodeAddress.data?.lat }}`

10. **Add failure event handler**:
    - Event: `Failure`
    - Action: `Show notification`
    - Title: `Location Not Found`
    - Description: `Could not find the address. Please try again.`

### 4.2 Search Hotels Query

1. Create another **Resource query** → choose `RapidAPI_Hotels`
2. **Name**: `searchHotels`
3. **Method**: `POST`
4. **URL path**: `/properties/v2/list`
5. **Body** (select JSON):
```json
{
  "currency": "USD",
  "eapid": 1,
  "locale": "en_US",
  "siteId": 300000001,
  "destination": {
    "coordinates": {
      "latitude": {{ geocodeAddress.data?.lat || 0 }},
      "longitude": {{ geocodeAddress.data?.lon || 0 }}
    }
  },
  "checkInDate": {
    "day": {{ moment(checkInDate.value).date() }},
    "month": {{ moment(checkInDate.value).month() + 1 }},
    "year": {{ moment(checkInDate.value).year() }}
  },
  "checkOutDate": {
    "day": {{ moment(checkOutDate.value).date() }},
    "month": {{ moment(checkOutDate.value).month() + 1 }},
    "year": {{ moment(checkOutDate.value).year() }}
  },
  "rooms": [{ "adults": 2 }],
  "resultsStartingIndex": 0,
  "resultsSize": 50,
  "sort": "PRICE_LOW_TO_HIGH",
  "filters": {
    "price": {
      "max": {{ maxPriceInput.value || 10000 }},
      "min": 0
    }
  }
}
```

6. **Run settings**: Uncheck "Run query on page load"
7. **Enable transformer** and paste:
```javascript
// Transform Hotels4 API response
const properties = data?.data?.propertySearch?.properties || [];
const searchLat = geocodeAddress.data?.lat || 0;
const searchLon = geocodeAddress.data?.lon || 0;
const minStars = parseInt(starRatingSelector.value) || 1;
const radiusMiles = parseInt(radiusSelect.value) || 10;

// Calculate distance in miles
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 3959;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

const transformed = properties.map(p => {
  const hotelLat = p.mapMarker?.latLong?.latitude || 0;
  const hotelLon = p.mapMarker?.latLong?.longitude || 0;
  const distance = calculateDistance(searchLat, searchLon, hotelLat, hotelLon);
  const starRating = p.star || 3;

  return {
    id: p.id,
    name: p.name || 'Unknown Hotel',
    starRating: starRating,
    price: p.price?.lead?.amount || 0,
    distance: distance,
    reviewScore: p.reviews?.score || null,
    reviewCount: p.reviews?.total || 0,
    amenities: p.amenities?.map(a => a.text) || [],
    availability: p.availability?.available !== false,
    image: p.propertyImage?.image?.url || '',
    bookingLink: p.id ? 'https://www.hotels.com/ho' + p.id : '',
    roomTypes: p.offerBadge?.primary?.text || 'Standard',
    neighborhood: p.neighborhood?.name || ''
  };
})
.filter(p => p.starRating >= minStars)
.filter(p => p.distance <= radiusMiles);

return { properties: transformed, totalCount: transformed.length };
```

8. **Add success event handler**:
   - Event: `Success`
   - Action: `Show notification`
   - Type: `Success`
   - Title: `Search Complete`
   - Description: `{{ searchHotels.data?.totalCount || 0 }} hotels found`

---

## Step 5: Wire Search Button

1. Select `searchButton`
2. **Add event handler**:
   - Event: `Click`
   - Action: `Trigger query`
   - Query: `geocodeAddress`

---

## Step 6: Add Results Table

1. Drag **Table** below the form
2. **ID**: `hotelsTable`
3. **Data**: `{{ searchHotels.data?.properties || [] }}`
4. **Loading state**: `{{ searchHotels.isFetching }}`

### Configure Columns

Click on table, go to **Columns** and configure:

| Column | Type | Mapped value | Sortable |
|--------|------|--------------|----------|
| image | Image | `{{ currentRow.image }}` | No |
| name | String | `{{ currentRow.name }}` | Yes |
| starRating | Custom | `{{ '★'.repeat(currentRow.starRating) }}` | Yes |
| price | Currency | `{{ currentRow.price }}` | Yes |
| distance | Custom | `{{ currentRow.distance.toFixed(1) + ' mi' }}` | Yes |
| reviewScore | Custom | `{{ currentRow.reviewScore + '/10' }}` | Yes |
| amenities | Tags | `{{ currentRow.amenities.slice(0,3) }}` | No |
| availability | Boolean | `{{ currentRow.availability }}` | Yes |
| bookingLink | Link | `{{ currentRow.bookingLink }}` | No |

For **sortable columns**, set the **Sort key** to the raw value:
- starRating sort key: `{{ currentRow.starRating }}`
- distance sort key: `{{ currentRow.distance }}`
- reviewScore sort key: `{{ currentRow.reviewScore }}`

---

## Step 7: Add Details Modal

1. Drag **Modal** component (or use Drawer)
2. **ID**: `hotelDetailsModal`
3. **Title**: `{{ hotelsTable.selectedRow?.name || 'Hotel Details' }}`

### Inside the Modal, add:

1. **Image**
   - Source: `{{ hotelsTable.selectedRow?.image }}`

2. **Text** (Hotel name)
   - Value: `{{ hotelsTable.selectedRow?.name }}`
   - Size: Heading 2

3. **Statistic** (Price)
   - Value: `{{ hotelsTable.selectedRow?.price }}`
   - Prefix: `$`
   - Suffix: `/night`

4. **Statistic** (Stars)
   - Value: `{{ hotelsTable.selectedRow?.starRating }}`
   - Suffix: ` ★`

5. **Statistic** (Review)
   - Value: `{{ hotelsTable.selectedRow?.reviewScore || 'N/A' }}`
   - Suffix: `/10`

6. **Text** (Amenities label)
   - Value: `Amenities`

7. **Tags**
   - Value: `{{ hotelsTable.selectedRow?.amenities || [] }}`

8. **Button** (Book Now)
   - Text: `Book Now`
   - Add click event:
     - Action: `Open URL`
     - URL: `{{ hotelsTable.selectedRow?.bookingLink }}`
     - Open in new tab: Yes

9. **Button** (Close)
   - Text: `Close`
   - Add click event:
     - Action: `Control component`
     - Component: `hotelDetailsModal`
     - Method: `Close`

---

## Step 8: Wire Table Row Click

1. Select `hotelsTable`
2. **Add event handler**:
   - Event: `Row click`
   - Action: `Control component`
   - Component: `hotelDetailsModal`
   - Method: `Open`

---

## Step 9: Test

1. Enter: `Times Square, New York, NY`
2. Set radius: `10 miles`
3. Pick dates
4. Set max price: `$500`
5. Select stars: `3★`
6. Click **Search Hotels**
7. Verify table populates
8. Click a row → modal opens
9. Click column headers → verify sorting works

---

## Component Summary

| ID | Type | Purpose |
|----|------|---------|
| addressInput | Text Input | Full address entry |
| radiusSelect | Select | 5-25 mile radius |
| checkInDate | Date | Check-in date picker |
| checkOutDate | Date | Check-out date picker |
| maxPriceInput | Number Input | Price filter |
| starRatingSelector | Button Group | Star rating filter |
| searchButton | Button | Triggers search |
| hotelsTable | Table | Results display |
| hotelDetailsModal | Modal | Hotel detail view |
| geocodeAddress | Query | Address → coordinates |
| searchHotels | Query | Fetch hotel data |

---

## Troubleshooting

**"Run query on page load" causing errors**: Make sure both queries have this unchecked.

**Dates not working**: Ensure moment.js is available (it's built into Retool).

**No results**: Check the transformer console for errors. Expand search radius or remove filters.

**Modal not opening**: Verify the table event handler targets the correct modal ID.
