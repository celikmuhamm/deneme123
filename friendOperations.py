from flask import Blueprint, render_template,session,request,flash,jsonify
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation
from relation import Friend

friends = Blueprint('friends', __name__)

@friends.route('/friendsPage',methods=['POST','GET'])
def getFriends():
    if session.get('user')!=None:
        current_app.friendStore.getFriends(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
    
@friends.route('/addNewFriends',methods=['POST','GET'])
def addFriends():
    if session.get('user')!=None:
        if request.method == 'POST':
            userName = request.form['user_name']
            friend = Friend()
            friend.friendUsername = userName
            friend.userName = current_app.user.username
            current_app.friendStore.addFriend(friend)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
    
    
@friends.route('/deleteFriend',methods=['POST','GET'])
def deleteFriends():
    if session.get('user')!=None:
        if request.method == 'POST':
            userName = request.form['user_name']
            friend = Friend()
            friend.friendUsername = userName
            friend.userName = current_app.user.username
            current_app.friendStore.addFriend(friend)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')