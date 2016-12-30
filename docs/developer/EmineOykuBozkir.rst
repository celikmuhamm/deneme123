Emine Öykü Bozkır Tarafından Gerçeklenen Bölümler
=====================================

User Map Tablosu ve Operasyonları
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

USERMAPTABLE tablosu; userMapid, user_id, mapInformation, loacationLabel, lat ve lng niteliklerinden oluşan ve kullanıcıların kendine ait lokasyonların tutulduğu tablodur. lat ve lng nitelikleri enlem ve boylam değerlerini göstermektedir. User_id, lokasyonun hangi kullanıcıya ait olduğunu tutan bir dış anahtar niteliğidir, USERTABLE tablosundan username niteliğine bağlıdır. Bu tablonun niteliklerini tutmak için UserLocation nesnesi kullanılmaktadır. UserLocation nesnesi tabloda bulunann bütün niteliklere kendi içinde sahiptir.

.. code-block:: python

   class UserLocation:
     def __init__(self, userName=None    , mapInfo=None, locationLabel=None,lat=None, lng=None):
         self.userName = userName
         self.mapInfo = mapInfo
         self.lat = lat
         self.locationLabel = locationLabel
         self.lng = lng
         self.locationId=0

Bir kullanıcıya ait birden fazla lokasyon olduğu için userLocation nesneleri UserLocationStore nesnesinin içinde dizi halinde tutulmaktadır. UserLocationStore nesnesi aynı zamanda veritabanına ekleme, silme, güncelleme gibi fonksiyonları barındırmaktadır. 

Yeni Lokasyon Ekleme

Aşağıdaki addLocation fonksiyonu, userLocation nesnesi türünde bir parametre alarak bu lokasyonu ve bütün bilgilerini veri tabanına yazar. 

.. code-block:: python

     def addLocation(self, userLocation):
        newUserLocation = UserLocation()
        self.lastLocationId+= 1
        newUserLocation.locationId = self.lastLocationId
        userLocation.locationId=self.lastLocationId
        newUserLocation.userName = userLocation.userName
        newUserLocation.mapInfo = userLocation.mapInfo
        newUserLocation.locationLabel =  userLocation.locationLabel
        newUserLocation.lat =  userLocation.lat
        newUserLocation.lng =  userLocation.lng
        self.myLocations.append(newUserLocation)
        try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapCursor.execute("""INSERT INTO USERMAPTABLE (userMap_id,user_id,mapInformation,locationLabel,lat,lng)               VALUES(%s,%s,%s,%s,%s,%s);""", (userLocation.locationId, userLocation.userName,                                           userLocation.mapInfo,userLocation.locationLabel,userLocation.lat, userLocation.lng ))
            userMapConnection.commit()
            userMapCursor.close()
            userMapConnection.close()
        except userMapConnection.Error as userMapError:
            print(userMapError)

Lokasyonu Veritabanından Okuma
---------------------------------
GetLocation fonksiyonu çağırıldığında, oturumda olan kullanıcının kullanıcı adını alarak veri tabanından lokasyonlarını getirir. Ayrıca, arkadaş haritasından, arkadaşın kullanıcı adını alarak onun lokasyonlarını getirir.

.. code-block:: python

      def getLocations(self,username):
        try:
            self.lastLocationId = 0
            self.myLocations = []
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapCursor.execute("""SELECT * FROM USERMAPTABLE WHERE user_id=%s;""",(username,))
            userMapConnection.commit()
            dbData = userMapCursor.fetchall()
            if dbData != None:
                for locations in dbData:

                    userLocations = UserLocation()
                    userLocations.userName = locations[1]
                    userLocations.mapInfo = locations[2]
                    userLocations.locationLabel = locations[3]
                    userLocations.lat = locations[4]
                    userLocations.lng = locations[5]
                    userLocations.locationId=locations[0]

                    self.myLocations.append(userLocations)
                    location = self.myLocations[0]
                    self.lastLocationId += 1

            userMapCursor.close()

            userMapConnection.close()
            except userMapConnection.Error as userMapError:
               print(userMapError)
            return self
            
