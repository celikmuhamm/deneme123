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
        if request.method == 'POST':
             userName = request.form['user_name']
             deleteUser(userName)
             current_app.userList.getUsers()
             return render_template('adminPage.html',user_name = current_app.user.username,userTable = current_app.userList.userTable)
        else:
             return render_template('home.html')

@adminTable.route('/updateFunction',methods=['POST','GET'])
def updateFunction():
        if request.method == 'POST':
              username = request.form['user_name']
              password = request.form['password']
              firstname = request.form['first_name']
              lastname = request.form['last_name']
              email = request.form['email']
              User.username = username
              User.password = password
              User.name = firstname
              User.surname = lastname
              User.email = email
              updateUser(User)
              current_app.userList.getUsers()
              return render_template('adminPage.html',user_name = current_app.user.username,userTable = current_app.userList.userTable)
        else:
             return render_template('home.html')