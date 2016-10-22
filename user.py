from sqlconnection import getConnection
from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username=None,  password=None,email=None, name=None,surname=None):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        
    def get_id(self):
        return self.username

def search(username,password):
        conn = getConnection()
        cursor = conn.cursor()

        try:
            cursor.execute(""" SELECT * FROM USERTABLE WHERE username= %s;""",
                        (username,)
                    )
            conn.commit()
            dbData = cursor.fetchone()
            
            if dbData is None:
                status = 'There is no user with this username: ' + username +' ,if you not already, Sign-up for free!'
            else:
                if password == dbData[1]:  
                    status = 'Success'
                else:
                    status = 'Password is invalid'

        except conn.Error as error:
            print(error)
            status = 'Password or Username is invalid' 

        cursor.close()
        conn.close()
        return status

def get_user(user_id):
        user = current_app.user
        return user    
def getUserFromDb(username):
    conn = getConnection()
    cursor = conn.cursor()
    try:
            cursor.execute(""" SELECT * FROM USERTABLE WHERE username= %s;""",
                        (username,)
                    )
            conn.commit()
            dbData = cursor.fetchone()
            User.username = dbData[0]
            User.password = dbData[1]
            User.email= dbData[2]
            User.name = dbData[3]
            User.surname = dbData[4]
            cursor.close()
            conn.close()
            return User
    except conn.Error as error:
            print(error)
            return 'Error'
def setUserToDb(User):
    connection = getConnection()
    cursor = connection.cursor()
    username = User.username
    password = User.password
    email = User.email
    name = User.name
    surname =User.surname
    try:
        cursor.execute("""INSERT INTO USERTABLE (username, password, email, name, surname) VALUES(%s,%s,%s,%s,%s);""",(username,password,email,name,surname))
        connection.commit()
        connection.close()
    except connection.Error as error:
            print(error)