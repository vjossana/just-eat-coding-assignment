import re
from flask import Flask, render_template, request
from restaurant_service import RestaurantService

app = Flask(__name__)

#Postcode format validation
def valid_postcode(postcode):
    pattern = "^[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}$"
    return re.match(pattern, postcode)

#Loading page and form submission
@app.route("/", methods=["GET" , "POST"])
def index():
    restaurants = []
    postcode = ''
    error = None

    #Fetch restaurants if form submitted
    if request.method == "POST":
        postcode = request.form.get("postcode", "").strip().upper()

        #Dont call API if postcode empty
        if not postcode:
            error = "Please enter a valid postcode"
        elif not valid_postcode(postcode):
            error = "Please enter a valid UK postcode (e.g. EC4M 7RF)"
        else:
            service = RestaurantService()
            restaurants = service.get_restaurants(postcode)

            if not restaurants:
                error = f"There are no restaurants found for '{postcode}'"
            
        return render_template("index.html", restaurants=restaurants, postcode=postcode, error=error)
    
if __name__ == "__main__":
    app.run(debug=True)
