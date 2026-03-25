import requests
import json
from restaurant import Restaurant

class RestaurantService:
    """Fetches and processes restaurant data from API"""
    def get_restaurants(self, postcode):
        
        url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        #Network Issues
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            print("Network Error: Could not connect to Just Eat API")
            return []
        
        #Bad Response
        if response.status_code != 200:
            print(f"Bad Response: No results found for postcode '{postcode}',")
            return []
        
        data = json.loads(response.text)
        restaurants = []

        #Requirement: Only show first 10 restaurants
        for item in data["restaurants"][:10]:
            try:
                name = item["name"]
                rating = item["rating"]["starRating"]
                cuisines = [c["name"] for c in item["cuisines"]]
                address = f"{item['address']['firstLine']}, {item['address']['city']}, {item['address']['postalCode']}"

                restaurant = Restaurant(name, rating, cuisines, address)
                restaurants.append(restaurant)

            except KeyError:
                # Skip restaurants with missing data
                continue
        
        return restaurants