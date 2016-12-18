Parts Implemented by Emine Öykü Bozkır
================================
  
Kullanıcının Sisteme Girişi için Arayüz (Sign-In)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Kayıtlı kullanıcı sisteme giriş yapabilmek için sağ üst köşedeki sign-in butonuna tıklar ve şekilde gösterilen pencere açılır. Kullanıcı
bu arayüzdeki forma bilgilerini girerek kendi hesabına ve profil bilgilerine ulaşabilir.
  
   .. figure:: oyku_pictures/signin.png
      :align: center
      :scale: 50 %

      Sign-in penceresi
      
    
Kayıtlı olmayan kullanıcı giriş yaparsa veya yanlış parola girilirse ekranın tepesinde aşağıdaki şekilde olduğu gibi bir uyarı çıkar.     
   .. figure:: oyku_pictures/wrongsignin.png
      :align: center
      :scale: 50 %
      :alt: sign-in front page

      Sign-in error

Kullanıcı hesabına giriş yaptıktan sonra sağ üstte kullanıcı adı görülmekte ve bu alana bastığında küçük bi dropdown menu çıkmaktadır.Bu menudeki butonlarla sistemden çıkabilmekte ya da profil sayfasına yönlendirilebilmektedir.

   .. figure:: oyku_pictures/sidebar2.png
      :align: center
      :scale: 50 %
      :alt: sign-in front page
  
  

Sidebar
^^^^^^^   
Kullanıcı hesabına giriş yaptıktan sonra sol tarafta bulunan sidebar ile arkadaş bağıntılarının bulunduğu Friends sayfasına, bildirimlerin olduğu notifications sayfasına kendi haritasının bulunduğu myMap sayfasına ve mesajların olduğu sayfaya ulaşabilmekte. Sidebar kapanıp açılabilmekte. Aşaqıda sidebarın kapalı ve açık ekran  görüntüleri bulunmakta.

  .. figure:: oyku_pictures/sidebar3.png
       :scale: 25 %
       :alt: sidebar front page
       
       Sidebar
       
  .. figure:: oyku_pictures/closedSidebar.png
       :scale: 25 %
       :alt: sidebarClosed front page
       
       Closed Sidebar       
       
User Map
^^^^^^^^

Kullanıcının giriş yaptıktan sonra karşılaşacağı sayfa aşağıdaki gibidir. Bu sayfa kullanıcının kendi haritasının olduğu sayfadır.

  .. figure:: oyku_pictures/mapUser.png
       :scale: 25 %
       :alt: map front page
       
       Kullanıcı haritası
       
Kullanıcı harita üzerinde herhangi bir lokasyona çift tıklayarak kendi haritasına yeni lokasyon ekleyebilir. Ekleme sırasında aşağıdaki gibi bir pencere açılır ve kullanıcı bu arayüzden o lokasyona ait etiket ve açıklama girmektedir. 

  .. figure:: oyku_pictures/newLocation.png
        :scale: 25 %
        :alt: add location front page
       
        Lokasyon ekleme
        
Lokasyon eklendikten sonra haritada şu şekilde görünmektedir:       

   .. figure:: oyku_pictures/showLocation.png
        :scale: 25 %
        :alt: added location front page
        
        Eklenen lokasyon
        
Eğer kullanıcı haritada yakın yerlere birden çok lokasyon eklediyse, harita uzaklaştırılınca lokasyonlar toplu bi şekilde görülmektedir.Aşağıda bulunan şekilde istanbul için dört farklı lokasyon eklenmiş, uzaktan toplu şekilde görülmekte, yakınlaştırdıkça lokasyonlar ayrılmaktadır.

   .. figure:: oyku_pictures/LocationArray.png
        :scale: 25 %
        :alt: locationArray front page
        
   .. figure:: oyku_pictures/closeLocation.png
        :scale: 25 %
        :alt: locationArray front page
        
        Lokasyon grupları
 
