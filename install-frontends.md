<pre>
1)Install Python3.6
apt-get update
add-apt-repository ppa:deadsnakes/ppa
apt update
apt upgrade

2)Correção PIP
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall

3)Inclusão de Python3 
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6
update-alternatives --config python3
rm /usr/bin/python3
ln -s python3.6 /usr/bin/python3

4)Install pacote Indy
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88
add-apt-repository "deb https://repo.sovrin.org/deb xenial stable
apt-get install libindy-crypto libindy-crypto-dev python3-indy-crypto indy-plenum indy-node indy-anoncreds

Se não funcionar compilar : 
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


5)Modulo Python Indy
pip3 install python3-indy


6)Biblioteca "libindystrgpostgres.so"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
apt install carg python3.6-gdbm
git clone https://github.com/hyperledger/indy-sdk.git
cd indy-sdk/experimental/plugins/postgres_storage
apt-get install -y    build-essential    pkg-config    cmake    libssl-dev    libsqlite3-dev    libzmq3-dev    libncursesw5-dev
cargo build
cp indy-sdk/experimental/plugins/postgres_storage/target/debug/libindystrgpostgres.so /usr/local/lib
<pre>






