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
            query = """INSERT INTO EVENTTABLE (title,date,place) VALUES (%s, %s, %s)"""
        try: 
            cursor.execute(query, (event.title, event.date, event.place))
            self.last_key = cursor.lastrowid
            connection.commit()
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
            query = """ SELECT * FROM EVENTTABLE WHERE event_id= %s;"""
        try:
            cursor.execute(query,(event_id,))
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            else:        
                title = fetched_data[0]
                date = fetched_data[1]
                place = fetched_data[2]
                event_id = fetched_data[3]
                event = [(Event(title, event_id, date, place))]
            connection.commit()
            
        except connection.Error as error:
            print(error)
        connection.close()
        return event

    
    def get_events(self):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM EVENTTABLE ORDER BY event_id;"""
        try:
            cursor.execute(query)
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            title = fetched_data[0]
            date = fetched_data[1]
            place = fetched_data[2]
            event_id = fetched_data[3]
            events = [(Event(title, event_id, date, place))]
            for row in cursor: 
                title,date,place,event_id = row
                events_row = [(Event(title, event_id, date, place))]
                events += events_row     
            connection.commit()
                           
        except connection.Error as error:
            print(error)
        connection.close()
        return events
    
    def get_total_events(self):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT COUNT(*) FROM EVENTTABLE;"""
        try:
            cursor.execute(query)
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            total_count = fetched_data
            connection.commit()
                
        except connection.Error as error:
            print(error)
        connection.close()
        return total_count
        
        
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
        
    def update_event_id(self, event_id, new_id):
        event = current_app.store.get_event(event_id)
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE EVENTTABLE SET event_id = %s WHERE event_id = %s """
        try:
            cursor.execute(query,(int(new_id), event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
   