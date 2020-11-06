1)Install Python 3.7
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
./configure --enable-optimizations --with-ssl
make
make altinstall

2)python3.7 -m pip install --upgrade pip

3)Install VENV
cd aries_community_demo
python3.7 -m venv venv
source venv/bin/activate

4)pip3 install -r requirements.txt 

arquivo requirements.txt
jango>=2.1.6,<3
djangorestframework>=3.9.1,<4
djangorestframework-bulk>=0.2.1,<1
django-cors-headers>=2.4.0,<3
django-filter>=1.1.0
python-dateutil>=2.7.2
#-e git+https://github.com/deschler/django-modeltranslation.git#egg=django-modeltranslation
django-extensions
markdown
aiohttp~=3.3.0
pyyaml
pyqrcode
pypng
pkce
requests
urllib3
pillow
sweetify
django-settings-export
django_token
django-bootstrap-modal-forms
django-widget-tweaks
django-crispy-forms
pyopenssl
git+https://github.com/ianco/aries-cloudagent-python#egg=aries-cloudagent

5)Database Postgres

CREATE DATABASE djangodb;
CREATE USER djangouser WITH PASSWORD 'serpro@01';
ALTER ROLE djangouser SET client_encoding TO 'utf8';
ALTER ROLE djangouser SET default_transaction_isolation TO 'read committed';
ALTER ROLE djangouser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE djangodb TO djangouser;

Settings.py Django

3)DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangodb',
        'USER': 'djangouser',
        'PASSWORD': 'serpro@01',
        'HOST': '192.168.1.7',
        'PORT': '5432',
    }
}

