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

#        query = """DROP TABLE IF  EXISTS EVENTTABLE"""
#        cursor.execute(query)

        cursor.execute("""DROP TABLE IF  EXISTS TIMETABLE """)

        cursor.execute("""DROP TABLE IF  EXISTS MMAPTABLE""") #main map table

    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS EVENTTABLE (title varchar(30), date varchar(10), place varchar(40), content varchar(150), event_id serial primary key)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS TIMETABLE (map_id varchar(40) primary key, decade int not null,year int not null,share_date date not null,content_type varchar(40),content_header  varchar(40))""")

        cursor.execute("""INSERT INTO TIMETABLE (map_id,decade,year,share_date,content_type,content_header) VALUES ('1',1960,1963,'1963-08-22','text','X-15 aircraft')""" )

        cursor.execute("""INSERT INTO TIMETABLE (map_id,decade,year,share_date,content_type,content_header) VALUES ('2',2010,2016,'1963-06-03','text','Mohammed Morsi')""" )

 #       cursor.execute("""INSERT INTO MMAPTABLE (post_id,user_id,lat,long,photo,video,document) VALUES (1,1,'41.1055936','29.0253398','https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/ITU-Lecture-Hall.JPG/270px-ITU-Lecture-Hall.JPG')""" )

        connection.commit()
    except connection.Error as error:
            print(error)

    connection.close()

    try:
         conn = getConnection();
         userCursor = conn.cursor()
         userCursor.execute("""CREATE TABLE IF NOT EXISTS USERTABLE (username varchar(20) UNIQUE,password varchar(20), email varchar(40),name varchar(20),surname varchar(20))""")
         conn.commit()

    except conn.Error as userError:
        print(userError)

    conn.close()

    try:
         userMapConnection = getConnection();
         userMapCursor = userMapConnection.cursor()
         userMapCursor.execute("""DROP TABLE IF  EXISTS USERMAPTABLE """)
         userMapCursor.execute("""CREATE TABLE IF NOT EXISTS USERMAPTABLE (userMap_id INT,user_id varchar(20),mapInformation varchar(250),locationLabel varchar(30),lat FLOAT(10) NOT NULL,lng FLOAT(10) NOT NULL)""")
         userMapConnection.commit()

    except userMapConnection.Error as userMapError:
        print(userMapError)

    userMapConnection.close()
    
    try:
         
         socialTableconn = getConnection();
         socialTablecursor = socialTableconn.cursor()
         socialTablecursor.execute("""DROP TABLE IF  EXISTS FRIENDSTABLE """)
         socialTablecursor.execute("""CREATE TABLE IF NOT EXISTS FRIENDSTABLE (friendRecordId INT,user_id varchar(20) references USERTABLE(username) on delete cascade,firends_id varchar(20) references USERTABLE(username) on delete cascade)""")
         socialTableconn.commit()

    except socialTableconn.Error as socialError:
        print(socialError)

    socialTableconn.close()