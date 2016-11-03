from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from user import User
from user import setUserToDb
from user import getUserFromDb
from user import search
from user import UserList
from userMap import UserLocationStore

register = Blueprint('register', __name__)

@register.route('/userPage',methods=['POST','GET'])
def login_page():

     if request.method == 'POST':
        username = request.form['username1']
        password = request.form.get('password1',None)
        status = search(username,password)
        if status == 'Success':
            current_app.user= getUserFromDb(username)
            session['user'] = username
            current_app.usermap.getLocations(username)
            return render_template('user_page.html',userMap = current_app.usermap.myLocations, user_name = username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
        else:
            flash(status)
            return render_template('home.html')

     if session.get('user')!=None:
        flash('Welcome back to your userpage: '+ current_app.user.username)
        return render_template('user_page.html',user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
     else:
        flash('Please sign in or register for DeepMap')
        return render_template('home.html')



@register.route('/register',methods=['GET', 'POST'])
def register_page():
     if request.method == 'POST':
         username = request.form['user_name']
         password = request.form['password']
         firstname = request.form['first_name']
         lastname = request.form['last_name']
         email = request.form['email']
         status = search(username,password)
         if status == 'There is no user with this username ':
             current_app.user.username = username
             current_app.user.password = password
             current_app.user.name = firstname
             current_app.user.surname = lastname
             current_app.user.email = email
             setUserToDb( current_app.user)
             return render_template('user_page.html',user_name = username,first_name = firstname,last_name = lastname,e_mail = email)
         else:
             flash('The username: '+username +' already using by another user' )
             return render_template('home.html')

     else:

         return render_template('home.html')
@register.route('/logout')
def log_out():
          session.pop('user', None)
          return render_template('home.html')
      
@register.route('/adminPage')
def adminPage():
          if current_app.user.username == 'deepMapAdmin':
              current_app.userList.getUsers()
              return render_template('adminPage.html',user_name = current_app.user.username,userTable = current_app.userList.userTable)
          else: 
              return render_template('home.html')
      
