from flask import Blueprint, render_template,session,request,flash
from flask import current_app
from flask import redirect,url_for
from datetime import datetime
from flask_login import LoginManager
from wtforms import Form
from user import User
from user import setUserToDb
from user import getUserFromDb
from user import search
register = Blueprint('register', __name__)

@register.route('/userPage',methods=['POST','GET'])
def login_page():

     if request.method == 'POST':
        username = 'blabla'
        username = request.form['username1']
        password = request.form.get('password1',None)
        status = search(username,password)
        if status == 'Success':
            current_app.user= getUserFromDb(username)
            session['user'] = username
            return render_template('user_page.html',user_name = username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
        else:
            return render_template('home.html')
    
     if session.get('user')==current_app.user.username:
        return render_template('user_page.html',user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
     else:
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
         if status is not 'Password is invalid':
             current_app.user.username = username
             current_app.user.password = password
             current_app.user.name = firstname
             current_app.user.surname = lastname
             current_app.user.email = email
             setUserToDb( current_app.user)
             return render_template('user_page.html',user_name = username,first_name = firstname,last_name = lastname,e_mail = email)
         
     else:
         return render_template('home.html')
@register.route('/logout')     
def log_out():
          session.pop('user', None)       
          return render_template('home.html')   
