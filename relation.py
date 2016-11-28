from sqlconnection import getConnection

class Friend:
    def __init__(self, userName=None    , friendUsername=None):
        self.userName = userName
        self.friendUsername = friendUsername
        self.friendId = 0
class FriendStore:
    def __init__(self):
        self.myFriends = []
        self.lastFriendId = 0

    def addFriend(self, Friend):
        self.lastFriendId+= 1
        Friend.friendId=self.lastFriendId
        self.myFriends.append(Friend)
        try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""INSERT INTO FRIENDSTABLE (friendRecordId,user_id,firends_id) VALUES(%s,%s,%s);""", (Friend.friendId,Friend.userName,Friend.friendUsername))
            friendTableConnection.commit()
            friendCursor.close()
            friendTableConnection.close()
        except friendTableConnection.Error as Error:
            print(Error)


    def getFriends(self,username):
        try:
            self.lastFriendId = 0
            self.myFriends = []
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""SELECT * FROM FRIENDSTABLE WHERE user_id=%s;""",(username,))
            friendTableConnection.commit()
            dbData = friendCursor.fetchall()
            if dbData != None:
                for friends in dbData:

                    myFriend = Friend()
                    myFriend.userName = friends[1]
                    myFriend.friendUsername = friends[2]
                    self.myFriends.append(myFriend)
                    self.lastFriendId += 1

            friendCursor.close()
           
            friendTableConnection.close()
        except friendTableConnection.Error as Error:
            print(Error)
        return self

    def updateFriends(self,friendId,newInfo):
         try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""UPDATE FRIENDSTABLE SET firends_id=%s WHERE userMap_id=%d;""",(newInfo,friendId))
            friendTableConnection.commit()
         except friendTableConnection.Error as Error:
            print(Error)

         friendTableConnection.close()

    def deleteRelation(self, friendId):
         try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""DELETE FROM FRIENDSTABLE WHERE userMap_id=%d;""",(friendId,))
            friendTableConnection.commit()
         except friendTableConnection.Error as Error:
            print(Error)

         friendTableConnection.close()