Arkadaş ekleme silme ve diğer operasyonlar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arkadaş Sayfası
---------------
Kullanıcı, sidebar da bulunan Friends sekmesine basınca arkadaşlarını görebileceği sayfaya yönlendirilir. Arkadaşlarının hesaplarını buradan, istediği kullanıcının üstüne tıklayarak görebilmektedir. Bu sayfa aşağıdaki gibi gözükmektedir:

   .. figure:: oyku_pictures/AllFriends.png
        :scale: 25 %
        :alt: friends front page
        
        Arkadaş sayfası
        

Arkadaşlık İsteği Yollama
---------------       
        
Kullanıcı, friends sayfasında en altta bulunan "Find New Friends" butonuna tıklayarak başka kullanıcılara arkadaşlık isteği yollayabilir. Açılan pencereye eklemek istediği kullanıcının kullanıcı adını girip add butonuna tıklayarak ona istek göndermiş olur. Eğer girdiği username kayıtlı bir kullanıcıya ait değilse,  ekranın tepesinde uyarı çıkmaktadır. Kullanıcı ayrca kendine ve zaten arkadaşı olan bi kullanıcıya request gönderemez ve yine hata mesajı alır. Arkadaşlık isteği bir kez gönderilirse o istek silinene kadar birdaha istek yollanamaz.     
   
   .. figure:: oyku_pictures/sendReq.png
        :scale: 25 %
        :alt: addfriend front page    
        
        Arkadalık isteği yollama penceresi
 
 Arkadaşlık isteği yollandıktan sonra işlemin başarıyla gerçekleştiğine dair bir bilgi mesajı, ekranın üstünde gösterilir.
  
   .. figure:: oyku_pictures/sendedReq.png
        :scale: 25 %
        :alt: addedfriend front page    
        
        Info Message
 
İstek yollanan kişi, notifications sayfasında mevcut arkadaşlık isteklerini görebilir onları kabul edebiliğr veya silebilir.Aşağıda bulunan resimde, kullanıcıya oykubzkr adlı kullanıcıdan bir arkadaşlık isteği geldiği görülmektedir. Bildirim kutusunun sağ tarafında üç tane buton bulunmaktadır. Eğer kullanıcı yeşil olan butona basarsa oykubzkr adlı kullanıcı arkadaş listesine eklenmiş olur ve ve Friends sayfasında görülür. Eğer kırmızı butona basarsa bu istek silinir ve arkadaş eklenmemiş olur. Mavi buton mesaj butonu olmakta ve kullanıcıyı mesaj sayfasına yönlendirmektedir.
 
   .. figure:: oyku_pictures/friendNotif.png
        :scale: 25 %
        :alt: addedfriend front page    
        
        Friend Notification


Diğer arkadaş işlemleri
--------------------------


İstek gönderilen kişi, isteği kabul ettikten sonra kullanıcı arkadaş olarak eklenmiş olur. Bu durumda Kullanıcı bu arkadaşı silebilir, bloklayabilir veya yakın arkadaş olarak ekleyebilir. Arkadaş kutucuğunda üç buton bulunmaktadır. Bunlardan yeşil olanına basılırsa o kişi her iki kullanıcıda da yakın arkadaş olarak eklenmiş olur. Sarı buton bloklama butonudur ve kullanıcı bu butona basarsa karşısındaki kullanıcının, kendi profilini görmesini engellemiş olur. Aynı butona tekrar basılarak bloklama özlliği kaldırılabilir. Kırmızı buton ise silme butonudur. Kullanıcı bu butona basarsa arkadaşlık tamamen her iki kullanıcıda da silinmiş olur.

  .. figure:: oyku_pictures/addedfriend.png
        :scale: 25 %
        :alt: addedfriend front page    
        
        Friend Notification      
        
Ayrıca kullanıcı adının yazılı olduğu butona basılarak o kullanıcının kendi profilindeki haritasına gidilebilir.
       
       
