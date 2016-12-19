'''
Created on 16 Eki 2016

@author: mert
'''
import os
import json
import re
import psycopg2 as dbapi2
from sql_connection_for_events import get_connection_for_events
from event import Document
from flask import current_app

class Store_Document:
    def __init__(self):
        self.documents = {}
        self.last_document_id = 0

    def add_document(self, document):
        self.last_document_id += 1
        self.documents[self.last_document_id] = document
        document._id = self.last_document_id
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            title = document.title
            date = document.date
            event_id = document.event_id
            document_id = document.document_id
            content = document.content
#            username = current_app.user.username;
#            query = """INSERT INTO DOCUMENTTABLE (title,date,content,event_id,document_id,username) VALUES (%s, %s, %s, %s, %s, %s)"""
            query = """INSERT INTO DOCUMENTTABLE (title,date,content,event_id,document_id) VALUES (%s, %s, %s, %s, %s)"""
        try: 
#            cursor.execute(query, (title,date,content,event_id,document_id, username))
            cursor.execute(query, (title,date,content,event_id,document_id))
            self.last_key = cursor.lastrowid
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

    def delete_document(self, document_id, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM DOCUMENTTABLE WHERE event_id = %s AND document_id = %s"""
        try:
            cursor.execute(query,(event_id,document_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        
    def get_document_id(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT COUNT(*) FROM DOCUMENTTABLE WHERE event_id= %s;"""
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
        
    
    def get_document(self, document_id, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM DOCUMENTTABLE WHERE event_id= %s AND document_id = %s;"""
        try:
            cursor.execute(query,(event_id,document_id))
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            else:        
                title = fetched_data[0]
                date = fetched_data[1]
                content = fetched_data[2]
                event_id = fetched_data[3]
                document_id = fetched_data[4]
                document = Document(event_id, document_id, content, title, date)
            connection.commit()
            
        except connection.Error as error:
            print(error)
        connection.close()
        return document

    
    def get_documents(self, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT * FROM DOCUMENTTABLE WHERE event_id = %s ORDER BY document_id;"""
        try:
            cursor.execute(query,(event_id,))
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            title = fetched_data[0]
            date = fetched_data[1]
            content = fetched_data[2]
            event_id = fetched_data[3]
            document_id = fetched_data[4]
            document = [(Document(event_id, document_id, content, title, date))]
            document_array = document
            for title, date, content, event_id, document_id in cursor: 
                document = [(Document(event_id, document_id, content, title, date))]
                document_array += document
            connection.commit()
                
        except connection.Error as error:
            print(error)
        connection.close()
        return document_array
        
    def update_document(self, document, event_id, document_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE DOCUMENTTABLE SET title = %s,date = %s, content = %s WHERE event_id = %s AND document_id = %s"""
        try:
            cursor.execute(query,(document.title, document.date, document.content, event_id, document_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
        
        
    def update_document_id(self, document_id, event_id, new_id):
        document = current_app.store_documents.get_document(document_id,event_id)
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE DOCUMENTTABLE SET document_id = %s WHERE event_id = %s AND document_id = %s """
        try:
            cursor.execute(query,(new_id, event_id, document_id))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
   
