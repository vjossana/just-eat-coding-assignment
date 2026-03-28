import unittest
from unittest.mock import patch, MagicMock
import json
from restaurant import Restaurant
from restaurant_service import RestaurantService
from app import app

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

if __name__ == "__main__":
    unittest.main()