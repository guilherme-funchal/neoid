# Usando o Curl para teste do ACA-Py 

### versão 0.6.0 Multitenant

### Iniciando o demo para Faber e Alice
<pre>
./run_demo faber --multitenant
./run_demo alice --multitenant
</pre>

## action-menu

## 1.basicmessage
### 1.1. Enviar mensagem entre conexões Faber e Alice : 

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

## 2.Connection

## 3.Credentials

## 4.Did exchange

## 5.Introduction

## 6.Issue credential
### 6.1. Envio de proposta de credencial
<pre>
curl -X POST "http://{{ Endereço IP }}:{{ Porta }}/issue-credential/records/{{ connection_id }}/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/records/d239b8bf-d275-476a-aaf6-99e508604371/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MDI3YmE4MS1jMjJiLTQ5NDMtYjNkZS0xOGIwOGJjZWU2MzEifQ.s_wqtCRIBj0rS7e7UClxHcG8RUY7-WybqiIQ-loLXq8"
</pre>


## 7.Ledger

## 8.Multitenancy

## 9.Out of band

## 10.Proof presentation

## 11.Revocation

## 12.Schema

## 13.Server

## 14.Trustping

## 15.Wallet
### 15.1. Listando credenciais na Wallet

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/credentials" -H "accept: application/json"
</pre>

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8"
</pre>

### 15.2. Lista as wallets do Agent
<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/multitenancy/wallets" -H "accept: application/json"
</pre>

**Exemplo :**
<pre>
$ curl -X GET "http://172.17.0.1:8021/multitenancy/wallets" -H "accept: application/json"

{"results": [{
"key_management_mode": "managed", 
"updated_at": "2021-01-05 14:04:45.293416Z", 
"wallet_id": "5027ba81-c22b-4943-b3de-18b08bcee631", 
"settings": {"wallet.type": "indy", 
"wallet.name": "Faber.initial", 
"default_label": "Faber.initial", 
"wallet.id": "5027ba81-c22b-4943-b3de-18b08bcee631"}, 
"created_at": "2021-01-05 14:04:45.293416Z"}]}

$ curl -X GET "http://172.17.0.1:8031/multitenancy/wallets" -H "accept: application/json"

{"results": [{
"created_at": "2021-01-05 14:04:48.541702Z", 
"settings": {
"wallet.type": "indy", 
"wallet.name": "Alice.initial", 
"default_label": "Alice.initial", 
"wallet.id": "4f4874b1-acb1-4a85-8157-7b0b48372be0"}, 
"wallet_id": "4f4874b1-acb1-4a85-8157-7b0b48372be0", 
"key_management_mode": "managed", 
"updated_at": "2021-01-05 14:04:48.541702Z"}]}
</pre>


### 15.3. Obtendo apenas uma sub wallet
<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/multitenancy/wallet/{{ wallet_id }}" -H "accept: application/json"
</pre>

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/multitenancy/wallet/4f4874b1-acb1-4a85-8157-7b0b48372be0" -H "accept: application/json"
</pre>

### 15.4. Criando uma sub wallet
<pre>
curl -X POST "http://{{ Endereço IP }}:{{ Porta }}/multitenancy/wallet" 
-H "accept: application/json" -H "Content-Type: application/json" 
-d "{ \"key_management_mode\": \"managed\", \"label\": \"Label\", \"wallet_key\": \"Senha\", \"wallet_name\": \"Nome\", \"wallet_type\": \"indy\"}"

</pre>

**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"key_management_mode\": \"managed\", \"label\": \"Alice\", \"wallet_key\": \"MySecretKey123\", \"wallet_name\": \"MyNewWallet\", \"wallet_type\": \"indy\"}"
</pre>


## 16.Keylist



