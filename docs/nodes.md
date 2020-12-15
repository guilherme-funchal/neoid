# 1.Instalação Indy Nodes no Ubuntu 18.04

**1.1 instalar o indy**
<pre>
mkdir -p /home/indy
mkdir -p /home/indy/ledger/sandbox
mkdir -p /home/indy/config/
mkdir -p /etc/indy/
cd /home/indy
git clone https://github.com/bcgov/von-network.git
apt install python3-pip

</pre>

**1.2 Instalar o rockesdb**
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

**1.3 Instalar os pacotes do Indy**
pip3 install python3-indy
pip3 install indy-plenum
pip3 install indy_node

**Obs.:Importante observar que o comando pip aponte para pip3, se não houver basta criar um link simbólico.**

**1.4 Incluir o script start_node no /usr/bin**
<pre>
cp /home/indy/von-network/scripts/start_node /usr/bin
</pre>

**1.5 Incluir o script von_generate_transactions  no /usr/bin**
<pre>
cp /home/indy/von-network/bin/von_generate_transactions /usr/bin
</pre>

**1.6 Inclusão de arquivos aml.json e taa.json no diretório "/home/indy/config/"**

aml.json
<pre>
cp /home/indy/von-network/config/sample_aml.json /home/indy/config/aml.json
</pre>

taa.json
<pre>
cp /home/indy/von-network/config/sample_taa.json /home/indy/config/taa.json
</pre>

**1.7 Instalar o lib-crypto**
<pre>
apt-get install libindy_crypto
cp /usr/lib/libindy_crypto.so /usr/local/lib/
</pre>


**1.8 Incluir o arquivo de configuração /etc/indy/indy_config.py**

<pre>
NETWORK_NAME = 'sandbox'
LEDGER_DIR = '/home/indy/ledger'
LOG_DIR = '/home/indy/log'
KEYS_DIR = LEDGER_DIR
GENESIS_DIR = LEDGER_DIR
BACKUP_DIR = '/home/indy/backup'
PLUGINS_DIR = '/home/indy/plugins'
NODE_INFO_DIR = LEDGER_DIR
CLI_BASE_DIR = '/home/indy/.indy-cli/'
CLI_NETWORK_DIR = '/home/indy/.indy-cli/networks'i
</pre>

**1.9 Incluir o arquivo de configuração /etc/indy/indy.env**

<pre>
NODE_NAME=Nome-do-node
NODE_IP=0.0.0.0
NODE_PORT=porta
NODE_CLIENT_IP=0.0.0.0
NODE_CLIENT_PORT=porta
CLIENT_CONNECTIONS_LIMIT=500
</pre>

**1.10 Instalar o webservice para a rede**
<pre>
cd /home/indy
git clone https://github.com/bcgov/von-network.git
</pre>

# 2.Iniciar os nodes

**2.1 Iniciarlizar os nodes**

init_indy_keys --name <Nome do Node>

Exemplo :
<pre>
init_indy_keys --name Node1
init_indy_keys --name Node2
init_indy_keys --name Node3
init_indy_keys --name Node4
</pre>
obs.:Cada node usado deve ser inicializado na console de cada instância.


**2.2 Geração do pool de transações**
generate_indy_pool_transactions --nodes <quantidade-de-nodes> --clients 5 --nodeNum <numero do node> --ips 'endereços IP' --network=<nome-da-rede>

Exemplo para criar dois nodes: 
<pre>
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 1 --ips '192.168.2.2,192.168.2.3,192.168.2.4.192.168.2.3' --network=sandbox
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 2 --ips '192.168.2.2,192.168.2.3,192.168.2.4.192.168.2.3' --network=sandbox
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 3 --ips '192.168.2.2,192.168.2.3,192.168.2.4.192.168.2.3' --network=sandbox
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 4 --ips '192.168.2.2,192.168.2.3,192.168.2.4.192.168.2.3' --network=sandbox
</pre>

obs.:Cada pool usado deve ser inicializado na console de cada instância.

**2.3 Iniciar os Nodes**
<pre>
start_indy_node Node1 0.0.0.0 9701 0.0.0.0 9702
start_indy_node Node2 0.0.0.0 9703 0.0.0.0 9704
start_indy_node Node3 0.0.0.0 9705 0.0.0.0 9706
start_indy_node Node4 0.0.0.0 9707 0.0.0.0 9708
</pre>

obs.:Cada node usado deve ser iniciado na console de cada instância.


**2.4 Iniciar o servidor Web**

<pre>
cd /home/indy/von-network
PORT=9000 python3 -m server.server
</pre>
Obs.: Somente na instância que será a usada para rodar o Ledger Browser

**2.5 Abrir o site do ledger Browser**

Abrir o browser no endereço http://endereço-ip:9000 e o browser irá abrir a página :


![Ledger-browser](ledger.png)
