**1.Iniciarlizar os nodes**

init_indy_keys --name <Nome do Node>

Exemplo :
<pre>
init_indy_keys --name Node1
init_indy_keys --name Node2
</pre>
obs.:Cada node usado deve ser inicializado na console de cada instância.


**2.Geração do pool de transações**
generate_indy_pool_transactions --nodes <quantidade-de-nodes> --clients 5 --nodeNum <numero do node> --ips 'endereços IP' --network=<nome-da-rede>

Exemplo para criar dois nodes: 
<pre>
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 1 --ips '192.168.2.8,192.168.2.27' --network=sandbox
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 2 --ips '192.168.2.8,192.168.2.27' --network=sandbox
</pre>

obs.:Cada pool usado deve ser inicializado na console de cada instância.

**3. Iniciar os Nodes**
<pre>
start_indy_node Node1 0.0.0.0 9701 0.0.0.0 9702
start_indy_node Node2 0.0.0.0 9703 0.0.0.0 9704
</pre>

obs.:Cada node usado deve ser iniciado na console de cada instância.


**4. Iniciar o servidor Web**

<pre>
cd von-network
PORT=9000 python3 -m server.server
</pre>
Obs.: Somente na instância que será a usada para rodar o Ledger Browser
