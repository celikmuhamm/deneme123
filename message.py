from sqlconnection import getConnection

class Message:
    def __init__(self, userName=None , friendUsername=None, content=None):
        self.userName = userName
        self.friendUsername = friendUsername
        self.content = content
        self.messageId = 0
class MessageStore:
    def __init__(self):
        self.myMessages = []
        self.lastMessageId = 0

    def addMessages(self, message):
        self.lastMessageId+= 1
        Message.messageId=self.lastMessageId
        newMessage = Message()
        newMessage.messageId=self.lastMessageId
        newMessage.userName = message.userName
        newMessage.friendUsername = message.friendUsername
        newMessage.content = message.content
        self.myMessages.append(newMessage)
        try:
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""INSERT INTO MESSAGETABLE (messageId,user_id,firends_id,content) VALUES(%s,%s,%s,%s);""", (message.messageId,message.userName,message.friendUsername,message.content))
            messageTableConnection.commit()
            messageCursor.close()
            messageTableConnection.close()
        except messageTableConnection.Error as Error:
            print(Error)


    def getMessages(self,username):
        try:
            self.lastMessageId = 0
            self.myMessages = []
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""SELECT * FROM MESSAGETABLE WHERE user_id=%s;""",(username,))
            messageTableConnection.commit()
            dbData = messageCursor.fetchall()
            if dbData != None:
                for messages in dbData:

                    myMessage = Message()
                    myMessage.userName = messages[1]
                    myMessage.friendUsername = messages[2]
                    myMessage.content = messages[3]
                    self.myMessages.append(myMessage)
                    self.lastMessageId += 1

            messageCursor.close()
           
            messageTableConnection.close()
        except messageTableConnection.Error as Error:
            print(Error)
        return self

    def updateMessages(self,messageId,newContent):
         try:
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""UPDATE MESSAGETABLE SET content=%s WHERE messageId=%d;""",(newContent,messageId))
            messageTableConnection.commit()
         except messageTableConnection.Error as Error:
            print(Error)

         messageTableConnection.close()

    def deleteMessage(self, messageId):
         try:
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""DELETE FROM MESSAGETABLE WHERE messageId=%d;""",(messageId,))
            messageTableConnection.commit()
         except messageTableConnection.Error as Error:
            print(Error)

         messageTableConnection.close()