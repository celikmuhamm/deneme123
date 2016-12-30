Muhammed Safa Celik Tarafından Gerçeklenen Bölümler
==================================================
Database ve SQL connection Kurulumu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Bluemix'te elephantsql hizmeti alındı ve projeye eklendi. Manifest.yml dosyasına services ve elephantsql servisi eklendi.
database için localde ve server üzerinde gerekli olan bağlantı fonksiyonları olan get_sqldb_dsn fonksiyonu ve getConnection fonksiyonları oluşturuldu. get_sqldb_dsn fonksiyonu projenin bluemix üzerindeki çevre değişkenlerine erişip json formatındaki değişkenlerden **elephantsql** isimli çevre değişkenini parse ederek database bağlantısı için gerekli olan dsn'i döndürmektedir.

.. code-block:: python

    def get_sqldb_dsn(vcap_services):
        """Returns the data source name for IBM SQL DB."""
        parsed = json.loads(vcap_services)
        uri = parsed["elephantsql"][0]["credentials"]["uri"]
        match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)',uri)
        user,password,host, _,port,dbname = match.groups()
        dsn = """user='{}' password='{}' host='{}' port={} dbname='{}'""".format(user, password, host, port, dbname)
        return dsn
        
getConnection fonksiyonu ise serverda eğer vcap servisi varsa get_sqldb_dsn fonksiyonu üzerinden elephantsql'e, localde **vagrant** üzerinde 'itucsdb' veritabanına bağlanmayı sağlamaktadır.

.. code-block:: python

  def getConnection():
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        dsn = get_sqldb_dsn(VCAP_SERVICES)
    else:
       dsn = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    
    with dbapi2.connect(dsn) as connection:
        return connection;

User Tablosu ve İlgili İşlemler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

USERTABLE tablosu user_id,username,name,surname,e-mail ve password'den oluşan bir tablo olup kullanıcı bilgilerini barındırmakta ve kullanıcı tabanlı sistemimizin temel tablosu olmaktadır.Kayıt işlemi sırasında alınan veya database'den okunan bilgiler User modeline alınarak diğer işlemlerde kullanılır.

.. code-block:: python

      class User(UserMixin):
          def __init__(self, username=None,  password=None,email=None, name=None,surname=None):
              self.userId = None
              self.username = username
              self.email = email
              self.password = password
              self.name = name
              self.surname = surname

          def get_id(self):
              return self.username
     
Kayıt sayfasından alınan kullanıcı bilgileri veritabanına eklenmek üzere login.py'a oradan da user.py'a gelerek setUserToDb fonksiyonuyla USERTABLE tablosuna yazılırlar.

.. code-block:: python

       def setUserToDb(User):
            connection = getConnection()
            cursor = connection.cursor()
            username = User.username
            password = User.password
            email = User.email
            name = User.name
            surname =User.surname
            try:
                cursor.execute("""INSERT INTO USERTABLE (username, password, email, name, surname) VALUES(%s,%s,%s,%s,%s);""",(username,password,email,name,surname))
                connection.commit()
                connection.close()
            except connection.Error as error:
                    print(error)

        
        
Veritabanından kullanıcı bilgilerinin alınması da yine user.py'daki getUserFromDb ve search fonksiyonlarıyla sağlanır. getUserFromDb fonksiyonu bir kullanıcının tablodaki bütün bilgilerinin alınmasını sağlar

.. code-block:: python

      def getUserFromDb(username):
          conn = getConnection()
          cursor = conn.cursor()
          try:
                  cursor.execute(""" SELECT * FROM USERTABLE WHERE username= %s;""",
                              (username,)
                          )
                  conn.commit()
                  dbData = cursor.fetchone()
                  User.userId = dbData[0]
                  User.username = dbData[1]
                  User.password = dbData[2]
                  User.email= dbData[3]
                  User.name = dbData[4]
                  User.surname = dbData[5]
                  cursor.close()
                  conn.close()
                  return User
          except conn.Error as error:
                  print(error)
                  return 'Error'
                  
 
Search fonksiyonu ise kayıt işleminde, giriş işleminde, mesajlaşma ve arkadaş sayfalarında girilen kullanıcının kullanıcı tablosunda bulunup bulunmadığı, girilen parolanın yanlış olup olmadığı gibi durumlara göre farklı sonuçlar döndüren USERTABLE tablosundan sadece username ve password bilgilerini alan fonksiyondur.

