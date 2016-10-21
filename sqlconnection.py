import os
import json
import re
import psycopg2 as dbapi2
from handlers import site

def get_sqldb_dsn(vcap_services):
    """Returns the data source name for IBM SQL DB."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)',uri)
    user,password,host, _,port,dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={} dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


def initialize_database():
    connection = getConnection();
    cursor = connection.cursor()
    """cursor.execute(DROP TABLE IF  EXISTS USERTABLE )"""
    try:
       cursor.execute("""CREATE TABLE IF NOT EXISTS USERTABLE (username varchar(20),password varchar(20), email varchar(40),name varchar(20),surname varchar(20))""")
       connection.commit()
    except connection.Error as error:
            print(error)
   
        
    connection.close()



def getConnection():
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        dsn = get_sqldb_dsn(VCAP_SERVICES)
    else:
       dsn = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    
    with dbapi2.connect(dsn) as connection:
        return connection;
                               