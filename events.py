from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from event import Event
from user import setUserToDb
from user import getUserFromDb
from user import search
event = Blueprint('event', __name__)


@event.route('/events/add_event', methods=['GET', 'POST'])
def add_new_event():
    if request.method == 'POST':
        title_temp = request.form['inputTitle']
        date_temp = request.form['inputDate']
        place_temp = request.form['inputPlace']
        event_id = 1
        event_temp = Event(title = title_temp, date=date_temp, place=place_temp,event_id = event_id)
        current_app.store.add_event(event_temp)
        return render_template('events.html')
    
@event.route('/events/delete_event', methods=['GET', 'POST'])
def delete_event():
    if request.method == 'POST':
        event_id_list = request.form.getlist('event_id_list')
        for event_id in event_id_list:
            current_app.store.delete_event(int(event_id))
            
        events=current_app.store.get_events()
        count=1
        if events:
            for event in events:
                if event.event_id != count:
                    current_app.store.update_event_id(int(event_id),count)
                count += 1
        
        return render_template('events.html')
    
    

   