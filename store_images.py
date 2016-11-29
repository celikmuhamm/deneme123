'''
Created on 16 Eki 2016

@author: mert
'''
import os
import json
import re
import psycopg2 as dbapi2
from sql_connection_for_events import get_connection_for_events
from event import Event,Image
from flask import current_app


class Store_Image:
    def __init__(self):
        self.images = {}
        self.last_image_id = 0

    def add_image(self, image):
        self.last_image_id = self.get_image_id(image.event_id)
        self.last_image_id += 1
        self.images[self.last_image_id] = image
        image._id = self.last_image_id
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            date = image.date
            event_id = image.event_id
            content = image.content
            image_id = image.image_id
            query = """INSERT INTO IMAGETABLE (date,event_id,content,image_id) VALUES (%s, %s, %s, %s)"""
        try: 
            cursor.execute(query, (date, event_id, content, image_id))
            self.last_key = cursor.lastrowid
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

    def delete_image(self, image_id, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM IMAGETABLE WHERE event_id = %s AND image_id = %s"""
        try:
            cursor.execute(query,(event_id,image_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        
    def get_image_id(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT COUNT(*) FROM IMAGETABLE WHERE event_id = %s;"""
        try:
            cursor.execute(query,(event_id,))
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            else:        
                count_image = fetched_data[0]
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        return count_image
    
    def get_image(self, image_id, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM IMAGETABLE WHERE event_id= %s AND image_id = %s;"""
        try:
            cursor.execute(query,(event_id,image_id,))
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            else:        
                event_id = fetched_data[0]
                image_id = fetched_data[1]
                date = fetched_data[2]
                content = fetched_data[3]
                image = Image(event_id, image_id, date, content)
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        return image

    
    def get_images(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM IMAGETABLE where event_id =%s ORDER BY image_id;"""
        try:
            cursor.execute(query,(event_id,))
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            event_id = fetched_data[0]
            image_id = fetched_data[1]
            date = fetched_data[2]
            content = fetched_data[3]
            image_row = [(Image(event_id, image_id, content, date))]
            images = image_row
            for event_id, image_id, date, content in cursor: 
                image_row = [(Image(event_id, image_id, content, date))]
                images += image_row
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        return images
    
    def update_image_id(self, image_id, event_id, new_id):
        image = current_app.store_images.get_image(image_id,event_id)
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE IMAGETABLE SET image_id = %s WHERE event_id = %s """
        try:
            cursor.execute(query,(int(new_id), event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
   