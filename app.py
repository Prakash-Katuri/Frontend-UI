import csv
from flask import Flask, request, jsonify
from config import Config
from models import db, City, Hotel, Restaurant, Place

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)
db.init_app(app)

def populate_cities_from_csv():
    with open("cities.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = City(name=row['name'], state=row['state'])
            db.session.add(city)
        db.session.commit()

def populate_hotels_from_csv():
    with open("hotels.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Find the city ID based on city name and state
            city = City.query.filter_by(name=row['City'], state=row['State']).first()
            if city:
                hotel = Hotel(
                    name=row['Name'],
                    address=row['Address'],
                    rating=float(row['Rating']),
                    website=row['Website'],
                    price=float(row['Price']),
                    city_id=city.id
                )
                db.session.add(hotel)
        db.session.commit()

def populate_restaurants_from_csv():
    with open("restaurants.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Find the city ID based on city name and state
            city = City.query.filter_by(name=row['City'], state=row['State']).first()
            if city:
                restaurant = Restaurant(
                    name=row['Name'],
                    address=row['Address'],
                    rating=float(row['Rating']),
                    price_level=row['Price Level'],
                    website=row['Website'],
                    city_id=city.id
                )
                db.session.add(restaurant)
        db.session.commit()

def populate_places_from_csv():
    with open("places.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Find the city ID based on city name and state
            city = City.query.filter_by(name=row['City'], state=row['State']).first()
            if city:
                place = Place(
                    name=row['Name'],
                    address=row['Address'],
                    rating=float(row['Rating']),
                    entry_fee=float(row['Entry Fee']),
                    website=row['Website'],
                    city_id=city.id
                )
                db.session.add(place)
        db.session.commit()

# Initialize database and populate data
with app.app_context():
    db.create_all()
    if not City.query.first():  # Populate cities if table is empty
        populate_cities_from_csv()
    if not Hotel.query.first():  # Populate hotels if table is empty
        populate_hotels_from_csv()
    if not Restaurant.query.first():  # Populate restaurants if table is empty
        populate_restaurants_from_csv()
    if not Place.query.first():  # Populate places if table is empty
        populate_places_from_csv()

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Fetch all cities with their IDs, names, and states."""
    cities = City.query.all()
    results = [{"id": city.id, "name": city.name, "state": city.state} for city in cities]
    return jsonify(results)

@app.route('/api/search/hotel', methods=['GET'])
def search_hotels():
    city_id = request.args.get('city_id', type=int)
    budget = request.args.get('budget', type=float)
    persons = request.args.get('persons', type=int)

    # Validate city_id
    city = City.query.get(city_id)
    if not city:
        return jsonify({"error": "City not found"}), 404

    # Calculate budget per room if persons is provided
    if persons:
        rooms_needed = (persons + 1) // 2  # Calculate rooms needed for given persons (2 persons per room)
        if rooms_needed > 0:
            budget_per_room = budget / rooms_needed
        else:
            return jsonify({"error": "Invalid number of persons or budget"}), 400
    else:
        budget_per_room = budget

    # Query hotels within the budget per room in the specified city, ordered by rating desc, name asc
    hotels = Hotel.query.filter(
        Hotel.city_id == city_id,
        Hotel.price <= budget_per_room
    ).order_by(Hotel.rating.desc(), Hotel.name.asc()).all()

    # Format the result
    results = [
        {
            "name": hotel.name,
            "address": hotel.address,
            "rating": hotel.rating,
            "website": hotel.website,
            "price": hotel.price
        }
        for hotel in hotels
    ]

    return jsonify(results)

@app.route('/api/search/restaurant', methods=['GET'])
def search_restaurants():
    city_id = request.args.get('city_id', type=int)
    budget = request.args.get('budget', type=float)

    # Validate city_id
    city = City.query.get(city_id)
    if not city:
        return jsonify({"error": "City not found"}), 404

    # convert budget to price level as price level 1 is < 100, 2 is < 200, 3 is < 300
    # So, price level = budget / 100 and round up
    budget = -(-budget // 100)

    # Query restaurants within the budget in the specified city, ordered by rating desc, name asc
    restaurants = Restaurant.query.filter(
        Restaurant.city_id == city_id,
        Restaurant.price_level <= budget
    ).order_by(Restaurant.rating.desc(), Restaurant.name.asc()).all()

    # Format the result
    results = [
        {
            "name": restaurant.name,
            "address": restaurant.address,
            "rating": restaurant.rating,
            "price_level": restaurant.price_level,
            "website": restaurant.website
        }
        for restaurant in restaurants
    ]

    return jsonify(results)

@app.route('/api/search/place', methods=['GET'])
def search_places():
    city_id = request.args.get('city_id', type=int)
    budget = request.args.get('budget', type=float)

    # Validate city_id
    city = City.query.get(city_id)
    if not city:
        return jsonify({"error": "City not found"}), 404

    # Query places within the budget in the specified city, ordered by rating desc, name asc
    places = Place.query.filter(
        Place.city_id == city_id,
        Place.entry_fee <= budget
    ).order_by(Place.rating.desc(), Place.name.asc()).all()

    # Format the result
    results = [
        {
            "name": place.name,
            "address": place.address,
            "rating": place.rating,
            "entry_fee": place.entry_fee,
            "website": place.website
        }
        for place in places
    ]

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

    #/usr/local/bin/git push heroku main

@app.route('/', methods=['GET'])
def hello():
        return jsonify({"message": "This is Trip Wise"})