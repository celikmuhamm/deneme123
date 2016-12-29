Nihat Mert Çiçek Tarafından Gerçeklenen Bölümler
================================
Olaylar (Events)
----------------

Genel Sınıf Tanımları (event.py + store.py)
+++++++++++++++++++++++++++

.. code-block:: python
	
	class Event:
		def __init__(self, title, event_id, date=None, place=None):
			self.title = title
			self.date = date
			self.place = place
			self.event_id=event_id

Bu sınıf veritabanından çekilen olaylar arasında iterasyon yaparken ve verileri html dosyasına gönderirken kullanılır. Başlık (title), tarih (date), yer (place) ve olay kimliği (event_id) sınıfın niteliklerini oluşturur. Sınıfın bir örneği oluşturulması durumunda (instatiation) kurucu fonksiyon alınan argümanları sınıfın uygun verilerine atar. 

.. code-block:: python

	class Store:
		def __init__(self):
			self.events = {}
			self.last_event_id = 0
			
"Store" sınıfı olay ekleme, silme, güncelleme, olayları sıralama gibi fonksiyonları gerçekler ve veritabanına bağlanarak "events" tablosunda gerekli düzenlemeleri yapar. Sınıfın kurucu fonksiyonu son olay kimliğini (last_event_id) varsayılan olarak "0" yapar ve olaylarla ilgili boş bir dizi oluşturur.

.. code-block:: python

		def add_event(self, event):
			self.last_event_id += 1
			self.events[self.last_event_id] = event
			event._id = self.last_event_id
	#        username = current_app.user.username;
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
	#            query = """INSERT INTO EVENTTABLE (title,date,place,username) VALUES (%s, %s, %s, %s)"""
				query = """INSERT INTO EVENTTABLE (title,date,place) VALUES (%s, %s, %s)"""
			try: 
	#            cursor.execute(query, (event.title, event.date, event.place, username))
				cursor.execute(query, (event.title, event.date, event.place))
				self.last_key = cursor.lastrowid
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

"Store" sınıfına ait "add_event" fonksiyonu olay eklemek için kullanılır. Bu fonskiyonda olay öncelikle tüm olaylar dizisinin son elemanına kaydedilir ve "get_connection_for_events" fonksiyonu ile veritabanına bağlanmak için "dsn" bağlantısı alınır. Veritabanına ekleme işlemi "try" bloğu içerisinde "INSERT INTO EVENTTABLE (title,date,place) VALUES (%s, %s, %s)" sorgusunun gerçekleştirilmesi ile yapılır. Hata durumunda except bloğu hatayı yakalar ve konsola hata mesajı yazar. Bağlantının sonlandırılması ile fonksiyondan çıkılır.
			