UserMApOperations.py dosaysının içindeki getLocations fonksiyonu, lokasyonların html'den alınarak veritabanına yazılmasını sağlar. Haritaya çift tıklanarak yeni bir lokasyon eklemek için bir form açılır. Bu formdan yeni bir lokasyon eklendiğinde bu fonksiyon "POST" metodu ile çağırılır haritadan gelen lokasyon bilgileri ve formdan gelen lokasyona ait etiket açıklama gibi bilgiler veritabanına eklenmek üzere userMap.py dosaysındaki addLocation fonksiyonuna gönderilir. Eğer, fonksiyon "GET" metodu ile çağırılırsa, userMap.py dosyasındaki getLocation fonksiyonu çağırılarak veritabanındani ilgili kullanıcıya ait lokasyonlar alınır.            

.. code-block:: python

          @myMap.route('/userPage/getLocations',methods=['POST','GET'])
          def getLocations():
                if request.method == 'POST':
                    data = request.get_json()
                    for location in data:
                        lat = location['lat']
                        lng = location['lng']
                        info = location['info']
                        label = location['label']
                        current_app.userlocation.userName = current_app.user.username
                        current_app.userlocation.lat = lat
                        current_app.userlocation.lng = lng
                        current_app.userlocation.mapInfo = info
                        current_app.userlocation.locationLabel = label
                        current_app.usermap.addLocation(current_app.userlocation)

                    markerLocations = []
                    for locations in current_app.usermap.myLocations:
                        newLocation =            {'lat':locations.lat,
                        'lng':locations.lng,'info':locations.mapInfo,'label':locations.locationLabel}
                        markerLocations.append(newLocation)

                    current_app.commentStore.getComments(current_app.user.username)
                    return render_template('user_page.html',comments = current_app.commentStore.comments,markerLocations =                     markerLocations, userMap = current_app.usermap.myLocations,
                    user_name = current_app.user.username,first_name=current_app.user.name,last_name =                                         current_app.user.surname,e_mail=current_app.user.email)
                else:
                    if session.get('user')!=None:
                        markerLocations = []
                        for locations in current_app.usermap.myLocations:
                            newLocation = {'lat':locations.lat,'lng':locations.lng,'info':locations.mapInfo,
                            'label':locations.locationLabel}
                            markerLocations.append(newLocation)

                        current_app.commentStore.getComments(current_app.user.username)
                        return render_template('user_page.html',comments = current_app.commentStore.comments,
                        markerLocations = markerLocations, userMap = current_app.usermap.myLocations, 
                        user_name = current_app.user.username,
                        first_name=current_app.user.name,
                        last_name = current_app.user.surname,e_mail=current_app.user.email)
                    else:
                        flash('Please sign in or register for DeepMap')
                        return render_template('home.html')



Lokasyonu Veritabanından Silme
------------------------------

"UserMap.py" dosyasında bulunan deleteLocation fonksiyonu, location_id alarak, veritabanından ilgili lokasyonu siler.

.. code-block:: python
    
    def deleteLocation(self, locationId):
         try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapcursor.execute("""DELETE FROM USERMAPTABLE WHERE userMap_id=%d;""",(locationId,))
            userMapConnection.commit()
         except userMapConnection.Error as userMapError:
            print(userMapError)

         userMapConnection.close()



Lokasyon Güncelleme
---------------------

"UserMap.py" dosyasında bulunan updateLocationInformation fonksiyonu, haritaki lokasyon açıklamasının güncellenmesini sağlayan fonksiyondur.

.. code-block:: python

        def updateLocationInformation(self, locationId, newInfo):
         try:
            userMapConnection = getConnection();
            userMapCursor = userMapConnection.cursor()
            userMapcursor.execute("""UPDATE USERMAPTABLE SET mapInformation=%s WHERE userMap_id=%d;""",(newInfo,locationId))
            userMapConnection.commit()
         except userMapConnection.Error as userMapError:
            print(userMapError)

         userMapConnection.close()
         

