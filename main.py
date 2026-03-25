from restaurant_service import RestaurantService

def main():
    postcode = input("Enter a postcode: ").strip()
    service = RestaurantService()
    restaurants = service.get_restaurants(postcode)
    for restaurant in restaurants:
        restaurant.desiplay()

if __name__ == "__main__":
    main()
