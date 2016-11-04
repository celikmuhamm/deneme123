'''
Created on 16 Eki 2016

@author: mert
'''
import os
import json
import re
import psycopg2 as dbapi2
from sql_connection_for_events import get_connection_for_events
from event import Event

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
            query = """DELETE FROM EVENTTABLE WHERE event_id = %s"""
        try:
            cursor.execute(query,(event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
    
    def get_event(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT title,date,place,content,event_id FROM EVENTTABLE WHERE event_id= %s;"""
        try:
            cursor.execute(query,(event_id,))
            fetched_data = cursor.fetchone()
            connection.commit()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            else:        
                title = fetched_data[0]
                content = fetched_data[1]
                date = fetched_data[2]
                place = fetched_data[3]
                event_id = fetched_data[4]
                event = Event(title, content, date, place)
        except connection.Error as error:
            print(error)
        connection.close()
        return event

    
    def get_events(self):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT title,date,place,content,event_id FROM EVENTTABLE ORDER BY event_id;"""
        try:
            cursor.execute(query)
            fetched_data = cursor.fetchone()
            connection.commit()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            title = fetched_data[0]
            content = fetched_data[1]
            date = fetched_data[2]
            place = fetched_data[3]
            event_id = fetched_data[4]
            events = [(event_id,(Event(title, content, date, place)))]
            for title, content, date, place, event_id in cursor: 
                events = [(event_id,(Event(title, content, date, place)))]
                
        except connection.Error as error:
            print(error)
        connection.close()
        return events
        
    def update_event(self, event, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE EVENTTABLE SET title = %s,date = %s, place = %s, content = %s WHERE event_id = %s"""
        try:
            cursor.execute(query,(event.title, event.date, event.place,event.content, event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
   