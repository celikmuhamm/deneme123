import datetime
import os
import json
import re
import psycopg2 as dbapi2
from flask import Flask,flash
from flask import render_template
from flask import url_for
from handlers import site
from login import register
from userMapOperations import myMap
from flask import redirect
from event import Event
from store import Store
from user import User
from user import UserList
from initialize_database import init_db
from userMap import UserLocationStore
from userMap import UserLocation



def create_app():
    app = Flask(__name__)
    app.user = User()
    app.userList = UserList()
    app.usermap = UserLocationStore()
    app.userlocation = UserLocation()
    app.register_blueprint(site)
    app.register_blueprint(myMap)
    app.register_blueprint(register)
    app.store = Store()
    app.init_db = init_db()
    app.store.add_event(Event('World War II', date='15/12/1942', place='Turkey',content= 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    app.store.add_event(Event('Train Accident', date='01/02/1985', place='California', content = 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    return app



def main():
    app = create_app()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTEENBUYUK'

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True



    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()



