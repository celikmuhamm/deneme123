from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from user import User
from user import UserList

adminTable = Blueprint('adminTable', __name__)


@adminTable.route('/adminTable',methods=['POST','GET'])
def updateFunction():
    if request.method == 'GET':
        return render_template('home.html')
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


                 return render_template('user_page.html',userMap = current_app.usermap.myLocations,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
