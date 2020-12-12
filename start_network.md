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