.. code-block:: python

      def search(username,password):
        conn = getConnection()
        cursor = conn.cursor()

        try:
            cursor.execute(""" SELECT * FROM USERTABLE WHERE username= %s;""",
                        (username,)
                    )
            conn.commit()
            dbData = cursor.fetchone()

            if dbData is None:
                status = 'There is no user with this username '
            else:
                if password == dbData[2]:
                    status = 'Success'
                else:
                    status = 'Password is invalid'

        except conn.Error as error:
            print(error)
            status = 'Password or Username is invalid'

        cursor.close()
        conn.close()
        return status

Status değişkeni **'There is no user with this username '** , **'Password is invalid'** ve **'Success'** sonuçlarıyla fonksiyonun çağırıldığı yere dönerek aldığı değere göre program işleyişinde önemli rol oynar. 

USERTABLE tablosunda silme ve güncelleme işlemleri ise admin girişi gerektirmektedir. Bu giriş login.py'da basit bir biçimde oturumdaki kullanıcının kullanıcı isminin kodda belirtilen isimle eşleşmesine bakar ve eğer eşleşme varsa adminPage sayfasına girmesine müsade eder eğer sayfaya ulaşmaya çalışan kullanıcı admin değilse anasayfaya yönlendirilir.

.. code-block:: python
  @register.route('/adminPage')
  
        def adminPage():
                  if current_app.user.username == 'deepMapAdmin':
                      current_app.userList.getUsers()
                      return render_template('adminPage.html',user_name = current_app.user.username,userTable = current_app.userList.userTable)
                  else:
                      return render_template('home.html')


Admin sayfasına gönderilen **UserTable** içeriği user.py'da Userlist class'ında getUsers metoduyla ve classın User yapısındaki elemanlardan oluşan array'iyle bütün kullanıcılar USERTABLE tablosundan okunarak sağlanır.

.. code-block:: python

    class UserList:
    def __init__(self):
        self.userTable = []
        self.lastUserCounter = 0

    def getUsers(self):
            conn = getConnection()
            cursor = conn.cursor()
            self.userTable = []
            self.lastUserCounter = 0
            try:
                    cursor.execute(""" SELECT * FROM USERTABLE;""")

                    conn.commit()
                    dbData = cursor.fetchall()
                    if dbData != None:
                        for users in dbData:

                            user = User()
                            user.userId = users[0]
                            user.username = users[1]
                            user.password = users[2]
                            user.email = users[3]
                            user.name = users[4]
                            user.surname = users[5]
                            self.userTable.append(user)
                            self.lastUserCounter += 1

                    cursor.close()
                    conn.close()
                    return User
            except conn.Error as error:
                    print(error)
                    return 'Error'
            return self
Admin sayfasından gelen silme isteği user.py'da deleteUser fonksiyonuyla USERTABLE tablosuna bir **DELETE** query'si gönderilerek, güncelleme isteği ise updateUser fonksiyonuyla bir **UPDATE** query'si gönderilerek sağlanır.

.. code-block:: python

        def updateUser(User):
            connection = getConnection()
            cursor = connection.cursor()
            username = User.username
            password = User.password
            email = User.email
            name = User.name
            surname =User.surname
            try:
                cursor.execute("""UPDATE USERTABLE SET username=%s, password=%s,email=%s, name=%s, surname=%s WHERE username=%s;""",(username,password,email,name,surname,username))
                connection.commit()
                connection.close()
            except connection.Error as error:
                    print(error)

        def deleteUser(username):
            connection = getConnection()
            cursor = connection.cursor()

            try:
                cursor.execute("""DELETE FROM USERTABLE WHERE username=%s;""",(username,))
                connection.commit()
                connection.close()
            except connection.Error as error:
                    print(error)
                    
                    

USERTABLE tablosunun temel işlemlerini gören fonksiyonlarının üzerinde login.py içerisinde yeralan kayıt ve giriş işlemlerini gerçekleştiren fonksiyonlar olan **login_page** ve **register_page** fonksiyonları bulunmaktadır. register_page fonksiyonu html dosyasından 'POST' metoduyla aldığı bilgileri önce daha önce bahsedilen user.py'a ait search fonksiyonunu çağırarak dönen sonuca göre işlemlere devam eder. Eğer çıkan sonuç **'There is no user with this username '** ise kullanıcı veritabanına eklenmek üzere setUserToDb fonksiyonuna verilir ve kullanıcı user_page sayfasına yönlendirilerek seansa ismi konularak giriş yapması sağlanır. Eğer zaten bu kullanıcı adını kullanan bir kullanıcı varsa ilgili hata mesajıyla kullanıcı anasayfaya yönlendirilir.

