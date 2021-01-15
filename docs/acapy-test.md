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

## 1.action-menu
### 1.1 Fecha o menu ativo associado a uma conexão
Post /action-menu/{conn_id}/close

<pre>
curl -X POST "http://172.17.0.1:8031/action-menu/f1ad2b46-aff5-4043-8a59-5907124e74d9/close" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMjFjZTNmZi0wNWU5LTRhZWQtYWE0ZS1lNzNhNjQ5NjkzNmIifQ.ncetke6si8Dkzr1wo_PPfAJkMJY4FRaeMQOt03Scew4"
</pre>

### 1.2 Busque o menu ativo
Post /action-menu/{conn_id}/fetch

<pre>
curl -X POST "http://172.17.0.1:8031/action-menu/f1ad2b46-aff5-4043-8a59-5907124e74d9/fetch" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMjFjZTNmZi0wNWU5LTRhZWQtYWE0ZS1lNzNhNjQ5NjkzNmIifQ.ncetke6si8Dkzr1wo_PPfAJkMJY4FRaeMQOt03Scew4"
</pre>

### 1.3 Execute uma ação associada ao menu ativo
Post /action-menu/{conn_id}/perform

<pre>
curl -X POST "http://172.17.0.1:8031/action-menu/f1ad2b46-aff5-4043-8a59-5907124e74d9/perform" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMjFjZTNmZi0wNWU5LTRhZWQtYWE0ZS1lNzNhNjQ5NjkzNmIifQ.ncetke6si8Dkzr1wo_PPfAJkMJY4FRaeMQOt03Scew4"
</pre>

### 1.4 Solicite o menu ativo
Post /action-menu/{conn_id}/request

<pre>
curl -X POST "http://172.17.0.1:8031/action-menu/f1ad2b46-aff5-4043-8a59-5907124e74d9/request" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMjFjZTNmZi0wNWU5LTRhZWQtYWE0ZS1lNzNhNjQ5NjkzNmIifQ.ncetke6si8Dkzr1wo_PPfAJkMJY4FRaeMQOt03Scew4"
</pre>

### 1..5 Envie um menu de ação para uma conexão
Post /action-menu/{conn_id}/send-menu 

<pre>
curl -X POST "http://172.17.0.1:8031/action-menu/f1ad2b46-aff5-4043-8a59-5907124e74d9/send-menu" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMjFjZTNmZi0wNWU5LTRhZWQtYWE0ZS1lNzNhNjQ5NjkzNmIifQ.ncetke6si8Dkzr1wo_PPfAJkMJY4FRaeMQOt03Scew4" -H "Content-Type: application/json" -d "{ \"menu\": { \"description\": \"User preferences for window settings\", \"errormsg\": \"Error: item not present\", \"options\": [ { \"description\": \"Window display preferences\", \"disabled\": \"False\", \"form\": { \"description\": \"Window preference settings\", \"params\": [ { \"default\": \"0\", \"description\": \"Delay in seconds before starting\", \"name\": \"delay\", \"required\": \"False\", \"title\": \"Delay in seconds\", \"type\": \"int\" } ], \"submit-label\": \"Send\", \"title\": \"Preferences\" }, \"name\": \"window_prefs\", \"title\": \"Window Preferences\" } ], \"title\": \"My Menu\" }}"
</pre>

## 2.basicmessage
### 2.1. Enviar mensagem entre conexões Faber e Alice : 
Post /connections/{{ connection_id }}/send-message


**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8031/connections/d199d2d6-c164-46a1-b7bb-6062a2371573/send-message" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8" 
-H "Content-Type: application/json" 
-d "{ \"content\": \"Teste\"}"
</pre>

## 3.Connection
### 3.1 Consultar conexões de agente para agente
Get /connections

<pre>
curl -X GET "http://172.17.0.1:8031/connections?invitation_key=HZfZf1zx1jEzsqFGS7tX1hf9Jw4MBDBZFtvhPK3UGeve" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
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

### 3.2 Crie um novo convite de conexão

Post /connections/create-invitation

<pre>
curl -X POST "http://172.17.0.1:8021/connections/create-invitation" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MWY1MzAwYS1hZTNkLTQyNjktOGNjMC05MmU5Njc3OGQzMGYifQ.v38pl0TbiKQc_wTkrID1ljJoXkGS-Wm3f7j82LIaDI0" 
-H "Content-Type: application/json" -d "{ \"metadata\": {}, \"recipient_keys\": [ \"H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV\" ], \"routing_keys\": [ \"H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV\" ], \"service_endpoint\": \"http://172.17.0.1:8020\"}"
</pre>

**Resposta :**
<pre>
{"connection_id": "4ff72769-0192-43d1-b0c4-64984cef0aff", 
"invitation": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation", 
"@id": "23ae0e3e-3654-4111-9064-11e705c604ad", 
"routingKeys": ["H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"], 
"serviceEndpoint": "http://172.17.0.1:8020", 
"label": "Faber.initial", 
"recipientKeys": ["H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"]}, 
"invitation_url": "http://172.17.0.1:8020?c_i=eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9jb25uZWN0aW9ucy8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiMjNhZTBlM2UtMzY1NC00MTExLTkwNjQtMTFlNzA1YzYwNGFkIiwgInJvdXRpbmdLZXlzIjogWyJIM0MyQVZ2TE12NmdtTU5hbTN1VkFqWnBma2NKQ3dEd25abjZ6M3dYbXFQViJdLCAic2VydmljZUVuZHBvaW50IjogImh0dHA6Ly8xNzIuMTcuMC4xOjgwMjAiLCAibGFiZWwiOiAiRmFiZXIuaW5pdGlhbCIsICJyZWNpcGllbnRLZXlzIjogWyJIM0MyQVZ2TE12NmdtTU5hbTN1VkFqWnBma2NKQ3dEd25abjZ6M3dYbXFQViJdfQ=="}
</pre>


### 3.3 Crie uma nova conexão estática
Post /connections/create-static

<pre>
curl -X POST "http://172.17.0.1:8021/connections/create-static" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MWY1MzAwYS1hZTNkLTQyNjktOGNjMC05MmU5Njc3OGQzMGYifQ.v38pl0TbiKQc_wTkrID1ljJoXkGS-Wm3f7j82LIaDI0" 
-H "Content-Type: application/json" -d "{ \"alias\": \"alice\", \"my_did\": \"WgWxqztrNooG92RXvxSTWv\", \"my_seed\": \"000000000000000000000000000Alice\", \"their_did\": \"WgWxqztrNooG92RXvxSTWv\", \"their_endpoint\": \"http://172.17.0.1:8021\", \"their_label\": \"alice\", \"their_seed\": \"alice\", \"their_verkey\": \"alice\"}"
</pre>

**Resposta :**
<pre>
{"my_did": "WgWxqztrNooG92RXvxSTWv", 
"my_verkey": "GRow3SpMJJ8K53oFk1549fSCPtdt55gaV1uGwErSw2Ae", 
"my_endpoint": "http://172.17.0.1:8020", 
"their_did": "WgWxqztrNooG92RXvxSTWv", 
"their_verkey": "alice", 
"record": 
{"state": "active", 
"routing_state": "none", 
"updated_at": "2021-01-06 19:40:55.812576Z",
"my_did": "WgWxqztrNooG92RXvxSTWv", 
"invitation_mode": "static", 
"alias": "alice", 
"connection_id": "50d1eeee-867a-461e-9218-6e3b39287088", 
"their_label": "alice", 
"accept": "manual", 
"their_did": "WgWxqztrNooG92RXvxSTWv",
"created_at": "2021-01-06 19:40:55.812576Z"}}
</pre>

### 3.4 Receba um novo convite de conexão
Post /connections/receive-invitation

