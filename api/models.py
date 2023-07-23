'''
Author: Miles Catlett
Date: 7/22/2023
File: models.py
This is a simple model for a database that keeps track of food trucks and their location at various breweries.
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BeerFoodTruck(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # I used a unique id here that is a combination of the brewery, food truck, and dates. This allows me
    # to check and see if it's already been scraped, so I only put new events in the database.
    uid = db.Column(db.String(255), unique=True, nullable=False)
    brewery = db.Column(db.String(255), nullable=False)
    food_truck = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

