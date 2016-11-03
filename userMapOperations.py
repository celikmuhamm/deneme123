from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation

myMap = Blueprint('myMap', __name__)


@myMap.route('/userPage/map',methods=['POST','GET'])
def insertFunction():
    if request.method == 'GET':
        return render_template('user_page.html',userMap = current_app.usermap.myLocations,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
         if request.method == 'POST':
             userName = current_app.user.username
             mapInfo = request.form['locationInfo']
             address = request.form['address']
             lat = request.form['lat']
             lng = request.form['lng']
             if current_app.userlocation.mapInfo == mapInfo:
                 return render_template('user_page.html',userMap = current_app.usermap.myLocations,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
             else:

                 current_app.userlocation.userName = userName
                 current_app.userlocation.mapInfo = mapInfo
                 current_app.userlocation.address = address
                 current_app.userlocation.lat = lat
                 current_app.userlocation.lng = lng
                 current_app.usermap.addLocation(current_app.userlocation)
                 return render_template('user_page.html',userMap = current_app.usermap.myLocations,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
