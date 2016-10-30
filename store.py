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
            query = """INSERT INTO EVENTTABLE (title,date,place) VALUES (%s, %s, %s)"""
        try: 
            cursor.execute(query, (event.title, event.date, event.place))
            connection.commit()
            self.last_key = cursor.lastrowid
        except connection.Error as error:
            print(error)
        connection.close()

    def delete_event(self, event_id):
        del self.events[event_id]

    def get_event(self, event_id):
        return self.events[event_id]

    def get_events(self):
        return self.events