from sqlconnection import getConnection

class Friend:
    def __init__(self, userName=None    , friendUsername=None):
        self.userName = userName
        self.friendUsername = friendUsername
        self.friendStatus = None
        self.friendId = 0
class FriendStore:
    def __init__(self):
        self.myFriends = []
        self.lastFriendId = 0

    def addFriend(self, Friend):
        self.lastFriendId+= 1
        Friend.friendStatus = 'casualFriend'
        self.myFriends.append(Friend)
        try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""INSERT INTO FRIENDSTABLE (user_id,firends_id,status) VALUES(%s,%s,%s);""", (Friend.userName,Friend.friendUsername,Friend.friendStatus))
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
                    myFriend.friendId = friends[0]
                    myFriend.userName = friends[1]
                    myFriend.friendUsername = friends[2]
                    if friends[3] != 'blocked2':
                        if friends[3] == 'blocked1':
                            myFriend.friendStatus = 'blockedByMe'
                        else:
                            myFriend.friendStatus = friends[3]
                        self.myFriends.append(myFriend)
                        self.lastFriendId += 1
            friendCursor.execute("""SELECT * FROM FRIENDSTABLE WHERE firends_id=%s;""",(username,))
            friendTableConnection.commit()
            dbData = friendCursor.fetchall()
            if dbData != None:
                for friends in dbData:

                    myFriend = Friend()
                    myFriend.friendId = friends[0]
                    myFriend.userName = friends[2]
                    myFriend.friendUsername = friends[1]
                    if friends[3] != 'blocked1':
                        if friends[3] == 'blocked2':
                            myFriend.friendStatus = 'blockedByMe'
                        else:
                            myFriend.friendStatus = friends[3]
                        self.myFriends.append(myFriend)
                        self.lastFriendId += 1
            friendCursor.close()
            friendTableConnection.close()
        except friendTableConnection.Error as Error:
            print(Error)
        return self
    def searchFriends(self,username,friendsname):
        try:

            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""SELECT * FROM FRIENDSTABLE WHERE user_id=%s;""",(username,))
            friendTableConnection.commit()
            dbData = friendCursor.fetchall()
            if dbData != None:
                for friends in dbData:
                    if friendsname == friends[2]:
                        return 'alreadyExists'
            friendCursor.execute("""SELECT * FROM FRIENDSTABLE WHERE firends_id=%s;""",(username,))
            friendTableConnection.commit()
            dbData = friendCursor.fetchall()
            if dbData != None:
                for friends in dbData:
                    if friendsname == friends[1]:
                        return 'alreadyExists'
            friendCursor.close()
            friendTableConnection.close()
        except friendTableConnection.Error as Error:
            print(Error)
        return 'newRelation'

    def updateFriends(self,friendId,newStatus):
         try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""UPDATE FRIENDSTABLE SET status=%s WHERE friendRecordId=%s;""",(newStatus,friendId))
            friendTableConnection.commit()
         except friendTableConnection.Error as Error:
            print(Error)

         friendTableConnection.close()
    def blockFriend(self,friendId,username):
         try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""SELECT * FROM FRIENDSTABLE WHERE friendRecordId=%s;""",(friendId,))
            dbData = friendCursor.fetchone()
            if dbData[1] == username:
                friendCursor.execute("""UPDATE FRIENDSTABLE SET status=%s WHERE friendRecordId=%s;""",('blocked1',friendId))
            if dbData[2] == username:
                friendCursor.execute("""UPDATE FRIENDSTABLE SET status=%s WHERE friendRecordId=%s;""",('blocked2',friendId))
            friendTableConnection.commit()
         except friendTableConnection.Error as Error:
            print(Error)

         friendTableConnection.close()
    def deleteRelation(self, friendId ):
         try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""DELETE FROM FRIENDSTABLE WHERE friendRecordId=%s;""",(friendId,))
            friendTableConnection.commit()
            self.lastFriendId = 0
            self.myFriends = []
         except friendTableConnection.Error as Error:
            print(Error)

         friendTableConnection.close()