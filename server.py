import datetime
import os

from flask import Flask
from flask import render_template
from flask import url_for
from handlers import site
from event import Event
from store import Store

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
	app.register_blueprint(site)
	
	app.store = Store()
    app.store.add_event(Event('World War II', date='15/12/1942', place='Turkey',content= 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    app.store.add_event(Event('Train Accident', date='01/02/1985', place='California', content = 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
   
    return app

def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
