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







