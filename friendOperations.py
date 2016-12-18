from flask import Blueprint, render_template,session,request,flash,jsonify
from flask import current_app
from flask import redirect,url_for
from userMap import UserLocationStore
from userMap import UserLocation
from relation import Friend
from user import search
from request import Request
from request import RequestStore
friends = Blueprint('friends', __name__)

@friends.route('/friendsPage',methods=['POST','GET'])
def getFriends():
    if session.get('user')!=None:
        current_app.friendStore.getFriends(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')

@friends.route('/sendRequest',methods=['POST','GET'])
def sendRequests():
    if session.get('user')!=None:
        if request.method == 'POST':
            userName = request.form['user_name']
            status = search(userName,'someqw19012341')
            if userName != current_app.user.username:

                if status == 'Password is invalid':
                    currentName = current_app.user.username
                    relationStatus = current_app.friendStore.searchFriends(currentName,userName)
                    if relationStatus == 'alreadyExists':
                        flash('You are already friends 0_0 or you have been blocked :D')
                    else:
                        requestStatus = current_app.requestStore.searchRequests(currentName,userName)
                        if requestStatus == 'alreadySent':
                            flash('You already sent a friend request to '+userName)
                        elif requestStatus == 'alreadyReceived':
                            flash('You already received a friend request from '+userName+' Please check your Notifications page')
                        else:
                            requests = Request()
                            requests.requested = userName
                            requests.requester = current_app.user.username
                            current_app.requestStore.addRequest(requests)
                            flash('Friend request has been sent to '+userName)
                else:
                    flash('There is no user with this username: '+userName)
            else:
                flash('very funny -_-')
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')


@friends.route('/deleteFriend',methods=['POST','GET'])
def deleteFriends():
    if session.get('user')!=None:
        if request.method == 'POST':
            friendId = request.form['friend_to_delete']
            current_app.friendStore.deleteRelation(friendId)
            current_app.friendStore.getFriends(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')

@friends.route('/addFriend',methods=['POST','GET'])
def addFriends():
    if session.get('user')!=None:
        if request.method == 'POST':
            requestId = request.form['friend_to_add']
            requests =  current_app.requestStore.getRequest(requestId)
            friend = Friend()
            friend.userName = requests.requested
            friend.friendUsername = requests.requester
            current_app.friendStore.addFriend(friend)
            current_app.requestStore.deleteRequest(requestId)
            current_app.requestStore.getRequests(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
@friends.route('/addBestFriend',methods=['POST','GET'])
def addBestFriends():
    if session.get('user')!=None:
        if request.method == 'POST':
            friendId = request.form['friendsId']
            bestFriend = 'bestFriend'
            current_app.friendStore.updateFriends(friendId,bestFriend)
            current_app.friendStore.getFriends(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
@friends.route('/makeCasual',methods=['POST','GET'])
def makeCasualFriend():
    if session.get('user')!=None:
        if request.method == 'POST':
            friendId = request.form['friendsId']
            casualFriend = 'casualFriend'
            current_app.friendStore.updateFriends(friendId,casualFriend)
            current_app.friendStore.getFriends(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')
@friends.route('/blockFriend',methods=['POST','GET'])
def blockFriends():
    if session.get('user')!=None:
        if request.method == 'POST':
            friendId = request.form['friendsId']
            currusername = current_app.user.username
            current_app.friendStore.blockFriend(friendId,currusername)
            current_app.friendStore.getFriends(current_app.user.username)
        return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
    else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')

