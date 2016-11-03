from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from event import Event
from user import setUserToDb
from user import getUserFromDb
from user import search
add = Blueprint('add', __name__)


@add.route('/events/documents/add', methods=['GET', 'POST'])
def add_new_document_page():
    if request.method == 'GET':
        form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
        events = current_app.store.get_events()
        return render_template('documents.html', events=sorted(events.items()), form=form)    
    else:
        title_temp = request.form['inputTitle']
        date_temp = request.form['inputDate']
        place_temp = request.form['inputPlace']
        content_temp = request.form['comment']
        event_temp = Event(title = title_temp, date=date_temp, place=place_temp,content= content_temp)
        current_app.store.add_event(event_temp)
        events = current_app.store.get_events()
        form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
        return render_template('documents.html', events=sorted(events.items()), form = form)
    
@add.route('/events/documents/delete', methods=['GET', 'POST'])
def delete_document():
    if request.method == 'GET':
        events = current_app.store.get_events()
        form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
        return render_template('documents.html', events=sorted(events.items()), form=form)
    else:
        event_id_list = request.form.getlist('event_id_list')
        for event_id in event_id_list:
            current_app.store.delete_event(int(event_id))
        events = current_app.store.get_events()
        form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
        return render_template('documents.html', events=sorted(events.items()), form=form)


   
    
@add.route('/events/documents/update/<int:event_id>', methods=['GET', 'POST'])
def update_documents_page(event_id):
    if request.method == 'GET':
        event = current_app.store.get_event(event_id)
        form = {'inputTitle': event.title, 'inputDate': event.date, 'inputPlace': event.place, 'comment':event.content}
        return render_template('update_documents.html', form=form)  
                               
    else:
        title_temp = request.form['inputTitle']
        date_temp = request.form['inputDate']
        place_temp = request.form['inputPlace']
        content_temp = request.form['comment']
        event_temp = Event(title = title_temp, date=date_temp, place=place_temp,content= content_temp)
        current_app.store.update_event(event_temp,event_id)
        events = current_app.store.get_events()
        form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
        return render_template('documents.html', events=sorted(events.items()), form=form)
    
    

   