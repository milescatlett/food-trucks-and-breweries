'''
Author: Miles Catlett
Date: 7/22/2023
File: app.py
This follows an application factory pattern. I use python dotenv to store login data such as usernames and passwords.
I use flask cors, but I think this is supposed to now be built in to flask so I'm not sure we need this. Also using
APscheduler to run some crud operations from scraping in the background.
'''
import os
from dotenv import load_dotenv
from flask import Flask
from models import db
from flask_cors import CORS
from create_db import create_db
from api import add_wmb, add_ftr, del_from_db, add_incendiary
from flask_apscheduler import APScheduler
load_dotenv()

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
un = os.getenv("DB_USERNAME")
pw = os.getenv("DB_PASSWORD")
hn = os.getenv("DB_HOSTNAME")
dt = os.getenv("DB_DATABASE")


def create_app():
    app = Flask(__name__, instance_path=project_root, template_folder=template_path, static_folder=static_path)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="mysql://" + un + ":" + pw + "@" + hn + "/" + dt,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )
    app.config.from_prefixed_env()
    from api import api
    app.register_blueprint(api)
    db.init_app(app)
    CORS(app)
    scheduler = APScheduler()
    scheduler.init_app(app)
    with app.app_context():
        create_db()
        db.create_all()
        # Here I had some trouble with the application context with regard to the scheduler tasks performing
        # crud operations with the database.
        scheduler.add_job(id='job1', func=add_ftr, trigger='interval', hours=20)
        scheduler.add_job(id='job2', func=add_wmb, trigger='interval', hours=24)
        scheduler.add_job(id='job3', func=del_from_db, trigger='interval', seconds=10)
        scheduler.add_job(id='job4', func=add_incendiary, trigger='interval', hours=24)
        scheduler.start()
    return app


app = create_app()
