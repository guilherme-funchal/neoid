# Instalar a von-network no Ubuntu 18.04

1. instalar o indy
<pre>
pip3 install python3-indy
pip3 install indy-plenum
pip3 install indy_node
</pre>

2. Instalar o rockesdb
<pre>
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
sudo add-apt-repository "deb https://repo.sovrin.org/deb xenial master"

sudo apt-get update
sudo apt-get install libbz2-dev \
    zlib1g-dev \
    liblz4-dev \
    libsnappy-dev \
    rocksdb \
    liblz4-dev

</pre>

3.Incluir o script start_node no /usr/bin

<pre>
#!/usr/bin/python3.7

import sys


from indy_node.utils.node_runner import run_node
from indy_common.config_util import getConfig


if __name__ == "__main__":
    if len(sys.argv) < 6:
        raise Exception("Provide name and two pairs of IP/port for running the node "
                        "and client stacks in form 'node_name node_ip node_port client_ip client_port'")

    config = getConfig()
    self_name = sys.argv[1]
    run_node(config, self_name,
             node_ip=sys.argv[2], node_port=int(sys.argv[3]),
             client_ip=sys.argv[4], client_port=int(sys.argv[5]))

</pre>

4.Incluir o script von_generate_transactions  no /usr/bin

5. Inclusão de arquivos aml.json e taa.json no diretório "/home/indy/config/"

aml.json
<pre>
{
  "version": "1.0",
  "context": "http://aml-context-descr",
  "aml": {
     "product_eula": "The agreement was included in the software product’s terms and conditions as part of a license to the end user.",
     "service_agreement": "The agreement was included in the terms and conditions the user accepted as part of contracting a service.",
     "at_submission": "The agreement was reviewed by the user and accepted at the time of submission of this transaction.",
     "for_session": "The agreement was reviewed by the user and accepted at some point in the user’s session prior to submission.",
     "wallet_agreement": "The agreement was reviewed by the user and this affirmation was persisted in the user’s wallet for use during submission.",
     "on_file": "An authorized person accepted the agreement, and such acceptance is on file with the user’s organization."
  }
}
</pre>

taa.json
<pre>
{
  "version": "1.1",
  "text": "TAA Goes *Here*\n\n- got it",
  "ratification_ts": 1597654073
}
</pre>

6. Compilar o lib-crypto
<pre>
git clone https://github.com/hyperledger/indy-crypto.git
cd ./indy-crypto/libindy-crypto
git checkout -b v0.4.5
cd libindy-crypto
cargo build
cd target/debug 
cp libindy_crypto.so /usr/local/lib/

cd ..
</pre>

7.Incluir o diretório "/home/indy/ledger/sandbox/"

8.Incluir o arquivo de configuração /etc/indy/indy_config.py 
