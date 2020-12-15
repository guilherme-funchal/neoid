1)Install Python3.6
<pre>
apt-get update
add-apt-repository ppa:deadsnakes/ppa
apt update
apt upgrade
</pre>

2)Correção PIP
<pre>
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
</pre>

3)Inclusão de Python3 
<pre>
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6
update-alternatives --config python3
rm /usr/bin/python3
ln -s python3.6 /usr/bin/python3
</pre>

4)Install pacote Indy
<pre>
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88
add-apt-repository "deb https://repo.sovrin.org/deb xenial stable"
apt-get install libindy-crypto libindy-crypto-dev python3-indy-crypto indy-plenum indy-node indy-anoncreds
</pre>

Se não funcionar compilar : 
<pre>
apt-get install gcc
wget https://download.libsodium.org/libsodium/releases/libsodium-1.0.18.tar.gz
tar -xf libsodium-1.0.18.tar.gz 
cd libsodium-1.0.18/
./configure
make
make install

git clone https://github.com/hyperledger/indy-sdk.git
cd indy-sdk/libindy/
apt get cmake
apt-get install libzmqpp-dev libzmq5 libzmq3-dev libtool pkg-config build-essential autoconf automake uuid-dev zmq-sys zmq checkinstall libzmq
checkinstall
ldconfig

cargo build
cp targget/debug/libindy.so /usr/local/lib/
</pre>

5)Modulo Python Indy
<pre>
pip3 install python3-indy
</pre>

6)Instalar Rust
<pre>
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
</pre>

7)Biblioteca "libindystrgpostgres.so"
<pre>
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
apt install carg python3.6-gdbm
git clone https://github.com/hyperledger/indy-sdk.git
cd indy-sdk/experimental/plugins/postgres_storage
apt-get install -y    build-essential    pkg-config    cmake    libssl-dev    libsqlite3-dev    libzmq3-dev    libncursesw5-dev
cargo build
cp indy-sdk/experimental/plugins/postgres_storage/target/debug/libindystrgpostgres.so /usr/local/lib/python3.6/dist-packages/
</pre>

8)Instalação de pacotes do Python
<pre>
pip install -r requiriments.txt
</pre>
requeriments.txt 
<pre>

django>=2.1.6,<3
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
pyOpenSSL
pkce
psycopg2-binary
requests
pillow
sweetify
python-oauth2
requests_oauthlib
django-settings-export
aries-cloudagent==0.5.3
git+https://github.com/ianco/aries-cloudagent-python#egg=aries-cloudagent
</pre>

9)Criação das bases de dados no Postgres
su - postgres
CREATE DATABASE banco-de-dados-django;
CREATE DATABASE banco-de-dados-wallets;
GRANT ALL PRIVILEGES ON DATABASE banco-de-dados-django TO usuario;
GRANT ALL PRIVILEGES ON DATABASE banco-de-dados-wallets TO usuario;

10)Ajuste das configurações do Django  no arquivo aries_community_demo/aries_community_demo/settings.py

10.1)Servidor de Blockchain e configurações de Wallet
<pre>
ARIES_CONFIG = {
    'storage_config': {'url': 'Ip ou nome:5432'},
    'storage_credentials': {'account': 'usuario', 'password': 'senha', 'admin_account': 'usuario', 'admin_password': 'senha'},
    'register_dids': True,
    'ledger_url': 'http://IP-ou-NOME:9000',
    'genesis_url': 'http://IP-ou-NOME:9000/genesis',
    'default_enterprise_seed': '000000000000o_anon_solutions_inc',
    'default_institution_seed': '00000000000000000000000000000000',
    'managed_agent_host': 'localhost',
    'webhook_host': 'localhost',
    'webhook_port': '8000',
    'webhook_root': '',
    #Path do ACA-PY local
    'aca_py_bin_path': '/usr/local/bin',
}
</pre>

10.2)Configuração de base de uso do Django
<pre>
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nome-do-banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'IP-ou-NOME',
        'PORT': '5432',
        }
}
</pre>


11)Criação da base de dados do Django
<pre>
cd aries_community_demo
./reload_db.sh
</pre>

12)Iniciar o agente trustee
./start_trustee_local.sh

13)Popular a base do Django com os esquemas 
<pre>
cd aries_community_demo
python3 manage.py loads_orgs ./trustee-org-docker.yml
python3 manage.py loads_schemas ./test-schemas.yml 1
python3 manage.py loads_orgs ./test-orgs.yml
</pre>

14)Subir servidor Django
<pre>
python3 manage.py runserver 0.0.0.0:8000
</pre>

15)Servidor Gnunicorn
<pre>
pip3 install gunicorn setproctitle
nohup gunicorn aries_community_demo.wsgi:application --bind 0.0.0.0:8000 &
</pre>

16)Proxypass com Nginx
<pre>
apt-get install nginx
</pre>

16.1)Configurar o site com os seguintes paramentros : 
<pre>
/etc/nginx/sites-enabled/default

server {
   listen 80;
   return 301 https://$host$request_uri;
}

server {

    listen 443;
    server_name proxy;

    ssl_certificate           /etc/nginx/cert.crt;
    ssl_certificate_key       /etc/nginx/cert.key;

    ssl on;
    ssl_session_cache  builtin:1000  shared:SSL:10m;
    ssl_protocols  TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
    ssl_prefer_server_ciphers on;

    access_log            /var/log/nginx/access.log;

    location /static/ {
        alias /var/www/html/static/;
    }



    location / {

      proxy_read_timeout 300s;
      proxy_connect_timeout 75s;
      proxy_send_timeout 300s;
      send_timeout 300s;
      proxy_set_header        Host $host;
      proxy_set_header        X-Real-IP $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header        X-Forwarded-Proto $scheme;

      # Fix the “It appears that your reverse proxy set up is broken" error.
      proxy_pass          http://IP-INTERNO:8000;
      proxy_redirect      http://IP-INTERNO:8000 https://IP-EXTERNO;
    }
  }

</pre>

16.2)Gerar certificado

<pre>
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt
</pre>
