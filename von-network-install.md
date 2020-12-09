Instalar a von-network no Ubuntu 18.04

1)instalar o indy
pip3 install python3-indy

2)Instalar o rockesdb

$ apt-get install build-essential libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev liblz4-dev
$ git clone https://github.com/facebook/rocksdb.git
$ cd rocksdb
$ mkdir build && cd build
$ cmake ..
$ make
$ cd ..
$ export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}${CPLUS_INCLUDE_PATH:+:}`pwd`/include/
$ export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}${LD_LIBRARY_PATH:+:}`pwd`/build/
$ export LIBRARY_PATH=${LIBRARY_PATH}${LIBRARY_PATH:+:}`pwd`/build/

$ apt-get install python-virtualenv python-dev
$ virtualenv pyrocks_test
$ cd pyrocks_test
$ . bin/active
$ pip install python-rocksdb

3)Instalar o indy-plenum
pip3 install indy-plenum

