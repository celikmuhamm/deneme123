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
    return render_template('events.html')

@site.route('/events/documents_all/<int:event_id>', methods=['GET', 'POST'])
def documents_all_page(event_id):
    documents_array = current_app.store_documents.get_documents(event_id)
    form = {'inputTitle': '', 'inputDate': '', 'event_number': '', 'comment':''}
 
    return render_template('documents.html', event_id=event_id, documents=documents_array, form=form)

@site.route('/events/events_list', methods=['GET', 'POST'])
def documents_page():
    form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
    events_array = current_app.store.get_events()
    
    return render_template('events_list.html', events=events_array, form=form)

@site.route('/events/images')
def images_page():
    events_array = current_app.store.get_events()
    image_array = None
    if events_array:
        for events in events_array:
            event_id = events.event_id
            image_series = current_app.store_images.get_images(event_id)
            images = [(image_series)]
            if image_series:
                if(event_id == 1):
                    image_array = images
                else:
                    if image_array is None:
                        image_array = images
                    else:
                        image_array += images
        
    return render_template('images_slide.html', images=image_array)

@site.route('/events/images/images_add')
def images_add_page():
    events = current_app.store.get_events()
    return render_template('add_images.html', events=events)

@site.route('/events/images_all/<int:event_id>')
def images_all_page(event_id):
    images = current_app.store_images.get_images(event_id)
    return render_template('images_all.html',images = images, event_id = event_id)

@site.route('/signUp')
def sign_up():
    return render_template('signUp.html')

@site.route('/maps')
def map_page():
    return render_template('map.html')

@site.route('/timeline')
def timeline_page():
    return render_template('index.html')

@site.route('/maps/edit')
def edit_location():
    return render_template('locationEdit.html')