<pre>
curl -X POST "http://172.17.0.1:8031/connections/receive-invitation" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1ZDk3NDQ2OC00ZTk3LTRiNTMtOGZhZi0wZmQxZjNiYWIwYjgifQ.QCLXyw7KIWhVU7H6NOQ0gM3cFUtl4dIxZnKh3Jx-cqw" -H "Content-Type: application/json" -d "{ \"@type\": \"did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation\", \"@id\": \"aea87a96-51e6-4b31-b488-f2427ed80e87\", \"recipientKeys\": [\"CbMzqNhvmm3EZVr9GTiFQYUQ8dQG5WfkuiSLcRGsosbh\"], \"label\": \"Faber.initial\", \"serviceEndpoint\": \"http://172.17.0.1:8020\"}"
</pre>

**Resultado :**
<pre>
{
"their_role": "inviter", 
"routing_state": "none", 
"state": "request", 
"created_at": "2021-01-08 17:48:48.222818Z", 
"request_id": "149c944a-4303-4b24-8eff-8f3dd0d6a618", 
"accept": "auto", "my_did": "H1seGcKYF4dzC3zqB7Woj5", 
"their_label": "Faber.initial", 
"invitation_mode": "once", 
"connection_id": "38d6d6a3-018c-49bf-b04f-5eb5e5ce593b", 
"invitation_key": "CbMzqNhvmm3EZVr9GTiFQYUQ8dQG5WfkuiSLcRGsosbh", 
"updated_at": "2021-01-08 17:48:48.244098Z"
}
</pre>

### 3.5 Buscar um único registro de conexão
Post /connections/{conn_id}

<pre>
curl -X GET "http://172.17.0.1:8031/connections/ef9743bd-ddda-44ac-854d-671b522bfdc3" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
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

### 3.6 Remover um registro de conexão existente
Delete /connections/{conn_id}

<pre>
curl -X DELETE "http://172.17.0.1:8031/connections/ef9743bd-ddda-44ac-854d-671b522bfdc3" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

### 3.7 Aceite um convite de conexão armazenado
Post /connections/{conn_id}/accept-invitation

<pre>
curl -X POST "http://172.17.0.1:8031/connections/6b929cc7-a146-4cb7-9be7-74bff7aeb87f/accept-invitation" 
-H "accept: application/json"
</pre>

### 3.8 Aceite uma solicitação de conexão armazenada
Post /connections/{conn_id}/accept-request

<pre>
curl -X POST "http://172.17.0.1:8031/connections/6b929cc7-a146-4cb7-9be7-74bff7aeb87f/accept-request" 
-H "accept: application/json"
</pre>

### 3.9 Atribuir outra conexão como a conexão de entrada

<pre>

</pre>

### 3.10 Buscar metadados da conexão

<pre>
curl -X GET "http://172.17.0.1:8031/connections/8efcea04-f922-4a35-91b5-5827d37967d0/metadata" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0MmM0OTc2OC02ZDM5LTRhZmYtYjliZi04MTlkYzdhZTUxNzYifQ.AbH_NDLt3G5zaKGh6s603IVpWBTXbO3omjM9LxWv-es"
</pre>

### 3.11 Definir metadados da conexão

<pre>
curl -X POST "http://172.17.0.1:8031/connections/8efcea04-f922-4a35-91b5-5827d37967d0/metadata" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0MmM0OTc2OC02ZDM5LTRhZmYtYjliZi04MTlkYzdhZTUxNzYifQ.AbH_NDLt3G5zaKGh6s603IVpWBTXbO3omjM9LxWv-es" 
-H "Content-Type: application/json" 
-d "{ \"metadata\": {}}
</pre>

## 4.Credential definition
### 4.1 Envia uma definição de credencial para o razão
Post /credential-definitions


**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/credential-definitions" 
-H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA" 
-H "Content-Type: application/json" 
-d "{ \"revocation_registry_size\": 1000, \"schema_id\": \"WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0\", \"support_revocation\": false, \"tag\": \"default\"}"
</pre>

### 4.2 Pesquise por definições de credenciais correspondentes que o agente originou
Post /credential-definitions/created

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/credential-definitions/created" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA"
</pre>

### 4.3  Obtém uma definição de credencial do razão
Get /credential-definitions/{{ credential_definition_id }}


**Exemplo :**

<pre>
curl -X GET "http://172.17.0.1:8021/credential-definitions/M786j533KXeifEnGd3gQLx%3A3%3ACL%3A94%3AFaber.initial.degree_schema" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA"
</pre>

## 5.Credential
### 5.1 Obter tipos de atributos MIME da carteira

Get /credential/mime-types/{{ credential_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/credential/mime-types/5111d8d2-7314-4a55-a081-dd313108a419" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkMTVjZTBiZC0xNDQzLTQxNzktOGNmNy1jOGJhNzJmZTY1ZGEifQ.s1AKvJb1eLZ4jd7NyG0sgtRtxhkxX5PR-UlUbAdcnnA"
</pre>


### 5.2 Consultar status de revogação de credencial por id

Get /credential/revoked/

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credential/revoked/c3706d85-91b9-4969-95a2-4125fc9750c7" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJjYjZkOTc3Yy00NmY5LTQxNmYtYjRmYi1lYjdiMDUzYTA5ZDMifQ.2EGp1lZkzenZRMRCsMh1CzYBwtqiIdh1yPULA89pNEk"
</pre>

### 5.3 Obter uma credencial da carteira por id

Get /credential/{{ credential_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credential/b4c8e92e-ec58-4446-8765-ea6c9e077fb3" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resultado :**
<pre>
{"referent": "b4c8e92e-ec58-4446-8765-ea6c9e077fb3", 
"attrs": {"age": "24", "date": "2018-05-28", "degree": "Maths", "timestamp": "1609939047", "name": "Alice Smith"}, 
"schema_id": "2Y4xCxUYA35FEMSC5ofGTh:2:degree schema:67.95.15", 
"cred_def_id": "2Y4xCxUYA35FEMSC5ofGTh:3:CL:106:Faber.initial.degree_schema", 
"rev_reg_id": null, "cred_rev_id": null}r
</pre>


### 5.4 Remova uma credencial da carteira por id

Get /credential/{{ credential_id }}

**Exemplo :**
<pre>
curl -X DELETE "http://172.17.0.1:8031/credential/b4c8e92e-ec58-4446-8765-ea6c9e077fb3" 
-H "accept: application/json"
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

### 5.5 Obter credenciais da carteira

Get /credential/mime-types/{{ connection_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
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

## 6.Did exchange
### 6.1 Receba um novo convite de conexão
Post /didexchange/receive-invitation

**Exemplo :**
<pre>

</pre>

### 6.2 Aceite um convite de conexão armazenado
Post /didexchange/{conn_id}/accept-invitation

**Exemplo :**
<pre>

</pre>

### 6.3 Aceite uma solicitação de conexão armazenada
Post /didexchange/{conn_id}/accept-request

**Exemplo :**
<pre>

</pre>

## 7.Introduction
### 7.1 Comece uma introdução entre duas conexões
Post /connections/{conn_id}/start-introduction

<pre>
curl -X POST "http://172.17.0.1:8021/connections/c51c8642-1b24-4862-8e08-a2ab889b6d8d/start-introduction?target_connection_id=c4a0882e-e20c-4ee7-b8bf-3f0903da8b35&message=message" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJlYmVjMmRlNS0zZTllLTQ1NTktYWU5Ny0xY2I3NTU3MTllOGQifQ.V74PkUzN4mCQC-h3WjVGfLtXNqbl4YJIyyx0b_UM88s"
</pre>

## 8.Issue credential
### 8.1. Envie ao titular uma credencial, automatizando todo o fluxo
Post /issue-credential/create

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/create" 
-H "accept: application/json" -H "Content-Type: application/json" 
-d "{ \"auto_remove\": true, \"comment\": \"string\", \"cred_def_id\": \"EsJ3Yf37JZhEYVsYcRqVc3:3:CL:121:default\", \"credential_proposal\": { \"@type\": \"issue-credential/1.0/credential-preview\", \"attributes\": [ { \"name\": \"score\", \"value\": \"10\" } ] }, \"issuer_did\": \"EsJ3Yf37JZhEYVsYcRqVc3\", \"schema_id\": \"EsJ3Yf37JZhEYVsYcRqVc3:2:prefs:1.0\", \"schema_issuer_did\": \"EsJ3Yf37JZhEYVsYcRqVc3\", \"schema_name\": \"prefs\", \"schema_version\": \"1.0\", \"trace\": false}" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2ZjNjI5Zi1hMjQxLTRmZmUtYWQyOC1jOGZhNWYyOTNlNDcifQ.efThQchCSPO3ue_P7flrQRVfnh_Vz0YU8EjzmuJrJqw"
</pre>

Observação : É necessário criar o esquema e a definição da credencial.

### 8.2. Obter todos os registros de troca de credenciais
Get /issue-credential/records

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/issue-credential/records" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>

### 8.3. Buscar um único registro de troca de credencial
Get /issue-credential/records/{cred_ex_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/issue-credential/records/c614d249-719c-4302-b272-72d8adc440c4" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>

### 8.4. Remover um registro de troca de credencial existente
Delete /issue-credential/records/{cred_ex_id}

**Exemplo :**
<pre>
curl -X DELETE "http://172.17.0.1:8031/issue-credential/records/c614d249-719c-4302-b272-72d8adc440c4" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>

### 8.5. Enviar uma credencial ao titular
Post /issue-credential/records/{cred_ex_id}/issue

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/issue-credential/records/c614d249-719c-4302-b272-72d8adc440c4/issue" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>

### 8.6. Envie um relatório de problema para troca de credencial
Post /issue-credential/records/{cred_ex_id}/problem-report

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/issue-credential/records/c614d249-719c-4302-b272-72d8adc440c4/problem-report" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"explain_ltxt\": \"string\"}" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>

### 8.7. Enviar ao titular uma oferta de credencial em referência a uma proposta com visualização
Post /issue-credential/records/{cred_ex_id}/send-offer

**Exemplo :**
<pre>


</pre>

### 8.8. Enviar ao emissor um pedido de credencial
Post /issue-credential/records/{cred_ex_id}/send-request

**Exemplo :**
<pre>


</pre>

### 8.9. Armazene uma credencial recebida
Post ​/issue-credential​/records​/{cred_ex_id}​/store

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/issue-credential/records/3177e7d0-1c0b-4c2a-847e-b170aab858a5/store" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"credential_id\": \"string\"}" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>

### 8.10. Envie ao titular uma credencial, automatizando todo o fluxo
Post /issue-credential/send

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/send" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"auto_remove\": true, \"comment\": \"string\", \"connection_id\": \"3a167ff0-e337-499d-bcaa-1db4c886380c\", \"cred_def_id\": \"V1frstKADpJ1GvR5wUW9sN:3:CL:159:default\", \"credential_proposal\": { \"@type\": \"issue-credential/1.0/credential-preview\", \"attributes\": [ { \"name\": \"score\", \"value\": \"10\" } ] }, \"issuer_did\": \"V1frstKADpJ1GvR5wUW9sN\", \"schema_id\": \"V1frstKADpJ1GvR5wUW9sN:2:prefs:1.0\", \"schema_name\": \"prefs\", \"schema_version\": \"1.0\", \"trace\": false}" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIzMDQ3NDU1Zi1hOGY1LTQ4YzItYjAwNy05NjJhMDdkZmVhYWEifQ.D5nBAakpb5rT3BMzfOGVa-waq9odzq1av6wYluyPFR4"
</pre>

**Resposta :**
<pre>
{"updated_at": "2021-01-15 13:29:17.878428Z", "state": "offer_sent", "auto_issue": true, "credential_proposal_dict": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/propose-credential", "@id": "c405739b-b861-4814-9015-0c68af6b9ab1", "schema_version": "1.0", "comment": "string", "cred_def_id": "V1frstKADpJ1GvR5wUW9sN:3:CL:159:default", "issuer_did": "V1frstKADpJ1GvR5wUW9sN", "schema_id": "V1frstKADpJ1GvR5wUW9sN:2:prefs:1.0", "schema_name": "prefs", "credential_proposal": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview", "attributes": [{"name": "score", "value": "10"}]}}, "credential_offer_dict": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/offer-credential", "@id": "c237d182-acb2-4d43-a82d-ddfdfcabf5b3", "~thread": {}, "comment": "create automated credential exchange", "credential_preview": {"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview", "attributes": [{"name": "score", "value": "10"}]}, "offers~attach": [{"@id": "libindy-cred-offer-0", "mime-type": "application/json", "data":...}
</pre>

**Pré-requisitos :**

1)Schema criado;
2)Dfinição de credencial;
3)Criar a credencial;

### 8.11. Envio de proposta de credencial
Post /issue-credential/records/{{ connection_id }}/send-offer

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/issue-credential/records/d239b8bf-d275-476a-aaf6-99e508604371/send-offer" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1MDI3YmE4MS1jMjJiLTQ5NDMtYjNkZS0xOGIwOGJjZWU2MzEifQ.s_wqtCRIBj0rS7e7UClxHcG8RUY7-WybqiIQ-loLXq8"
</pre>

### 8.12. Envie ao emissor uma proposta de credencial
Post /issue-credential/send-proposal

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/issue-credential/send-proposal" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"auto_remove\": true, \"comment\": \"string\", \"connection_id\": \"5d19d6e4-e2a1-424e-b7ed-310aef5f7287\", \"cred_def_id\": \"WgWxqztrNooG92RXvxSTWv:3:CL:20:tag\", \"credential_proposal\": { \"@type\": \"issue-credential/1.0/credential-preview\", \"attributes\": [ { \"mime-type\": \"image/jpeg\", \"name\": \"favourite_drink\", \"value\": \"martini\" } ] }, \"issuer_did\": \"WgWxqztrNooG92RXvxSTWv\", \"schema_id\": \"WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0\", \"schema_issuer_did\": \"WgWxqztrNooG92RXvxSTWv\", \"schema_name\": \"preferences\", \"schema_version\": \"1.0\", \"trace\": false}" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwMzM0ZTE3OC01OTg4LTQ5YjktYjM0Ni1kMDI4NzE5MDhjYjUifQ.YcWZ3ckVXFP1U6BwSgImfeBdRwPaURvhMno2uyTiIe4"
</pre>


## 9.Ledger
### 9.1. Obtenha o ponto de extremidade para um DID do razão
Get /ledger/did-endpoint

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/ledger/did-endpoint?did=VWcuij6MDYDLUv8nvMmKP9" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwZmFiNGEwMy01MjFiLTRhOTctYmQ4YS02OTA2NDFkN2U2ODEifQ.aBHKbOgQnv3JLE4exhX0RKfF9H20fJLYhXdZUvODwAE"
</pre>

**Resposta :**
<pre>
{"endpoint": "http://172.17.0.1:8020"}
</pre>

### 9.2. Obtenha o verkey para um DID do razão
Get /ledger/did-verkey

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/ledger/did-verkey?did=VWcuij6MDYDLUv8nvMmKP9" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwZmFiNGEwMy01MjFiLTRhOTctYmQ4YS02OTA2NDFkN2U2ODEifQ.aBHKbOgQnv3JLE4exhX0RKfF9H20fJLYhXdZUvODwAE"
</pre>

**Resposta :**
<pre>
{"verkey": "GYHAJG5YovSXBjS1pShdFizePPMswp7rctQBeNga28S5"}
</pre>

### 9.3. Obtenha a função do registro do NYM de um DID público
Get /ledger/get-nym-role

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/ledger/get-nym-role?did=VWcuij6MDYDLUv8nvMmKP9" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwZmFiNGEwMy01MjFiLTRhOTctYmQ4YS02OTA2NDFkN2U2ODEifQ.aBHKbOgQnv3JLE4exhX0RKfF9H20fJLYhXdZUvODwAE"
</pre>

**Resposta :**
<pre>
{"role": "ENDORSER"}
</pre>

### 9.4. Envie um registro NYM para o razão.
Post /ledger/register-nym

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/ledger/register-nym?did=VWcuij6MDYDLUv8nvMmKP9&verkey=GYHAJG5YovSXBjS1pShdFizePPMswp7rctQBeNga28S5&role=ENDORSER" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwZmFiNGEwMy01MjFiLTRhOTctYmQ4YS02OTA2NDFkN2U2ODEifQ.aBHKbOgQnv3JLE4exhX0RKfF9H20fJLYhXdZUvODwAE"
</pre>

### 9.5. Gire o par de chaves para DID público.
Patch /ledger/rotate-public-did-keypair

**Exemplo :**
<pre>
curl -X PATCH "http://172.17.0.1:8021/ledger/rotate-public-did-keypair" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwZmFiNGEwMy01MjFiLTRhOTctYmQ4YS02OTA2NDFkN2U2ODEifQ.aBHKbOgQnv3JLE4exhX0RKfF9H20fJLYhXdZUvODwAE"
</pre>

### 9.6. Busque o acordo do autor da transação atual, se houver
Get /ledger/taa

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/ledger/taa" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIwZmFiNGEwMy01MjFiLTRhOTctYmQ4YS02OTA2NDFkN2U2ODEifQ.aBHKbOgQnv3JLE4exhX0RKfF9H20fJLYhXdZUvODwAE"
</pre>

**Resposta :**
<pre>
{"result": {"aml_record": null, "taa_record": null, "taa_required": false, "taa_accepted": null}}
</pre>

### 9.7. Aceite o contrato do autor da transação
Post /ledger/taa/accept

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/ledger/taa/accept" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"mechanism\": \"string\", \"text\": \"string\", \"version\": \"string\"}"  
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1NzljZmE3Ny0zNzQzLTQ4YWEtYTI0OS0wNTJhNjYwOGNkYzQifQ.RhYZoNSP5sLBoiM5TFJDB6aPIcHbXgLqZxb7RLB1Lbw"
</pre>

**Observação :** É necessário que o arquivo taa.json tenha sido criado nos ledgers para que o contrato exista.

## 10.mediation
### 10.1. Solicitar mediação da conexão
Post /mediation/request/{conn_id}

**Exemplo :**
<pre>
 curl -X POST "http://172.17.0.1:8031/mediation/request/4e85c556-c891-404f-9207-706b01517474" 
 -H "accept: application/json" 
 -H "Content-Type: application/json" 
 -d "{ \"mediator_terms\": [ \"string\" ], \"recipient_terms\": [ \"string\" ]}" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1NzljZmE3Ny0zNzQzLTQ4YWEtYTI0OS0wNTJhNjYwOGNkYzQifQ.RhYZoNSP5sLBoiM5TFJDB6aPIcHbXgLqZxb7RLB1Lbw"
</pre>

**Resposta :**
<pre>
{
"updated_at": "2021-01-11 13:54:49.553616Z", 
"created_at": "2021-01-11 13:54:49.553616Z", 
"recipient_terms": ["string"], 
"state": "request", 
"mediation_id": "cd58ef93-2b59-4d90-befb-39be04f3a7c8", 
"routing_keys": [], 
"connection_id": "4e85c556-c891-404f-9207-706b01517474", 
"role": "client", 
"mediator_terms": ["string"]
}
</pre>

### 10.2. Solicitações de mediação de consulta, lista de retorno de todos os registros de mediação
Get /mediation/requests

**Exemplo :**
<pre>
 curl -X GET "http://172.17.0.1:8021/mediation/requests" 
 -H "accept: application/json" 
 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2ZjNjI5Zi1hMjQxLTRmZmUtYWQyOC1jOGZhNWYyOTNlNDcifQ.efThQchCSPO3ue_P7flrQRVfnh_Vz0YU8EjzmuJrJqw"
</pre>

### 10.3. Recuperar registro de solicitação de mediação
Get /mediation/requests/{mediation_id}

**Exemplo :**
<pre>
 curl -X GET "http://172.17.0.1:8021/mediation/requests/cd58ef93-2b59-4d90-befb-39be04f3a7c8" 
 -H "accept: application/json" 
 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1NzljZmE3Ny0zNzQzLTQ4YWEtYTI0OS0wNTJhNjYwOGNkYzQifQ.RhYZoNSP5sLBoiM5TFJDB6aPIcHbXgLqZxb7RLB1Lbw"
</pre>

**Resposta :**
<pre>
{
"updated_at": "2021-01-11 13:54:49.553616Z", 
"created_at": "2021-01-11 13:54:49.553616Z", 
"recipient_terms": ["string"], 
"state": "request", "mediation_id": "cd58ef93-2b59-4d90-befb-39be04f3a7c8", 
"routing_keys": [], "connection_id": "4e85c556-c891-404f-9207-706b01517474", 
"role": "client", "mediator_terms": ["string"]
}
</pre>

### 10.4. Excluir solicitação de mediação por ID
Delete /mediation/requests/{mediation_id}

**Exemplo :**
<pre>
curl -X DELETE "http://172.17.0.1:8031/mediation/requests/cd58ef93-2b59-4d90-befb-39be04f3a7c8" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1NzljZmE3Ny0zNzQzLTQ4YWEtYTI0OS0wNTJhNjYwOGNkYzQifQ.RhYZoNSP5sLBoiM5TFJDB6aPIcHbXgLqZxb7RLB1Lbw"
</pre>

### 10.5. Negar um pedido de mediação armazenado
Post /mediation/requests/{mediation_id}/deny

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/mediation/requests/cd58ef93-2b59-4d90-befb-39be04f3a7c8/deny" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1NzljZmE3Ny0zNzQzLTQ4YWEtYTI0OS0wNTJhNjYwOGNkYzQifQ.RhYZoNSP5sLBoiM5TFJDB6aPIcHbXgLqZxb7RLB1Lbw"
</pre>

### 10.6. Conceder mediação recebida
Post /mediation/requests/{mediation_id}/grant

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/mediation/requests/cd58ef93-2b59-4d90-befb-39be04f3a7c8/grant" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI1NzljZmE3Ny0zNzQzLTQ4YWEtYTI0OS0wNTJhNjYwOGNkYzQifQ.RhYZoNSP5sLBoiM5TFJDB6aPIcHbXgLqZxb7RLB1Lbw"
</pre>

## 11.Multitenancy
### 11.1. Criar wallet
Post /multitenancy/wallet

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"key_management_mode\": \"managed\", \"label\": \"Alice\", \"wallet_key\": \"MySecretKey123\", \"wallet_name\": \"MyNewWallet\", \"wallet_type\": \"indy\"}"
</pre>

**Resposta :**
<pre>
{"key_management_mode": "managed", "wallet_id": "729ecda2-3229-48e3-ac12-7ce7e82e433a", "settings": {"wallet.type": "indy", "wallet.name": "MyNewWallet1", "default_label": "Alice", "wallet.id": "729ecda2-3229-48e3-ac12-7ce7e82e433a"}, "created_at": "2021-01-06 17:58:49.231591Z", "updated_at": "2021-01-06 17:58:49.231591Z", "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI3MjllY2RhMi0zMjI5LTQ4ZTMtYWMxMi03Y2U3ZTgyZTQzM2EifQ.kNhkvUGVPcEEp8y4Ulg0YY-pUPmadrbMThi7EnPbWoc"}
</pre>

### 11.2. Obtenha uma única subwallet
Get /multitenancy/wallet/{wallet_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/multitenancy/wallet/729ecda2-3229-48e3-ac12-7ce7e82e433a" 
-H "accept: application/json"
</pre>

**Resposta :**
<pre>
{"key_management_mode": "managed", "wallet_id": "729ecda2-3229-48e3-ac12-7ce7e82e433a", "settings": {"wallet.type": "indy", "wallet.name": "MyNewWallet1", "default_label": "Alice", "wallet.id": "729ecda2-3229-48e3-ac12-7ce7e82e433a"}, "created_at": "2021-01-06 17:58:49.231591Z", "updated_at": "2021-01-06 17:58:49.231591Z"}
</pre>

### 11.3. Remove uma sub wallet
Post /multitenancy​/wallet​/{wallet_id}​/remove

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet/729ecda2-3229-48e3-ac12-7ce7e82e433a/remove" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"wallet_key\": \"MySecretKey123\"}"
</pre>

### 11.4. Obtenha o token de autenticação para um subwallet
Post /multitenancy/wallet/{wallet_id}/token

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet/60fd663c-e246-4dd2-97ca-a3e22ef2385e/token" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"wallet_key\": \"MySecretKey123\"}"
</pre>

**Resposta :**
<pre>
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI2MGZkNjYzYy1lMjQ2LTRkZDItOTdjYS1hM2UyMmVmMjM4NWUifQ.VysFhjz9CfhcjQNH2qxNDU3ifbBTr0--dFgJbBmblTg"}
</pre>

### 11.5. List all subwallets
Get /multitenancy/wallets

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/multitenancy/wallets" 
-H "accept: application/json"
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

## 12.Out of band
### 12.1 Crie um novo convite de conexão
Post /out-of-band/create-invitation

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/out-of-band/create-invitation" 
-H "accept: application/json" 
-H "Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE" 
-H "Content-Type: application/json" 
-d "{ \"attachments\": [ { \"id\": \"string\", \"type\": \"string\" } ], \"include_handshake\": true, \"metadata\": {}, \"use_public_did\": true}"
</pre>

### 12.2 receba um novo convite de conexão
Post /out-of-band/receive-invitation

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/out-of-band/receive-invitation" 
-H "accept: application/json" 
-H "Authorization: Bearer  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE" 
-H "Content-Type: application/json" 
-d "{ \"attachments\": [ { \"id\": \"string\", \"type\": \"string\" } ], \"include_handshake\": true, \"metadata\": {}, \"use_public_did\": true}"
</pre>

## 13.Proof presentation
### 13.1. Cria uma solicitação de apresentação não vinculada a nenhuma proposta ou conexão existente
Post /present-proof/create-request

**Exemplo :**
<pre>

</pre>

### 13.3. Obter todos os registros de troca à prova de presente
Get /present-proof/records

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/present-proof/records?connection_id=7f91f6fe-4699-4ecf-868d-1aa7d7e24744" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkZGUwYzdlMS0zOWMwLTQyNGMtOGJlYy02MmZiMmRlMjE4MWQifQ.Kr2l2FFOiY_DoMmZ_N8I_amo1P4kXARMblC1CuwOG4E"
</pre>

### 13.3. Buscar um único registro de troca de apresentação
Get /present-proof/records/{pres_ex_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/present-proof/records/fd17de3a-5198-4fdc-ab45-a794f2786558" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkZGUwYzdlMS0zOWMwLTQyNGMtOGJlYy02MmZiMmRlMjE4MWQifQ.Kr2l2FFOiY_DoMmZ_N8I_amo1P4kXARMblC1CuwOG4E"
</pre>

### 13.4. Remover um registro de troca de apresentação existente
Delete /present-proof/records/{pres_ex_id}

**Exemplo :**
<pre>
curl -X DELETE "http://172.17.0.1:8031/present-proof/records/fd17de3a-5198-4fdc-ab45-a794f2786558" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkZGUwYzdlMS0zOWMwLTQyNGMtOGJlYy02MmZiMmRlMjE4MWQifQ.Kr2l2FFOiY_DoMmZ_N8I_amo1P4kXARMblC1CuwOG4E"
</pre>

### 13.5. Obter credenciais para um pedido de apresentação na carteira
Get /present-proof/records/{pres_ex_id}/credentials

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/present-proof/records/6f8229d6-86cf-4516-a23e-f1f2014761c0/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJkZGUwYzdlMS0zOWMwLTQyNGMtOGJlYy02MmZiMmRlMjE4MWQifQ.Kr2l2FFOiY_DoMmZ_N8I_amo1P4kXARMblC1CuwOG4E"
</pre>

**Resultado :**
<pre>
[{
"cred_info": 
{
"referent": "f1da556f-cd70-4c82-9bcd-919c27d002cf", 
"attrs": {"name": "Alice Smith", "age": "24", "date": "2018-05-28", "timestamp": "1610044239", "degree": "Maths"}, 
"schema_id": "EbPC6bZWbET89R44zWhNAF:2:degree schema:56.81.41", 
"cred_def_id": "EbPC6bZWbET89R44zWhNAF:3:CL:142:Faber.initial.degree_schema", 
"rev_reg_id": null, 
"cred_rev_id": null
}, 
"interval": null, 
"presentation_referents": ["0_degree_uuid", "0_name_uuid", "0_age_GE_uuid", "0_date_uuid"]
}]
</pre>

### 13.6. Envia uma prova de apresentação
Post /present-proof/records/{pres_ex_id}/send-presentation

**Exemplo :**
<pre>

</pre>

### 13.7. Envia um pedido de apresentação em referência a uma proposta
Post /present-proof/records/{pres_ex_id}/send-request

**Exemplo :**
<pre>

</pre>

### 13.8. Verifique uma apresentação recebida
Post /present-proof/records/{pres_ex_id}/verify-presentation

**Exemplo :**
<pre>

</pre>

### 13.9. Envia uma proposta de apresentação
Post /present-proof/send-proposal

**Exemplo :**
<pre>

</pre>

### 13.10. Envia uma solicitação de apresentação gratuita não vinculada a nenhuma proposta
Post /present-proof​/send-request

**Exemplo :**
<pre>

</pre>

## 14. Revocation
### 14.1. Obtenha o registro de revogação ativo atual por ID de definição de credencial
Get /revocation​/active-registry​/{cred_def_id}

**Exemplo :**
<pre>curl -X GET "http://172.17.0.1:8021/revocation/active-registry/LAm2sZX5hgQo57s7TB2HR8%3A3%3ACL%3A40%3AFaber.initial.degree_schema" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJhMWFhY2NjMS05NTBmLTQyYWItODEwMy03MjA1ZWQ1NWU5MTQifQ.HdSf0bufZrmsdB2Tdc22QO1aicC0hU5rR6aA0NnKzSk"
</pre>

**Resultado :**
<pre>
{
"result": {"revoc_def_type": "CL_ACCUM", "tails_local_path": "/home/indy/.indy_client/tails/LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:c5731da5-7062-4331-a83f-5c24b64a3311/44Macz4Hd4uSHu6zuGjezakNDkGKw5mzirNa9NaDJgVV", 
"state": "active", 
"revoc_reg_entry": {"ver": "1.0", "value": {"accum": "21 12DF0D6B2F11F31421D6D574958FE276DE550CC612BC0F679B137ADED14ECE277 21 12D58743E0C31BD303D0DEBBF9F0421862DB654FF8991C1B5AF0123F331B8F06D 6 5E6C571623714FC8BD127984489F7990EA04080AE3AFA1586812DCD482329125 4 2D7F6D105742676943A638F69F5E0CA2FBD242402B96B13DA28B8C69C0734A86 6 67EC51BCFFEDAFFD214B8B59635B14504CC144953105EE2748329F396C14636E 4 2A5F614F19CA556A19D0E39F97FAACF1E783006698F9ADE06B3425F464C99BCD"}}, 
"created_at": "2021-01-07 19:38:25.417134Z", "tails_public_uri": "http://729eb267dac9.ngrok.io/LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:c5731da5-7062-4331-a83f-5c24b64a3311", "issuer_did": "LAm2sZX5hgQo57s7TB2HR8", 
"revoc_reg_id": "LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:c5731da5-7062-4331-a83f-5c24b64a3311", 
"record_id": "c5731da5-7062-4331-a83f-5c24b64a3311", 
"pending_pub": [], "updated_at": "2021-01-07 19:38:31.408884Z", 
"max_cred_num": 100, "tag": "c5731da5-7062-4331-a83f-5c24b64a3311", 
"tails_hash": "44Macz4Hd4uSHu6zuGjezakNDkGKw5mzirNa9NaDJgVV", 
"cred_def_id": "LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema", 
"revoc_reg_def": {"ver": "1.0", "id": "LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:c5731da5-7062-4331-a83f-5c24b64a3311", "revocDefType": "CL_ACCUM", "tag": "c5731da5-7062-4331-a83f-5c24b64a3311", "credDefId": "LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema", 
"value": {"issuanceType": "ISSUANCE_BY_DEFAULT", "maxCredNum": 100, "publicKeys": {"accumKey": {"z": "1 12254F3E7FEE89BDD45A31CECA59EA9A04B8E6DD41A32C4A5B4E65E8722F5DD9 1 2417710795091CD682BBE4EDF1D8E89CE50B46820374A4F494A70B9E22E247F0 1 042A8F03DA54A04E4F453873083DC669FD3C94E521D2BD2462B115FDF41306D0 1 0624C184D0DB4066200932C323C4C104AFF1F3829CFFA7A7D9CE859F41F22F39 1 18F4887EBED185BFCF4E5084719CBEA95FE2C51B18A6A6ECB59CB43B49FF4E5F 1 13569A8D6D6F51B3D06781600211572C8BEF46497B87ABE4F5C20D9138090046 1 0F067DD585D04F66FCFD9090672DC6D19110E50ABC453615E04B05718EAB96D4 1 245F17644FE6CBCBF2007C5EE82B3CE9B5C545B98939B642C4AECC62C1C1AE61 1 0EA598BB068E0139AA56A3D36AFC6FF9A1ECB36A646437DA3503F1153D9AADEF 1 14B6494F8257C9D7CA23DA74405048471B507BB670DF61DCCD7166F16B62DD93 1 24C1254362FF558BED423151993E5B68D9101E3F42286894BB58ED53DC9BA8E9 1 0B6CC76D4D0EAEEE9C1F490EB622C102724370FC6036CEA7F697821D85B02CD4"}}, "tailsHash": "44Macz4Hd4uSHu6zuGjezakNDkGKw5mzirNa9NaDJgVV", 
"tailsLocation": "http://729eb267dac9.ngrok.io/LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:c5731da5-7062-4331-a83f-5c24b64a3311"}}}
</pre>

### 14.2. Limpar revogações pendentes
Post /revocation​/clear-pending-revocations

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/revocation/clear-pending-revocations" 
-H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo" 
-H "Content-Type: application/json" 
-d "{ \"purge\": { \"additionalProp1\": [ \"12345\" ], \"additionalProp2\": [ \"12345\" ], \"additionalProp3\": [ \"12345\" ] }}"
</pre>

### 14.3. Cria um novo registro de revogação
Post /revocation​/create-registry

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/revocation/create-registry" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo" 
-H "Content-Type: application/json" 
-d "{ \"credential_definition_id\": \"2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema\", \"max_cred_num\": 1000}"
</pre>

**Resposta :**
<pre>
{"result": {"record_id": "03ac1cc3-48c1-4085-8df8-036949246abc", "updated_at": "2021-01-08 12:14:05.535939Z", "state": "generated", "cred_def_id": "2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema", "revoc_reg_def": {"ver": "1.0", "id": "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:03ac1cc3-48c1-4085-8df8-036949246abc", "revocDefType": "CL_ACCUM", "tag": "03ac1cc3-48c1-4085-8df8-036949246abc", "credDefId": "2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema", "value": {"issuanceType": "ISSUANCE_BY_DEFAULT", "maxCredNum": 1000, "publicKeys": {"accumKey": {"z": "1 019C27CCA8A107489B2B4E3A798A86CA2F4C0E7CDE009F531065F217F23B143D 1 1F783F441C694C191F80B42F286CEB2A33B7B389CB68A736D10FF5A1956ED390 1 0F99395E287D8B23ED6BA1C68C2FDF875562AF8936535A5582B0058C1CB90F5A 1 112477EAD2388390D8A5BD32F09E06B74CDE5ABA50578B8A0847DFE5F0E2D2CB"}}, "tailsHash": "5PHTce3vFRgj3h2F6P2SxKywv2JfbA8DTUjkfgfSV1us", "tailsLocation": "/home/indy/.indy_client/tails/.hopper/5PHTce3vFRgj3h2F6P2SxKywv2JfbA8DTUjkfgfSV1us"}}, "created_at": "2021-01-08 12:14:03.249287Z", "tails_local_path": "/home/indy/.indy_client/tails/2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:03ac1cc3-48c1-4085-8df8-036949246abc/5PHTce3vFRgj3h2F6P2SxKywv2JfbA8DTUjkfgfSV1us", "revoc_reg_entry": {"ver": "1.0", "value": {"accum": "21 52F2BD277F4A8ACBD760E933E6B57E24AF11F3A9CEC5B89822D3F61308067CA7 4 10ADE1ED92C6128CE79D5EB69468B9C051E39EB7BB5623BF0852D0CA4F7689EB"}}, "tag": "03ac1cc3-48c1-4085-8df8-036949246abc", "revoc_def_type": "CL_ACCUM", "tails_hash": "5PHTce3vFRgj3h2F6P2SxKywv2JfbA8DTUjkfgfSV1us", "revoc_reg_id": "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:03ac1cc3-48c1-4085-8df8-036949246abc", "max_cred_num": 1000, "pending_pub": [], "issuer_did": "2mArThE9e4QndCZvD7JRCK"}}
</pre>

### 14.4. Obter status de revogação de credencial
Get /revocation​/credential-record

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/revocation/credential-record?cred_rev_id=1&rev_reg_id=2mArThE9e4QndCZvD7JRCK%3A4%3A2mArThE9e4QndCZvD7JRCK%3A3%3ACL%3A51%3AFaber.initial.degree_schema%3ACL_ACCUM%3Aee3784c7-c314-4f47-8127-26b244c030b7" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo"
</pre>

**Resposta :**
<pre>
{"result": {"record_id": "aab91121-8713-4415-bf38-31e87d613af2", "updated_at": "2021-01-08 11:43:00.893762Z", "state": "issued", "cred_def_id": "2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema", "cred_rev_id": "1", "created_at": "2021-01-08 11:43:00.893762Z", "cred_ex_id": "e994d940-d387-4835-a71a-f5e041bd3d3c", "rev_reg_id": "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:ee3784c7-c314-4f47-8127-26b244c030b7"}}
</pre>

### 14.5. Publicar revogações pendentes no razão
Post /revocation​/publish-revocations

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/revocation/publish-revocations" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo" 
-H "Content-Type: application/json" 
-d "{ \"rrid2crid\": { \"additionalProp1\": [ \"12345\" ] }}"
</pre>

### 14.6. Pesquisar registros de revogação correspondentes que o agente atual criou
Get /revocation/registries/created

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/revocation/registries/created?cred_def_id=LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJhMWFhY2NjMS05NTBmLTQyYWItODEwMy03MjA1ZWQ1NWU5MTQifQ.HdSf0bufZrmsdB2Tdc22QO1aicC0hU5rR6aA0NnKzSk"
</pre>

**Resposta :**
<pre>
{"rev_reg_ids": ["LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:9811f770-adfc-4e11-873e-82fd71158efe", "LAm2sZX5hgQo57s7TB2HR8:4:LAm2sZX5hgQo57s7TB2HR8:3:CL:40:Faber.initial.degree_schema:CL_ACCUM:c5731da5-7062-4331-a83f-5c24b64a3311"]}
</pre>

### 14.7. Obter registro de revogação por id de registro de revogação
Get /revocation​/registry​/{rev_reg_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/revocation/registries/created" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo"
</pre>

**Resposta :**
<pre>
{"rev_reg_ids": ["2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:03ac1cc3-48c1-4085-8df8-036949246abc", "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:2933955d-6a2c-472c-9424-23a375b5a137", "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:ee3784c7-c314-4f47-8127-26b244c030b7", "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:5eda3bf6-1c19-4b70-8693-8eb8e542cfbb"]}
</pre>

### 14.8. Atualize o registro de revogação com o novo URI público em seu arquivo caudas
Patch /revocation​/registry​/{rev_reg_id}

**Exemplo :**
<pre>
curl -X PATCH "http://172.17.0.1:8021/revocation/registry/2mArThE9e4QndCZvD7JRCK%3A4%3A2mArThE9e4QndCZvD7JRCK%3A3%3ACL%3A51%3AFaber.initial.degree_schema%3ACL_ACCUM%3Aee3784c7-c314-4f47-8127-26b244c030b7" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo" 
-H "Content-Type: application/json" 
-d "{ \"tails_public_uri\": \"http://192.168.56.133:6543/revocation/registry/WgWxqztrNooG92RXvxSTWv:4:WgWxqztrNooG92RXvxSTWv:3:CL:20:tag:CL_ACCUM:0/tails-file\"}"
</pre>

**Resposta :**
<pre>
{"result": {"record_id": "ee3784c7-c314-4f47-8127-26b244c030b7", "updated_at": "2021-01-08 12:37:53.836873Z", "state": "active", "cred_def_id": "2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema", "revoc_reg_def": {"ver": "1.0", "id": "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:ee3784c7-c314-4f47-8127-26b244c030b7", "revocDefType": "CL_ACCUM", "tag": "ee3784c7-c314-4f47-8127-26b244c030b7", "credDefId": "2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema", "value": {"issuanceType": "ISSUANCE_BY_DEFAULT", "maxCredNum": 100, "publicKeys": {"accumKey": {"z": "1 00D9B88A9AB17C39449247D2926165CA49C8E9B3FD6A63046687FEC8FE788516 1 112F36283FD96F48CD9DD041F19A44B6351FC702E55618974229609EA58FBFDB 1 1C1222B559E2A1415494BF93758BFCDBB059A9789D83747256700440982ABAFC 1 18FFD561CBAE2B27C70A7F796B7AAF2AD7B0EF16B5F5E5C13529A644B768ED6C"}}, "tailsHash": "7kiapiYv4QP96bfC1DLHWBVbNr2VpvR2yPTe4kXa9NsM", "tailsLocation": "http://192.168.56.133:6543/revocation/registry/WgWxqztrNooG92RXvxSTWv:4:WgWxqztrNooG92RXvxSTWv:3:CL:20:tag:CL_ACCUM:0/tails-file"}}, "created_at": "2021-01-08 11:36:37.636679Z", "tails_local_path": "/home/indy/.indy_client/tails/2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:ee3784c7-c314-4f47-8127-26b244c030b7/7kiapiYv4QP96bfC1DLHWBVbNr2VpvR2yPTe4kXa9NsM", "revoc_reg_entry": {"ver": "1.0", "value": {"accum": "21 8B852ACB8185E41A6CEA3882B0AF209DB60EC95482AF52A1B6D75DC11783734D 4 12D539945D341522A7B164B25623B4144D76DAD0B8247745DB3DEA3F93B3EE38"}}, "tag": "ee3784c7-c314-4f47-8127-26b244c030b7", "revoc_def_type": "CL_ACCUM", "tails_hash": "7kiapiYv4QP96bfC1DLHWBVbNr2VpvR2yPTe4kXa9NsM", "revoc_reg_id": "2mArThE9e4QndCZvD7JRCK:4:2mArThE9e4QndCZvD7JRCK:3:CL:51:Faber.initial.degree_schema:CL_ACCUM:ee3784c7-c314-4f47-8127-26b244c030b7", "max_cred_num": 100, "pending_pub": [], "issuer_did": "2mArThE9e4QndCZvD7JRCK", "tails_public_uri": "http://192.168.56.133:6543/revocation/registry/WgWxqztrNooG92RXvxSTWv:4:WgWxqztrNooG92RXvxSTWv:3:CL:20:tag:CL_ACCUM:0/tails-file"}}
</pre>

### 14.9. Enviar definição de registro de revogação para o razão
Post /revocation/registry/{rev_reg_id}​/definition

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/revocation/registry/2mArThE9e4QndCZvD7JRCK%3A4%3A2mArThE9e4QndCZvD7JRCK%3A3%3ACL%3A51%3AFaber.initial.degree_schema%3ACL_ACCUM%3Aee3784c7-c314-4f47-8127-26b244c030b7/definition" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo"
</pre>

### 14.10. Enviar entrada do registro de revogação para o razão
Post /revocation​/registry​/{rev_reg_id}​/entry

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8021/revocation/registry/2mArThE9e4QndCZvD7JRCK%3A4%3A2mArThE9e4QndCZvD7JRCK%3A3%3ACL%3A51%3AFaber.initial.degree_schema%3ACL_ACCUM%3Aee3784c7-c314-4f47-8127-26b244c030b7/entry" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI4ZmQ1YTlhYi01MjlhLTRmNzQtOWNiYS1kYmZjYjEwMTIxYjIifQ.5AXaNQk1P-PO_RHAWr_N_igtYwz0yEq2oaGlWhERcJo"
</pre>

### 14.11. Obtenha o número de credenciais emitidas no registro de revogação
Get /revocation​/registry​/{rev_reg_id}​/issued

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/revocation/registry/5k8nbJA5Cx9RbJqb4E7Qw7%3A4%3A5k8nbJA5Cx9RbJqb4E7Qw7%3A3%3ACL%3A61%3AFaber.initial.degree_schema%3ACL_ACCUM%3A8bab36e2-5164-4fb9-950a-76d716698deb/issued" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2RmYjU2NC1mODRhLTRmMTgtYTdkNy02YTg2MGU1NTM0MzMifQ.rrNi_Wyac10aUuZv73E35p5JRt7ivla_3kNKLoGF0mU"
</pre>

**Resposta :**
<pre>
{"result": 2}
</pre>

### 14.12. Definir o estado do registro de revogação manualmente
Patch /revocation​/registry​/{rev_reg_id}​/set-state

**Estados possíveis :**
* init
* posted
* generated
* active
* full

**Exemplo :**
<pre>
curl -X PATCH "http://172.17.0.1:8021/revocation/registry/5k8nbJA5Cx9RbJqb4E7Qw7%3A4%3A5k8nbJA5Cx9RbJqb4E7Qw7%3A3%3ACL%3A61%3AFaber.initial.degree_schema%3ACL_ACCUM%3A8bab36e2-5164-4fb9-950a-76d716698deb/set-state?state=posted" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2RmYjU2NC1mODRhLTRmMTgtYTdkNy02YTg2MGU1NTM0MzMifQ.rrNi_Wyac10aUuZv73E35p5JRt7ivla_3kNKLoGF0mU"
</pre>

**Resultado :**
<pre>
{"result": {"tails_hash": "5J441HWb4z7GF9iv2j9x6z19Pi7gZQ4mKkpMVQzXpqMx", "revoc_reg_id": "5k8nbJA5Cx9RbJqb4E7Qw7:4:5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema:CL_ACCUM:8bab36e2-5164-4fb9-950a-76d716698deb", "record_id": "8bab36e2-5164-4fb9-950a-76d716698deb", "state": "posted", "updated_at": "2021-01-08 12:48:36.415779Z", "revoc_reg_def": {"ver": "1.0", "id": "5k8nbJA5Cx9RbJqb4E7Qw7:4:5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema:CL_ACCUM:8bab36e2-5164-4fb9-950a-76d716698deb", "revocDefType": "CL_ACCUM", "tag": "8bab36e2-5164-4fb9-950a-76d716698deb", "credDefId": "5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema", "value": {"issuanceType": "ISSUANCE_BY_DEFAULT", "maxCredNum": 100, "publicKeys": {"accumKey": {"z": "1 1B00F03A074C6208216294C526F1D21B19EFF773973CEBCBB178C0D7B5FC4D92 1 055C0CBEBC308D29ABF6EA349467D009EB4641A67C749C45911929EE6484A186 1 223B80BF315BCB9A2205BAA89A77D5DFC3E570F658B2568BD45D22B77EC62FEC 1 1D85366BD1D96CA1E6D2196189B1124F2E649C78371AE24F9EE76FF3576392A6"}}, "tailsHash": "5J441HWb4z7GF9iv2j9x6z19Pi7gZQ4mKkpMVQzXpqMx", "tailsLocation": "http://73007dd583c4.ngrok.io/5k8nbJA5Cx9RbJqb4E7Qw7:4:5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema:CL_ACCUM:8bab36e2-5164-4fb9-950a-76d716698deb"}}, "tails_public_uri": "http://73007dd583c4.ngrok.io/5k8nbJA5Cx9RbJqb4E7Qw7:4:5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema:CL_ACCUM:8bab36e2-5164-4fb9-950a-76d716698deb", "pending_pub": [], "max_cred_num": 100, "revoc_def_type": "CL_ACCUM", "created_at": "2021-01-08 12:43:17.889136Z", "revoc_reg_entry": {"ver": "1.0", "value": {"accum": "21 109C12E0E5F8C8D20257B8FC01843B723FA683D1873B2FB835529A8461E990871 21 11DCE82754E37CD01BE08E14FB5EA91C2BE1AD014AC6E072B2EB2DF4E6EF58255 6 6C8507D343F09291DCDB3089D441B4E8F8BAF68AD0D132B24E3B1EF8EF24EE67 4 2F9462E4E38452C7126F11CF93B3923A35CE5446987D91871FD230EF9ECAB667"}}, "tails_local_path": "/home/indy/.indy_client/tails/5k8nbJA5Cx9RbJqb4E7Qw7:4:5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema:CL_ACCUM:8bab36e2-5164-4fb9-950a-76d716698deb/5J441HWb4z7GF9iv2j9x6z19Pi7gZQ4mKkpMVQzXpqMx", "tag": "8bab36e2-5164-4fb9-950a-76d716698deb", "issuer_did": "5k8nbJA5Cx9RbJqb4E7Qw7", "cred_def_id": "5k8nbJA5Cx9RbJqb4E7Qw7:3:CL:61:Faber.initial.degree_schema"}}
</pre>

### 14.13. Carregar arquivo local tails para o servidor
Put /revocation​/registry​/{rev_reg_id}​/tails-file

**Exemplo :**
<pre>
curl -X PUT "http://172.17.0.1:8021/revocation/registry/5k8nbJA5Cx9RbJqb4E7Qw7%3A4%3A5k8nbJA5Cx9RbJqb4E7Qw7%3A3%3ACL%3A61%3AFaber.initial.degree_schema%3ACL_ACCUM%3A8bab36e2-5164-4fb9-950a-76d716698deb/tails-file" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2RmYjU2NC1mODRhLTRmMTgtYTdkNy02YTg2MGU1NTM0MzMifQ.rrNi_Wyac10aUuZv73E35p5JRt7ivla_3kNKLoGF0mU"
</pre>

### 14.14. Baixar arquivo tails
Get /revocation​/registry​/{rev_reg_id}​/tails-file

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/revocation/registry/5k8nbJA5Cx9RbJqb4E7Qw7%3A4%3A5k8nbJA5Cx9RbJqb4E7Qw7%3A3%3ACL%3A61%3AFaber.initial.degree_schema%3ACL_ACCUM%3A8bab36e2-5164-4fb9-950a-76d716698deb/tails-file" 
-H "accept: application/octet-stream" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2RmYjU2NC1mODRhLTRmMTgtYTdkNy02YTg2MGU1NTM0MzMifQ.rrNi_Wyac10aUuZv73E35p5JRt7ivla_3kNKLoGF0mU" --output teste.tmp
</pre>

### 14.15. Revogar uma credencial emitida
Post /revocation​/revoke

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/revocation/registry/5k8nbJA5Cx9RbJqb4E7Qw7%3A4%3A5k8nbJA5Cx9RbJqb4E7Qw7%3A3%3ACL%3A61%3AFaber.initial.degree_schema%3ACL_ACCUM%3A8bab36e2-5164-4fb9-950a-76d716698deb/tails-file" 
-H "accept: application/octet-stream" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiIyM2RmYjU2NC1mODRhLTRmMTgtYTdkNy02YTg2MGU1NTM0MzMifQ.rrNi_Wyac10aUuZv73E35p5JRt7ivla_3kNKLoGF0mU" --output teste.tmp
</pre>

## 15.Schema
### 15.1 Envia um esquema para o razão
Post /schemas

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/schemas" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE" -H "Content-Type: application/json" 
-d "{ \"attributes\": [ \"score\" ], \"schema_name\": \"prefs\", \"schema_version\": \"1.0\"}"
</pre>

### 15.2 Pesquise o esquema correspondente que o agente originou

Get /schemas/created

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/schemas/created?schema_id=2Y4xCxUYA35FEMSC5ofGTh%3A2%3Adegree%20schema%3A67.95.15" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

### 15.3 Obtém um esquema do livro-razão
Get /schemas/{schema_id}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/schemas/2Y4xCxUYA35FEMSC5ofGTh%3A2%3Adegree%20schema%3A67.95.15" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
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

## 16.Server
### 16.1 Query supported features
Get /features

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8021/features" 
-H "accept: application/json"
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

### 16.2 Pega a lista de plugins carregados
Get /plugins

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/plugins" 
-H "accept: application/json"
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

### 16.3 Desligar servidor
Get /shutdown

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/shutdown" 
-H "accept: application/json"
</pre>


### 16.4 Obter o status do servidor
Get /status

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/status" 
-H "accept: application/json"
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

### 16.5 Verificação de vivo
Get /status/live

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/status/live" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta :**

<pre>
{"alive": true}
</pre>


### 16.6 Verificação de pronto
Get /status/ready

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/status/ready" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

**Resposta :**

<pre>
{"ready": true}
</pre>

### 16.7 Reset nas estatísticas
Post /status/reset

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/status/reset" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiJmMmEwMDI5NC02NGRmLTRmMzgtYTY2Zi1kNzg3OGE2N2JlNjkifQ.K0hwyvTcFvC3c18reBWTcKG4Fk6mNUSxknVCiUbYjaE"
</pre>

## 17.Trustping 
### 17.1 Envie um ping de confiança para uma conexão
Post /connections/{conn_id}/send-ping

**Exemplo :**
<pre>
curl -X POST "http://172.17.0.1:8031/connections/1f412482-9b16-4484-b99c-9c7095104f39/send-ping" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"comment\": \"string\"}" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"

Resposta :

{"thread_id": "31080d88-1937-4af8-82ba-dbfc792d8343"}

</pre>

## 18.Wallet
### 18.1. Listando credenciais na Wallet

Get /credentials

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/credentials" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0ZjQ4NzRiMS1hY2IxLTRhODUtODE1Ny03YjBiNDgzNzJiZTAifQ.eCQcaIwaJYoAcG-xJ901U5DSJDyvJJiRoRF8FTVTBF8"
</pre>

### 18.2. Lista as wallets do Agent

Get /multitenancy/wallets

**Exemplo :**
<pre>
$ curl -X GET "http://172.17.0.1:8021/multitenancy/wallets" 
-H "accept: application/json"

{"results": [{
"key_management_mode": "managed", 
"updated_at": "2021-01-05 14:04:45.293416Z", 
"wallet_id": "5027ba81-c22b-4943-b3de-18b08bcee631", 
"settings": {"wallet.type": "indy", 
"wallet.name": "Faber.initial", 
"default_label": "Faber.initial", 
"wallet.id": "5027ba81-c22b-4943-b3de-18b08bcee631"}, 
"created_at": "2021-01-05 14:04:45.293416Z"}]}

$ curl -X GET "http://172.17.0.1:8031/multitenancy/wallets" 
-H "accept: application/json"

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


### 18.3. Obtendo apenas uma sub wallet

Get /multitenancy/wallet/{{ wallet_id }}

**Exemplo :**
<pre>
curl -X GET "http://172.17.0.1:8031/multitenancy/wallet/4f4874b1-acb1-4a85-8157-7b0b48372be0" 
-H "accept: application/json"
</pre>

### 18.4. Criando uma sub wallet

Post /multitenancy/wallet

**Exemplo :**

<pre>
curl -X POST "http://172.17.0.1:8021/multitenancy/wallet" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"key_management_mode\": \"managed\", \"label\": \"Alice\", \"wallet_key\": \"MySecretKey123\", \"wallet_name\": \"MyNewWallet\", \"wallet_type\": \"indy\"}"
</pre>


## 19.Keylist
### 19.1 Recuperar listas de chaves por conexão ou função

Get /mediation/keylists

<pre>
curl -X GET "http://172.17.0.1:8031/mediation/keylists?role=client" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"

curl -X GET "http://172.17.0.1:8031/mediation/keylists?role=server" 
-H "accept: application/json" 
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3YWxsZXRfaWQiOiI0M2Q2YWZhMi04NjQzLTRiMTctYTQzYS03MzNkYjBmODE5MDcifQ.4piqFm98kVs9zh4OdeER_mYbHHCOKw4jhqWGPrSbHLM"
</pre>

### 19.2 Envie a consulta da lista de chaves para o mediador
Post /mediation/keylists/{mediation_id}/send-keylist-query

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/mediation/keylists/{mediation_id}/send-keylist-query" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>

### 19.3 atualizar a lista de chaves.
Post /mediation/keylists/{mediation_id}/send-keylist-update

<pre>
curl -X GET "http://{{ Endereço IP }}:{{ Porta }}/mediation/keylists/{mediation_id}/send-keylist-update" 
-H "accept: application/json" 
-H "Authorization: Bearer {{ Token }}"
</pre>
