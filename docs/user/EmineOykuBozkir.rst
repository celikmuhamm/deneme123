Emine Öykü Bozkır Tarafından Gerçeklenen Bölümler
===============================================
  
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


Hesap Bilgileri
^^^^^^^^^^^^^^^^

Kullanıcı girişi yapıldıktan sonra, sağ üste köşede kullanıcı adı belirmekte ve buraya tıklayınca çeşitli seçeneklerin olduğu dropdown menü açılmaktadır. Bu menüden "Profile" seçeneği seçilirse, kullanıcının kişisel bilgilerinin olduğu kullanıcı hesabına yönlendirilir. Bu sayfanın ekran görüntüsü aşağıda gösterilmiştir.
       
  .. figure:: safa_resimler/profile.png
       :scale: 50 %
       :alt: sidebarClosed front page
       
       Closed Sidebar 

---------------------------------------------

Kullanıcı Haritası
^^^^^^^^^^^^^^^^^^^

Kullanıcının giriş yaptıktan sonra karşılaşacağı sayfa aşağıdaki gibidir. Bu sayfa kullanıcının kendi haritasının olduğu sayfadır.

  .. figure:: oyku_pictures/mapUser.png
       :scale: 50 %
       :alt: map front page
       
       Kullanıcı haritası
       
Kullanıcı harita üzerinde herhangi bir lokasyona çift tıklayarak kendi haritasına yeni lokasyon ekleyebilir. Ekleme sırasında aşağıdaki gibi bir pencere açılır ve kullanıcı bu arayüzden o lokasyona ait etiket ve açıklama girmektedir. Aşağıdaki görsel, yeni lokasyon ekleme arayüzünü göstermektedir. 

  .. figure:: oyku_pictures/newLocation.png
        :scale: 50 %
        :alt: add location front page
       
        Lokasyon ekleme
        
Lokasyon eklendikten sonra haritada şu şekilde görünmektedir:       

   .. figure:: oyku_pictures/showLocation.png
        :scale: 50 %
        :alt: added location front page
        
        Eklenen lokasyon

        
   .. figure:: oyku_pictures/closeLocation.png
        :scale: 25 %
        :alt: locationArray front page
        
        Lokasyonlar

--------------------------------------

Arkadaş ekleme silme ve diğer operasyonlar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arkadaş Sayfası
---------------

Kullanıcı, sidebar da bulunan Friends sekmesine basınca arkadaşlarını görebileceği sayfaya yönlendirilir. Arkadaşlarının hesaplarını buradan, istediği kullanıcının üstüne tıklayarak görebilmektedir. Bu sayfa aşağıdaki gibi gözükmektedir:

   .. figure:: oyku_pictures/AllFriends.png
        :scale: 50 %
        :alt: arkadaş sayfası
        
        Arkadaş sayfası
        

Arkadaşlık İsteği Yollama
---------------       
        
Kullanıcı, friends sayfasında en altta bulunan "Find New Friends" butonuna tıklayarak başka kullanıcılara arkadaşlık isteği yollayabilir. Açılan pencereye eklemek istediği kullanıcının kullanıcı adını girip add butonuna tıklayarak ona istek göndermiş olur. Eğer girdiği username kayıtlı bir kullanıcıya ait değilse, ekranın tepesinde uyarı çıkmaktadır. Kullanıcı ayrıca kendine ve zaten arkadaşı olan bi kullanıcıya arkadaşlık isteği gönderemez ve yine hata mesajı alır. Arkadaşlık isteği bir kez gönderilirse o istek silinene kadar bir daha istek yollanamaz.     
   
   .. figure:: oyku_pictures/sendReq.png
        :scale: 50 %
        :alt: istek yollama   
        
        Arkadalık isteği yollama penceresi
 
 Arkadaşlık isteği yollandıktan sonra işlemin başarıyla gerçekleştiğine dair bir bilgi mesajı, ekranın üstünde gösterilir.
  
   .. figure:: oyku_pictures/sendedReq.png
        :scale: 50 %
        :alt: Bilgilendirme   
        
        Bilgilendirme
 