.. code-block:: python

		def delete_event(self, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """DELETE FROM EVENTTABLE WHERE event_id = %s"""
			try:
				cursor.execute(query,(event_id,))
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

"Store" sınıfına ait "delete_event" fonksiyonu olay silmek için kullanılır. Olayın kimliğini (event_id) alan bu fonksiyon öncelikle veritabanına bağlanmak için gerekli işlemleri yapar. Daha sonra "DELETE FROM EVENTTABLE WHERE event_id = %s" sorgusu alınan kimlik değeri için "try" bloğu içerisinde çalıştırılarak ilgili olay "events" tablosundan silinir. Hata durumunda except bloğu hatayı yakalar ve konsola hata mesajı yazar. Bağlantının sonlandırılması ile fonksiyondan çıkılır.

.. code-block:: python

		def get_event(self, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT * FROM EVENTTABLE WHERE event_id= %s;"""
			try:
				cursor.execute(query,(event_id,))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				else:        
					title = fetched_data[0]
					date = fetched_data[1]
					place = fetched_data[2]
					event_id = fetched_data[3]
					event = [(Event(title, event_id, date, place))]
				connection.commit()
				
			except connection.Error as error:
				print(error)
			connection.close()
			return event

"Store" sınıfına ait "get_event" fonksiyonu olay kimliği ile olayın tüm verilerini elde etmek için kullanılır. Veritabanına bağlantı yapıldıktan sonra "try" bloğu içerisinde " SELECT * FROM EVENTTABLE WHERE event_id= %s " sorgusu çalıştırılır. "cursor.fetchone()" fonksiyonu ile tablodan bir veri istenir. Eğer tabloda tüm satırlar boş ise fonksiyonu boş döner. Aksi takdirde elde edilen veri sırasıyla değişkenlere atanır ve bu değişkenler kullanılarak "Event" sınıfından bir örnekleme "instantiation" fonksiyondan geri döndürülür.

.. code-block:: python

		def get_events(self):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT * FROM EVENTTABLE ORDER BY event_id;"""
			try:
				cursor.execute(query)
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				title = fetched_data[0]
				date = fetched_data[1]
				place = fetched_data[2]
				event_id = fetched_data[3]
				events = [(Event(title, event_id, date, place))]
				for row in cursor: 
					title,date,place,event_id = row
					events_row = [(Event(title, event_id, date, place))]
					events += events_row     
				connection.commit()
							   
			except connection.Error as error:
				print(error)
			connection.close()
			return events

"Store" sınıfına ait "get_events" fonksiyonu tüm olayları dizi olarak elde etmek için kullanılır. Veritabanına bağlantı yapıldıktan sonra "try" bloğu içerisinde " SELECT * FROM EVENTTABLE ORDER BY event_id" sorgusu çalıştırılır. "cursor.fetchone()" fonksiyonu ile tablodan bir veri istenir. Eğer tablo boş ise fonksiyon boş döner. Aksi takdirde elde edilen veri ile "Event" sınıfının bir örneklemesi (instantiation) oluşturulur ve "events" dizisine eklenir. "for row in cursor" kodu ile veritabanındaki tüm satırlar arasında gezilir ve çekilen veriler "events" dizisinin sonuna eklenir. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar. Yapılan sorgular işlenir (commit) ve bağlantı sonlandırıldıktan sonra fonksiyon "events" dizisini döndürür.


.. code-block:: python

		def get_total_events(self):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT COUNT(*) FROM EVENTTABLE;"""
			try:
				cursor.execute(query)
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				total_count = fetched_data
				connection.commit()
					
			except connection.Error as error:
				print(error)
			connection.close()
			return total_count
		
"Store" sınıfına ait "get_total_events" fonksiyonu tüm olayların toplam sayısını elde etmek için kullanılır. " SELECT COUNT(*) FROM EVENTTABLE" sorgusu ile tabloda bulunan satırların sayısı "try" bloğu içerisinde sorgulanır. Eğer tabloda hiç veri yoksa fonksiyon boş döner aksi takdirde yapılan sorgu işlenir (commit) ve fonksiyon toplam satır sayısını döndürür. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.


.. code-block:: python

		def update_event(self, event, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """UPDATE EVENTTABLE SET title = %s,date = %s, place = %s, content = %s WHERE event_id = %s"""
			try:
				cursor.execute(query,(event.title, event.date, event.place,event.content, event_id,))
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()
	
"Store" sınıfına ait "update_event" fonksiyonu olay kimliğine göre tablodaki bir satırı değiştirme için kullanılır. "UPDATE EVENTTABLE SET title = %s,date = %s, place = %s, content = %s WHERE event_id = %s" sorgusunun "try" bloğu içerisinde çalıştırılması ile bir olayın tarihi, zamanı, içeriği ve yeri güncellenebilir. Sorgular işlendikten sonra (commit) fonksiyon herhangi bir şey döndürmez.
	

.. code-block:: python

		def update_event_id(self, event_id, new_id):
			event = current_app.store.get_event(event_id)
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """UPDATE EVENTTABLE SET event_id = %s WHERE event_id = %s """
			try:
				cursor.execute(query,(int(new_id), event_id,))
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

"Store" sınıfına ait "update_event_id" fonksiyonu "events" tablosunun birincil anahtarı olan olay kimliklerini herhangi bir olay silme veya güncelleme durumunda doğru değerlerine güncelleyebilmek amacıyla oluşturulmuştur. "UPDATE EVENTTABLE SET event_id = %s WHERE event_id = %s " sorgusu "try" bloğu içerisinde çalıştırılır ve işlenir. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar. 

Yardımcı Fonksiyonlar (events.py)
+++++++++++++++++++++++++++

.. code-block:: python

	@event.route('/events/add_event', methods=['GET', 'POST'])
	def add_new_event():
		if request.method == 'POST':
	#        if session.get('user')!=None:
				title_temp = request.form['inputTitle']
				date_temp = request.form['inputDate']
				place_temp = request.form['inputPlace']
				event_id = 1
				event_temp = Event(title = title_temp, date=date_temp, place=place_temp,event_id = event_id)
				current_app.store.add_event(event_temp)
				return render_template('events.html')
	#        else:
	#            flash('Please sign in or register for DeepMap')
	#            return render_template('home.html')


Kullanım kılavuzunda bahsedilen olay ekleme sayfasındaki form doldurulduktan sonra "save" butonuna tıklanınca çağrılan fonksiyon yukarıda görüldüğü gibidir. Tüm alanların doldurulması durumunda 'request.method' 'post' olarak gönderildiği için 'if' bloğunun içine girilir. 'request.form[]' metotları ile formda doldurulan veriler değişkenlere atanır ve bu değişkenler kullanılarak "Event" sınıfından bir nesne oluşturulur. Oluşturulan bu nesne veritabanı tablosuna **current_app.store.add_event(event_temp)** fonksiyonu kullanılarak eklenir. Son olarak **"render_template('events.html')"** fonksiyonu ile kullanıcı olaylar sayfasına yönlendirilir.


.. code-block:: python

	@event.route('/events/delete_event', methods=['GET', 'POST'])
	def delete_event():
		if request.method == 'POST':
			event_id_list = request.form.getlist('event_id_list')
			for event_id in event_id_list:
				current_app.store.delete_event(int(event_id))
				
			events=current_app.store.get_events()
			count=1
			if events:
				for event in events:
					if event.event_id != count:
						current_app.store.update_event_id(event.event_id,count)
					count += 1
			
			return render_template('events.html')


Olay silmek için "Delete" butonuna basılması durumunda çağrılan fonksiyon yukarıda görülmektedir. Kontrol kutuları işaretlenen olayların olay kimliklerinin (event_id) listesi **"request.form.getlist('event_id_list')"** yardımcı fonksiyonu ile elde edilir. Kimlikleri alınan tüm olaylar 'for' döngüsü yardımıyla veritabanı tablosundan **current_app.store.delete_event(int(event_id))** fonksiyonunu kullanarak silinir. Geriye kalan satırların birincil anahtarları olan 'event_id' sütunlarını ardışıl olarak düzenleyebilmek amacıyla tüm olaylar veritabanı tablosundan **current_app.store.get_events()** fonksiyonu ile alınır ve **current_app.store.update_event_id(event.event_id,count)** fonksiyonu ile 'event_id' değerleri güncellenir. Son olarak **render_template('events.html')** fonksiyonu ile kullanıcı olaylar sayfasına yönlendirilir.
			

Dökümanlar (Documents)
----------------

Genel Sınıf Tanımları (event.py + store_documents.py)
+++++++++++++++++++++++++++

.. code-block:: python

	class Document:
		def __init__(self, event_id, document_id, content, title, date=None):
			self.event_id = event_id
			self.document_id = document_id
			self.date = date
			self.content = content
			self.title = title

"Document" sınıfı veritabanından çekilen dökümanlar arasında iterasyon yaparken ve verileri html dosyasına gönderirken kullanılır. Bu sınıfın ait bir nesne oluşturulması durumunda (instantiation) kurucu fonksiyon alınan argümanları sınıfın uygun verilerine atar. Başlık (title), tarih (date), içerik (content), olay kimliği(event_id) ve döküman kimliği (document_id) sınıfın niteliklerini oluşturur.

			

.. code-block:: python

	class Store_Document:
		def __init__(self):
			self.documents = {}
			self.last_document_id = 0

"Store_Document" sınıfının kurucu (constructor) fonksiyonu yukarıda görülmektedir. "server.py" 'da sınıfın bir nesnesi oluşturulduğunda kurucu fonksiyon çağrılır ve "documents" niteliği boş bir diziye atanırken "last_document_id" niteliğine sıfır olarak ilk değer atanır. 

			
.. code-block:: python

		def add_document(self, document):
			self.last_document_id += 1
			self.documents[self.last_document_id] = document
			document._id = self.last_document_id
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				title = document.title
				date = document.date
				event_id = document.event_id
				document_id = document.document_id
				content = document.content
	#            username = current_app.user.username;
	#            query = """INSERT INTO DOCUMENTTABLE (title,date,content,event_id,document_id,username) VALUES (%s, %s, %s, %s, %s, %s)"""
				query = """INSERT INTO DOCUMENTTABLE (title,date,content,event_id,document_id) VALUES (%s, %s, %s, %s, %s)"""
			try: 
	#            cursor.execute(query, (title,date,content,event_id,document_id, username))
				cursor.execute(query, (title,date,content,event_id,document_id))
				self.last_key = cursor.lastrowid
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

			
"Store_Document" sınıfının bir fonksiyonu olan "add_document" önceden eklenmiş bir olaya döküman eklemek amacıyla kullanılır. Döküman kimliği (document_id) ve "documents" dizisi ile ilgili gerekli atamalar yapıldıktan sonra **get_connection_for_events()** fonksiyonu ile veritabanına bağlanılır. Fonksiyona giriş argümanı olarak verilen "document" nesnesinin nitelikleri değişkenlere atanır. Bu değişkenler **"INSERT INTO DOCUMENTTABLE (title,date,content,event_id,document_id) VALUES (%s, %s, %s, %s, %s)"** sorgusunun "try" bloğu içerisinde çalıştırılması ve işlenmesi (commit) ile dökümanlar (documents) tablosunun karşılık gelen sütunlarına eklenir. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.

.. code-block:: python

		def delete_document(self, document_id, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """DELETE FROM DOCUMENTTABLE WHERE event_id = %s AND document_id = %s"""
			try:
				cursor.execute(query,(event_id,document_id,))
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

"Store_Document" sınıfının bir fonksiyonu olan "delete_document" önceden eklenmiş olaya ait dökümanı silerken kullanılır. Döküman kimliği (document_id) ve olay kimliğini (event_id) giriş argümanı olarak alan fonksiyon veritabanına bağlandıktan sonra **"DELETE FROM DOCUMENTTABLE WHERE event_id = %s AND document_id = %s"** sorgusunun "try" bloğu içerisinde çalıştırılması(execute) ve işlenmesi(commit) ile ilgili satır tablodan silinmiş olur. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.
			
			
.. code-block:: python

		def get_document_id(self, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT COUNT(*) FROM DOCUMENTTABLE WHERE event_id= %s;"""
			try:
				cursor.execute(query,(event_id,))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				else:        
					count_image = fetched_data[0]
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()
			return count_image

"Store_Document" sınıfının bir fonksiyonu olan "get_document_id" bir olay için eklenmiş olan dökümanların toplam sayısını döndürmek için kullanılır. Bu sayede yeni eklenecek olan dökümanın kimlik değeri (document_id) tespit edilir. Veritabanına bağlandıktan sonra **" SELECT COUNT(*) FROM DOCUMENTTABLE WHERE event_id= %s;"** sorgusu "try" bloğu içerisinde çalıştırılır ve toplam sayı **cursor.fetchone()** yardımcı fonksiyonu ile bir değişkene atanır. Değişkenin değerinin boş olup olmadığı kontrol edilir ve sorgu işlendikten (commit) sonra toplam sayı döndürülür. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.
			

.. code-block:: python

		def get_document(self, document_id, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT * FROM DOCUMENTTABLE WHERE event_id= %s AND document_id = %s;"""
			try:
				cursor.execute(query,(event_id,document_id))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				else:        
					title = fetched_data[0]
					date = fetched_data[1]
					content = fetched_data[2]
					event_id = fetched_data[3]
					document_id = fetched_data[4]
					document = Document(event_id, document_id, content, title, date)
				connection.commit()
				
			except connection.Error as error:
				print(error)
			connection.close()
			return document

"Store_Document" sınıfının bir fonksiyonu olan "get_document" kullanıcının döküman güncellemesi durumunda döküman güncelleme sayfasındaki forma eski bilgileri gönderebilmek amacıyla kullanılan bir fonksiyondur. Veritabanına bağlandıktan sonra **" SELECT * FROM DOCUMENTTABLE WHERE event_id= %s AND document_id = %s;"** sorgusu "try" bloğu içerisinde çalıştırılır (execute) ve **cursor.fetchone()** ile alınan satır bir değişkene atanır. Eğer bu değişken boş değilse **Document** sınıfından bir nesne oluşturulur ve bu nesne fonksiyondan döndürülür. Hata durumunda except bloğu hatayı yakalar ve konsola hata mesajı yazar.
			

.. code-block:: python

		def get_documents(self, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT * FROM DOCUMENTTABLE WHERE event_id = %s ORDER BY document_id;"""
			try:
				cursor.execute(query,(event_id,))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				title = fetched_data[0]
				date = fetched_data[1]
				content = fetched_data[2]
				event_id = fetched_data[3]
				document_id = fetched_data[4]
				document = [(Document(event_id, document_id, content, title, date))]
				document_array = document
				for title, date, content, event_id, document_id in cursor: 
					document = [(Document(event_id, document_id, content, title, date))]
					document_array += document
				connection.commit()
					
			except connection.Error as error:
				print(error)
			connection.close()
			return document_array
			
"Store_Document" sınıfının bir fonksiyonu olan "get_documents" bir olaya ait tüm dökümanlara dizi olarak erişebilmek amacıyla kullanılır. Bu sayede tüm dökümanlar 'html' dosyasına gönderilir. Veritabanına bağlandıktan sonra **" SELECT * FROM DOCUMENTTABLE WHERE event_id = %s ORDER BY document_id;"** sorgusu "try" bloğu içerisinde çalıştırılır ve **cursor.fetchone()** fonksiyonu ile bir satır alınarak boş olup olmadığı kontrol edilir. Eğer boş değilse "Document" sınıfının bir nesnesi oluşturulur ve **for title, date, content, event_id, document_id in cursor: ** döngüsü ile tüm satırlardan oluşturulan "Document" nesneleri bir diziye eklenir. Fonksiyon bağlantıyı kapatarak ve diziyi döndürerek sonlanır. Hata durumunda "except" bloğu hatayı yakalar ve ekrana hata mesajı yazar.


.. code-block:: python

		def update_document(self, document, event_id, document_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """UPDATE DOCUMENTTABLE SET title = %s,date = %s, content = %s WHERE event_id = %s AND document_id = %s"""
			try:
				cursor.execute(query,(document.title, document.date, document.content, event_id, document_id,))
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

"Store_Document" sınıfının bir fonksiyonu olan "update_document" döküman güncellemek amacıyla kullanılan bir fonksiyondur. Veritabanına bağlandıktan sonra olay kimliği (event_id) ve döküman kimliğine (document_id) göre döküman güncellemek için**"UPDATE DOCUMENTTABLE SET title = %s,date = %s, content = %s WHERE event_id = %s AND document_id = %s"** sorgusu "try" bloğu içerisinde çalıştırılır ve işlenir. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.
			
			
.. code-block:: python

		def update_document_id(self, document_id, event_id, new_id):
			document = current_app.store_documents.get_document(document_id,event_id)
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """UPDATE DOCUMENTTABLE SET document_id = %s WHERE event_id = %s AND document_id = %s """
			try:
				cursor.execute(query,(new_id, event_id, document_id))
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

"Store_Document" sınıfının bir fonksiyonu olan "update_document_id" bir döküman silme durumunda tüm dökümanların birincil anahtarları olan 'event_id' ve 'document_id' niteliklerini ardışıl olarak sıralayabilmek amacıyla kullanılan bir fonksiyondur. Öncelikle kimlik değeri verilen döküman tablodan **get_document** fonksiyonu yardımıyla bir değişkene atanır. Veritabanına bağlandıktan sonra "UPDATE DOCUMENTTABLE SET document_id = %s WHERE event_id = %s AND document_id = %s " sorgusu çalıştırılarak 'document_id' niteliği güncellenir ve sorgu işlenir. Hata durumunda 'except' bloğu hatayı yakalayarak konsola hata mesajı yazar. 
			

Yardımcı Fonksiyonlar (documents.py)
+++++++++++++++++++++++++++

.. code-block:: python

	@add_doc.route('/events/documents/add', methods=['GET', 'POST'])
	def add_new_document_page():
		if request.method == 'GET':
			form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
			events = current_app.store.get_events()
			return render_template('documents.html', events=events, form=form)    
		else:
			title_temp = request.form['inputTitle']
			date_temp = request.form['inputDate']
			id_temp = request.form['event_number']
			content_temp = request.form['comment']
			document_id = current_app.store_documents.get_document_id(id_temp) + 1
			document_temp = Document(title = title_temp, date=date_temp, event_id=id_temp,content= content_temp, document_id = document_id)
			current_app.store_documents.add_document(document_temp)
			documents = current_app.store_documents.get_documents(id_temp)
			return render_template('documents.html', documents=documents)

Kullanım kılavuzunda bahsedilen döküman ekleme sayfasındaki "New" butonuna tıklanınca çağrılan fonksiyon yukarıda görüldüğü gibidir. Başlangıçta formun boş olarak görünmesi için form verisi boş olarak 'documents.html' sayfasına gönderilir ve kullanıcı bu sayfaya yönlendirilir ('request.method' 'get' olarak alındığında). Eğer kullanıcı formu doldurup 'save' butonuna basarsa fonksiyon 'request.method' 'post' olarak alınır ve formlardaki veriler 'request.form[]' yardımcı fonksiyonları yardımıyla değişkenlere atanarak "Document" sınıfından bir nesne oluşturulur. 'add_document' fonksiyonuyla bu nesne veritabanına eklenir ve 'get_documents' fonksiyonuyla alınan tüm dökümanlar html dosyasına değişken olarak verilir bu sayede kullanıcı eklediği dökümanı görebileceği dökümanlar sayfasına yönlendirilir.
			

.. code-block:: python

  @add_doc.route('/events/documents/delete', methods=['GET', 'POST'])
    def delete_document():
      if request.method == 'POST':
        document_id_list = request.form.getlist('document_id_list')
        event_id = request.form['delete']
        for document_id in document_id_list:
          current_app.store_documents.delete_document(int(document_id), int(event_id))
        documents=current_app.store_documents.get_documents(int(event_id))
        count=1
        if documents:
          for document in documents:
            if document.document_id != count:
              current_app.store_documents.update_document_id(int(document.document_id), int(event_id),count)
            count += 1

        documents = current_app.store_documents.get_documents(event_id)
        return render_template('documents.html', documents=documents)

Bu fonksiyon kullanıcının silmek istediği dökümanın altındaki kontrol kutularını işaretleyerek 'Delete' butonuna basması sonucu çağrılır. **'request.form.getlist('document_id_list')'** ile silinmek istenen dökümanların kimlik değerleri dizi olarak bir değişkene atanır. Silinmek istenen olayın kimliği de aynı şekilde 'request.form[]' kullanılarak elde edilir. Alınan kimlik değerlerine göre tüm elemanlar 'for' döngüsü yardımıyla **current_app.store_documents.delete_document(int(document_id), int(event_id))** fonksiyonunu kullanarak silinir. Silinmenin ardından geri kalan dökümanların döküman kimlik değerlerini ardışıl olarak güncelleyebilmek amacıyla tüm dökümanlar alındıktan sonra **current_app.store_documents.update_document_id(int(document.document_id), int(event_id),count)** fonksiyonu ile 'id' güncelleme işlemleri veritabanı tablosunda gerçekleştirilir. Son olarak kullanıcı silinen dökümanın ait olduğu olaya ait tüm dökümanların olduğu sayfaya **current_app.store_documents.get_documents(event_id)** fonksiyonu aracılığıyla yönlendirilir.
			
			
.. code-block:: python

  @add_doc.route('/events/documents/update/<int:event_id>/<int:document_id>', methods=['GET', 'POST'])
    def update_documents_page(document_id, event_id):
      if request.method == 'GET':
        document = current_app.store_documents.get_document(document_id, event_id)
        event = current_app.store.get_event(int(document.event_id))
        event=event[0]
        events = current_app.store.get_events()
        form = {'inputTitle': document.title, 'inputDate': document.date, 'comment':document.content}
        return render_template('update_documents.html', events=events, form=form)  

      else:
        title_temp = request.form['inputTitle']
        date_temp = request.form['inputDate']
        content_temp = request.form['comment']
        document_temp = Document(title = title_temp, date=date_temp, event_id=event_id,content= content_temp, document_id = document_id)
        current_app.store_documents.update_document(document_temp,event_id,document_id)
        documents = current_app.store_documents.get_documents(event_id)
        return render_template('documents.html', documents=documents)

Kullanıcı bir olaya ait dökümanı güncellemek amacıyla butona tıkladığında çağrılan fonksiyon yukarıda görülmektedir. Form isteğinin (request.method) 'get' olarak alındığı durumda güncellenecek dökümanın eski bilgilerini formda doldurulmuş olarak getirebilmek için ilgili döküman veritabanından **get_document** fonksiyonu ile alınır ve form verisinin karşılık gelen değerlerine atanarak kullanıcı dökümanlar sayfasına yönlendirilir. Eğer kullanıcı döküman güncelleme sayfasında istediği değişikleri yaptıktan sonra 'save' butonuna tıkladıysa fonksiyon 'else' bloğuna girer ve 'request.form[]' ile form verileri değişkenlere atanır. Son olarak **current_app.store_documents.update_document(document_temp,event_id,document_id)** fonksiyonu çağrılarak istenen güncelleme veritabanı tablosunda gerçekleştirilir ve kullanıcı güncellenen dökümanın ait olduğu olaya ait tüm dökümanların olduğu sayfaya **'render_template('documents.html', documents=documents)'** fonksiyonu ile yönlendirilir.
			
			
Resimler (Images)
---------------------

Genel Sınıf Tanımları (event.py + store_images.py)
+++++++++++++++++++++++++++
.. code-block:: python

	class Image:
		def __init__(self, event_id, image_id, content, date=None):
			self.event_id = event_id
			self.image_id = image_id
			self.date = date
			self.content = content

Bu sınıf veritabanından çekilen resimler arasında iterasyon yaparken ve verileri html dosyasına gönderirken kullanılır. İçerik (içerik), tarih (date), resim kimliği (image_id) ve olay kimliği (event_id) sınıfın niteliklerini oluşturur. Sınıfın bir nesnesi oluşturulması durumunda (instantiation) kurucu fonksiyon alınan argümanları sınıfın uygun verilerine atar. 

			
.. code-block:: python

	class Store_Image:
		def __init__(self):
			self.images = {}
			self.last_image_id = 0

"Store_Image" sınıfının kurucu (constructor) fonksiyonu yukarıda görüldüğü gibidir. "server.py" 'da sınıfın bir nesnesi oluşturulduğunda kurucu fonksiyon çağrılır ve "images" niteliği boş bir diziye atanırken "last_image_id" niteliğine sıfır olarak ilk değer atanır. 


.. code-block:: python

		def add_image(self, image):
			self.last_image_id = self.get_image_id(image.event_id)
			self.last_image_id += 1
			self.images[self.last_image_id] = image
			image._id = self.last_image_id
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				date = image.date
				event_id = image.event_id
				content = image.content
				image_id = image.image_id
	#            username = current_app.user.username;
	#            query = """INSERT INTO IMAGETABLE (date,event_id,content,image_id,username) VALUES (%s, %s, %s, %s, %s)"""
				query = """INSERT INTO IMAGETABLE (date,event_id,content,image_id) VALUES (%s, %s, %s, %s)"""
			try: 
	#            cursor.execute(query, (date, event_id, content, image_id, username))
				cursor.execute(query, (date, event_id, content, image_id))
				self.last_key = cursor.lastrowid
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()

Veritabanına resim ekleme işlemini gerçekleştiren fonksiyon olan **"add_image"** giriş argümanı olarak resmin bir nesnesini alır. Uygun kimlik değeri ve dizi atamaları yapıldıktan sonra veritabanına bağlanılarak **"INSERT INTO IMAGETABLE (date,event_id,content,image_id) VALUES (%s, %s, %s, %s)"** sorgusu çalıştırılır (execute) ve işlenir (commit). Burada resmin ikili(binary) değeri tablonun "content" içeriğine kaydedilmektedir. Resmin sisteme yüklendiği tarih "date" niteliğine kaydedilir. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.


.. code-block:: python

    def delete_image(self, image_id, event_id):
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM IMAGETABLE WHERE event_id = %s AND image_id = %s"""
        try:
            cursor.execute(query,(event_id,image_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

Veritabanı tablosundan resim silme işlemini gerçekleştiren fonksiyon "delete_image" yukarıda görülmektedir. Veritabanına bağlandıktan sonra **"DELETE FROM IMAGETABLE WHERE event_id = %s AND image_id = %s"** sorgusu çalıştırılarak olay kimliğine (event_id) ve resim kimliğine (image_id) göre istenilen satır tablodan silinir ve sorgular işlenir. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.
	

.. code-block:: python

		def get_image_id(self, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT COUNT(*) FROM IMAGETABLE WHERE event_id = %s;"""
			try:
				cursor.execute(query,(event_id,))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				else:        
					count_image = fetched_data[0]
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()
			return count_image

"Store_Image" sınıfının bir fonksiyonu olan "get_image_id" bir olay için eklenmiş olan resimlerin toplam sayısını döndürmek için kullanılır. Bu sayede yeni eklenecek olan resmin kimlik değeri (document_id) tespit edilir. Veritabanına bağlandıktan sonra **" SELECT COUNT(*) FROM IMAGETABLE WHERE event_id= %s;"** sorgusu "try" bloğu içerisinde çalıştırılır ve toplam sayı **cursor.fetchone()** yardımcı fonksiyonu ile bir değişkene atanır. Değişkenin değerinin boş olup olmadığı kontrol edilir ve sorgu işlendikten (commit) sonra toplam sayı döndürülür. Hata durumunda "except" bloğu hatayı yakalar ve konsola hata mesajı yazar.


.. code-block:: python

		def get_image(self, image_id, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT * FROM IMAGETABLE WHERE event_id= %s AND image_id = %s;"""
			try:
				cursor.execute(query,(event_id,image_id,))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				else:        
					event_id = fetched_data[0]
					image_id = fetched_data[1]
					date = fetched_data[2]
					content = fetched_data[3]
					image = Image(event_id, image_id, date, content)
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()
			return image

"Store_Image" sınıfının bir fonksiyonu olan "get_image" olay kimliği (event_id) ve resim kimliği (image_id) ile veritabanında kayıtlı bir resme erişmek amacıyla kullanılmıştır. Veritabanına bağlanıp **" SELECT * FROM IMAGETABLE WHERE event_id= %s AND image_id = %s;"** sorgusunun çalıştırılması ve **cursor.fetchone()** yardımcı fonksiyonu ile verilen bilgilere uygun resmin kayıtlı olup olmadığı kontrol edilir ve kayıtlıysa fonksiyon elde edilen bu satırı **"Image"** sınıfından bir nesneye dönüştürerek fonksiyondan geri döndürülür ve bağlantı kapanır.

.. code-block:: python

		def get_images(self, event_id):
			dsn = get_connection_for_events();
			with dbapi2.connect(dsn) as connection:
				cursor = connection.cursor()
				query = """ SELECT * FROM IMAGETABLE where event_id =%s ORDER BY image_id;"""
			try:
				cursor.execute(query,(event_id,))
				fetched_data = cursor.fetchone()
				if fetched_data is None:
					status = 'There is no event '
					connection.close()
					return None
				event_id = fetched_data[0]
				image_id = fetched_data[1]
				date = fetched_data[2]
				content = fetched_data[3]
				image_row = [(Image(event_id, image_id, content, date))]
				images = image_row
				for event_id, image_id, date, content in cursor: 
					image_row = [(Image(event_id, image_id, content, date))]
					images += image_row
				connection.commit()
			except connection.Error as error:
				print(error)
			connection.close()
			return images
			
"Store_Image" sınıfının bir fonksiyonu olan "get_images" veritabanındaki bir olay için kaydedilmiş olan tüm resimleri döndürür. Benzer şekilde veritabanına bağlanarak **" SELECT * FROM IMAGETABLE where event_id =%s ORDER BY image_id;"** sorgusu çalıştırılır ve **cursor.fetchone()** yardımcı fonksiyonu ile olaya ait resim olup olmadığı kontrol edilir. Ardından işaretçinin (cursor) tüm satırları for döngüsü ile alınır ve bu satırlar her bir elemanı "Image" sınıfının bir nesnesi olan dizi halinde fonksiyondan döndürülür.

.. code-block:: python

    def update_image_id(self, image_id, event_id, new_id):
        image = current_app.store_images.get_image(image_id,event_id)
        dsn = get_connection_for_events();
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE IMAGETABLE SET image_id = %s WHERE event_id = %s """
        try:
            cursor.execute(query,(int(new_id), event_id,))
            connection.commit()
        except connection.Error as error:
            print(error)
        connection.close()

"Store_Image" sınıfının bir fonksiyonu olan "update_image_id" veritabanından herhangi bir resim silinmesi durumunda kayıtlı tüm resim kimliklerini (image_id) ardışıl olarak sıralamak amacıyla kullanılan fonksiyondur. Değiştirilmek istenen resmin olay kimliği (event_id) ve resim kimliği (image_id) değerlerini aldıktan sonra **"UPDATE IMAGETABLE SET image_id = %s WHERE event_id = %s "** sorgusunun çalıştırılması ile resim kimliği güncellenir.

Yardımcı Fonksiyonlar (images.py)
+++++++++++++++++++++++++++

.. code-block:: python

  @image.route('/events/images/images_add/add', methods=['GET', 'POST'])
  def add_new_image_page():
      if request.method == 'GET':
          return render_template('add_images.html')    
      else:
          image_file = request.files.get('upload')
          content = image_file.read()
          filetype = image_file.content_type
          encoded = base64.b64encode(content)
          encoded_str=encoded.decode("utf-8")
          output = 'data:' + filetype + ';base64,' + encoded_str
          now = datetime.now()
          date = now.strftime('%x')
          event_id = request.form['country']
          event_id = int(event_id)
          image_id = current_app.store_images.get_image_id(event_id) + 1
          image = Image(content=output, event_id=event_id , image_id = image_id, date=date)
          current_app.store_images.add_image(image)
          images = current_app.store_images.get_images(event_id)
          return render_template('images_all.html',images = images, event_id = event_id)
		
Bu fonksiyon kullanım kılavuzunda bahsedilen yeni resim ekleme sayfasında kullanıcının "submit" butonuna basması durumunda resmin yerel diskten alınarak veritabanı tablosuna kaydedilmesi işleminde kullanılmıştır. **"request.files.get('upload')"** yardımcı fonksiyonu ile kullanıcıdan alınan resim "image_file" değişkenine atanır. **image_file.read()** yardımcı fonksiyonu ile resmin içeriği bir "content" değişkenine atanır. **image_file.content_type** yardımcı fonksiyonu ile dosya tipi elde edilerek "filetype" değişkenine atanır. **"encoded = base64.b64encode(content)"** ve "**encoded_str=encoded.decode("utf-8")**" yardımcı fonksiyonları ile önce string olan resmin içeriği kodlanır daha sonra ise **"utf-8"** formatına çözümlenerek veritabanına kaydedilecek formata dönüştürülmüş olur. **"output = 'data:' + filetype + ';base64,' + encoded_str"** satırı ile resim formatı oluşturulur. **"datetime.now()"** yardımcı fonksiyonu ile resmin yüklendiği tarih otomatik olarak kaydedilir. Aşağıya doğru açılan menüden seçilen resmin kaydedileceği olay **"request.form['']"** yardımcı fonksiyonu ile alınır. Resmin kimliği "**get_image_id()**" yardımcı fonksiyonu kullanılarak belirlenir ve elde edilen tüm değişkenler kullanılarak oluşturulan "Image" sınıfının nesnesi veritabanına "add_image" yardımcı fonksiyonu ile eklenir. Fonksiyon kullanıcıyı olaya ait tüm resimlerin galeri şeklinde sunulduğu sayfaya **render_template()** fonksiyonu ile yönlendirir.

.. code-block:: python

  @image.route('/events/images/delete', methods=['GET', 'POST'])
  def delete_image():
      if request.method == 'POST':
          image_id_list = request.form.getlist('image_id_list')
          event_id = request.form['delete']
          event_id = int(event_id)
          for image_id in image_id_list:
              current_app.store_images.delete_image(int(image_id), int(event_id))
          images=current_app.store_images.get_images(int(event_id))
          count=1
          if images:
              for image in images:
                  if image.image_id != count:
                      current_app.store_images.update_image_id(int(image.image_id), int(event_id),count)
                  count += 1

          images = current_app.store_images.get_images(event_id)
          return render_template('images_all.html', images=images, event_id = event_id)
		
Resim silme durumunda çağrılan fonksiyon yukarıda görülmektedir. **"request.form.getlist('image_id_list')"** ile silinmek istenen tüm resimlerin kimlik değerleri bir diziye atanır ve bu resimler for döngüsü ile "delete_image" fonksiyonunu kullanarak silinir. Silinme sonrasında tüm kimlik değerlerini ardışıl bir şekilde sıralayabilmek amacıyla **update_image_id()** fonksiyonu kullanılmıştır. Son olarak kullanıcı silinen resimlerin olay kimliğine sahip olan resimlerin bulunduğu sayfaya yönlendirilir.

Ana Fonksiyonlar (handlers.py)
---------------------

.. code-block:: python

	@site.route('/')
	def home_page():
		now = datetime.now()
		day = now.strftime('%A')
		return render_template('home.html', day_name=day)

Kullanıcı siteye ilk giriş yaptığında yönlendirildikleri "home" sayfasının işleyici (handler) fonksiyonu yukarıda görülmektedir. Mevcut gün bilgisi **html** dosyasına gönderilerek kullanıcıya sunulur.

.. code-block:: python

	@site.route('/events')
	def events_page():
	#    if session.get('user')!=None:
			 return render_template('events.html')
	#    else:
	#        flash('Please sign in or register for DeepMap')
	#        return render_template('home.html')
	
Kullanıcı "events" butonuna tıkladığında olaylar sayfasının yönlendirilmesi için çağrılan fonksiyon yukarıda görülmektedir. (Yorum satırları kullanıcının giriş yapması ile erişim vermek amacıyla konulmuştur.)

.. code-block:: python

  @site.route('/events/documents_all/<int:event_id>', methods=['GET', 'POST'])
  def documents_all_page(event_id):
      documents_array = current_app.store_documents.get_documents(event_id)
      form = {'inputTitle': '', 'inputDate': '', 'event_number': '', 'comment':''}
      if documents_array != None:
          return render_template('documents.html', event_id=event_id, documents=documents_array, form=form)
      else:
          flash('Please first add a document')
          form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
          events_array = current_app.store.get_events()
          if events_array!=None:
              return render_template('events_list.html', events=events_array, form=form)
          else:
              flash('Please first add an event')
              return render_template('events.html')
			
Kullanıcı dökümanlarını görüntülemek istediği olaya tıkladığında çağrılan fonksiyon yukarıda görülmektedir. İlgili olaya ait dökümanlar bir dizi halinde veritabanından alınır ve boş olup olmadığı kontrol edilir. Eğer boş ise kullanıcının öncelikle bir döküman eklemesi gerektiği uyarısı "**flash('Please first add a document')**" ile verilir. Ardından mevcut olaylar veritabanından sorgulanarak daha önce olay eklenip eklenmediği kontrol edilir. Eğer hiçbir olay girilmemiş ise kullanıcı "**flash('Please first add an event')**" mesajı ile uyarılır, aksi takdirde kayıtlı olaylar olması durumunda kullanıcı olayların liste halinde sıralandığı sayfaya yönlendirilir.

.. code-block:: python

  @site.route('/events/events_list', methods=['GET', 'POST'])
  def documents_page():
      form = {'inputTitle': '', 'inputDate': '', 'inputPlace': '', 'comment':''}
      events_array = current_app.store.get_events()
      if events_array!=None:
          return render_template('events_list.html', events=events_array, form=form)
      else:
          flash('Please first add an event')
          return render_template('events.html')
		
Kullanıcının dökümanlarını görmek istediği olayları seçebileceği olayların listelendiği sayfanın ana fonksiyonudur. Benzer şekilde olay eklenmemiş ise kullanıcı **flash** mesajı ile uyarılır; aksi takdirde kullanıcı olayların listelendiği sayfaya yönlendirilir.

.. code-block:: python

  @site.route('/events/all_events', methods=['GET', 'POST'])
  def all_events_page():
      events_array = current_app.store.get_events()
      if events_array!=None:
          return render_template('all_events.html', events=events_array)
      else:
          flash('Please first add an event')
          return render_template('events.html')
		
Bu fonksiyon olaylar sayfasında kullanıcının "All Events" butonuna tıklaması ile çağrılır. Benzer şekilde olay eklenmemiş ise kullanıcı **flash** mesajı ile uyarılır; aksi takdirde kullanıcı olayların listelendiği sayfaya yönlendirilir.

.. code-block:: python

  @site.route('/events/images')
  def images_page():
      events_array = current_app.store.get_events()
      image_array = None
      if events_array:
          for events in events_array:
              event_id = events.event_id
              image_series = current_app.store_images.get_images(event_id)
              images = [(image_series)]
              if image_series:
                  if(event_id == 1):
                      image_array = images
                  else:
                      if image_array is None:
                          image_array = images
                      else:
                          image_array += images
          return render_template('images_slide.html', images=image_array)
      else:
          flash('Please first add an event')
          return render_template('events.html')
		
Kullanıcıya resimlerin slayt gösterisi olarak "carousel" içerisinde sunulabilmesini sağlayan fonksiyondur. Tüm olaylar veritabanından alındıktan sonra her olayın sahip olduğu resimler bir dizi halinde veritabanından alınır. Bu resim dizilerinin birleştirilmesi ile oluşan her elemanı bir olaya ait resimleri içeren dizi "carousel yapısında kullanmak için "**html** dosyasına gönderilir ve kullanıcı ilgili sayfaya **render_template()** ile yönlendirilir. Herhangi bir olay eklenmemiş ise kullanıcı **flash()** mesajı ile uyarılır.

.. code-block:: python

  @site.route('/events/images/images_add')
  def images_add_page():
      events = current_app.store.get_events()
      return render_template('add_images.html', events=events)
	
Kullanıcıyı resim ekleme sayfasına yönlendiren ana fonksiyon yukarıda görülmektedir. Veritabanından "get_events" fonksiyonu ile alınan mevcut olaylar kullanıcıya resmi eklemek istediği olayı menüden seçebilmesi amacıyla **html** dosyasına gönderilir. 

.. code-block:: python

  @site.route('/events/images_all/<int:event_id>')
  def images_all_page(event_id):
      images = current_app.store_images.get_images(event_id)
      return render_template('images_all.html',images = images, event_id = event_id)
	
Yukarıdaki fonksiyon kullanıcının "Browse Gallery" butonuna tıklaması sonucu çağrılır ve kullanıcıya olaya ait tüm resimleri galeri şeklinde sunar. **"get_images()"** yardımcı fonksiyonu ile alınan tüm resimler **html** dosyasına gönderilir.
