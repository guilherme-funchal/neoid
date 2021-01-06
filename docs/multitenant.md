# Usando o Curl para teste do ACA-Py 

### versão 0.6.0 Multitenant

### Iniciando o demo para Faber e Alice
<pre>
./run_demo faber --multitenant
./run_demo alice --multitenant
</pre>


### Abrindo o Swagger UI 

1. Abrir a URL conforme abaixo :

http://{{ Endereço IP }}:8021/api/doc

2. Efetuar o login clicando no botão abaixo :

![Login1](swegger1.png)

3.Inserir o valor de Token JWT gerado conforme abaixo :

![Login2](swagger1-1.png)

## action-menu

## 1.basicmessage
### 1.1. Enviar mensagem entre conexões Faber e Alice : 
Post /connections/{{ connection_id }}/send-message


**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8031/connections/d199d2d6-c164-46a1-b7bb-6062a2371573/send-message" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8" 
-H "Content-Type: application/json" 
-d "{ \"content\": \"Teste\"}"
</pre>

## 2.Connection

## 3.Credential definition

### 3.1 Envia uma definição de credencial para o razão
Post /credential-definitions


**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/credential-definitions" 
-H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA" 
-H "Content-Type: application/json" 
-d "{ \"revocation_registry_size\": 1000, \"schema_id\": \"WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0\", \"support_revocation\": false, \"tag\": \"default\"}"
</pre>

### 3.2 Pesquise por definições de credenciais correspondentes que o agente originou
Post /credential-definitions/created

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/credential-definitions/created" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA"
</pre>

### 3.3  Obtém uma definição de credencial do razão
Get /credential-definitions/{{ credential_definition_id }}


**Exemplo :**

<pre>
curl -X GET "http://172.17.0.1:8021/credential-definitions/M786j533KXeifEnGd3gQLx%3A3%3ACL%3A94%3AFaber.initial.degree_schema" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA"
</pre>

## 4.Credential

### 4.1 Obter tipos de atributos MIME da carteira

