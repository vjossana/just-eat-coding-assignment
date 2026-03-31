from restaurant_service import RestaurantService

def main():
    
    print("Welcome to Just Eat Restaurant Finder!")

    postcode = input("Enter a postcode: ").strip().upper()

    if not postcode:
        print("Please enter a valid postcode.")
        return

    service = RestaurantService()
    restaurants = service.get_restaurants(postcode)

    if restaurants is None:
        print(f"Could not connect to Just Eat. Please check your internet connection and try again. ")
        return
    
    if not restaurants:
        print(f"Sorry, no restaurants found for {postcode}.")
        return

    print(f"\nHere are the first 10 restaurants for {postcode}:\n")

    for restaurant in restaurants:
        restaurant.display()

    print("Thanks for using the Just Eat Restaurant Finder!")

if __name__ == "__main__":
    main()