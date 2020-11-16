
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
</pre>
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6
update-alternatives --config python3
rm /usr/bin/python3
ln -s python3.6 /usr/bin/python3
</pre>

4)Install pacote Indy
<pre>
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88
add-apt-repository "deb https://repo.sovrin.org/deb xenial stable
apt-get install libindy-crypto libindy-crypto-dev python3-indy-crypto indy-plenum indy-node indy-anoncreds
</pre>
Se não funcionar compilar : 
<pre>
wget https://download.libsodium.org/libsodium/releases/libsodium-1.0.18.tar.gz
tar -xf libsodium-1.0.18.tar.gz 
cd libsodium-1.0.18/
./configure
make
make install

git clone https://github.com/hyperledger/indy-sdk.git
cd indy-sdk/libindy/
apt install pkg-config
apt-get install zmq
apt-get install zmq-sys
apt-get install libtool pkg-config build-essential autoconf automake uuid-dev
apt-get libzmq
checkinstall
ldconfig
apt install checkinstall
apt-get install libzmqpp-de libzmq5 libzmq3-dev 
cargo build
cp targget/debug/libindy.so /usr/local/lib/
cp targget/debug/libindy.so /usr/lib/
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





