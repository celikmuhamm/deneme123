Teknik Kılavuz
===============

Veritabanı dizaynı
^^^^^^^^^^^^^^^^^^

Deep Map sitesinde , misafir ve kayıtlı kullanıcı olarak iki çeşit kullanıcı bulunmaktadır. Bu nedenle Kayıtlı kullanıcı ve ilişkili tablolar bir arada, ilişkili olmayan tablolar ayrı gösterilmiştir. 

Kulalnıcı tarafı için varlık ilişki diygramı:
----------------------------------------------
Kullanıcı için oluşturulan veritabanı dizaynı aşağıdaki görselde gösterilmiştir. Kullanıcıya ait lokasyon tablosu, arkadaş ilişkileri, arkadaşlık istekleri,  yorum, mesaj, bildirim gibi tablo bağıntıları ifade edilmiştir.

   .. figure:: ErDiagrams/erDiagram.png
      :scale: 50 %
      :alt: e/r diagram

      Kullanıcı tarafının varlık ilişki diyagramı

Event için varlık ilişki diyagramı:
------------------------------------
Bu kısımkullanıcıdan bağımsız oluşturulabilmektedir, bu nedenle kullanıcı tablosuna bağlanmamıştır. Event tablosu ve bu eventlara bağlı döküman ve görsel tabloları bulunmaktadır.

   .. figure:: ErDiagrams/erDiagram2.png
      :scale: 50 %
      :alt: e/r diagram

      Event için varlık ilişki diyagramı


Code
^^^^
Server.py dosyasında bulunun create_app fonksiyonu uygulamayı oluşturmaktadır. Uygulama ile ilgili ayrıntılar ileriki bölümlerde anlatılacaktır.

Uygulamayı başlatma
---------------------

 .. code-block:: python
      
      def create_app():
          app = Flask(__name__)
          app.user = User()
          app.userList = UserList()
          app.usermap = UserLocationStore()
          app.friendStore = FriendStore()
          app.messageStore = MessageStore()
          app.userlocation = UserLocation()
          app.register_blueprint(site)
          app.register_blueprint(myMap)
          app.register_blueprint(register)
          app.register_blueprint(adminTable)
          app.register_blueprint(add)
          app.register_blueprint(add_doc)
          app.register_blueprint(image)
          app.register_blueprint(event)
          app.register_blueprint(notifications)
          app.store = Store()
          app.commentStore = CommentStore()
          app.requestStore = RequestStore()
          app.store_images = Store_Image()
          app.store_documents = Store_Document()
          app.register_blueprint(friends)
          app.register_blueprint(messages)
          app.register_blueprint(new)
          app.time = Timesql()
          app.init_db = init_db()
          app.savelocation = SaveLocation()
          app.notificationStore = NotificationStore()
          return app

Veritabanını oluşturma
-----------------------

