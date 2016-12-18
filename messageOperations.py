from flask import Blueprint, render_template,session,request,flash,jsonify
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation
from relation import Friend
from message import Message
from user import search
messages = Blueprint('messages', __name__)

@messages.route('/messagePage',methods=['POST','GET'])
def getMessages():
    if session.get('user')!=None:
        current_app.messageStore.getMessages(current_app.user.username)
        return render_template('messages.html',messages = current_app.messageStore.conversations, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
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
            message.sender = current_app.user.username
            message.receiver = userName
            message.content = content;
            status = search(userName,'someqw19012341')
            if userName != current_app.user.username:

                if status == 'Password is invalid':
                    currentName = current_app.user.username
                    relationStatus = current_app.friendStore.searchFriends(currentName,userName)
                    if relationStatus == 'alreadyExists':
                        current_app.messageStore.sendMessage(message)
                        current_app.messageStore.getMessages(current_app.user.username)
                        xxx = current_app.messageStore.conversations[0].messages
                    else:
                        flash('you are not friends with '+userName)
                else:
                    flash('There is no user with this username: '+userName)
            else:
                flash('very funny -_-')
        return render_template('messages.html',messages = current_app.messageStore.conversations,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
@messages.route('/deleteMessage',methods=['POST','GET'])
def deleteMessages():
    if session.get('user')!=None:
        if request.method == 'POST':
            messageId = request.form['message_to_delete']
            current_app.messageStore.updateAndDeleteMessages(messageId,current_app.user.username)
            current_app.messageStore.getMessages(current_app.user.username)
        return render_template('messages.html',messages = current_app.messageStore.conversations,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')

