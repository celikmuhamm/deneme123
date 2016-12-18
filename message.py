from sqlconnection import getConnection

class Message:
    def __init__(self, receiver=None , sender=None, content=None):
        self.receiver = receiver
        self.sender = sender
        self.content = content
        self.status = None
        self.messageId = 0
class Conversation:
    def __init__(self, sender=None):
        self.sender = sender
        self.lastMessageId = 0
        self.messages = []
    def addMessages(self, message):
         self.lastMessageId+= 1
         self.messages.append(message)
class MessageStore:
    def __init__(self):
        self.conversations = []
        self.lastConversationId = 0

    def sendMessage(self, message):
        newMessage = Message()
        newMessage.sender = message.sender
        newMessage.receiver = message.receiver
        newMessage.content = message.content
        newMessage.status = 'normal'
        try:
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""INSERT INTO MESSAGETABLE (user_id,firends_id,content,status) VALUES(%s,%s,%s,%s);""", (message.sender,message.receiver,message.content,message.status))
            messageTableConnection.commit()
            messageCursor.close()
            messageTableConnection.close()
        except messageTableConnection.Error as Error:
            print(Error)


    def getMessages(self,username):
        try:
            self.lastConversationId = 0
            self.conversations = []
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""SELECT * FROM MESSAGETABLE WHERE firends_id=%s OR user_id=%s;""",(username,username))
            messageTableConnection.commit()
            dbData = messageCursor.fetchall()
            if dbData != None:
                for messages in dbData:
                    myMessage = Message()
                    myMessage.messageId = messages[0]
                    myMessage.sender = messages[1]
                    myMessage.receiver = messages[2]
                    myMessage.content = messages[3]
                    myMessage.status = messages[4]
                    found = 'false'
                    if myMessage.status == 'deleted':
                        if username == myMessage.receiver:
                            continue
                    if self.conversations != None:
                        i = 0
                        while i < self.lastConversationId:
                            if self.conversations[i].sender == messages[1] or self.conversations[i].sender == messages[2]:
                                self.conversations[i].addMessages(myMessage)
                                found = 'true'
                                self.conversations[i].lastMessageId += 1
                            i += 1
                    if found == 'false':
                         newConversation = Conversation()
                         newConversation.addMessages(myMessage)
                         if myMessage.sender == username:
                            newConversation.sender =  myMessage.receiver
                         else:
                            newConversation.sender =  myMessage.sender
                         self.conversations.append(newConversation)
                         self.lastConversationId += 1


            messageCursor.close()

            messageTableConnection.close()
        except messageTableConnection.Error as Error:
            print(Error)
        return self

    def updateAndDeleteMessages(self,messageId,username):
         try:
            messageTableConnection = getConnection();
            messageCursor = messageTableConnection.cursor()
            messageCursor.execute("""SELECT * FROM MESSAGETABLE WHERE messageId=%s;""",(messageId,))
            dbData = messageCursor.fetchone()
            if dbData[1] == username:
                messageCursor.execute("""DELETE FROM MESSAGETABLE WHERE messageId=%s;""",(messageId,))
            else:
                newContent = 'deleted'
                messageCursor.execute("""UPDATE MESSAGETABLE SET status=%s WHERE messageId=%s;""",(newContent,messageId))

            messageTableConnection.commit()
         except messageTableConnection.Error as Error:
            print(Error)

         messageTableConnection.close()