.. code-block:: python
    
    @register.route('/register',methods=['GET', 'POST'])
        def register_page():
             if request.method == 'POST':
                 username = request.form['user_name']
                 password = request.form['password']
                 firstname = request.form['first_name']
                 lastname = request.form['last_name']
                 email = request.form['email']
                 status = search(username,password)
                 if status == 'There is no user with this username ':
                     current_app.user.username = username
                     current_app.user.password = password
                     current_app.user.name = firstname
                     current_app.user.surname = lastname
                     current_app.user.email = email
                     session['user'] = username
                     setUserToDb( current_app.user)
                     markerLocations = []
                     return render_template('user_page.html',markerLocations = markerLocations,user_name = username,first_name = firstname,last_name = lastname,e_mail = email)
                 else:
                     flash('The username: '+username +' already using by another user' )
                     return render_template('home.html')

             else:

                 return render_template('home.html')
                 
                 
login_page fonksiyonu ise hmtl dosyasından aldığı kullanıcı adı ve parolayı search fonksiyonuna vererek çıkan sonuca göre kullanıcının giriş yapmasını sağlar veya anasayfaya yönlendirerek iligli hata mesajını verir. Daha önce search fonksiyonu altında bahsedilen status değişkeni ile döndürülen sonuçlar aslında login_page fonksiyonu için yapılmıştır.

.. code-block:: python

    @register.route('/userPage',methods=['POST','GET'])
      def login_page():

           if request.method == 'POST':
              username = request.form['username1']
              password = request.form.get('password1',None)
              status = search(username,password)
              if status == 'Success':
                  current_app.user= getUserFromDb(username)
                  session['user'] = username
                  current_app.usermap.getLocations(username)
                  markerLocations = []
                  for locations in current_app.usermap.myLocations:
                     newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
                     markerLocations.append(newLocation)

                  current_app.commentStore.getComments(username)
                  return render_template('user_page.html',comments = current_app.commentStore.comments,markerLocations = markerLocations, userMap = current_app.usermap.myLocations, user_name = username)
              else:
                  flash(status)
                  return render_template('home.html')

           if session.get('user')!=None:
              markerLocations = []
              for locations in current_app.usermap.myLocations:
                     newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
                     markerLocations.append(newLocation)
              current_app.commentStore.getComments(username)
              return render_template('user_page.html',comments = current_app.commentStore.comments,markerLocations = markerLocations, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)

           else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')
              
Kullanıcı sayfası ve bununla ilgili içerikle sadece kayıtlı kullanıcılara açık olduğundan yetki verilmeden erişilmeye çalışıldığında ilgili hata ile anasayfaya yönlendirme gerçekleştirilir. Giriş yapıldıktan sonra kullanıcı profiline gitmek istediğinde profile fonksiyonu çağırılır ve getUserFromDb fonksiyonu çağırılarak kullanıcının bütün bilgileri veritabanından alınır ve şifresi hariç profil sayfasında gösterilir.

