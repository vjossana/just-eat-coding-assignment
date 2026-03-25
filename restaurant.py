class Restaurant:
    """Represents a single restaurant with desired fields"""
    def __init__(self, name, rating, cuisines, address):
        self.name = name
        self.rating = rating
        self.cuisines = cuisines
        self.address = address

    def display(self):
        print(f"Name: {self.name}")
        print(f"Rating: {self.rating}")
        print(f"Cuisines: {', '.join(self.cuisines)}")
        print(f"Address: {self.address}")
        print("---")