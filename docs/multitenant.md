# Usando o Curl para teste do ACA-Py e Hyperledger Indy

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


### 2.1 Consultar conexões de agente para agente
Get /connections

<pre>
curl -X GET "http://172.17.0.1:8031/connections?invitation_key=HZfZf1zx1jEzsqFGS7tX1hf9Jw4MBDBZFtvhPK3UGeve" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resultado :**
<pre>
{"results": [{
"state": "active", 
"invitation_mode": "once", 
"their_label": "Faber.initial", 
"created_at": "2021-01-06 12:57:01.078389Z", 
"their_role": "inviter", 
"connection_id": "ef9743bd-ddda-44ac-854d-671b522bfdc3", 
"request_id": "3dcc517d-3ad6-4d4a-b18b-65f9d81efa16",
"updated_at": "2021-01-06 12:57:01.362119Z", 
"accept": "auto", 
"invitation_key": "HZfZf1zx1jEzsqFGS7tX1hf9Jw4MBDBZFtvhPK3UGeve", 
"routing_state": "none", 
"my_did": "JrDRaYRFiqz75TATYixWMT", 
"their_did": "45uU7QVdZMDMV6gFazwuYN"}]}r
</pre>

### 2.2 Crie um novo convite de conexão

Post /connections/create-invitation

<pre>

</pre>

### 2.3 Crie uma nova conexão estática
Post /connections/create-static

<pre>

</pre>

### 2.4 Receba um novo convite de conexão
Post /connections/receive-invitation

<pre>

</pre>

### 2.5 Buscar um único registro de conexão
Post /connections/{conn_id}

<pre>
curl -X GET "http://172.17.0.1:8031/connections/ef9743bd-ddda-44ac-854d-671b522bfdc3" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resultado :**
<pre>
{"state": "active", 
"invitation_mode": "once", 
"their_label": "Faber.initial", 
"created_at": "2021-01-06 12:57:01.078389Z",
"their_role": "inviter", 
"connection_id": "ef9743bd-ddda-44ac-854d-671b522bfdc3", 
"request_id": "3dcc517d-3ad6-4d4a-b18b-65f9d81efa16", 
"updated_at": "2021-01-06 12:57:01.362119Z", 
"accept": "auto", 
"invitation_key": "HZfZf1zx1jEzsqFGS7tX1hf9Jw4MBDBZFtvhPK3UGeve", 
"routing_state": "none", 
"my_did": "JrDRaYRFiqz75TATYixWMT", 
"their_did": "45uU7QVdZMDMV6gFazwuYN"}
</pre>

### 2.6 Remover um registro de conexão existente
Delete /connections/{conn_id}

<pre>
curl -X DELETE "http://172.17.0.1:8031/connections/ef9743bd-ddda-44ac-854d-671b522bfdc3" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

### 2.7 Aceite um convite de conexão armazenado
Post /connections/{conn_id}/accept-invitation

<pre>

</pre>

### 2.8 Aceite uma solicitação de conexão armazenada
Post /connections/{conn_id}/accept-request

<pre>

</pre>

### 2.9 Atribuir outra conexão como a conexão de entrada

<pre>

</pre>

### 2.10 Buscar metadados da conexão

<pre>

</pre>

### 2.11 Definir metadados da conexão

<pre>

</pre>

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
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJjYjZkOTc3Yy00NmY5LTQxNmYtYjRmYi1lYjdiMDUzYTA5ZDMifQ.2EGp1lZkzenZRMRCsMh1CzYBwtqiIdh1yPULA89pNEk"
</pre>

### 4.3 Obter uma credencial da carteira por id

