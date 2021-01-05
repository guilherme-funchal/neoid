# Usando o Curl para teste do ACA-Py versão 0.6.0 Multitenant

## 1. Iniciando o demo para Faber e Alice
<pre>
./run_demo faber --multitenant
./run_demo alice --multitenant
</pre>

## 2. Enviar mensagem entre conexões Faber e Alice : 

<pre>
curl -X POST "http://{{ Endereço IP }}:8031/connections/{{ connection_id }}/send-message" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}" 
-H "Content-Type: application/json" 
-d "{ \"content\": \"Mensagem\"}"
</pre>

**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8031/connections/d199d2d6-c164-46a1-b7bb-6062a2371573/send-message" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8" 
-H "Content-Type: application/json" 
-d "{ \"content\": \"Teste\"}"
</pre>

## 3. Listando credenciais na Wallet

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/credentials" -H "accept: application/json"
</pre>


<pre>
curl -X GET "http://172.17.0.1:8031/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8"
<pre>


## 4. Envio de proposta de credencial
<pre>
curl -X POST "http://{{ Endereço IP }}:{{ Porta }}/issue-credential/records/{{ connection_id }}/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"

</pre>


<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/records/d239b8bf-d275-476a-aaf6-99e508604371/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MDI3YmE4MS1jMjJiLTQ5NDMtYjNkZS0xOGIwOGJjZWU2MzEifQ.s_wqtCRIBj0rS7e7UClxHcG8RUY7-WybqiIQ-loLXq8"
</pre>
