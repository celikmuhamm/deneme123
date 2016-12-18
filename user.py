from sqlconnection import getConnection
from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username=None,  password=None,email=None, name=None,surname=None):
        self.userId = None
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
                status = 'There is no user with this username '
            else:
                if password == dbData[2]:
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
            User.userId = dbData[0]
            User.username = dbData[1]
            User.password = dbData[2]
            User.email= dbData[3]
            User.name = dbData[4]
            User.surname = dbData[5]
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
def updateUser(User):
    connection = getConnection()
    cursor = connection.cursor()
    username = User.username
    password = User.password
    email = User.email
    name = User.name
    surname =User.surname
    try:
        cursor.execute("""UPDATE USERTABLE SET username=%s, password=%s,email=%s, name=%s, surname=%s WHERE username=%s;""",(username,password,email,name,surname,username))
        connection.commit()
        connection.close()
    except connection.Error as error:
            print(error)

def deleteUser(username):
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("""DELETE FROM USERTABLE WHERE username=%s;""",(username,))
        connection.commit()
        connection.close()
    except connection.Error as error:
            print(error)


class UserList:
    def __init__(self):
        self.userTable = []
        self.lastUserCounter = 0

    def getUsers(self):
            conn = getConnection()
            cursor = conn.cursor()
            self.userTable = []
            self.lastUserCounter = 0
            try:
                    cursor.execute(""" SELECT * FROM USERTABLE;""")

                    conn.commit()
                    dbData = cursor.fetchall()
                    if dbData != None:
                        for users in dbData:

                            user = User()
                            user.userId = users[0]
                            user.username = users[1]
                            user.password = users[2]
                            user.email = users[3]
                            user.name = users[4]
                            user.surname = users[5]
                            self.userTable.append(user)
                            self.lastUserCounter += 1

                    cursor.close()
                    conn.close()
                    return User
            except conn.Error as error:
                    print(error)
                    return 'Error'
            return self