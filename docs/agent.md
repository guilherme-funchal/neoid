## Start agent

<pre>
--endpoint http://172.17.0.1:8020 
--label Faber.Agent 
--auto-accept-invites 
--auto-accept-requests
--auto-provision
--auto-ping-connection 
--auto-respond-messages 
--inbound-transport http 0.0.0.0 8020 
--outbound-transport http 
--admin 0.0.0.0 8021 
--admin-insecure-mode 
--wallet-type indy 
--wallet-name faber.agent783472 
--wallet-key Faber.Agent783472 
--preserve-exchange-records 
 --multitenant 
--multitenant-admin 
--jwt-secret very_secret_secret 
--genesis-transactions  
--seed <SEED>
--webhook-url http://172.17.0.1:8022/webhooks 
--tails-server-base-url https://ff934cffeb2c.ngrok.io 
</pre>
