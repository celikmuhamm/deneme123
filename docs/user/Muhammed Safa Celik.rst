Muhammed Safa Çelik Tarafından Gerçeklenen Bölümler
=================================================


Kullanıcının Sisteme Kaydı (Sign-Up)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kullanıcının kendine ait bir haritasının olması ve kendi lokasyonlarını ekleyebilmesi için sisteme kayıt yapması gerekmektedir. Ayrıca, arkadaş ekleyebilme, haritalarına yorum yapabilme ve mesaj gönderebilme gibi özelliklere de kayıt olarak ulaşılabilmektedir. 

Siteye ilk girildiğinde sağ üst köşede iki tane buton ile karşılaşılmaktadır. Bu butonlar siteye kayıt olmayı ve sisteme girmeyi sağlar. Sign-Up butonu ile kullanıcı kayıt yapabilmektedir. Bu butona basılınca aşağıdaki şekilde gösterilen pencere açılmaktadır.

   .. figure:: safa_resimler/signuppage.png
      :align: center
      :scale: 50 %

      Sign-up penceresi
      
Açılan pencereye istenilen bilgiler girilerek sisteme kaydolunur. Bu bilgiler kullanıcı adı (username), isim, soyisim, e-mail adresi ve şifredir. Buradan alınan bilgiler, veritabanında user tablosuna eklenmektedir. Fakat, tabloya eklenmeden önce bilgilerin kontrolü sağlanmaktadır. Örneğin, e-mail kutusuna girilen input, e-mail formatına uygun olmalıdır, veya iki kez girilen şifreler birbirini tutmalıdır ve her input kutusu doldurulmalıdır. Aksi taktirde hata mesajı alınır. Aşağıdaki şekiller, bu hata mesajlarını göstermektedir.

   .. figure:: safa_resimler/signuperror1.png
      :align: center
      :scale: 50 %
      :alt: sign-up_error
      
      Sign_up e-mail hatası

   .. figure:: safa_resimler/signuperror2.png
      :align: center
      :scale: 50 %
      :alt: sign-up_error
      
      Sign_up password hatası

Bütün bilgiler doğru ve tam bir şekilde girildikten sonra veritabanına kaydedilmektedir. Burada dikkat edilmesi gereken nokta username kısmının, yani kullanıcı adının kullanılmıyor olmasıdır. Eğer başka bir kullanıcı tarafından kullanılan bir username girilirse veritabanına kayıt olunamaz. Bu durumda giriş sayfasına yönlendirilir ve bu sayfada bu kullanıcı adının zaten var olduğuna dair bir hata mesajı gösterilir.



Admin Sayfası
^^^^^^^^^^^^^
Admin, bütün kullanıcıların bilgilerine erişebilmekte ve gerekirse bu bilgiler üzerinde değişiklik yapabilmekte, hatta kullanıcıları silebilmektedir. Bu fonksiyonlara ulaşabilmek için "deepMapAdmin" kullanıcı adı ile giriş yapıldıktan sonra açılan sayfanın linkine "userPage" yerine "/adminPage" uzantısı eklenerek ulaşılabilir.

Admin sayfasına giriş yapldıktan sonra kullanıcılarının bilgilerinin olduğu tabloya ulaşılır. Ayrıca update ve delete butonları ile de kullanıcı bilgileri üzerinde değişiklik yapılabilmektedir. Aşağıdaki şekilde admin sayfası gösterilmektedir.

   .. figure:: safa_resimler/adminpage.png
      :align: center
      :scale: 50 %
      :alt: adminpage
      
      Admin Sayfası

Kayıt Güncelleme
-----------------
Admin sayfasında bulunan update butonu ile kullanıcı bilgileri güncellenebilmektedir. Bu butona basılınca gerekli bilgilerin girilebildiği bir pencere açılır. Bu pencereye bilgisi güncellenmek istenen kullanıcının adı ve güncellenecek bilgiler girilir ve submit butonuna basılır. Bu sayede kullanıcının bilgileri güncellenmiş olur. Güncelleme penceresi aşağıdaki şekilde gösterilmiştir.

   .. figure:: safa_resimler/adminupdate.png
      :align: center
      :scale: 50 %
      :alt: adminupdate
      
      Admin Update Sayfası


Kayıt Silme
-----------------
Kayıt silme, yine admin sayfasında bulunan delete butonuna basılarak gerçekleşmektedir. Bu butoa basılınca aşağıda bulunan ekran görülmektedir. Bu ekrana silinmek istenen kaydın kullanıcı adı girilerek submit butonuna basılır. Bu şekilde bu kuullanıcıya ait kayıtlar veritabanından silinmiş olur ve bu kullanıcı yeniden kayıt olmadığı sürece siteye giriş yapamaz.

   .. figure:: safa_resimler/admindelete.png
      :align: center
      :scale: 50 %
      :alt: admindelete
      
      Admin Delete Sayfası

--------------------------

