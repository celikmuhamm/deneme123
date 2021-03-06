import os
import json
import re
import psycopg2 as dbapi2
from handlers import site
from sql_connection_for_events import get_connection_for_events
from sqlconnection import getConnection

def init_db():
    dsn = get_connection_for_events()
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()

        """cursor.execute(DROP TABLE IF  EXISTS USERTABLE )"""

#        query = """DROP TABLE IF  EXISTS DOCUMENTTABLE """
#        cursor.execute(query)
#        query = """DROP TABLE IF  EXISTS IMAGETABLE """
#        cursor.execute(query)
#        query = """DROP TABLE IF  EXISTS EVENTTABLE """
#        cursor.execute(query)

        cursor.execute("""DROP TABLE IF  EXISTS TIMETABLE """)

        cursor.execute("""DROP TABLE IF  EXISTS MMAPTABLE""") #main map table

    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS EVENTTABLE (title varchar(30), date varchar(10), place varchar(40), event_id serial primary key)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS IMAGETABLE (event_id int references eventtable ON DELETE CASCADE , image_id int not null, date varchar(10), content text, primary key (event_id,image_id))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS DOCUMENTTABLE (title varchar(30), date varchar(10), content text, event_id int references eventtable ON DELETE CASCADE, document_id int not null, primary key (event_id, document_id))""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS TIMETABLE (map_id varchar(40) primary key references TIMEMAPTABLE(mapID) on delete cascade, decade int not null,year int not null,share_date date not null,content_type varchar(40),content_header  varchar(40))""")

 #       cursor.execute("""INSERT INTO TIMETABLE (map_id,decade,year,share_date,content_type,content_header) VALUES ('1',1960,1963,'1963-08-22','text','X-15 aircraft')""" )

 #       cursor.execute("""INSERT INTO TIMETABLE (map_id,decade,year,share_date,content_type,content_header) VALUES ('2',2010,2016,'1963-06-03','text','Mohammed Morsi')""" )

 #       cursor.execute("""INSERT INTO MMAPTABLE (post_id,user_id,lat,long,photo,video,document) VALUES (1,1,'41.1055936','29.0253398','https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/ITU-Lecture-Hall.JPG/270px-ITU-Lecture-Hall.JPG')""" )

        connection.commit()
    except connection.Error as error:
            print(error)

    connection.close()

    try:
         conn = getConnection()
         userCursor = conn.cursor()
         userCursor.execute("""CREATE TABLE IF NOT EXISTS USERTABLE (userId SERIAL PRIMARY KEY,username varchar(20) UNIQUE,password varchar(20), email varchar(40),name varchar(20),surname varchar(20))""")
         conn.commit()

    except conn.Error as userError:
        print(userError)

    conn.close()
    try:
         timeMapconnection = getConnection();
         timeMapCursor = timeMapconnection.cursor()
         timeMapCursor.execute("""DROP TABLE IF  EXISTS TIMEMAPTABLE """)
         timeMapCursor.execute("""CREATE TABLE IF NOT EXISTS TIMEMAPTABLE (mapID varchar(40) primary key, number_of_shared_item int not null)""")
         timeMapCursor.execute("""INSERT INTO TIMEMAPTABLE (mapID,number_of_shared_item) VALUES ('0',60)""")
         timeMapCursor.execute("""INSERT INTO TIMEMAPTABLE (mapID,number_of_shared_item) VALUES ('1',190)""")
         timeMapCursor.execute("""INSERT INTO TIMEMAPTABLE (mapID,number_of_shared_item) VALUES ('2',160)""")
         timeMapCursor.execute("""INSERT INTO TIMEMAPTABLE (mapID,number_of_shared_item) VALUES ('3',1000)""")
         timeMapconnection.commit()
    except timeMapconnection.Error as timeMapError:
         print(timeMapError)

    timeMapconnection.close()
    try:
         userMapConnection = getConnection()
         userMapCursor = userMapConnection.cursor()
         userMapCursor.execute("""CREATE TABLE IF NOT EXISTS USERMAPTABLE (userMap_id INT,user_id varchar(20),mapInformation varchar(250),locationLabel varchar(30),lat FLOAT(10) NOT NULL,lng FLOAT(10) NOT NULL)""")
         userMapConnection.commit()

    except userMapConnection.Error as userMapError:
        print(userMapError)

    userMapConnection.close()

    try:

         socialTableconn = getConnection()
         socialTablecursor = socialTableconn.cursor()
         socialTablecursor.execute("""CREATE TABLE IF NOT EXISTS FRIENDSTABLE (friendRecordId SERIAL PRIMARY KEY ,user_id varchar(20) references USERTABLE(username) on delete cascade,firends_id varchar(20) references USERTABLE(username) on delete cascade,status varchar(20))""")
         socialTableconn.commit()

    except socialTableconn.Error as socialError:
        print(socialError)

    socialTableconn.close()

    try:
        requestTableconn = getConnection()
        requestTableCursor = requestTableconn.cursor()
        requestTableCursor.execute("""CREATE TABLE IF NOT EXISTS REQUESTTABLE (requestId SERIAL PRIMARY KEY, requester varchar(20) references USERTABLE(username) on delete cascade, requested varchar(20) references USERTABLE(username) on delete cascade)""")
        requestTableconn.commit()
    except requestTableconn.Error as requestError:
        print(requestError)


    try:

         messageTableConn = getConnection()
         messageTableCursor = messageTableConn.cursor()
         messageTableCursor.execute("""CREATE TABLE IF NOT EXISTS MESSAGETABLE (messageId SERIAL PRIMARY KEY,user_id varchar(20) references USERTABLE(username) on delete cascade,firends_id varchar(20) references USERTABLE(username) on delete cascade,content varchar(300),status varchar(20))""")
         messageTableConn.commit()

    except messageTableConn.Error as messageError:
        print(messageError)

    messageTableConn.close()

    try:

         commentTableConn = getConnection()
         commentTableCursor = commentTableConn.cursor()
         commentTableCursor.execute("""CREATE TABLE IF NOT EXISTS COMMENTTABLE (commentId SERIAL PRIMARY KEY,userId INT references USERTABLE(userId) on delete cascade,user_name varchar(20) references USERTABLE(username) on delete cascade,friendUsername varchar(20) references USERTABLE(username) on delete cascade,content varchar(300))""")
         commentTableConn.commit()

    except commentTableConn.Error as messageError:
        print(messageError)

    commentTableConn.close()
    try:

         notificationTableConn = getConnection()
         notificationTableCursor = notificationTableConn.cursor()
         notificationTableCursor.execute("""CREATE TABLE IF NOT EXISTS NOTIFICATIONTABLE (notificationId SERIAL PRIMARY KEY,user_name varchar(20) references USERTABLE(username) on delete cascade,friendUsername varchar(20) references USERTABLE(username) on delete cascade,messageId INT references MESSAGETABLE(messageId),commentId INT references COMMENTTABLE(commentId))""")
         notificationTableConn.commit()

    except notificationTableConn.Error as messageError:
        print(messageError)

    notificationTableConn.close()