Yükleme Rehberi
==========

Projeyi çalıştırabilmek için aşağıdaki paketler ve programlar yüklenmelidir.

**Python 3.4.3 Yükle**

Python şu adresten indirilebilir : https://www.python.org/downloads/release/python-343/

**PostgreSQL Yükle**

PostgreSQL şu adresten yüklenebilir : http://www.postgresql.org/download/

**Flask Framework Yükle**

Flask şu adresten indirilebilir : http://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz veya "pip" kullanarak yükleyebilirsiniz.

.. code-block:: python
	
	pip install Flask

**Psycopg2 Yükle**

Psycopg2 şu adresten indirilebilir : http://www.stickpeople.com/projects/python/win-psycopg/ veya "pip" kullanarak yükleyebilirsiniz.

.. code-block:: python
	
	pip install psycopg2


Projeyi yerel diskte çalıştırabilmek için yükleme sırasında kullanıcı adı ve şifrenizi istediğiniz gibi seçebilirsiniz. Daha sonra **sqlconnection.py** ve **sql_connection_for_events.py** 'da **'seç'** olan yerleri uygun şekilde doldurmanız gerekmektedir.

.. code-block:: python

	def get_connection_for_events():
		VCAP_SERVICES = os.getenv('VCAP_SERVICES')
		if VCAP_SERVICES is not None:
			dsn = get_sqldb_dsn(VCAP_SERVICES)
		else:
			dsn = """user='seç' password='seç'
								   host='localhost' port=seç dbname='seç'"""
		
		return dsn;
		
	def getConnection():
		VCAP_SERVICES = os.getenv('VCAP_SERVICES')
		if VCAP_SERVICES is not None:
			dsn = get_sqldb_dsn(VCAP_SERVICES)
		else:
		   dsn = """user='seç' password='seç'
								   host='localhost' port=seç dbname='seç'"""
		
		with dbapi2.connect(dsn) as connection:
			return connection;	
	
	def main():
		app = create_app()
		app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTEENBUYUK'

		VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
		if VCAP_APP_PORT is not None:
			port, debug = int(VCAP_APP_PORT), False
		else:
			port, debug = 5000, True



		app.run(host='0.0.0.0', port=port, debug=debug)

	if __name__ == '__main__':
		main()

**Run server.py**

Komut satırında proje klasörünün bulunduğu dizine giderek aşağıdaki komutu çalıştırınız.

.. code-block:: python
	
	python server.py



