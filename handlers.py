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
    events = current_app.store.get_events()
    now = datetime.now()
    day = now.strftime('%A')
    return render_template('events.html', events=sorted(events.items()),day_name=day )

@site.route('/events/documents')
def documents_page():
    events = current_app.store.get_events()
    return render_template('documents.html', events=sorted(events.items()))

@site.route('/signUp')
def sign_up():
    return render_template('signUp.html')


