import datetime
import os
import json
import re
from flask import Flask
from flask import render_template
from flask import url_for
from handlers import site
from flask import redirect
from event import Event
from store import Store

app = Flask(__name__)

def create_app():
   
    app.register_blueprint(site)
    app.store = Store()
    app.store.add_event(Event('World War II', date='15/12/1942', place='Turkey',content= 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    app.store.add_event(Event('Train Accident', date='01/02/1985', place='California', content = 'Donec sed odio dui. Etiam porta sem malesuada magna mollis euismod. Nullam id dolor id nibh ultricies vehicula ut id elit'))
    return app

def get_sqldb_dsn(vcap_services):
    """Returns the data source name for IBM SQL DB."""
    parsed = json.loads(vcap_services)
    credentials = parsed["sqldb"][0]["credentials"]
    user = credentials["username"]
    password = credentials["password"]
    host = credentials["hostname"]
    port = credentials["port"]
    dbname = credentials["db"]
    dsn = """DATABASE={};HOSTNAME={};PORT={};UID={};PWD={};""".format(dbname, host, port, user, password)
    return dsn

@app.route('/initdb')
def initialize_database():
    try:
        connection = ibm_db.connect(app.config['dsn'], '', '')
        query = """DROP TABLE COUNTER"""
        ibm_db.exec_immediate(connection, query)
    except:
        pass

    try:
        connection = ibm_db.connect(app.config['dsn'], '', '')
        query = """CREATE TABLE COUNTER (N INTEGER)"""
        ibm_db.exec_immediate(connection, query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        ibm_db.exec_immediate(connection, query)
    except:
        pass
    return redirect(url_for('site.home_page'))


@app.route('/count')
def counter_page():
    try:
        connection = ibm_db.connect(app.config['dsn'], '', '')

        query = "UPDATE COUNTER SET N = N + 1"
        ibm_db.exec_immediate(connection, query)

        query = "SELECT N FROM COUNTER"
        statement = ibm_db.exec_immediate(connection, query)
        (count,) = ibm_db.fetch_tuple(statement)
    except:
        count = -1
    return "This page was accessed %d times." % count



def main():
    app = create_app()
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_sqldb_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """DATABASE=itucsdb;HOSTNAME=localhost;PORT=5000;UID=vagrant;PWD=vagrant;"""
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()