Get /credential/mime-types/{{ credential_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/credential/mime-types/5111d8d2-7314-4a55-a081-dd313108a419" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA"
</pre>


### 4.2 Consultar status de revogação de credencial por id

Get /credential/revoked/

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credential/revoked/c3706d85-91b9-4969-95a2-4125fc9750c7" 
-H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJjYjZkOTc3Yy00NmY5LTQxNmYtYjRmYi1lYjdiMDUzYTA5ZDMifQ.2EGp1lZkzenZRMRCsMh1CzYBwtqiIdh1yPULA89pNEk"
</pre>

### 4.3 Obter uma credencial da carteira por id

Get /credential/{{ Token }}

**Exemplo :**
<pre>
</pre>


### 4.4 Remova uma credencial da carteira por id

Get /credential/{{ Token }}

**Exemplo :**
<pre>
</pre>

### 4.5 Obter credenciais da carteira

Get /credential/mime-types/{{ connection_id }}

**Exemplo :**
<pre>
</pre>

## 5.Did exchange

## 6.Introduction

## 7.Issue credential
### 7.1. Envio de proposta de credencial
Post /issue-credential/records/{{ connection_id }}/send-offer

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/records/d239b8bf-d275-476a-aaf6-99e508604371/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MDI3YmE4MS1jMjJiLTQ5NDMtYjNkZS0xOGIwOGJjZWU2MzEifQ.s_wqtCRIBj0rS7e7UClxHcG8RUY7-WybqiIQ-loLXq8"
</pre>


## 8.Ledger

## 9.Multitenancy

## 10.Out of band

## 11.Proof presentation

## 12.Revocation

## 13.Schema

## 14.Server

### 14.1 Query supported features
Get /features
<pre>
curl -X GET "http://172.17.0.1:8021/features" -H "accept: application/json"
</pre>

**Resposta : **

<pre>
{
  "results": {
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/discover-features/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0": {},
    "https://didcomm.org/action-menu/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/out-of-band/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0": {},
    "https://didcomm.org/present-proof/1.0": {},
    "https://didcomm.org/introduction-service/0.1": {},
    "https://didcomm.org/routing/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0": {},
    "https://didcomm.org/coordinate-mediation/1.0": {},
    "https://didcomm.org/basicmessage/1.0": {},
    "https://didcomm.org/discover-features/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/trust_ping/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0": {},
    "https://didcomm.org/didexchange/1.0": {},
    "https://didcomm.org/out-of-band/1.0": {},
    "https://didcomm.org/connections/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/introduction-service/0.1": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0": {},
    "https://didcomm.org/issue-credential/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/action-menu/1.0": {},
    "https://didcomm.org/notification/1.0": {},
    "https://didcomm.org/trust_ping/1.0": {},
    "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/coordinate-mediation/1.0": {}
  }
}

</pre>

### 14.2 Pega a lista de plugins carregados
Get /plugins

<pre>
curl -X GET "http://172.17.0.1:8031/plugins" -H "accept: application/json"
</pre>

**Resposta : **
<pre>
{
  "result": [
    "aries_cloudagent.holder",
    "aries_cloudagent.ledger",
    "aries_cloudagent.messaging.credential_definitions",
    "aries_cloudagent.messaging.schemas",
    "aries_cloudagent.multitenant.admin",
    "aries_cloudagent.protocols.actionmenu",
    "aries_cloudagent.protocols.basicmessage",
    "aries_cloudagent.protocols.connections",
    "aries_cloudagent.protocols.coordinate_mediation",
    "aries_cloudagent.protocols.didexchange",
    "aries_cloudagent.protocols.discovery",
    "aries_cloudagent.protocols.introduction",
    "aries_cloudagent.protocols.issue_credential",
    "aries_cloudagent.protocols.out_of_band",
    "aries_cloudagent.protocols.present_proof",
    "aries_cloudagent.protocols.problem_report",
    "aries_cloudagent.protocols.routing",
    "aries_cloudagent.protocols.trustping",
    "aries_cloudagent.revocation",
    "aries_cloudagent.wallet"
  ]
}
</pre>

### 14.3 Desligar servidor
Get /shutdown

<pre>
curl -X GET "http://172.17.0.1:8031/shutdown" -H "accept: application/json"
</pre>


### 14.4 Obter o status do servidor
Get /status

<pre>
curl -X GET "http://172.17.0.1:8031/status" -H "accept: application/json"
</pre>

**Resposta : **
<pre>
{"version": "0.6.0-pre", 
"label": "Alice.Agent", "
conductor": 
{
"in_sessions": 0,
"out_encode": 0, 
"out_deliver": 0, 
"task_active": 1, 
"task_done": 15, 
"task_failed": 0, 
"task_pending": 0
}}
</pre>

### 14.5 Verificação de vivo
Get /status/live

<pre>
curl -X GET "http://172.17.0.1:8031/status/live" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta : **

<pre>
{"alive": true}
</pre>


### 14.6 Verificação de pronto
Get /status/ready

<pre>
curl -X GET "http://172.17.0.1:8031/status/ready" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta : **

<pre>
{"ready": true}
</pre>

### 14.7 Reset nas estatísticas
Post /status/reset

<pre>
curl -X POST "http://172.17.0.1:8031/status/reset" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
<pre>

## 15.Trustping 

### 15.1 Envie um ping de confiança para uma conexão
Post /connections/{conn_id}/send-ping

<pre>
curl -X POST "http://172.17.0.1:8031/connections/1f412482-9b16-4484-b99c-9c7095104f39/send-ping" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"comment\": \"string\"}" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"

Resposta :

{"thread_id": "31080d88-1937-4af8-82ba-dbfc792d8343"}

</pre>

## 16.Wallet
### 16.1. Listando credenciais na Wallet

Get /credentials

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8"
</pre>

### 16.2. Lista as wallets do Agent

Get /multitenancy/wallets

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


### 16.3. Obtendo apenas uma sub wallet

Get /multitenancy/wallet/{{ wallet_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/multitenancy/wallet/4f4874b1-acb1-4a85-8157-7b0b48372be0" 
-H "accept: application/json"
</pre>

### 16.4. Criando uma sub wallet

Post /multitenancy/wallet

**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"key_management_mode\": \"managed\", \"label\": \"Alice\", \"wallet_key\": \"MySecretKey123\", \"wallet_name\": \"MyNewWallet\", \"wallet_type\": \"indy\"}"
</pre>


## 17.Keylist

### 17.1 Recuperar listas de chaves por conexão ou função

Get /mediation/keylists

<pre>
curl -X GET "http://172.17.0.1:8031/mediation/keylists?role=client" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"

curl -X GET "http://172.17.0.1:8031/mediation/keylists?role=server" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"
</pre>

### 17.2 Envie a consulta da lista de chaves para o mediador
Post /mediation/keylists/{mediation_id}/send-keylist-query

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/mediation/keylists/{mediation_id}/send-keylist-query" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>

### 17.3 atualizar a lista de chaves.
Post /mediation/keylists/{mediation_id}/send-keylist-update

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/mediation/keylists/{mediation_id}/send-keylist-update" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>
