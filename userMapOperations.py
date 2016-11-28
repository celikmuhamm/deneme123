from flask import Blueprint, render_template,session,request,flash,jsonify
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation

myMap = Blueprint('myMap', __name__)

@myMap.route('/userPage/getLocations',methods=['POST','GET'])
def getLocations():
    if request.method == 'POST':
        data = request.get_json()
        for location in data:
            lat = location['lat']
            lng = location['lng']
            info = location['info']
            label = location['label']
            current_app.userlocation.userName = current_app.user.username
            current_app.userlocation.lat = lat
            current_app.userlocation.lng = lng
            current_app.userlocation.mapInfo = info
            current_app.userlocation.locationLabel = label
            current_app.usermap.addLocation(current_app.userlocation)
        
        markerLocations = []
        for locations in current_app.usermap.myLocations:
            newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
            markerLocations.append(newLocation)
           
            
        return render_template('user_page.html',markerLocations = markerLocations, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        if session.get('user')!=None:
            markerLocations = []
            for locations in current_app.usermap.myLocations:
                newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
                markerLocations.append(newLocation)
            return render_template('user_page.html',markerLocations = markerLocations, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
        else:
            flash('Please sign in or register for DeepMap')
            return render_template('home.html')