Initialize_database.py dosyasnda bulunan init_db fonksiyonu, database'in oluşmasını sağlayan fonksiyondur. İlgili tablolar eğer daha önce oluşturulmamışsa bu fonksiyon aracılığıyla oluşturulur.

 .. code-block:: python
 
      def init_db():
      dsn = get_connection_for_events()
      with dbapi2.connect(dsn) as connection:
      cursor = connection.cursor()
      
        try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS EVENTTABLE (title varchar(30), date varchar(10), place varchar(40), event_id serial primary key)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS IMAGETABLE (event_id int references eventtable ON DELETE CASCADE , image_id int not null, date varchar(10), content text, primary key (event_id,image_id))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS DOCUMENTTABLE (title varchar(30), date varchar(10), content text, event_id int references eventtable ON DELETE CASCADE, document_id int not null, primary key (event_id, document_id))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS TIMETABLE (map_id varchar(40) primary key references TIMEMAPTABLE(mapID) on delete cascade, decade int not null,year int not null,share_date date not null,content_type varchar(40),content_header  varchar(40))""")
         
        connection.commit()
        except connection.Error as error:
            print(error)

         connection.close()
         try:
         conn = getConnection()
         userCursor = conn.cursor()
         userCursor.execute("""CREATE TABLE IF NOT EXISTS USERTABLE (userId SERIAL PRIMARY KEY,username varchar(20) UNIQUE,password varchar(20), email varchar(40),name varchar(20),surname varchar(20))""")
         conn.commit()

    except conn.Error as userError:
        print(userError)

    conn.close()
 
    try:
         userMapConnection = getConnection()
         userMapCursor = userMapConnection.cursor()
         userMapCursor.execute("""CREATE TABLE IF NOT EXISTS USERMAPTABLE (userMap_id INT,user_id varchar(20),mapInformation varchar(250),locationLabel varchar(30),lat FLOAT(10) NOT NULL,lng FLOAT(10) NOT NULL)""")
         userMapConnection.commit()

    except userMapConnection.Error as userMapError:
        print(userMapError)

    userMapConnection.close()

    try:

         socialTableconn = getConnection()
         socialTablecursor = socialTableconn.cursor()
         socialTablecursor.execute("""CREATE TABLE IF NOT EXISTS FRIENDSTABLE (friendRecordId SERIAL PRIMARY KEY ,user_id varchar(20) references USERTABLE(username) on delete cascade,firends_id varchar(20) references USERTABLE(username) on delete cascade,status varchar(20))""")
         socialTableconn.commit()

    except socialTableconn.Error as socialError:
        print(socialError)

    socialTableconn.close()

    try:
        requestTableconn = getConnection()
        requestTableCursor = requestTableconn.cursor()
        requestTableCursor.execute("""CREATE TABLE IF NOT EXISTS REQUESTTABLE (requestId SERIAL PRIMARY KEY, requester varchar(20) references USERTABLE(username) on delete cascade, requested varchar(20) references USERTABLE(username) on delete cascade)""")
        requestTableconn.commit()
    except requestTableconn.Error as requestError:
        print(requestError)


    try:

         messageTableConn = getConnection()
         messageTableCursor = messageTableConn.cursor()
         messageTableCursor.execute("""CREATE TABLE IF NOT EXISTS MESSAGETABLE (messageId SERIAL PRIMARY KEY,user_id varchar(20) references USERTABLE(username) on delete cascade,firends_id varchar(20) references USERTABLE(username) on delete cascade,content varchar(300),status varchar(20))""")
         messageTableConn.commit()

    except messageTableConn.Error as messageError:
        print(messageError)

    messageTableConn.close()

    try:

         commentTableConn = getConnection()
         commentTableCursor = commentTableConn.cursor()
         commentTableCursor.execute("""CREATE TABLE IF NOT EXISTS COMMENTTABLE (commentId SERIAL PRIMARY KEY,userId INT references USERTABLE(userId) on delete cascade,user_name varchar(20) references USERTABLE(username) on delete cascade,friendUsername varchar(20) references USERTABLE(username) on delete cascade,content varchar(300))""")
         commentTableConn.commit()

    except commentTableConn.Error as messageError:
        print(messageError)

    commentTableConn.close()
    try:

         notificationTableConn = getConnection()
         notificationTableCursor = notificationTableConn.cursor()
         notificationTableCursor.execute("""CREATE TABLE IF NOT EXISTS NOTIFICATIONTABLE (notificationId SERIAL PRIMARY KEY,user_name varchar(20) references USERTABLE(username) on delete cascade,friendUsername varchar(20) references USERTABLE(username) on delete cascade,messageId INT references MESSAGETABLE(messageId),commentId INT references COMMENTTABLE(commentId))""")
         notificationTableConn.commit()

    except notificationTableConn.Error as messageError:
        print(messageError)

    notificationTableConn.close()
 
.. toctree::

   Muhammed Safa Celik
   Emine Oyku Bozkir
   cicekn_developer

