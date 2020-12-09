Instalar a von-network no Ubuntu 18.04

1. instalar o indy
<pre>
pip3 install python3-indy
</pre>

1. Instalar o rockesdb
<pre>
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
</pre>

1. Instalar o indy-plenum
<pre>
pip3 install indy-plenum
</pre>

1. Alterar o /usr/local/lib/python3.7/dist-packages/plenum/common/util.py linha 349
remover linha 349 : 
<pre>
loop.call_soon(asyncio.async, callback(*args, **kwargs))
</pre>
Incluir :
<pre>
if hasattr(asyncio, 'ensure_future'):
  ensure_future = asyncio.ensure_future
else:
  ensure_future =  getattr(asyncio, "async")
loop.call_soon(ensure_future, callback(*args, **kwargs))
<pre>
