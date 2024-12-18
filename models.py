from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    hotels = db.relationship('Hotel', backref='city', lazy=True)


class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255))
    rating = db.Column(db.Float)
    price = db.Column(db.Float)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    image = db.Column(db.Text)  # Column for base64 encoded image data

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    price_level = db.Column(db.String(10), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    image = db.Column(db.Text)  # Column for base64 encoded image data

    city = db.relationship('City', backref=db.backref('restaurants', lazy=True))

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    entry_fee = db.Column(db.Float)
    website = db.Column(db.String(255), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    image = db.Column(db.Text)  # Column for base64 encoded image data

    city = db.relationship('City', backref=db.backref('places', lazy=True))