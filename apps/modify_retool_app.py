#!/usr/bin/env python3
"""
Modify Retool app JSON to use Booking.com API instead of Hotels4.

This script updates:
1. searchHotels query - Change endpoint to Booking.com /v1/hotels/searchHotelsByCoordinates
2. filteredHotelsTransformer - Map Booking.com fields and calculate real distances
"""

import json
import re
import sys

def load_app(filepath):
    """Load the Retool app JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_app(data, filepath):
    """Save the modified app JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, separators=(',', ':'))

def update_search_hotels_query(app_state):
    """Update the searchHotels query to use Booking.com API."""

    # Replace the resource name
    app_state = app_state.replace(
        '"^1?","RapidAPI_Hotels"',
        '"^1?","RapidAPI_Booking"'
    )

    # Replace the old Hotels4 query URL with Booking.com endpoint
    old_query = '/locations/v3/search?q={{ addressInput.value || \'new york\' }}&locale=en_US&langid=1033&siteid=300000001'
    new_query = '/v1/hotels/searchHotelsByCoordinates?latitude={{ geocodeAddress.data[0]?.lat || 40.7128 }}&longitude={{ geocodeAddress.data[0]?.lon || -74.006 }}&arrival_date={{ moment(checkInDate.value).format(\'YYYY-MM-DD\') || moment().add(1, \'days\').format(\'YYYY-MM-DD\') }}&departure_date={{ moment(checkOutDate.value).format(\'YYYY-MM-DD\') || moment().add(2, \'days\').format(\'YYYY-MM-DD\') }}&adults=2&room_qty=1&units=metric&page_number=1&temperature_unit=c&languagecode=en-us&currency_code=USD'

    app_state = app_state.replace(
        f'"query","{old_query}"',
        f'"query","{new_query}"'
    )

    # Update the description
    app_state = app_state.replace(
        'Searches for hotels using Hotels4 API based on coordinates, dates, and filters',
        'Searches for hotels using Booking.com API based on coordinates, dates, and filters'
    )

    return app_state

