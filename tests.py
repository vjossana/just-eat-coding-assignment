import requests
import unittest
from unittest.mock import patch, MagicMock
import json
from restaurant import Restaurant
from restaurant_service import RestaurantService
from app import app

#Test Restaurant

class TestRestaurant(unittest.TestCase):

    def test_restaurant_created_correctly(self):
        # Arrange & Act
        restaurant = Restaurant("Krusty Krab", 4.5, ["Burgers", "American"], "1 Fleet Place, London, EC4M 7RF")

        # Assert all four fields are stored correctly
        self.assertEqual(restaurant.name, "Krusty Krab")
        self.assertEqual(restaurant.rating, 4.5)
        self.assertEqual(restaurant.cuisines, ["Burgers", "American"])
        self.assertEqual(restaurant.address, "1 Fleet Place, London, EC4M 7RF")

    def test_restaurant_with_empty_cuisines(self):
        # Edge case where cuisines list is empty
        restaurant = Restaurant("Krusty Krab", 4.5, [], "1 Fleet Place, London, EC4M 7RF")

        # Assert empty list is handled
        self.assertEqual(restaurant.cuisines, [])
        
    def test_rating_is_stored_as_number(self):
        # Rating should be a float not a string
        restaurant = Restaurant("Krusty Krab", 4.5, ["Burgers"], "1 Test St, London, EC4M 7RF")
        self.assertIsInstance(restaurant.rating, float)

#Test RestaurantService

class TestRestaurantService(unittest.TestCase):

    @patch("restaurant_service.requests.get")
    def test_returns_first_10_restaurants(self, mock_get):
        # Arrange - create fake API response with 20 restaurants
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "restaurants": [
                {
                    "name": f"Restaurant {i}",
                    "rating": {"starRating": 4.0},
                    "cuisines": [{"name": "Italian"}],
                    "address": {"firstLine": "1 Test St", "city": "London", "postalCode": "EC4M 7RF"}
                }
                for i in range(20)
            ]
        })
        mock_get.return_value = mock_response

        # Act
        service = RestaurantService()
        results = service.get_restaurants("EC4M7RF")

        # Assert - should only return 10 even though 12 were in the response
        self.assertEqual(len(results), 10)

    @patch("restaurant_service.requests.get")
    def test_returns_none_on_network_error(self, mock_get):
        # Arrange - simulate a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        # Act
        service = RestaurantService()
        result = service.get_restaurants("EC4M7RF")

        # Assert - should return None on network error
        self.assertIsNone(result)

    @patch("restaurant_service.requests.get")
    def test_returns_none_on_bad_response(self, mock_get):
        # Arrange - simulate API returning error status
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Act
        service = RestaurantService()
        result = service.get_restaurants("INVALID")

        # Assert - should return None on bad response
        self.assertIsNone(result)

    @patch("restaurant_service.requests.get")
    def test_filters_out_non_cuisines(self, mock_get):
        # Arrange - Restaurant with promotional tags mixed in cuisines to check filter
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({
            "restaurants": [
                {
                    "name": "Krusty Krab",
                    "rating": {"starRating": 4.5},
                    "cuisines": [{"name": "Burgers"}, {"name": "Deals"}, {"name": "Collect stamps"}],
                    "address": {"firstLine": "1 Test St", "city": "London", "postalCode": "EC4M 7RF"}
                }
            ]
        })
        mock_get.return_value = mock_response

        # Act
        service = RestaurantService()
        results = service.get_restaurants("EC4M7RF")

        # Assert - Deals and Collect stamps should be filtered out
        self.assertEqual(results[0].cuisines, ["Burgers"])

# Test Flask Routes

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        # Set up a test client so we can make requests without running server
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage_loads(self):
        # Test that GET request returns a 200 status code
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_empty_postcode_shows_error(self):
        # Test that empty postcode shows an error message
        response = self.client.post("/", data={"postcode": ""})
        self.assertIn(b"error", response.data)

    def test_invalid_postcode_shows_error(self):
        # Test that invalid postcode format shows an error message
        response = self.client.post("/", data={"postcode": "HELLO"})
        self.assertIn(b"error", response.data)

if __name__ == "__main__":
    unittest.main()