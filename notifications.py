from flask import Blueprint, render_template,session,request,flash,jsonify
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation
from relation import Friend
from user import search
from request import Request
from request import RequestStore
notifications = Blueprint('notifications', __name__)

@notifications.route('/notificationsPage',methods=['POST','GET'])
def getNotifications():
    if session.get('user')!=None:
        current_app.requestStore.getRequests(current_app.user.username)
        return render_template('notifications.html',requests = current_app.requestStore.myRequests,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')

@notifications.route('/deleteFriendRequest',methods=['POST','GET'])
def deleteRequests():
    if session.get('user')!=None:
        if request.method == 'POST':
            requestId = request.form['request_to_delete']
            current_app.requestStore.deleteRequest(requestId)
            current_app.requestStore.getRequests(current_app.user.username)
            return render_template('notifications.html',requests = current_app.requestStore.myRequests,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')

