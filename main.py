from restaurant_service import RestaurantService

def main():
    
    print("Welcome to the Just Eat!")

    postcode = input("Enter a postcode: ").strip().upper()

    if not postcode:
        print("Please enter a valid postcode.")
        return

    service = RestaurantService()
    restaurants = service.get_restaurants(postcode)

    if not restaurants:
        print(f"Sorry, no restaurants found for {postcode}.")
        return

    print(f"\nHere are the top 10 restaurants for {postcode}:\n")

    for restaurant in restaurants:
        restaurant.display()

    print("Thanks for using the Just Eat!")

if __name__ == "__main__":
    main()