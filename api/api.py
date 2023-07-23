'''
Author: Miles Catlett
Date: 7/22/2023
File: api.py
This is the interface for allowing the React app to get the json data from the python app. Originally, the crud
operations were part of routes, but then I figured out how to use APscheduler and put them on a timer. I left them in
the file for convenience sake.
'''
from flask import Blueprint, jsonify
from models import BeerFoodTruck
from ftr import fht
from wsb import wmb, wmb_next
from incendiary import incendiary
from datetime import date
from datetime import datetime

api = Blueprint('api', __name__)


@api.route("/get-ftb")
def get_ftb():
    ftb = []
    # I am doing some ordering of data on the back end so I don't have to worry about sorting and formatting
    # once in the React app.
    data = BeerFoodTruck.query.order_by(BeerFoodTruck.start.asc()).all()
    for f in data:
        ftb.append({
            "brewery": f.brewery,
            "food_truck": f.food_truck,
            # This is also some pretty date formatting on the back end to make the react app look better.
            "start": datetime.strftime(f.start, "%I:%M (%m/%d)"),
            "end": datetime.strftime(f.end, "%I:%M (%m/%d)")
        })
    return jsonify({'ftb': ftb})


def add_ftr():
    from app import db
    from app import app
    # Once I changed this over to AP scheduler, adding the application context here allow the code to work.
    with app.app_context():
        data = fht()
        if data:
            db.session.add_all(data)
            db.session.commit()
        print('ftr success!')


def add_incendiary():
    from app import db
    from app import app
    with app.app_context():
        data = incendiary()
        if data:
            db.session.add_all(data)
            db.session.commit()
        print('incendiary success!')


def add_wmb():
    from app import db
    from app import app
    with app.app_context():
        data = wmb()
        if data:
            db.session.add_all(data)
            db.session.commit()
        more_data = wmb_next()
        if more_data:
            db.session.add_all(more_data)
            db.session.commit()
        print('wmb success!')


def del_from_db():
    from app import db
    from app import app
    today = date.today()
    with app.app_context():
        # I learned with the delete operation that I would need to iterate in order to delete all. I figured
        # another way to do this is to schedule the scheduler to delete the old rows each minute until there are
        # no more to delete.
        data = BeerFoodTruck.query.filter(BeerFoodTruck.start < today).first()
        if data:
            db.session.delete(data)
            db.session.commit()
            print('item deleted!')
