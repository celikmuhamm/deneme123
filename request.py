from sqlconnection import getConnection


class Request:
    def __init__(self,requestId=None, requester=None, requested=None):
        self.requester = requester
        self.requested = requested
        self.requestId = requestId

class RequestStore:
    def __init__(self):
        self.myRequests = []
        self.lastRequestId = 0
    def searchRequests(self,requester,requested):
        try:
            self.lastRequestId = 0
            self.myRequests = [];
            reqTableConn = getConnection();
            reqCursor = reqTableConn.cursor()
            reqCursor.execute("""SELECT * FROM REQUESTTABLE WHERE requested = %s;""",(requested,))
            reqTableConn.commit()
            dataFromDb = reqCursor.fetchall()
            if dataFromDb != None:
                for request in dataFromDb:
                    if request[1] == requester:
                        return 'alreadySent'
            reqCursor.execute("""SELECT * FROM REQUESTTABLE WHERE requester = %s;""",(requested,))
            reqTableConn.commit()
            dataFromDb2 = reqCursor.fetchall()
            if dataFromDb2 != None:
                for request in dataFromDb2:
                    if request[2] == requester:
                        return 'alreadyReceived'
            reqCursor.close()
            reqTableConn.close()
        except reqTableConn.Error as reqErr:
            print(reqErr)
        return 'available'
    def getRequest(self,requestID):
        reqTableConn = getConnection()
        reqCursor = reqTableConn.cursor();
        reqCursor.execute("""SELECT * FROM REQUESTTABLE WHERE requestId = %s;""",(requestID,))
        reqTableConn.commit()
        dataFromDb = reqCursor.fetchone()
        myReq = Request()
        myReq.requestId = dataFromDb[0]
        myReq.requester = dataFromDb[1]
        myReq.requested = dataFromDb[2]
        return myReq

    def addRequest(self, request):
        self.lastRequestId +=1
        self.myRequests.append(request)
        try:
            reqTableConn = getConnection()
            requestCursor = reqTableConn.cursor()
            requestCursor.execute("""INSERT INTO REQUESTTABLE(requester, requested) VALUES(%s,%s);""",(request.requester, request.requested))
            reqTableConn.commit()
            requestCursor.close()
            reqTableConn.close()
        except reqTableConn.Error as reqErr:
            print(reqErr)

    def getRequests(self,username):
        try:
            self.lastRequestId = 0
            self.myRequests = [];
            reqTableConn = getConnection();
            reqCursor = reqTableConn.cursor()
            reqCursor.execute("""SELECT * FROM REQUESTTABLE WHERE requested = %s;""",(username,))
            reqTableConn.commit()
            dataFromDb = reqCursor.fetchall()
            if dataFromDb != None:
                for request in dataFromDb:
                    myReq = Request()
                    myReq.requestId = request[0]
                    myReq.requester = request[1]
                    myReq.requested = request[2]
                    self.myRequests.append(myReq)
                    self.lastRequestId += 1
            reqCursor.close()
            reqTableConn.close()
        except reqTableConn.Error as reqErr:
            print(reqErr)
        return self


    def deleteRequest(self, requestId):
        try:
            reqTableConn = getConnection();
            reqCursor = reqTableConn.cursor()
            reqCursor.execute("""DELETE FROM REQUESTTABLE WHERE requestId=%s;""",(requestId,))
            reqTableConn.commit()
            self.lastRequestId = 0
            self.myRequests= []
            reqCursor.close()
            reqTableConn.close()

        except reqTableConn.Error as reqErr:
            print(reqErr)







