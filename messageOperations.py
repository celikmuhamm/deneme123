from flask import Blueprint, render_template,session,request,flash,jsonify
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation
from relation import Friend
from message import Message
messages = Blueprint('messages', __name__)

@messages.route('/messagePage',methods=['POST','GET'])
def getMessages():
    if session.get('user')!=None:
        current_app.messageStore.getMessages(current_app.user.username)
        return render_template('messages.html',messages = current_app.messageStore.myMessages, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
    
@messages.route('/sendMessage',methods=['POST','GET'])
def sendMessages():
    if session.get('user')!=None:
        if request.method == 'POST':
            userName = request.form['user_name']
            content = request.form['content']
            message = Message()
            message.friendUsername = current_app.user.username
            message.userName = userName
            message.content = content;
            current_app.messageStore.addMessages(message)
        return render_template('messages.html',messages = current_app.messageStore.myMessages,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')