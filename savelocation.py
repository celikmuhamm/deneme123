import os
import json
import re
import psycopg2 as dbapi2
from sqlconnection import getConnection
from location import Location

class SaveLocation:
    def __init__(self):
        self.locations = {}
        self.lastid = 0

    def AddLocation(self, location):
        self.lastid += 1
        self.locations[self.lastid] = location
        location._id = self.lastid
        connection = getConnection()
        cursor = connection.cursor()
        query = """INSERT INTO MMAPTABLE (lat, long, photo, video, document) VALUES (%s, %s, %s, %s, %s)"""
        try:
            cursor.execute(query, (location.lat, location.long, location.photo, location.video, location.document))
            self.last_key = cursor.lastrowid
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

    def DeleteLocation(self, location_id):
        connection = getConnection()
        cursor = connection.cursor()
        query = """DELETE FROM MMAPTABLE WHERE location_id = %s"""
        try:
            cursor.execute(query,(location_id))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

    def GetLocation(self, location_id):
        connection = getConnection()
        cursor = connection.cursor()
        query = """ SELECT location_id,user_id,lat,long,photo,video,document FROM EVENTTABLE WHERE location_id= %s;"""
        try:
            cursor.execute(query,(location_id))
            fetched_data = cursor.fetchone()
            connection.commit()
            if fetched_data is None:
                status = 'Invalid or no location data'
                connection.close()
                return None
            else:
                location_id = fetched_data[0]
                lat = fetched_data[1]
                long = fetched_data[2]
                photo = fetched_data[3]
                video = fetched_data[4]
                document = fetched_data[5]
                location = Location(location_id, lat,long,photo,video,document)
        except connection.Error as error:
            print(error)
        connection.close()
        return location

    def GetLocations(self):
        connection = getConnection()
        cursor = connection.cursor()
        query = """ SELECT * FROM EVENTTABLE ORDER BY event_id;"""
        try:
            cursor.execute(query)
            fetched_data = cursor.fetchone()
            if fetched_data is None:
                status = 'No location data '
                connection.close()
                return None
            lat = fetched_data[0]
            long = fetched_data[1]
            photo = fetched_data[2]
            video = fetched_data[3]
            document = fetched_data[4]
            locations = [(Location(lat, long, photo, video, document))]
            for row in cursor:
                location_id, lat, long, photo, video, document = row
                locations_row = [(Location(location_id, lat, long, photo, video, document))]
                locations += locations_row
            connection.commit()

        except connection.Error as error:
            print(error)
        connection.close()
        return locations


    def UpdateLocation(self, event, event_id):
        connection = getConnection()
        cursor = connection.cursor()
        query = """UPDATE MMAPTABLE SET lat = %s, long = %s, photo = %s, video = %s, document = %s WHERE location_id = %s"""
        try:
            cursor.execute(query,(location.lat, location.long, location.photo, location.video, location.document))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

