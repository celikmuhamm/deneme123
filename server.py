import datetime
import os
from flask import Flask,flash
from flask import render_template
from flask import url_for
from handlers import site
from login import register
from flask import redirect
from event import Event
from store import Store
from user import User
from flask_login import LoginManager
import user
from sqlconnection import initialize_database
lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return getUser(user_id)

def create_app():
    app = Flask(__name__)
    app.user = User()
    app.register_blueprint(site)
    app.register_blueprint(register)
    lm.init_app(app)
    lm.login_view = 'register.user_page'
    app.store = Store()
    app.store.add_event(Event('World War II', date='15/12/1942', place='Turkey',content= 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    app.store.add_event(Event('Train Accident', date='01/02/1985', place='California', content = 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    app.initialize_database=initialize_database()
    
    
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



