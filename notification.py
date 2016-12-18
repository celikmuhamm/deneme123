from sqlconnection import getConnection


class Notification:
    def __init__(self, requester=None, requested=None):
        self.requester = requester
        self.requested = requested
        self.notificationId = None
        self.typeId = None
        self.type = None

class NotificationStore:
    def __init__(self):
        self.myNotifications = []
        self.lastNotificationId = 0

    def sendCommentNotification(self, notification):
        try:
            notificationTableConn = getConnection()
            notificationCursor = notificationTableConn.cursor()
            notificationCursor.execute("""INSERT INTO NOTIFICATIONTABLE(user_name, friendUsername,commentId) VALUES(%s,%s,%s);""",(notification.requester, notification.requested,notification.typeId))
            notificationTableConn.commit()
            notificationCursor.close()
            notificationTableConn.close()
        except notificationTableConn.Error as error:
            print(error)
    def sendMessageNotification(self, notification):
        try:
            notificationTableConn = getConnection()
            notificationCursor = notificationTableConn.cursor()
            notificationCursor.execute("""INSERT INTO NOTIFICATIONTABLE(user_name, friendUsername,messageId) VALUES(%s,%s,%s);""",(notification.requester, notification.requested,notification.typeId))
            notificationTableConn.commit()
            notificationCursor.close()
            notificationTableConn.close()
        except notificationTableConn.Error as error:
            print(error)
    def getNotifications(self,username):
        try:
            self.lastNotificationId = 0
            self.myNotifications = [];
            notificationTableConn = getConnection();
            notificationCursor = notificationTableConn.cursor()
            notificationCursor.execute("""SELECT * FROM NOTIFICATIONTABLE WHERE friendUsername = %s;""",(username,))
            notificationTableConn.commit()
            dataFromDb = notificationCursor.fetchall()
            if dataFromDb != None:
                for notifications in dataFromDb:
                    notification = Notification()
                    notification.notificationId = notifications[0]
                    notification.requester = notifications[1]
                    notification.requested = notifications[2]
                    messageId = notifications[3]
                    if messageId:
                        notification.type = 'message'
                        notification.typeId = messageId
                    commentId = notifications[4]
                    if commentId:
                        notification.type = 'comment'
                        notification.typeId = commentId
                    self.myNotifications.append(notification)
                    self.lastNotificationId += 1
            notificationCursor.close()
            notificationTableConn.close()
        except notificationTableConn.Error as error:
            print(error)
        return self


    def deleteNotification(self, notificationId):
        try:
            notificationTableConn = getConnection();
            notificationCursor = notificationTableConn.cursor()
            notificationCursor.execute("""DELETE FROM NOTIFICATIONTABLE WHERE notificationId =%s;""",(notificationId,))
            notificationTableConn.commit()
            notificationCursor.close()
            notificationTableConn.close()

        except notificationTableConn.Error as error:
            print(error)

