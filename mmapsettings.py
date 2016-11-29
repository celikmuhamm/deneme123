from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from location import Location
from user import setUserToDb
from user import getUserFromDb
from user import search
new = Blueprint('new', __name__)

@new.route('/maps')
def map_page():
    return render_template('map.html')


@new.route('/maps/add', methods=['GET', 'POST'])
def newLocation():
    if request.method == 'GET':
        form = {'lat': '','long': '', 'photo': '', 'video':'', 'document':''}
        locations = current_app.savelocation.GetLocations()
        return render_template('locationAdd.html', locations=locations, form=form)
    else:
        lonT = request.form['long']
        latT = request.form['lat']
        phoT = request.form['photo']
        vidT = request.form['video']
        docT = request.form['document']
        locT = Location(long = lonT, lat = latT, photo = phoT, video = vidT, document = docT)
        current_app.savelocation.AddLocation(locT)
        locations = current_app.savelocation.GetLocations()
        form = {'long': '', 'lat': '', 'photo': '', 'video':'', 'document':''}
        return render_template('map.html', locations=locations, form = form)
    

# @new.route('/events/documents/delete', methods=['GET', 'POST'])
# def delete_document():
#     if request.method == 'GET':0
#         events = current_app.store.get_events()
#         form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
#         return render_template('documents.html', events=events, form=form)
#     else:
#         event_id_list = request.form.getlist('event_id_list')
#         for event_id in event_id_list:
#             current_app.store.delete_event(int(event_id))
#         events = current_app.store.get_events()
#         form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
#         return render_template('documents.html', events=events, form=form)
#
#
#
#
# @add.route('/events/documents/update/<int:event_id>', methods=['GET', 'POST'])
# def update_documents_page(event_id):
#     if request.method == 'GET':
#         event = current_app.store.get_event(event_id)
#         form = {'inputTitle': event.title, 'inputDate': event.date, 'inputPlace': event.place, 'comment':event.content}
#         return render_template('update_documents.html', form=form)
#
#     else:
#         title_temp = request.form['inputTitle']
#         date_temp = request.form['inputDate']
#         place_temp = request.form['inputPlace']
#         content_temp = request.form['comment']
#         event_temp = Event(title = title_temp, date=date_temp, place=place_temp,content= content_temp)
#         current_app.store.update_event(event_temp,event_id)
#         events = current_app.store.get_events()
#         form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
#         return render_template('documents.html', events=events, form=form)




