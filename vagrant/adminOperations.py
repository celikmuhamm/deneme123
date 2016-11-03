from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from user import User
from user import UserList
from user import deleteUser
from user import updateUser
adminTable = Blueprint('adminTable', __name__)


@adminTable.route('/deleteFunction',methods=['POST','GET'])
def deleteFunction():
             userName = request.form['user_name']
             deleteUser(userName)
             current_app.userList.getUsers()
             return render_template('adminPage.html',user_name = current_app.user.username,userTable = current_app.userList.userTable)

@adminTable.route('/updateFunction',methods=['POST','GET'])
def updateFunction():
              User.username = username
              User.password = password
              User.name = firstname
              User.surname = lastname
              User.email = email
              updateUser(User)
              current_app.userList.getUsers()
              return render_template('adminPage.html',user_name = current_app.user.username,userTable = current_app.userList.userTable)