Kullanıcı Haritası HTML ve Scriptleri
-------------------------------------

Google apisini kullanarak eklenen haritada bir lokasyon işartelemek için "clickListener()" eklenerek çift tıklama durumunda, haritaya yeni marker eklenmesi sağlanmıştır. Aynı zamanda, bu eklenen markerların lokasyonları, bir dizide tutulurken, her marker eklendiğinde açığa çıkan etiket ve açıklama panelinde "Share" butonuna basıldığında bu lokasyonu barındıran dizi, yeni lokasyonla beraber JSON formatından string formatına çevrilerek python dosyasına gönderilir. Bunu gerçekleyen fonksiyon aşağıda gösterilmektedir. 

.. code-block:: javascript

    $(function() {
    $('#share').bind('click', function(form) {
      var locationLabel = document.getElementById("label").value;
      var locationInfo = document.getElementById("info").value;
      newLocations.push({lat: event.latLng.lat(),lng: event.latLng.lng(),label: locationLabel,info: locationInfo});
      $.ajax({
        url: "/userPage/getLocations",
        type: "POST",
        data: JSON.stringify(newLocations),
        contentType: "application/json; charset=utf-8",
        success: function(dat) { console.log(dat); }
    });
 
Bu fonksiyon, javascript içerisinden harita bilgilerini html formundan da etiket ve açıklama bilgilerini alarak yeni lokasyonu oluşturur ve python dosyasında getLocations fonksiyonuna yollar.


Haritaya her çift tıklandığında "clickListener" ın altındaki bölgeler çalışmaya başlar. Öncelikle tıklanan lokasyona bir marker eklenir. Aynı zamanda marker lokasyonlar dizisine de eklenir. Bu sırada input penceresinin açılması için işaret verilir.

.. code-block:: javascript

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
         
    });
  
------------------------------------

Arkadaş Tablosu, Request Tablosu ve Operasyonları
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

FRIENDSTABLE; friendREcordId, user_id, friend_id ve status nitelikleirnden oluşan ve arkadaşlık bilgilerini tutan tablodur. Birincil anahtar olarak, otomatik arttırılan friendRecordId niteliği kullanılmaktadır. User_id ve friend_id dış anahtarlar olup, iki nitelik de user tablosuna başvurmaktadır. Status niteliği bir arkadaşlığın özelliğini belirtmektedir. Bu özellikler yakın arkadaş, normal arkadaş veya bloklanmış arkadaş olmaktadır. Friends table nitelikeri, Friend nesnesiyle python dosyalarında kullanılırlar.

.. code-block:: python

  class Friend:
      def __init__(self, userName=None    , friendUsername=None):
          self.userName = userName
          self.friendUsername = friendUsername
          self.friendStatus = None
          self.friendId = 0
          
Bütün arkadaşlık ilişkilerinin düzenlenmesini sağlamak amacıyla FriendStore nesnesi kullanılır. Friend nesnelerinden oluşan bir dizi tutmaktadır, ayrıca add,delete, update ,block gibi friend opearsyonlarını gerçekler.

Arkadaş Ekleme
-----------------

Request tablosu request_id, requester ve requested niteliklerinden oluşan ve arkadaş olma ilişkisini düzenleyen bir tablodur. Tabloda request_id otomatik artan birincil anahtar olup requester ve requested nitelikleri user tablosuna bağlı dış anahtarlardır. Arkadaş eklemek için önce bir request yollanması gerekmektedir. Request yollamak içinse zaten arkadaş olmamak ve zaten request yollamış olmamak gerekmektedir.

Bir request'in pyhton içerisinde rahatlıkla kullanılabilmesi için request.py dosyasındaki request nesnesi kullanılır.

.. code-block:: python
    
    class Request:
    def __init__(self,requestId=None, requester=None, requested=None):
        self.requester = requester
        self.requested = requested
        self.requestId = requestId

Gönderilen istekler kullanıcıların notification sayfalarında görünmeden önce veritabanından okunarak bir liste halini alırlar bunun için requestStore nesnesi kullanılmaktadır. Bu nesne aynı zamanda bütün veritabanı işlemlerini gerçekleştirmektedir.

.. code-block:: python
    
    class RequestStore:
        def __init__(self):
            self.myRequests = []
            self.lastRequestId = 0

Bir requestin halihazırda gönderildiğini veya alındığını belirlemek için searchRequests fonkisyonu kullanılmaktadır. Bu fonksiyon REQUESTTABLE tablosunun hem requester hem requested niteliklerini kontrol ederek bir requestin varlığını aramaktadır eğer yoksa yeni requestin gönderilebileceği yönünde sonuç döndürmektedir.

.. code-block:: python
   
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


Request'ler tabloya eklendikten sonra requestStore içerisinde request nesnelerinden oluşan diziye eklenirler. Bu dizi sayesinde dosyalar arası request aktarımı yapılmaktadır. "getRequests" fonksiyonu ilgili kullanıcının bütün requestlerini veritabanından almaktadır. Bu fonksiyon ilgili user_id'ye ait bütün requestleri getirmektedir.

.. code-block:: python
   
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
        
Request tablosuna eklenmiş olan bir isteğin request_id'sine göre getirilebilmesi için getRequest fonksiyonu kullanılır. Bu fonksiyon sayesinde bir request üzerinde işlem yapılabilmektedir. Yukarıda anlatılan fonksiyonun aksine, bu fonksyion request_id'ye bakarak sadece bir request döndürür.

.. code-block:: python
   
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
        

Requestler kabul edildiklerinde veya reddedildiklerinde aynı sonuç olarak silinirler. Bu silme işlemini requestStore içerisindeki deleteRequest fonksiyonu yapmaktadır. Bu fonksiyon ile request, tablodan tamamen silinir ve kullanıcı, bildirim ekranında birdaha bu request'i görmez. Request kabul edilmediği veya reddedilmediği sürece bildirim ekranında durmaya devam eder.

.. code-block:: python
   
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
            
Arkadaşlık isteği yollamanın asıl işlerinin görüldüğü yer ise sendRequest fonksiyonunda gerçekleşmektedir. Bu fonksiyon halihazırda arkadaş olunup olunmadığına, böyle bir kullanıcının varolup olmadığına veya kendi kendine request yollamaya   çalışıldığını tespit ederek bir sonuç döndürür ve eğer başarılı sonuç dönerse yukarıda bahsedilen fonksiyonları kullanarak request tablosuna yeni bir request ekler. 

.. code-block:: python
 
        @friends.route('/sendRequest',methods=['POST','GET'])
        def sendRequests():
            if session.get('user')!=None:
                if request.method == 'POST':
                    userName = request.form['user_name']
                    status = search(userName,'someqw19012341')
                    if userName != current_app.user.username:

                        if status == 'Password is invalid':
                            currentName = current_app.user.username
                            relationStatus = current_app.friendStore.searchFriends(currentName,userName)
                            if relationStatus == 'alreadyExists':
                                flash('You are already friends 0_0 or you have been blocked :D')
                            else:
                                requestStatus = current_app.requestStore.searchRequests(currentName,userName)
                                if requestStatus == 'alreadySent':
                                    flash('You already sent a friend request to '+userName)
                                elif requestStatus == 'alreadyReceived':
                                    flash('You already received a friend request from '+userName+' Please check your Notifications page')
                                else:
                                    requests = Request()
                                    requests.requested = userName
                                    requests.requester = current_app.user.username
                                    current_app.requestStore.addRequest(requests)
                                    flash('Friend request has been sent to '+userName)
                        else:
                            flash('There is no user with this username: '+userName)
                    else:
                        flash('very funny -_-')
                return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
            else:
                flash('Please sign in or register for DeepMap')
                return render_template('home.html')

Eğer gönderilmiş bir request kabul edilirse. request ilişkisi silirken arkadaş tablosuna yeni kayıt eklenmesi için süreç başlar. addFriend fonksiyonları bu görevi gerçekleştirmektedir. Bu fonksiyon relation.py içerisinde yer alır ve friendOperations.py içerisinde bulunan addFriend fonksiyonundan aldığı verileri arkadaş tablosuna ekler.

.. code-block:: python
    
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

FriendOperations.py içerisinde yer alan addFriend fonksiyonu kabul edilmiş requestleri alarak requestlerin html dosyalarında gizli bulunan inputların 'POST' metoduyla fonksiyona gelmesiyle hem arkadaşlık isteği gönderen kullanıcının kullanıcı adına hem de isteğin request_id'sine ulaşmış olur. Bu sayede hem request'in tablodan silinmesi hem de arkadaşlık ilişkisinin FRİENDSTABLE tablosuna eklenmesi sağlanmış olur.

.. code-block:: python

    @friends.route('/addFriend',methods=['POST','GET'])
    def addFriends():
        if session.get('user')!=None:
            if request.method == 'POST':
                requestId = request.form['friend_to_add']
                requests =  current_app.requestStore.getRequest(requestId)
                friend = Friend()
                friend.userName = requests.requested
                friend.friendUsername = requests.requester
                current_app.friendStore.addFriend(friend)
                current_app.requestStore.deleteRequest(requestId)
                current_app.requestStore.getRequests(current_app.user.username)
            return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
        else:
            flash('Please sign in or register for DeepMap')
            return render_template('home.html')


Arkadaş Sorgulama
-----------------

Arkadaşlık ilişkisi, friendsTable tablosunda ekleyen ve eklenen olarak tutulmaktadır. Bu ilişki, request tablosundan geldiği için bu şekildedir. bu durumdan yola çıkarak bir kullanıcının arkadaşları hem onu ekleyenler hem de kendi ekledikleri olacağından, veritabanından sorgulanırken hem user_id hem de friend_id niteliklerine ayrı ayrı select query'si yollanır. Bu sayede ilgili kullanıcıya ait tüm arkadaşlar getirilmiş olur. Bu operasyonu gerçekleyen fonksiyon relation.py dosyasında bulunan getFriends fonksiyonudur. User_id ve friend_id niteliklerine sorgu yollar ve çıkan sonuçları bir array olarak döndürür.

.. code-block:: python
      
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

FriendOperations.py dosyasında bulunan getFriends fonksiyonu ise oturumda olan kullanıcıya ait user_id'yi alır ve bu id'yi, bütün arkadaşları getirmesi için, relation.py dosyasındaki getFriends fonksiyonuna gönderir.

.. code-block:: python
    
      @friends.route('/friendsPage',methods=['POST','GET'])
      def getFriends():
          if session.get('user')!=None:
              current_app.friendStore.getFriends(current_app.user.username)
              return render_template('friends.html',friends = current_app.friendStore.myFriends, userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
          else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')

Bunun dışında, zaten arkadaş olarak ekli bir kullanıcıya yeni request gönderilmesini engellemek için, o iki kullanıcı adı ile yapılan bir search query'si gerekmektedir. relation.py dosyasında bulunan searchFriends fonksiyonu, bu işlemi gerçekleştirmektedir. Paramaetre olarak kullanıcı adı ve arkadaşın kullanıcı adını alır. Böyle bir arkadaşlık olup olmadığını kontrol eder. Bu fonksiyon daha önce anlatılan sendRequests fonksiyonunda kullanılmaktadır.

.. code-block:: python

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

Arkadaş Silme
---------------

.. code-block:: python

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
         
        
         
.. code-block:: python
     @friends.route('/deleteFriend',methods=['POST','GET'])
    def deleteFriends():
        if session.get('user')!=None:
            if request.method == 'POST':
                friendId = request.form['friend_to_delete']
                current_app.friendStore.deleteRelation(friendId)
                current_app.friendStore.getFriends(current_app.user.username)
            return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
        else:
            flash('Please sign in or register for DeepMap')
            return render_template('home.html')
            
Arkadaş Güncelleme
-------------------

Arkadaş tablosu için güncelleme operasyonu, status niteliği üzerinden olabilmektedir. Bir arkadaşlık ilişkisi, tabloya ilk eklendiğinde status "casual" olmaktadır. Bu arkadaş sıradan arkadaştır ve ona mesaj atılabilir, yorum yazılabilir ve haritası görüntülenebilir. Bunun dışında kullanıcı arkadaşı yakın arkadaş olarak ekleyebilir veya bloklayabilir. Blokladığı arkadaş, kullanıcının tablosuna ulaşamaz ve ona mesaj atamaz.

1.Arkadaşlık Statüsü Değiştirme: 

yakın arkadaş eklemek için html blogundaki yakın arkadaş ekleme ikonuna tıklandığında gizli input python dosyasına yollanarak arkadaşın kullanıcı adı ve yakın arkadaş ekleme görevi güncelleme fonksiyonlarına dağıtılır. addBestFriends fonksiyonu html'den aldığı bilgiyi updateFriends Fonksiyonunu 'bestFriend' statüsüyle çağırarak uygular. updateFriends fonksiyonu bestfriend çıkarmada da kullanılmaktadır.

.. code-block:: python

    def updateFriends(self,friendId,newStatus):
         try:
            friendTableConnection = getConnection();
            friendCursor = friendTableConnection.cursor()
            friendCursor.execute("""UPDATE FRIENDSTABLE SET status=%s WHERE friendRecordId=%s;""",(newStatus,friendId))
            friendTableConnection.commit()
         except friendTableConnection.Error as Error:
            print(Error)

addBestFriends ve makeCasualFriend fonksiyonları html dosyasında farklı inputlara cevap olarak çağrılırlar. addBestFriends fonksiyonu sadece yakın arkadaş ekleme için kullanılırken makeCasualFriends fonksiyonu hem yakın arkadaşlıktan çıkarma hem de blocklamanın kaldırılması durumlarında html dosyasından ilgili ikona tıklanarak çağırılır. İki fonksyion da relation.py'da updateFriends fonksiyonunu farklı statülerle çağırarak işlemlerini yaparlar.

.. code-block:: python

      @friends.route('/addBestFriend',methods=['POST','GET'])
      def addBestFriends():
          if session.get('user')!=None:
              if request.method == 'POST':
                  friendId = request.form['friendsId']
                  bestFriend = 'bestFriend'
                  current_app.friendStore.updateFriends(friendId,bestFriend)
                  current_app.friendStore.getFriends(current_app.user.username)
              return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
          else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')

      @friends.route('/makeCasual',methods=['POST','GET'])
      def makeCasualFriend():
          if session.get('user')!=None:
              if request.method == 'POST':
                  friendId = request.form['friendsId']
                  casualFriend = 'casualFriend'
                  current_app.friendStore.updateFriends(friendId,casualFriend)
                  current_app.friendStore.getFriends(current_app.user.username)
              return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
          else:
              flash('Please sign in or register for DeepMap')
              return render_template('home.html')


2.Blocklama:

Html dosyasından blocklama ikonuna basılarak çağırılan blockFriends fonksiyonu relation.py'daki blockFriend fonksiyonunu çağırır. Bu fonksiyon diğer update fonksiyonundan farklı olarak önce bir select komutu çalıştırmaktadır. Bunun sebebi blocklama durumunun diğer durumlardan farklı olarak karşılıklı değil tek taraflı olmasıdır. Başka bir değişle yakın arkadaş ekleme bu ilişkide statü'yi bestFriend olarak güncellemekten ibaretken blocklamanın hangi kullanıcı tarafından yaptığı önem arzetmektedir. Bu nedenle bu fonksiyon friend sayfasından friend_id'yi alır ve işlemi yapan kullanıcının kullanıcı ismiyle arkadaş tablosunda bu kullanıcının bulunduğu tarafı belirtecek şekilde 'blocked1' veya 'blocked2' yazarak blocklama yapan kişinin tablonun hangi kolonunda bulunduğunu belirtir.
 
              
.. code-block:: python

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
         
Bu işlem bittikten sonra blockFriends fonksiyonu arkadaşları tekrar okur ve artık kullanıcı blocklanmış vaziyette arkadaşların arasında görünür. eğer arkadaşlık ilişkisi silinirse block durumu ortadan kalkacağından, kullanıcı blocklanan kişi tarafından tekrar arkadaş eklenebilir.       

.. code-block:: python     

         @friends.route('/blockFriend',methods=['POST','GET'])
          def blockFriends():
              if session.get('user')!=None:
                  if request.method == 'POST':
                      friendId = request.form['friendsId']
                      currusername = current_app.user.username
                      current_app.friendStore.blockFriend(friendId,currusername)
                      current_app.friendStore.getFriends(current_app.user.username)
                  return render_template('friends.html',friends = current_app.friendStore.myFriends,userMap = current_app.usermap.myLocations, user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
              else:
                  flash('Please sign in or register for DeepMap')
                  return render_template('home.html')
                  
------------------------------------------------------------

Bildirimler
^^^^^^^^^^^^

NOTIFICATIONTABE tablosu otomatik artan birincil anahtar olan notificationId, user tablosundan dış anahtar olarak kullanılan username ve friendsUsername , message tablosundan dış anahtar olarak kullanılan messageId, comment tablosundan dış anahtar olarak kullanılan commentId niteliklerindne oluşmaktadır. Bu nitelikleri python ortamında rahat elealabilmek için notification nesnesi kullanılmaktadır.

.. code-block:: python     

  class Notification:
      def __init__(self, requester=None, requested=None):
          self.requester = requester
          self.requested = requested
          self.notificationId = None
          self.typeId = None
          self.type = None

Bir kullanıcının birden fazla bildirimi olduğu bilindiğinden bu bildirimlerin toplu halde bulunabileceği ve üzerinde veritabanı işlemlerinin yapılabileceği bir notificationStore nesnesi oluşturulmuştur.

.. code-block:: python     

  class NotificationStore:
      def __init__(self):
          self.myNotifications = []
        
        self.lastNotificationId = 0

Notification tablosundan da anlaşılacağı üzere notification sistemi iki farklı bildirim yollayabilmektedir. Bunlardan birincisi  yorum bildirimi yollamaya yarayan sendCommentNotification fonksiyonudur. Her yorum yapıldığında bu fonksiyon da çağırılarak ilgili kullanıcıya bildirimin gönderilmesi sağlanır. MessageId bölümü boş bırakılarak bildirim oluşturulur.


.. code-block:: python     

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
            
İkinci bildirim ise mesaj bildirimi. Bir kullanıcı her yeni mesaj aldığında sendMessageNotification fonksiyonu çağırılarak bildirim tablosuna commentId boş bırakılarak yeni bildirim oluşturulur.


.. code-block:: python     

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

Notifications sayfasında html kodunda bulununan delete ikonlarına tıklandığında gizli input'tan alınan notificationId deleteNotifications fonksiyonuna gelir ve silinmek üzere notification.pydaki deleteNotification fonksiyonuna gönderilir.

.. code-block:: python     

  @notifications.route('/deleteNotification',methods=['POST','GET'])
  def deleteNotifications():
      if session.get('user')!=None:
          if request.method == 'POST':
              notificationId = request.form['notification_to_delete']
              current_app.notificationStore.deleteNotification(notificationId)
              current_app.notificationStore.getNotifications(current_app.user.username)
              return render_template('notifications.html',notifications = current_app.notificationStore.myNotifications,requests = current_app.requestStore.myRequests,user_name = current_app.user.username,first_name=current_app.user.name,last_name = current_app.user.surname,e_mail=current_app.user.email)
      else:
          flash('Please sign in or register for DeepMap')
          return render_template('home.html')

deleteNotification fonksiyonu da notificationId ile bildirimi silmektedir.

.. code-block:: python     

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