Get /credential/{{ credential_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credential/b4c8e92e-ec58-4446-8765-ea6c9e077fb3" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resultado :**
<pre>
{"referent": "b4c8e92e-ec58-4446-8765-ea6c9e077fb3", 
"attrs": {"age": "24", "date": "2018-05-28", "degree": "Maths", "timestamp": "1609939047", "name": "Alice Smith"}, 
"schema_id": "2Y4xCxUYA35FEMSC5ofGTh:2:degree schema:67.95.15", 
"cred_def_id": "2Y4xCxUYA35FEMSC5ofGTh:3:CL:106:Faber.initial.degree_schema", 
"rev_reg_id": null, "cred_rev_id": null}r
</pre>


### 4.4 Remova uma credencial da carteira por id

Get /credential/{{ credential_id }}

**Exemplo :**
<pre>
curl -X DELETE "http://172.17.0.1:8031/credential/b4c8e92e-ec58-4446-8765-ea6c9e077fb3" 
-H "accept: application/json"
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

### 4.5 Obter credenciais da carteira

Get /credential/mime-types/{{ connection_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credentials" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resultado :**
<pre>
{"results": [{
"referent": "01eacf8b-797d-4b1c-9fb6-21ee03cab9fc", 
"attrs": {"age": "24", "date": "2018-05-28",
"name": "Alice Smith", 
"timestamp": "1609940569", 
"degree": "Maths"}, 
"schema_id": "2Y4xCxUYA35FEMSC5ofGTh:2:degree schema:67.95.15", 
"cred_def_id": "2Y4xCxUYA35FEMSC5ofGTh:3:CL:106:Faber.initial.degree_schema", 
"rev_reg_id": null, 
"cred_rev_id": null}]}
</pre>

## 5.Did exchange

### 5.1 Receba um novo convite de conexão
Post /didexchange/receive-invitation

**Exemplo :**
<pre>

</pre>

### 5.2 Aceite um convite de conexão armazenado
Post /didexchange/{conn_id}/accept-invitation

**Exemplo :**
<pre>

</pre>

### 5.3 Aceite uma solicitação de conexão armazenada
Post /didexchange/{conn_id}/accept-request

**Exemplo :**
<pre>

</pre>

## 6.Introduction

## 7.Issue credential
### 7.1. Envie ao titular uma credencial, automatizando todo o fluxo
Post /issue-credential/create

**Exemplo :**
<pre>


</pre>

### 7.2. Obter todos os registros de troca de credenciais
Get /issue-credential/records

**Exemplo :**
<pre>


</pre>

### 7.3. Buscar um único registro de troca de credencial
Get /issue-credential/records/{cred_ex_id}

**Exemplo :**
<pre>


</pre>

### 7.4. Remover um registro de troca de credencial existente
Delete /issue-credential/records/{cred_ex_id}

**Exemplo :**
<pre>


</pre>

### 7.5. Enviar uma credencial ao titular
Post /issue-credential/records/{cred_ex_id}/issue

**Exemplo :**
<pre>


</pre>

### 7.6. Envie um relatório de problema para troca de credencial
Post /issue-credential/records/{cred_ex_id}/problem-report

**Exemplo :**
<pre>


</pre>

### 7.7. Enviar ao titular uma oferta de credencial em referência a uma proposta com visualização
Post /issue-credential/records/{cred_ex_id}/send-offer

**Exemplo :**
<pre>


</pre>

### 7.8. Enviar ao emissor um pedido de credencial
Post /issue-credential/records/{cred_ex_id}/send-request

**Exemplo :**
<pre>


</pre>

### 7.9. Armazene uma credencial recebida
Post ​/issue-credential​/records​/{cred_ex_id}​/store

**Exemplo :**
<pre>


</pre>

### 7.10. Envie ao titular uma credencial, automatizando todo o fluxo
Post /issue-credential/send

**Exemplo :**
<pre>


</pre>

### 7.11. Envio de proposta de credencial
Post /issue-credential/records/{{ connection_id }}/send-offer

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/records/d239b8bf-d275-476a-aaf6-99e508604371/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MDI3YmE4MS1jMjJiLTQ5NDMtYjNkZS0xOGIwOGJjZWU2MzEifQ.s_wqtCRIBj0rS7e7UClxHcG8RUY7-WybqiIQ-loLXq8"
</pre>

### 7.12. Envie ao emissor uma proposta de credencial
Post /issue-credential/send-proposal

**Exemplo :**
<pre>


</pre>


## 8.Ledger

### 8.1. Obtenha o ponto de extremidade para um DID do razão
Get /ledger/did-endpoint

**Exemplo :**
<pre>


</pre>

### 8.2. Obtenha o verkey para um DID do razão
Get /ledger/did-verkey

**Exemplo :**
<pre>


</pre>

### 8.3. Obtenha a função do registro do NYM de um DID público
Get /ledger/get-nym-role

**Exemplo :**
<pre>


</pre>

### 8.4. Envie um registro NYM para o razão.
Post /ledger/register-nym

**Exemplo :**
<pre>


</pre>

### 8.5. Gire o par de chaves para DID público.
Patch /ledger/rotate-public-did-keypair

**Exemplo :**
<pre>


</pre>

### 8.6. Busque o acordo do autor da transação atual, se houver
Get /ledger/taa

**Exemplo :**
<pre>


</pre>

### 8.7. Aceite o contrato do autor da transação
Post /ledger/taa/accept

**Exemplo :**
<pre>


</pre>

## 9.mediation

### 9.1. Solicitar mediação da conexão
Post /mediation/request/{conn_id}

**Exemplo :**
<pre>


</pre>

### 9.2. Solicitações de mediação de consulta, lista de retorno de todos os registros de mediação
Get /mediation/requests

**Exemplo :**
<pre>


</pre>

### 9.3. Recuperar registro de solicitação de mediação
Get /mediation/requests/{mediation_id}

**Exemplo :**
<pre>


</pre>


### 9.4. Excluir solicitação de mediação por ID
Delete /mediation/requests/{mediation_id}

**Exemplo :**
<pre>


</pre>

### 9.5. Negar um pedido de mediação armazenado
Post /mediation/requests/{mediation_id}/deny

**Exemplo :**
<pre>


</pre>

### 9.6. Conceder mediação recebida
Post /mediation/requests/{mediation_id}/grant

**Exemplo :**
<pre>


</pre>

## 10.Multitenancy

### 10.1. Criar wallet
Post /multitenancy/wallet

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"key_management_mode\": \"managed\", \"label\": \"Alice\", \"wallet_key\": \"MySecretKey123\", \"wallet_name\": \"MyNewWallet\", \"wallet_type\": \"indy\"}"
</pre>

**Resposta :**
<pre>
{"key_management_mode": "managed", "wallet_id": "729ecda2-3229-48e3-ac12-7ce7e82e433a", "settings": {"wallet.type": "indy", "wallet.name": "MyNewWallet1", "default_label": "Alice", "wallet.id": "729ecda2-3229-48e3-ac12-7ce7e82e433a"}, "created_at": "2021-01-06 17:58:49.231591Z", "updated_at": "2021-01-06 17:58:49.231591Z", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI3MjllY2RhMi0zMjI5LTQ4ZTMtYWMxMi03Y2U3ZTgyZTQzM2EifQ.kNhkvUGVPcEEp8y4Ulg0YY-pUPmadrbMThi7EnPbWoc"}
</pre>

### 10.2. Obtenha uma única subwallet
Get /multitenancy/wallet/{wallet_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/multitenancy/wallet/729ecda2-3229-48e3-ac12-7ce7e82e433a" -H "accept: application/json"
</pre>

**Resposta :**
<pre>
{"key_management_mode": "managed", "wallet_id": "729ecda2-3229-48e3-ac12-7ce7e82e433a", "settings": {"wallet.type": "indy", "wallet.name": "MyNewWallet1", "default_label": "Alice", "wallet.id": "729ecda2-3229-48e3-ac12-7ce7e82e433a"}, "created_at": "2021-01-06 17:58:49.231591Z", "updated_at": "2021-01-06 17:58:49.231591Z"}
</pre>

### 10.3. Remove uma sub wallet
Post /multitenancy​/wallet​/{wallet_id}​/remove

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet/729ecda2-3229-48e3-ac12-7ce7e82e433a/remove" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"wallet_key\": \"MySecretKey123\"}"
</pre>

### 10.4. Obtenha o token de autenticação para um subwallet
Post /multitenancy/wallet/{wallet_id}/token

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet/60fd663c-e246-4dd2-97ca-a3e22ef2385e/token" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"wallet_key\": \"MySecretKey123\"}"
</pre>

**Resposta :**
<pre>
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI2MGZkNjYzYy1lMjQ2LTRkZDItOTdjYS1hM2UyMmVmMjM4NWUifQ.VysFhjz9CfhcjQNH2qxNDU3ifbBTr0--dFgJbBmblTg"}
</pre>

### 10.5. List all subwallets
Get /multitenancy/wallets

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/multitenancy/wallets" -H "accept: application/json"
</pre>

**Resposta :**
<pre>
{
  "results": [
    {
      "key_management_mode": "managed",
      "wallet_id": "98d96530-e27b-4540-b7a1-cb66748e12d7",
      "settings": {
        "wallet.type": "indy",
        "wallet.name": "MyNewWallet",
        "default_label": "Alice",
        "wallet.id": "98d96530-e27b-4540-b7a1-cb66748e12d7"
      },
      "created_at": "2021-01-06 17:57:57.811745Z",
      "updated_at": "2021-01-06 17:57:57.811745Z"
    }
  ]
}
</pre>

## 11.Out of band

### 11.1 Crie um novo convite de conexão
Post /out-of-band/create-invitation

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/out-of-band/create-invitation" -H "accept: application/json" -H "Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE" 
-H "Content-Type: application/json" 
-d "{ \"attachments\": [ { \"id\": \"string\", \"type\": \"string\" } ], \"include_handshake\": true, \"metadata\": {}, \"use_public_did\": true}"
</pre>

### 11.2 receba um novo convite de conexão
Post /out-of-band/receive-invitation

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/out-of-band/receive-invitation" -H "accept: application/json" -H "Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE" 
-H "Content-Type: application/json" 
-d "{ \"attachments\": [ { \"id\": \"string\", \"type\": \"string\" } ], \"include_handshake\": true, \"metadata\": {}, \"use_public_did\": true}"
</pre>

## 12.Proof presentation

## 13.Revocation

## 14.Schema

### 14.1 Envia um esquema para o razão
Post /schemas

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/schemas" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE" -H "Content-Type: application/json" -d "{ \"attributes\": [ \"score\" ], \"schema_name\": \"prefs\", \"schema_version\": \"1.0\"}"
</pre>

### 14.2 Pesquise o esquema correspondente que o agente originou

Get /schemas/created

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/schemas/created?schema_id=2Y4xCxUYA35FEMSC5ofGTh%3A2%3Adegree%20schema%3A67.95.15" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

### 14.3 Obtém um esquema do livro-razão
Get /schemas/{schema_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/schemas/2Y4xCxUYA35FEMSC5ofGTh%3A2%3Adegree%20schema%3A67.95.15" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta :**

<pre>
{"schema": 
{"ver": "1.0", 
"id": "2Y4xCxUYA35FEMSC5ofGTh:2:degree schema:67.95.15", 
"name": "degree schema", 
"version": "67.95.15", 
"attrNames": ["age", "timestamp", "date", "degree", "name"], "seqNo": 106}
}
</pre>

## 15.Server

### 15.1 Query supported features
Get /features

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/features" -H "accept: application/json"
</pre>

**Resposta :**

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

### 15.2 Pega a lista de plugins carregados
Get /plugins

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/plugins" -H "accept: application/json"
</pre>

**Resposta :**
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

### 15.3 Desligar servidor
Get /shutdown

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/shutdown" -H "accept: application/json"
</pre>


### 15.4 Obter o status do servidor
Get /status

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/status" -H "accept: application/json"
</pre>

**Resposta :**
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

### 15.5 Verificação de vivo
Get /status/live

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/status/live" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta :**

<pre>
{"alive": true}
</pre>


### 15.6 Verificação de pronto
Get /status/ready

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/status/ready" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta :**

<pre>
{"ready": true}
</pre>

### 15.7 Reset nas estatísticas
Post /status/reset

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/status/reset" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

## 16.Trustping 

### 16.1 Envie um ping de confiança para uma conexão
Post /connections/{conn_id}/send-ping

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/connections/1f412482-9b16-4484-b99c-9c7095104f39/send-ping" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"comment\": \"string\"}" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"

Resposta :

{"thread_id": "31080d88-1937-4af8-82ba-dbfc792d8343"}

</pre>

## 17.Wallet
### 17.1. Listando credenciais na Wallet

Get /credentials

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8"
</pre>

### 17.2. Lista as wallets do Agent

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


### 17.3. Obtendo apenas uma sub wallet

Get /multitenancy/wallet/{{ wallet_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/multitenancy/wallet/4f4874b1-acb1-4a85-8157-7b0b48372be0" 
-H "accept: application/json"
</pre>

### 17.4. Criando uma sub wallet

Post /multitenancy/wallet

**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"key_management_mode\": \"managed\", \"label\": \"Alice\", \"wallet_key\": \"MySecretKey123\", \"wallet_name\": \"MyNewWallet\", \"wallet_type\": \"indy\"}"
</pre>


## 18.Keylist

### 18.1 Recuperar listas de chaves por conexão ou função

Get /mediation/keylists

<pre>
curl -X GET "http://172.17.0.1:8031/mediation/keylists?role=client" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"

curl -X GET "http://172.17.0.1:8031/mediation/keylists?role=server" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"
</pre>

### 18.2 Envie a consulta da lista de chaves para o mediador
Post /mediation/keylists/{mediation_id}/send-keylist-query

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/mediation/keylists/{mediation_id}/send-keylist-query" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>

### 18.3 atualizar a lista de chaves.
Post /mediation/keylists/{mediation_id}/send-keylist-update

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/mediation/keylists/{mediation_id}/send-keylist-update" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>
