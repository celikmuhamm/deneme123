'''
Created on 16 Eki 2016

@author: mert
'''
import os
import json
import re
import psycopg2 as dbapi2
from sql_connection_for_events import get_connection_for_events

class Store:
    def __init__(self):
        self.events = {}
        self.last_event_id = 0

    def add_event(self, event):
        self.last_event_id += 1
        self.events[self.last_event_id] = event
        event._id = self.last_event_id
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            title = event.title
            date = event.date
            place = event.place
            content = event.content
            query = """INSERT INTO EVENTTABLE (title,date,place,content) VALUES (%s, %s, %s, %s)"""
        try: 
            cursor.execute(query, (event.title, event.date, event.place, event.content))
            connection.commit()
            self.last_key = cursor.lastrowid
        except connection.Error as error:
            print(error)
        connection.close()

    def delete_event(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM EVENTTABLE WHERE event_id = %d"""
        try:
            cursor.execute(query,(event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        del self.events[event_id]
    
    def get_event(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT title,date,place,content FROM EVENTTABLE WHERE event_id= %d;"""
        try:
            cursor.execute(query,(event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
    
        return self.events[event_id]

    def get_events(self):
        return self.events
    
    def update_event(self, event, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE EVENTTABLE SET title = %s,date = %s, place = %s, content = %s WHERE event_id = %d"""
        try:
            cursor.execute(query,(event.title, event.date, event.place,event.content, event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        self.events[event_id] = event
