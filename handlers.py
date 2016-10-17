from flask import Blueprint, render_template
from flask import current_app

from datetime import datetime


site = Blueprint('site', __name__)


@site.route('/')
def home_page():
    now = datetime.now()
    day = now.strftime('%A')
    return render_template('home.html', day_name=day)


@site.route('/events')
def events_page():
    total_number = current_app.store.last_event_id
    return render_template('events.html',tot_num =total_number )

@site.route('/events/documents')
def documents_page():
    events = current_app.store.get_events()
    return render_template('documents.html', events=sorted(events.items()))

@site.route('/signUp')
def sign_up():
    return render_template('signUp.html')

@site.route('/maps')
def map_page():
    return render_template('map.html')

@site.route('/timeline')
def timeline_page():
    return render_template('index.html')
