
import os
import json
import re
import psycopg2 as dbapi2
from sql_connection_for_events import get_connection_for_events
from timeModel import Time

class Timesql:
    def __init__(self):
        self.timeline = {}
        self.last_map_id = 0

    def add_timeinfo(self, time):
        self.last_map_id += 1
        self.timeline[self.last_map_id] = time
        map._id = self.last_map_id
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            map_id=time.map_id
            decade=time.decade
            year=time.year
            share_date=time.share_date
            content_type=time.content_type
            content_header=time.content_header
            query = """INSERT INTO TIMETABLE (map_id,decade,year,share_date,content_type,content_header) VALUES (%s, %d, %d, %d, %s, %s)"""
        try:
            cursor.execute(query, (time.map_id, time.decade, time.year, time.share_date,time.content_type,time.content_header ))
            connection.commit()
            self.last_key = cursor.lastrowid
        except connection.Error as error:
            print(error)
        connection.close()

    def delete_timeinfo(self, map_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM TIMETABLE WHERE map_id = %s"""
        try:
            cursor.execute(query,(map_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

    def get_time(self, map_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT map_id,decade,year,share_date,content_type,content_header FROM TIMETABLE WHERE map_id= %s;"""
        try:
            cursor.execute(query,(map_id,))
            fetched_data = cursor.fetchone()
            connection.commit()
            if fetched_data is None:
                status = 'There is no timeinfo '
                connection.close()
                return None
            else:
                map_id=fetched_data[0]
                decade=fetched_data[1]
                year=fetched_data[2]
                share_date=fetched_data[3]
                content_type=fetched_data[4]
                content_header=fetched_data[5]
                time = Time(decade, year, share_date, content_type,content_header)
        except connection.Error as error:
            print(error)
        connection.close()
        return time


    def get_timeinfo(self):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """ SELECT map_id,decade,year,share_date,content_type,content_header FROM TIMETABLE ORDER BY map_id;"""
        try:
            cursor.execute(query)
            fetched_data = cursor.fetchone()
            connection.commit()
            if fetched_data is None:
                status = 'There is no event '
                connection.close()
                return None
            map_id=fetched_data[0]
            decade=fetched_data[1]
            year=fetched_data[2]
            share_date=fetched_data[3]
            content_type=fetched_data[4]
            content_header=fetched_data[5]
            timeline = [(map_id,(Time(title, content, date, place)))]
            for title, content, date, place, event_id in cursor:
                events = [(event_id,(Event(decade, year, share_date, content_type,content_header)))]

        except connection.Error as error:
            print(error)
        connection.close()
        return timeline

    def update_timeinfo(self, time, map_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE TIMETABLE SET decade = %d, year = %d, share_date = %d, content_type= %s,content_header= %s WHERE map_id = %s"""
        try:
            cursor.execute(query,( map_id, time.decade, time.year,time.share_date,time.content_type,time.content_header,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()
