from sqlconnection import getConnection

class Comment:
    def __init__(self,userId = None, userName=None    , friendUsername=None,content=None):
        self.userId = userId
        self.userName = userName
        self.friendUsername = friendUsername
        self.content = content
        self.commentId = 0
class CommentStore:
    def __init__(self):
        self.comments = []
        self.lastCommentId = 0

    def addComment(self, Comment):
        self.lastCommentId+= 1
        self.comments.append(Comment)
        try:
            commentTableConn = getConnection();
            commentTableCursor = commentTableConn.cursor()
            commentTableCursor.execute("""INSERT INTO COMMENTTABLE (userId,user_name,friendUsername,content) VALUES(%s,%s,%s,%s);""", (Comment.userId,Comment.userName,Comment.friendUsername,Comment.content))
            commentTableConn.commit()
            commentTableCursor.close()
            commentTableConn.close()
        except commentTableConn.Error as Error:
            print(Error)


    def getComments(self,username):
        try:
            self.lastCommentId = 0
            self.comments = []
            commentTableConn = getConnection();
            commentTableCursor = commentTableConn.cursor()
            commentTableCursor.execute("""SELECT * FROM COMMENTTABLE WHERE friendUsername=%s;""",(username,))
            commentTableConn.commit()
            dbData = commentTableCursor.fetchall()
            if dbData != None:
                for comment in dbData:
                    myComment = Comment()
                    myComment.commentId = comment[0]
                    myComment.userId = comment[1]
                    myComment.userName = comment[2]
                    myComment.friendUsername = comment[3]
                    myComment.content = comment[4]
                    self.comments.append(myComment)
                    self.lastCommentId += 1
            commentTableCursor.close()
            commentTableConn.close()
        except commentTableConn.Error as Error:
            print(Error)
        return self

    def deleteComment(self, commentId ):
         try:
            commentTableConn = getConnection();
            commentTableCursor = commentTableConn.cursor()
            commentTableCursor.execute("""DELETE FROM COMMENTTABLE WHERE commentId=%s;""",(commentId,))
            commentTableConn.commit()
            self.lastFriendId = 0
            self.myFriends = []
         except commentTableConn.Error as Error:
            print(Error)

         commentTableConn.close()