Mesajlaşma
^^^^^^^^^^^^^^^
Kullanıcı,giriş yaptıktan sonra, sayfanın sol tarafında bulunan sidebar içeriklerini kullanarak messaj sayfasına ulaşabilmektedir. Bu sayfada kullanıcı kendine gelen mesajlarını görebilir, onlara cevap yazabilir veya yeni bir görüşme başlatabilir. Her kullanıcıyla olan mesajlar farklı kutucuklarda bulunmaktadır. Bu kutucukların üstüne basıldığında geçmiş mesajlaşmalar görülebilmektedir. 

Aşağıdaki görselde, farklı kullanıcılarla yapılan mesajlaşma ve yeni mesaj kutusu oluşturma seçenekleri görülmektedir. "Start New Conversation" butonu ile yeni bir sohbet açılabilir, "chat with naber" kutucuğu ile, "naber" adlı kullanıcı ile yapılan görüşmelere ulaşılabilir ve bu kullnaıcıya yeni mesaj gönderilebilir.

   .. figure:: safa_resimler/messages.png
      :align: center
      :scale: 50 %
      :alt: message window
      
      Mesaj Sayfası

Yukarıda da açıklandığı gibi "Start New Chat" butonu ile yeni bir görüşme başlatılabilmektedir. Aşağıdaki görselde bulunan "username" kısmına mesaj gönderilmek istenen kullanıcı adı, alttaki input kutusuna ise mesajın içeriği girilir. Send butonuna basılarak mesaj gönderilmiş olur. 

   .. figure:: safa_resimler/startchat.png
      :align: center
      :scale: 50 %
      :alt: chat window
      
      Yeni Mesaj Yazma

Burada dikkat edilmesi gereken nokta, girilen kullanıcı adı ile bir arkadaşlık bağlantısının olmasıdır. Eğer bu kullanıcı arkadaş olarak eklenmemişse mesaj gönderilemez ve ekranın tepesinde hata mesajı görülür.

   .. figure:: safa_resimler/messageerror.png
      :align: center
      :scale: 50 %
      :alt: chat window error
      
      Arkadaş Değilsin Hatası
      
Bunun dışında, olmayan bir kullanıcıya mesaj gönderilmeye çalışılırsa veya kullanıcı kendine mesaj yollamaya çalışırsa da hata mesajları gösterilmektedir.

Eğer mesaj başarıyla gönderilirse mesajı alan kişi notifications sayfasında ilgili bildirimle birlikte, kullanıcıların karşılıklı adları ile yeni bir sohbet kutucuğu oluşturulur, bu kullanıcı ile olan bütün mesajlar bu kutuda gösterilmektedir. Şekildeki görselde user adlı kullanıcı deepMapAdmin kullanıcısına mesaj göndererek yeni bir sohbet başlatmıştır.

   .. figure:: safa_resimler/addnewchat.png
      :align: center
      :scale: 50 %
      :alt: new chat window
    
      deepMapAdmin ile başlatılan sohbet

Bu kutulardan chat with "deepMapAdmin" yazılı olana basılırsa bu kullanıcı ile olan görüşme sayfası açılır ve gönderilen ve gelen mesajlar gösterilir.

   .. figure:: safa_resimler/chatscreen.png
      :align: center
      :scale: 50 %
      :alt: new chat window
    
      deepMapAdmin ile yapılan sohbet
    
Karşılıklı mesajlaşma bu şekilde görülmektedir:

   .. figure:: safa_resimler/conversationscreen.png
      :align: center
      :scale: 50 %
      :alt: new chat window
    
      

Her mesaj gönderen kişi tarafından silinebilir. Eğer mesajı alan kullanıcı mesajı silmek isterse mesaj ona görünmez hale gelir fakat gönderen kişi mesajı hala görmeye devam eder.

 
--------------------------

Yorumlar
^^^^^^^^^^^^^^^

Her kullanıcı hem kendi haritasına hem de arkadaş olduğu kullanıcıların haritalarına yorum yapabilmektedir. Arkadaş oldukları kullanıcıların sayfalarına friends sayfasından ulaştıktan sonra yorum alanına yazıp submit butonuna bastıklarında kullanıcı isimleriyle yorum içerikleri o kullanıcının haritasının altına eklenmiş olur. Bu yorumları haritanın sahibi olan kullanıcı ve onun arkadaşları görebilirler ve silebilirler.

   .. figure:: safa_resimler/comments.png
      :align: center
      :scale: 50 %
      :alt: new chat window
    
      yorumlar 


--------------------------

Ekstralar
^^^^^^^^^^^^^^^

Kullanıcı haritalarına cluster servisi eklendi. kullanıcıların sürekli marker eklemesiyle markerların uzaklaştığında birbirlerini engellemelerinin önüne geçmek için google cluster servisi kullanıldı. Bu sayede haritada markerlar kendilerine en yakın olan markerlarla birleşip cluster'ları oluşturup kaç marker barındırıyorlarsa o rakamı üstlerinde barındırarak haritaya rahat okunma ve rahat analiz edilme yeteneklerini kazandırmış oldular.

   .. figure:: safa_resimler/closeLocs.png
      :align: center
      :scale: 50 %
      :alt: new chat window
    
      yakından görünüm 
      
   .. figure:: safa_resimler/locArray.png
      :align: center
      :scale: 50 %
      :alt: new chat window
    
      uzaktan görünüm       