İstek yollanan kişi, notifications sayfasında mevcut arkadaşlık isteklerini görebilir onları kabul edebilir veya silebilir. Aşağıda bulunan resimde, kullanıcıya oykubzkr adlı kullanıcıdan bir arkadaşlık isteği geldiği görülmektedir. Bildirim kutusunun sağ tarafında üç tane buton bulunmaktadır. Eğer kullanıcı yeşil olan butona basarsa oykubzkr adlı kullanıcı arkadaş listesine eklenmiş olur ve ve Friends sayfasında görülür. Eğer kırmızı butona basarsa bu istek silinir ve arkadaş eklenmemiş olur. Mavi buton mesaj butonu olmakta ve kullanıcıyı mesaj sayfasına yönlendirmektedir.
 
   .. figure:: oyku_pictures/friendNotif.png
        :scale: 50 %
        :alt: istek bildirimi    
        
        Friend Notification


Diğer arkadaş işlemleri
--------------------------

İstek gönderilen kişi, isteği kabul ettikten sonra kullanıcı arkadaş olarak eklenmiş olur. Bu durumda Kullanıcı bu arkadaşı silebilir, bloklayabilir veya yakın arkadaş olarak ekleyebilir. 

Arkadaş kutucuğunda üç buton bulunmaktadır. Bunlardan yeşil olanına basılırsa o kişi her iki kullanıcıda da yakın arkadaş olarak eklenmiş olur. Sarı buton bloklama butonudur ve kullanıcı bu butona basarsa karşısındaki kullanıcının, kendi profilini görmesini engellemiş olur. Aynı butona tekrar basılarak bloklama özlliği kaldırılabilir. Kırmızı buton ise silme butonudur. Kullanıcı bu butona basarsa arkadaşlık tamamen her iki kullanıcıda da silinmiş olur.

  .. figure:: oyku_pictures/addedfriend.png
        :scale: 50 %
        :alt: arkadaslık_istegi    
        
        Arkadaşlık isteği      
        
Ayrıca kullanıcı adının yazılı olduğu butona basılarak o kullanıcının kendi profilindeki haritasına gidilebilir.
Bir kullanıcı, başka bir kullanıcının haritasını görmek istiyorsa, arkadaş olarak eklenmiş olmalıdır. Aksi taktirde başka kullanıcıların haritalarını göremez, yorum yapamaz.
       
--------------------------------------

Bildirimler
^^^^^^^^^^^^

Sol tarafta bulunan sekmelerden "Notifications" seçeneğine tıklanırsa, kullanıcı bidirimlerin olduğu sayfaya yönlendirilir. Bu sayfa, başka kullanıcılar tarafından kendi hesabıyla ilgili operasyonlar gerçekleştiğinde kullanıcıyı bu durumdan haberdar etmek için bulunmaktadır. Örneğin, daha önce de anlatıldığı gibi başka bir kullanıcı tarafından arkadaş olarak eklenilirse, bu durum bildirimler sayfasında gösterilmekte ve bu sayfadan gerekli işlemler yapılabilmektedir.

Arkadaş olarak eklenme dışında, eğer başka bir kullanıcı, kullanıcı haritasına yorum yapmış ise, bu durum da bildirimler sayfasında "(Username) has commented on your Map" şeklinde bir uyarıyla görülebilmektedir. Burada Username yerine, yorumu yapan kişinin kullanıcı adı geçmektedir.

Bunun dışında, yeni gelen mesajlar da "(Username) sent you a message" şeklinde bir uyarıyla kullanıcıya bildirilmektedir.

Aşağıda bulunan görselde yorum ve mesaj bildiirmlerinin örnekleri görülebilmektedir.

  .. figure:: oyku_pictures/notifs.png
        :scale: 50 %
        :alt: Yorum_mesaj_bildirimleri   
        
        Yorum ve Mesaj Bildirimleri


Bu görselde de başka bir kullanıcı tarafından gelen arkadaşlık isteği bildirimi eklenmiştir.

  .. figure:: oyku_pictures/friendnotif.png
        :scale: 50 %
        :alt: addedfriend notif    
        
        Arkadaşlık isteği 