def update_transformer(app_state):
    """Update the filteredHotelsTransformer to handle Booking.com response."""

    # The new transformer code that handles Booking.com response
    new_transformer = '''// Transform Booking.com API response to table-friendly format
// Expected shape: searchHotels.data.result is array of hotel objects

const response = {{ searchHotels.data }} || {};
const results = response.result || response.data?.result || [];

// Get search coordinates from geocoding result
const searchLat = {{ geocodeAddress.data[0]?.lat }} || 0;
const searchLon = {{ geocodeAddress.data[0]?.lon }} || 0;

// Filters from UI
const minStars = Math.round({{ starRatingSelector2.value }}) || 1;
const radiusMiles = {{ radiusSelect.value }} ? parseInt({{ radiusSelect.value }}) : 25;
const maxPrice = {{ maxPriceInput.value }} || Infinity;

// Haversine formula to calculate distance in miles
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 3959; // Earth's radius in miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

const transformedProperties = results.map((hotel, index) => {
  // Extract coordinates from Booking.com response
  const hotelLat = hotel.latitude || hotel.location?.latitude || 0;
  const hotelLon = hotel.longitude || hotel.location?.longitude || 0;

  // Calculate actual distance from search point
  const distance = calculateDistance(searchLat, searchLon, hotelLat, hotelLon);

  // Extract real data from Booking.com response
  const starRating = hotel.class || hotel.property_class || hotel.star_rating || 3;
  const price = hotel.min_total_price || hotel.price_breakdown?.gross_price || hotel.composite_price_breakdown?.gross_amount_per_night?.value || 0;
  const reviewScore = hotel.review_score || hotel.review_score_word ? parseFloat(hotel.review_score) : null;

  return {
    id: hotel.hotel_id || hotel.id || `hotel-${index}`,
    name: hotel.hotel_name || hotel.name || 'Unknown Hotel',
    starRating: starRating,
    price: price,
    priceFormatted: hotel.price_breakdown?.currency ? `${hotel.price_breakdown.currency} ${price.toFixed(0)}` : `$${price.toFixed(0)}`,
    distance: distance,
    reviewScore: reviewScore,
    reviewCount: hotel.review_nr || hotel.number_of_reviews || 0,
    amenities: hotel.facilities_block?.facilities?.map(f => f.name) || [],
    availability: hotel.is_available !== false,
    image: hotel.main_photo_url || hotel.max_photo_url || hotel.photo_url || 'https://images.pexels.com/photos/261102/pexels-photo-261102.jpeg',
    bookingLink: hotel.url || hotel.hotel_url || `https://www.booking.com/hotel/${hotel.hotel_id || hotel.id}.html`,
    roomTypes: hotel.unit_configuration_label || 'Standard Room',
    neighborhood: hotel.district || hotel.city || '',
    address: hotel.address || hotel.address_trans || '',
    lat: hotelLat,
    lon: hotelLon,
    fullData: hotel
  };
})
// Filter by minimum star rating
.filter((p) => p.starRating >= minStars)
// Filter by radius
.filter((p) => p.distance <= radiusMiles)
// Filter by max price
.filter((p) => maxPrice === Infinity || p.price <= maxPrice)
// Sort by distance
.sort((a, b) => a.distance - b.distance);

return transformedProperties;'''

    # Escape the transformer for JSON string embedding
    # Replace newlines and escape quotes
    escaped_transformer = new_transformer.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

    # Find and replace the old transformer funcBody
    # The pattern is: "funcBody","...old code..."
    old_funcbody_start = '"funcBody","// Transform Hotels4 locations search response'
    old_funcbody_pattern = r'"funcBody","// Transform Hotels4 locations search response[^"]*fullData: item \};\n\n\}\)\n// Filter by minimum star rating \(synthetic\)\n\.filter\(\(p\) => p\.starRating >= minStars\)\n// Filter by max price \(synthetic\)\n\.filter\(\(p\) => p\.price <= maxPrice\);\n\nreturn transformedProperties;"'

    # Simpler approach: find the funcBody and replace it
    # Look for the start marker
    start_marker = '"funcBody","// Transform Hotels4 locations search response to table-friendly format'
    end_marker = 'return transformedProperties;"'

    start_idx = app_state.find(start_marker)
    if start_idx > 0:
        # Find the end of this funcBody (ends with return transformedProperties;")
        search_start = start_idx + len('"funcBody","')
        end_idx = app_state.find(end_marker, search_start)
        if end_idx > 0:
            end_idx += len(end_marker)
            # Replace the entire funcBody section
            old_funcbody = app_state[start_idx:end_idx]
            new_funcbody = f'"funcBody","{escaped_transformer}"'
            app_state = app_state[:start_idx] + new_funcbody + app_state[end_idx:]
            print("✓ Updated filteredHotelsTransformer funcBody")
        else:
            print("✗ Could not find end of funcBody")
    else:
        print("✗ Could not find funcBody start marker")

    return app_state

def main():
    input_file = "/Users/kevin/Documents/Agentic workflows/Retool Builder/apps/hotelappv2.json"
    output_file = "/Users/kevin/Documents/Agentic workflows/Retool Builder/apps/hotel-search-v2.json"

    print(f"Loading {input_file}...")
    data = load_app(input_file)

    # Get the appState string
    app_state = data.get("page", {}).get("data", {}).get("appState", "")
    print(f"appState length: {len(app_state)} chars")

    # Apply modifications
    print("\nUpdating searchHotels query...")
    app_state = update_search_hotels_query(app_state)

    print("Updating filteredHotelsTransformer...")
    app_state = update_transformer(app_state)

    # Put the modified appState back
    data["page"]["data"]["appState"] = app_state

    # Update the app name/uuid for the new version
    data["uuid"] = "hotel-search-booking-v2"

    print(f"\nSaving to {output_file}...")
    save_app(data, output_file)

    print("✓ Done!")
    print(f"\nOutput: {output_file}")
    print("\nNext steps:")
    print("1. Create 'RapidAPI_Booking' resource in Retool")
    print("   - Base URL: https://booking-com15.p.rapidapi.com")
    print("   - Headers: X-RapidAPI-Key, X-RapidAPI-Host")
    print("2. Import hotel-search-v2.json into Retool")
    print("3. Connect the searchHotels query to the new resource")

if __name__ == "__main__":
    main()