.. code-block:: python


        @register.route('/profilePage')
        def profile():
                  if session.get('user')!=None:
                      return render_template('profile.html',user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
                  else:
                      return render_template('home.html')
                      
USERTABLE ve kullanıcı işlemleri mesaj,arkadaş,bildirim,talep,yorum ve harita nesnelerinin hepsinin temelinde bulunduğu için bütün fonksiyonları bunlarla içiçe geçmiştir.

Message Tablosu ve İlgili İşlemler
--------------------------

MESSAGETABLE tablosu birincil anahtar olarak message_id , yabancı anahtar olarak user_id ve friend_id kolonlarını barındırmakta ayrıca content ve status olmak üzere 2 kolon daha barındarmaktadır. user_id ve friend_id USERTABLE tablosundan username kolonuna silme kaskadıyla bağlı yabancı anahtarlardır ve user_id mesajı atan tarafı friend_id mesajı alan tarafı temsil eder. Message nesnesi htmlden gelen veya veritabanından gelen bir mesajın bilgilerini tutar.

.. code-block:: python

      class Message:
    def __init__(self, receiver=None , sender=None, content=None):
        self.receiver = receiver
        self.sender = sender
        self.content = content
        self.status = None
        self.messageId = 0
        
Conversation nesnesi ise mesaj sayfasındaki conversation kutuları için oluşturulmuştur. Her bir converstaion veritabanından okunan veya html dosyasından gelen karşılıklı mesajlar esas alınarak oluşturulur.

.. code-block:: python

     class Conversation:
    def __init__(self, sender=None):
        self.sender = sender
        self.lastMessageId = 0
        self.messages = []
    def addMessages(self, message):
         self.lastMessageId+= 1
         self.messages.append(message)
         
sender değişkeni conversation kutusu mesajlar sayfasında görüldüğünde konuşulmakta olan kullanıcının isminin kutunun üstünde görünmesi için tutulmaktadır. Bir kullanıcı yüzlerce kullanıcı ile konuşabileceğinden Conversation'ları tutan bir MessageStore nesnesi oluşturulmuştur. bu nesne bir kullanıcıya ait bütün Conversation'ları tutar ve bütün datanın aktarımını kolaylaştırır. Ayrıca mesajlarla ilgili bütün temel işlemler bu class'ın içinde yapılmaktadır.

.. code-block:: python

    class MessageStore:
    def __init__(self):
        self.conversations = []
        self.lastConversationId = 0

Mesaj sayfasından mesaj gönderildiğinde bu mesaj veritabanına sendMessage fonksiyonuyla yazılır. Bu fonksiyon bir message nesnesi alır ve bu nesnenin içindeki verileri veritabanına yazar.

.. code-block:: python

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
            
Gönderilen bir mesaj gittiği kullanıcının mesaj sayfasına gelirken aldığı ilk yolu getMessages fonksiyonuyla alır. Bu fonksiyon select query ile mesajları aranan kullanıcının hem attığı hem de aldığı mesajları toplar.Bunu yaparken hem user_id hem de friend_id kolonlarındaki isimleri karşılaştırır ve ikili konuşmaları tespit ederek conversation'ları oluşturur. Eğer mesaj karşıdan geliyorsa ve statüsü **deleted** ise bu mesaj messageStore'a konmayarak kullanıcıya gizlenir. Mesajlar veritabanından okundukça ilgili conversation'a eklenirler eğer sender veya receiver değişkenlerinden biri daha önce messageStore'a eklenen conversation'larda yoksa yeni conversation oluşturulur ve  diğer kullanıcının ismi conversation içindeki sender değişkenine atanır.Mesajlar conversation'ların içindeki arraylara conversation'lar da messageStore'daki conversation arrayine alınıp süreç tamamlanarak messageStore döndürülür.

.. code-block:: python

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
        
Güncelleme ve silme işlemleri mesaj sistemi için aslında oldukça yakın hale geldiler. Bir mesajı sadece o mesajı atan kişi silebilmektedir. Eğer mesajı gören kişi onu siliyorsa statü'sü güncellenerek deleted yapılır ve artık ona gösterilmez. silme ve güncelleme query'lerini aynı fonksiyon barındarmaktadır. Önce bir select komutu yollayarak silme işlemi yapmak isteyen kişinin gönderen mi alıcı mı olduğunu belirer ve eğer alıcıysa güncelleme yaparak mesajın statü'sünü deleted olarak günceller eğer işlemi yapan kullanıcı gönderen ise mesajı MESSAGETABLE tablosundan siler.


.. code-block:: python

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
         
Mesaj gönderme ve alma kısmında daha yukarı seviyedeki fonksiyonlara geçmeden önce html bölümünün çalışma sisteminden bahsedilecektir. Mesajlaşma gibi veya daha karmaşık reply yapılabilen html birleşenlerinde sayfanın ön işlemleri ile arka işlemleri daha çok iç içe geçmekte ve yapılar birbirlerini daha çok etkilemekteler. Örneğin bu projede her bir konuşmanın htmlde ayrı birer conversation olarak tutulması, python'da böyle bir ihtiyacı doğurmuş ve  conversation nesnesi oluşmuştur. MessageOperations.py'daki getMessages fonksiyonu önceden bahsedilen ve message.py'da yeralan getMessages metodunu çağırarak messageStorun conversations isimli conversation nesnelerini tutan arrayini messages.html sayfasına **messages** ismiyle gönderir. Html sayfasına gelen array, içindeki conversationlar için bir for döngüsüne girer. Her bir conversation için collapse containerlar oluşturulur ve isimleri **'chat with conversation.sender'** olacak şekilde ayarlanır. Her bir container'ın bağımsız bir biçimde açılması için container_id'ler tekil olmak zorunda olduğundan onlar da **conversation.sender** değişkeniyle atanır. bu sayede her container bağımsız şekilde açılıp kapanabilir. Yine her container içinde bir send input bölgesi barındırmaktadır. Buraya mesaj yazılıp send butonuna basıldığında container'in içinde gizli input olarak da bulunan sender bilgisiyle mesaj içeriği daha sonra anlatılacak olan sendMessage fonksiyonuna verilir. Container'ın ilk for'unun conversation'lar olduğu belirtilmişti sırada ise  eğer varsa önce gönderenden başlamak üzere sırayla conversation'ın bütün mesajları yazdırılır.


.. code-block:: python

         {% if messages %}
        {%for conversation in messages%}
        <div class="container">
            <div class="row">
                <div class="col-md-5">
                    <div class="panel panel-primary">
                        <div class="panel-heading" id="accordion">
                            <div class="btn-group ">
                                <a type="button" class="btn btn-primary btn-block btn-lg" data-toggle="collapse" data-parent="#accordion" href='#{{conversation.sender}}'>
                                    <span class="glyphicon glyphicon-comment"> Chat with {{conversation.sender}}</span>
                                </a>
                            </div>
                        </div>
                        <div class="panel-collapse collapse" id='{{conversation.sender}}'>
                        <div class="panel-body">
                            <ul class="chat">
                   {%for message in conversation.messages%}

                              {%if user_name == message.receiver %}
                                <li class="left clearfix"><span class="chat-img pull-left">
                                    <img src="http://placehold.it/50/55C1E7/fff&text=U" alt="User Avatar" class="img-circle" />
                                </span>
                                    <div class="chat-body clearfix">
                                        <div class="header">
                                            <strong class="primary-font">{{message.sender}}</strong> <small class="pull-right text-muted">
                                                <span class="glyphicon glyphicon-time"></span></small>
                                        </div>
                                         <form method="post" action = '/deleteMessage'>
                                <input type=hidden value="{{message.messageId}}"name="message_to_delete"></input>
                                <button type= "submit"class="btn btn-danger  btn-xs glyphicon glyphicon-trash"  title="Delete"></button>
                               </form>
                                        <p>
                                            {{message.content}}
                                        </p>
                                    </div>
                                </li>
                                {%endif%}
                                {%if message.sender == user_name %}
                                <li class="right clearfix"><span class="chat-img pull-right">
                                    <img src="http://placehold.it/50/FA6F57/fff&text=ME" alt="User Avatar" class="img-circle" />
                                </span>
                                    <div class="chat-body clearfix">
                                        <div class="header">
                                            <small class=" text-muted"><span class="glyphicon glyphicon-time"></span></small>
                                            <strong class="pull-right primary-font">{{message.sender}}</strong>
                                        </div>
                                        <form method="post" action = '/deleteMessage'>
                                <input type=hidden value="{{message.messageId}}"name="message_to_delete"></input>
                                <button type= "submit"class="btn btn-danger  btn-xs glyphicon glyphicon-trash"  title="Delete"></button>
                               </form>
                                        <p>
                                           {{message.content}}
                                        </p>

                                    </div>
                                </li>
                                 {% endif %}


                   {%endfor%}
                        </ul>
                        </div>
                        <div class="panel-footer">
                            <div class="input-group">
                            <form method = "post" action = '/sendMessage'>
                                <input id="btn-input" name="content" type="text" class="form-control input-sm" placeholder="Type your message here..." />
                                <input type=hidden value="{{ conversation.sender}}"name="user_name"></input>
                                <span class="input-group-btn">
                                    <button class="btn btn-warning btn-sm" id="btn-chat">
                                        Send</button>
                                </span>
                             </form>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
        {% endif %}
        
Mesajlar gösterildikten sonra **'Start New Conversation'** etiketli container görünür ve bu containerdan girilen kullanıcı adı sendMessages fonksiyonuna verilir. Bu fonksiyon gerek onversation'ların içindeki gizli inputlardan gerek yeni konuşma oluşturulurken girilen kullanıcı ismini alır. Search fonksiyonuyla böyle bir kullanıcının olup olmadığına baktıktan sonra mesajın gönderici kısmına oturumda olan kullanıcıyı, alıcı kısmına fonksiyona html'den verilen kullanıcıyı content'e html'den alınan içeriği status'ü ise boş bırakarak message.py'daki sendMessage fonksiyonunu çağırarak database'e mesajı ekler. ardından ilgili notifikasyonu gönderir ve mesajların yeniden sınflandırılması için database'den tekrar okuyarak sayfayı yeniler. Arkadaş olunmadan mesajlaşma gerçekleşmesine izin verilmediği için fonksiyon arkadaşlık durumunu da sorgulamaktadır.

.. code-block:: python

     @messages.route('/sendMessage',methods=['POST','GET'])
      def sendMessages():
          if session.get('user')!=None:
              if request.method == 'POST':
                  userName = request.form['user_name']
                  content = request.form['content']
                  message = Message()
                  message.sender = current_app.user.username
                  message.receiver = userName
                  message.content = content;
                  status = search(userName,'someqw19012341')
                  if userName != current_app.user.username:

                      if status == 'Password is invalid':
                          currentName = current_app.user.username
                          relationStatus = current_app.friendStore.searchFriends(currentName,userName)
                          if relationStatus == 'alreadyExists':
                              current_app.messageStore.sendMessage(message)
                              current_app.messageStore.getMessages(current_app.user.username)
                              notification = Notification()
                              for conversation in current_app.messageStore.conversations:
                                  if conversation.sender == userName:
                                      for messages in conversation.messages:
                                          if  message.sender == currentName and  message.receiver == userName:
                                              notification.requester = currentName
                                              notification.requested = userName
                                              notification.typeId = messages.messageId
                              current_app.notificationStore.sendMessageNotification(notification)
                          else:
                              flash('you are not friends with '+userName)
                      else:
                          flash('There is no user with this username: '+userName)
                  else:
                      flash('very funny -_-')
              return render_template('messages.html',messages = current_app.messageStore.conversations,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
          else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')
              
Mesajların silinmesi ve güncellenmesi işlemlerinin temelde nasıl yapıldığından daha önce bahsedilmişti. Bu işlem için daha yukarıda conversation'lar ve collapse container'ların açıklanmasında kullanılan html kodunda her bir mesajın yanında bir silme ikonu ve bu ikona bağlı 'POST' metodu ile gizli inputla deleteMessage fonksiyonunu çağıran form'lar görülmektedir. Bu sayede deleteMEssages fonksiyonu silinmek istenen mesajın yine conversation.sender değişkeniyle çağırılır ve daha önce bahsedilen hem güncelleme hem silme yönünde çalışan message.py fonksiyonuna yollanır. bu fonksiyon bahsedildiği üzere bu mesajın silineceğine mi yoksa deleted olarak işaretlenip sadece gönderene mi gösterileceğine karar verir.

.. code-block:: python

    @messages.route('/deleteMessage',methods=['POST','GET'])
    def deleteMessages():
        if session.get('user')!=None:
            if request.method == 'POST':
                messageId = request.form['message_to_delete']
                current_app.messageStore.updateAndDeleteMessages(messageId,current_app.user.username)
                current_app.messageStore.getMessages(current_app.user.username)
            return render_template('messages.html',messages = current_app.messageStore.conversations,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
        else:
            flash('Please sign in or register for DeepMap')
            return render_template('home.html')
            


Comment Tablosu ve İlgili İşlemler
--------------------------

COMMENTTABLE birincil anahtar commentId ,dış anahtarlar user_name ve friendUsername ayrıca content olmak üzere dört kolondan oluşmaktadır. Bir kullanıcı kendi haritasına yorum yapabileceği gibi arkadaş sayfasından arkadaşlarının kullanıcı adlarına tıklayarak gittiği arkadaşlarının haritalarına da yorum yapabilir. Html sayfasından veya veritabanından gelen yorum bilgileri Comment nesnesi kullanılarak tutulur. 

.. code-block:: python

    class Comment:
      def __init__(self,userId = None, userName=None    , friendUsername=None,content=None):
          self.userId = userId
          self.userName = userName
          self.friendUsername = friendUsername
          self.content = content
          self.commentId = 0
        
        
Her bir kullanıcının haritasına kendi veya arkadaşları tarafından yapılmış yorumları getirmek için bir commentStore nesnesi kullanılır ve yorumlarla ilgili bütün işlemler bu nesne altında toplanır. 
  
.. code-block:: python

      class CommentStore:
         def __init__(self):
            self.comments = []
            self.lastCommentId = 0

Yeni yorum eklenirken user_page'den login.py'a gelen yorum bilgisi comment.py'a gelerek addComment metoduyla veritabanına eklenir. Yorum yapan kişi username bölümüne yorum yapılan kullanıcı friendsUsername bölümüne kaydedilir. addComment metodu bunu sağlar.
  
.. code-block:: python

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
            
Veritabanına eklenmiş olan yorumlar her user_page sayfası yüklenirken COMMENTTABLE tablosunun friendsUSername kolonunda sayfası yüklenen kullanıcının ismi select komutuyla aratılarak alınır. getComments metoduyla veritabanından alınan yorumlar login.py'a verilir.
  
.. code-block:: python

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

Yorumların silme işlemi de comment.py'da deleteComment metoduyla sağlanır.
  
.. code-block:: python

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

Bir kullanıcı başka bir kullanıcının haritasını görmek üzere onun sayfasına giderken kullanıcı adı haritasına gidilen kullanıcının adıyla gelir ve yorumlarda gizli input olarak tutulur. bir kullanıcı yorum yapmak istediğinde bu sayede gönderilen form hedef kullanıcının da adını içermiş olur. makeComment fonksiyonuyla işlemler gerçekleştirilir.

  
.. code-block:: python

      @register.route('/makeComment',methods=['POST','GET'])
      def makeComment():
           if request.method == 'POST':
              friendsUsername = request.form['friendsName']
              content = request.form['content']
              username = current_app.user.username
              userId = current_app.user.userId
              comment = Comment()
              comment.userName = username
              comment.userId = userId
              comment.friendUsername = friendsUsername
              comment.content = content
              current_app.commentStore.addComment(comment)
              friendsMap = UserLocationStore()
              friendsMap.getLocations(friendsUsername)
              markerLocations = []
              for locations in friendsMap.myLocations:
                     newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
                     markerLocations.append(newLocation)
              current_app.commentStore.getComments(friendsUsername)
              notification = Notification()
              for comment in current_app.commentStore.comments:
                  if  comment.userName == username and  comment.friendUsername == friendsUsername:
                      notification.requester = username
                      notification.requested = friendsUsername
                      notification.typeId = comment.commentId
              current_app.notificationStore.sendCommentNotification(notification)
              return render_template('user_page.html',comments = current_app.commentStore.comments,markerLocations = markerLocations, userMap = friendsMap.myLocations, user_name = friendsUsername)
           else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')

Yorumlar üzerindeki silme ikonlarına basıldığında da bu ikonların hedef aldığı formlarda bulunan gizli inputlar o yorumun kimliğini deleteComment fonksiyonuna verir ve yorumun silinmesini sağlar.

  
.. code-block:: python

  @register.route('/deleteComment',methods=['POST','GET'])
      def deleteComment():

           if request.method == 'POST':
              commentId = request.form['comment_to_delete']
              current_app.commentStore.deleteComment(commentId)
              username=current_app.user.username
              friendsMap = UserLocationStore()
              friendsMap.getLocations(username)
              markerLocations = []
              for locations in friendsMap.myLocations:
                     newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
                     markerLocations.append(newLocation)
              current_app.commentStore.getComments(username)
              return render_template('user_page.html',comments = current_app.commentStore.comments,markerLocations = markerLocations, userMap = friendsMap.myLocations, user_name = current_app.user.username)

           else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')

Ekstralar
--------------------------

Google apisi ile kullanıcı haritasında cluster servisi çağırıldı servis hem clickListener'da her yeni lokasyon eklendiğinde anlık olarak hem de lokasyonlar veritabanından getirilirken scriptin başında çağırıldı. Bu sayede harita düzenli bir hal almış oldu.


  
.. code-block:: python

        var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
           google.maps.event.addListener(map, 'dblclick', function(event) {
          locations.push({lat: event.latLng.lat(),lng: event.latLng.lng()});
          addMarker(event.latLng, map);
             function addMarker(location, map) {
        markers = locations.map(function(location, i) {
          return new google.maps.Marker({
            position: location
          });
        });
        markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
        $('#squareSigninModal').modal('show');
