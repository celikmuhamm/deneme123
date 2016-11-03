from sqlconnection import getConnection

class UserLocation:
    def __init__(self, userName=None, mapInfo=None, address=None, lat=None, lng=None):
        self.userName = userName
        self.mapInfo = mapInfo
        self.address = address
        self.lat = lat
        self.lng = lng
        self.locationId=0

class UserLocationStore:
    def __init__(self):
        self.myLocations = []
        self.lastLocationId = 0

    def addLocation(self, userLocation):
        self.lastLocationId+= 1
        userLocation.locationId=self.lastLocationId
        self.myLocations.append(userLocation)
        try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapCursor.execute("""INSERT INTO USERMAPTABLE (userMap_id,user_id,mapInformation,address,lat,lng) VALUES(%s,%s,%s,%s,%s,%s)""", (userLocation.locationId, userLocation.userName, userLocation.mapInfo, userLocation.address, userLocation.lat, userLocation.lng ))
            userMapConnection.commit()

        except userMapConnection.Error as userMapError:
            print(userMapError)

        userMapConnection.close()

    def getLocations(self,username):
        try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapCursor.execute("""SELECT * FROM USERMAPTABLE WHERE user_id=%s""",(username,))
            userMapConnection.commit()
            dbData = userMapCursor.fetchall()
            if dbData != None:
                for locations in dbData:

                    userLocations = UserLocation()
                    userLocations.userName = locations[1]
                    userLocations.mapInfo = locations[2]
                    userLocations.address = locations[3]
                    userLocations.lat = locations[4]
                    userLocations.lng = locations[5]
                    userLocations.locationId=locations[0]
                    self.myLocations.append(userLocations)
                    self.lastLocationId += 1


        except userMapConnection.Error as userMapError:
            print(userMapError)

        userMapConnection.close()
        return self

    def updateLocationInformation(self, locationId, newInfo):
         try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapcursor.execute("""UPDATE USERMAPTABLE SET mapInformation=%s WHERE userMap_id=%d""",(newInfo,locationId))
            userMapConnection.commit()
         except userMapConnection.Error as userMapError:
            print(userMapError)

         userMapConnection.close()

    def updateLocationAddress(self, locationId, newAddress):
         try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapcursor.execute("""UPDATE USERMAPTABLE SET address=%s WHERE userMap_id=%d""",(newaddress,locationId))
            userMapConnection.commit()
         except userMapConnection.Error as userMapError:
            print(userMapError)

         userMapConnection.close()

    def deleteLocation(self, locationId, newAddress):
         try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapcursor.execute("""DELETE FROM USERMAPTABLE WHERE userMap_id=%d""",(locationId,))
            userMapConnection.commit()
         except userMapConnection.Error as userMapError:
            print(userMapError)

         userMapConnection.close()