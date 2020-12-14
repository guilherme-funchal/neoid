Create Pool transations

von_generate_transactions

PORT=9000 python3 -m server.server

generate_indy_pool_transactions --nodes 4 --clients 0 --ips 127.0.0.1,127.0.0.1,127.0.0.1,127.0.0.1

init_indy_keys --name Node1

init_indy_keys --name Node2

init_indy_keys --name Node3

init_indy_keys --name Node4

von_generate_transactions -n 4

generate_indy_pool_transactions --nodes 4 --clients 0 --nodeNum 4 --ips 127.0.0.1,127.0.0.1,127.0.0.1,127.0.0.1

start_indy_node Node4 0.0.0.0 9707 0.0.0.0 9708


von_generate_transactions -n 3

generate_indy_pool_transactions --nodes 4 --clients 0 --nodeNum 3 --ips 127.0.0.1,127.0.0.1,127.0.0.1,127.0.0.1

start_indy_node Node3 0.0.0.0 9705 0.0.0.0 9706

von_generate_transactions -n 2

generate_indy_pool_transactions --nodes 4 --clients 0 --nodeNum 2 --ips 127.0.0.1,127.0.0.1,127.0.0.1,127.0.0.1

start_indy_node Node2 0.0.0.0 9703 0.0.0.0 9704


von_generate_transactions -n 1

generate_indy_pool_transactions --nodes 4 --clients 0 --nodeNum 1 --ips 127.0.0.1,127.0.0.1,127.0.0.1,127.0.0.1

start_indy_node Node1 0.0.0.0 9701 0.0.0.0 9702



1.Iniciarlizar os nodes

init_indy_keys --name <Nome do Node>

Exemplo :
<pre>
init_indy_keys --name Node1
</pre>
obs.:Cada node usado deve ser inicializado

2.Geração do pool de transações
generate_indy_pool_transactions --nodes <quantidade-de-nodes> --clients 5 --nodeNum <numero do node> --ips 'endereços IP' --network=<nome-da-rede>

Exemplo para criar dois nodes: 
<pre>
generate_indy_pool_transactions --nodes 2 --clients 5 --nodeNum 1 --ips '192.168.2.8,192.168.2.27' --network=sandbox
</pre>

3. Iniciar os Nodes
<pre>
start_indy_node Node1 0.0.0.0 9701 0.0.0.0 9702
start_indy_node Node2 0.0.0.0 9703 0.0.0.0 9704
</pre>
