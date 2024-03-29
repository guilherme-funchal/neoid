import os
import urllib
import threading
import subprocess
import time
import requests
import os.path

from rest_framework.response import Response
from .indy_utils import *



DEFAULT_INTERNAL_HOST = "127.0.0.1"
DEFAULT_EXTERNAL_HOST = "localhost"
DUMMY_SEED = "00000000000000000000000000000000"
MAX_CRED_NUM = "50"

######################################################################
# utilities to provision Aries agents
######################################################################
def aries_provision_config(
        agent_name: str, 
        api_key: str,
        callback_key: str,
        wallet_key: str,
        http_port: int,
        admin_port: int,
        public_endpoint: str,
        admin_endpoint: str,
        did_seed: str=None, 
        genesis_data: str = None,
        params: dict = {},
        webhook_url: str = None,
        start_agent: bool = False
    ):
    """
    Build a configuration object for an Aries agent
    """

    internal_host = DEFAULT_INTERNAL_HOST
    external_host = DEFAULT_EXTERNAL_HOST

    rand_name = str(random.randint(100_000, 999_999))

    # TODO pull from settings file ARIES_CONFIG
    storage_type = "indy"
    wallet_type = "indy"
    wallet_name = agent_name.lower().replace(" ", "") + rand_name
    postgres = True
    postgres_config = settings.ARIES_CONFIG['storage_config']
    postgres_creds = settings.ARIES_CONFIG['storage_credentials']
    genesis_url = os.environ.get('GENESIS_URL', settings.ARIES_CONFIG['genesis_url'])
    webhook_host = settings.ARIES_CONFIG['webhook_host']
    webhook_port = settings.ARIES_CONFIG['webhook_port']
    webhook_root = settings.ARIES_CONFIG['webhook_root']
    webhook_url = "http://" + webhook_host + ":" + webhook_port + webhook_root + "/agent_cb/" + callback_key

    # endpoint exposed by ngrok

    PUBLIC_TAILS_URL = "http://903291ff6280.ngrok.io"

    provisionConfig = []


    if start_agent:
        provisionConfig.extend([
            ("--endpoint", public_endpoint),
            ("--label", agent_name),
            "--auto-ping-connection",
            "--auto-accept-invites",
            "--auto-accept-requests",
            "--auto-store-credential",
            "--auto-verify-presentation",
            # "--preserve-exchange-records",
            ("--inbound-transport", "http", "0.0.0.0", str(http_port)),
            ("--outbound-transport", "http"),
            ("--admin", "0.0.0.0", str(admin_port)),
            ("--admin-api-key", api_key),
            "--enable-undelivered-queue",
            #           "--admin-insecure-mode",
            "--auto-respond-messages",
            "--auto-respond-presentation-request",
            "--auto-respond-credential-offer",
            "--auto-respond-credential-request",
            "--auto-respond-presentation-proposal",
        ])
    provisionConfig.extend([
        ("--wallet-type", wallet_type),
        ("--wallet-name", wallet_name),
        ("--wallet-key", wallet_key),
    ])
    if genesis_data:
        provisionConfig.append(("--genesis-transactions", genesis_data))
    else:
        provisionConfig.append(("--genesis-url",  genesis_url))
    if did_seed:
        provisionConfig.append(("--seed", did_seed))
    if storage_type:
        provisionConfig.append(("--storage-type", storage_type))
    if postgres:
        provisionConfig.extend(
            [
                ("--wallet-storage-type", "postgres_storage"),
                ("--wallet-storage-config", json.dumps(postgres_config)),
                ("--wallet-storage-creds", json.dumps(postgres_creds)),
            ]
        )
    provisionConfig.append(("--webhook-url", webhook_url))
    provisionConfig.append(("--tails-server-base-url", PUBLIC_TAILS_URL))
    return provisionConfig


def get_unused_ports(count: int) -> []:
    ret = []
    for i in range(count):
        port = random.randrange(16000, 32000)
        ret.append(port)
    return ret


def initialize_and_provision_agent(
        agent_name: str, raw_password, did_seed=None, org_role='', start_agent_proc=False,
        mobile_agent=False, managed_agent=None, admin_port=None, admin_endpoint=None,
        http_port=None, http_endpoint=None, api_key=None, webhook_key=None
    ) -> AriesAgent:
    """
    Initialize and provision a new Aries Agent.
    """

    agent = AriesAgent(agent_name=agent_name)
    agent.api_key = api_key if api_key else random_an_string(40)
    agent.callback_key = webhook_key if webhook_key else random_an_string(20)
    agent.mobile_agent = mobile_agent
    agent.managed_agent = managed_agent

    if mobile_agent or (not managed_agent):
        start_agent_proc = False

    if not mobile_agent:
        ports = get_unused_ports(2)
        agent.agent_admin_port = admin_port if admin_port else ports[0]
        agent.agent_http_port = http_port if http_port else ports[1]
        managed_agent_host = settings.ARIES_CONFIG['managed_agent_host']
        public_endpoint = http_endpoint if http_endpoint else "http://" + managed_agent_host + ":" + str(agent.agent_http_port)
        admin_endpoint = admin_endpoint if admin_endpoint else "http://" + managed_agent_host + ":" + str(agent.agent_admin_port)

        startConfig = aries_provision_config(
                                agent.agent_name,
                                agent.api_key, 
                                agent.callback_key,
                                raw_password, 
                                agent.agent_http_port,
                                agent.agent_admin_port,
                                public_endpoint,
                                admin_endpoint,
                                did_seed=did_seed,
                                start_agent=True
                            )
        startConfig_json = json.dumps(startConfig)
        agent.agent_config = startConfig_json
        agent.public_endpoint = public_endpoint
        agent.admin_endpoint = admin_endpoint

    if did_seed:
        nym_info = create_and_register_did(agent.agent_name, did_seed)

    if start_agent_proc:
        try:
            start_agent(agent, config=startConfig)
        except:
            raise

    return agent


def start_agent(agent, cmd: str='start', config=None):
    """
    Start up an instance of an Aries Agent.
    Only start if necessary (checks if it is already running).
    """
    start_agent_if_necessary(agent, initialize_agent=True, cmd=cmd, config=config)


def stop_agent(agent):
    """
    Shut down a running Aries Agent.
    """
    if agent.mobile_agent or (not agent.managed_agent):
        return

    stop_aca_py(agent.agent_name)



######################################################################
# low-level utilities to manage aca-py processes
######################################################################

if 'aca_py_bin_path' in settings.ARIES_CONFIG:
    DEFAULT_BIN_PATH = settings.ARIES_CONFIG['aca_py_bin_path']
else:
    DEFAULT_BIN_PATH = "../venv/bin/"

DEFAULT_PYTHON_PATH = ".."
START_TIMEOUT = 30.0
s_print_lock = threading.Lock()
running_procs = {}

def get_ADMIN_REQUEST_HEADERS(agent):
    ADMIN_REQUEST_HEADERS = {}
    # set admin header per agent
    ADMIN_REQUEST_HEADERS["Content-Type"] = "application/json"
#   ADMIN_REQUEST_HEADERS["accept"] = "application/json"
    if agent.api_key is not None:
       ADMIN_REQUEST_HEADERS["x-api-key"] = agent.api_key
    return ADMIN_REQUEST_HEADERS

def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)

def output_reader(proc_name, proc):
    while True:
        line = proc.stdout.readline()
        if line and 0 < len(line):
            s_print("Stdout {0}: {1}".format(proc_name, line), end="")
        else:
            break

def stderr_reader(proc_name, proc):
    while True:
        line = proc.stderr.readline()
        if line and 0 < len(line):
            s_print("Stderr-> {0}: {1}".format(proc_name, line), end="")
        else:
            break

def detect_process(admin_url, ADMIN_REQUEST_HEADERS, start_timeout=START_TIMEOUT):
    text = None

    def fetch_swagger(url: str, ADMIN_REQUEST_HEADERS: dict, timeout: float):
        text = None
        wait_time = START_TIMEOUT
        # always test at least once
        while wait_time >= 0:
            try:
                resp = requests.get(url, headers=ADMIN_REQUEST_HEADERS)
                resp.raise_for_status()
                text = resp.text
                return text
            except Exception:
                pass
            wait_time = wait_time - 0.5
            if wait_time < 0:
                return None
            time.sleep(0.5)
        return None

    status_url = admin_url + "/status"
    status_text = fetch_swagger(status_url, ADMIN_REQUEST_HEADERS, start_timeout)
    print("Agent running with admin url", admin_url)

    if not status_text:
        raise Exception(
            "Timed out waiting for agent process to start. "
            + f"Admin URL: {status_url}"
        )
    ok = False
    try:
        status = json.loads(status_text)
        ok = isinstance(status, dict) and "version" in status
    except json.JSONDecodeError:
        pass
    if not ok:
        raise Exception(
            f"Unexpected response from agent process. Admin URL: {status_url}"
        )

def start_aca_py(agent_name, agent_args, admin_endpoint, ADMIN_REQUEST_HEADERS, bin_path=None, python_path=None, wait=True):
    """
    Start an aca-py process and record the process handle by agent name
    """
    cmd_path = "aca-py"
    if bin_path is None:
        bin_path = DEFAULT_BIN_PATH
    if bin_path:
        cmd_path = os.path.join(bin_path, cmd_path)
    cmd_args = list(flatten(([cmd_path, "start"], agent_args)))

    my_env = os.environ.copy()
    python_path = DEFAULT_PYTHON_PATH if python_path is None else python_path
    if python_path:
        my_env["PYTHONPATH"] = python_path

    print("Starting aca-py with:", cmd_args)
    proc = subprocess.Popen(
        cmd_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=my_env,
        encoding="utf-8",
    )
    time.sleep(0.5)
    t1 = threading.Thread(target=output_reader, args=(agent_name, proc,))
    t1.start()
    t2 = threading.Thread(target=stderr_reader, args=(agent_name, proc,))
    t2.start()

    print("Started, waiting for status check ...")
    if wait:
        time.sleep(1.0)
        detect_process(admin_endpoint, ADMIN_REQUEST_HEADERS)

    proc_info = {"name": agent_name, "proc": proc, "threads": [t1, t2,]}
    running_procs[agent_name] = proc_info
    print("Agent started.")
    return proc_info


def stop_aca_py(proc_name):
    """
    Stop an aca-py process by agent name (if running)
    """
    print("Terminating aca-py process ...")
    proc = None
    threads = []
    proc_info = running_procs.get(proc_name)
    if proc_info:
        proc = proc_info["proc"]
        threads = proc_info["threads"]

    try:
        if proc and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=1.0)
                print(f"Exited with return code {proc.returncode}")
            except subprocess.TimeoutExpired:
                msg = "Process did not terminate in time"
                print(msg)
                raise Exception(msg)
        print("Joining threads ...")
        for tn in threads:
            tn.join()
    finally:
        try:
            running_procs.pop(proc_name)
        except:
            pass


def stop_all_aca_py():
    """
    Shut down all aca-py processes
    """
    while 0 < len(running_procs):
        proc_name = next(iter(running_procs))
        stop_aca_py(proc_name)


######################################################################
# utilities to create schemas and credential defitions
######################################################################
MAX_RETRIES = 20

def agent_post_with_retry(url, payload, headers=None):
    retries = 0
    while True:
        try:
            # test code to test exception handling
            #if retries < MAX_RETRIES:
            #    raise Exception("Fake exception!!!")
            response = requests.post(
                url,
                payload,
                headers=headers,
            )
            time.sleep(10)
            response.raise_for_status()

            return response
        except Exception as e:
            print("Error posting", url, e)
            retries = retries + 1
            if retries > MAX_RETRIES:
                raise e
            time.sleep(10)


def get_public_did(agent):
    try:
        response = requests.get(
                agent.admin_endpoint + "/wallet/did/public",
                headers=get_ADMIN_REQUEST_HEADERS(agent),
        )
        response.raise_for_status()
        my_did = response.json()
        if "result" in my_did and "did" in my_did["result"]:
            return my_did["result"]["did"]
        else:
            return None
    except:
        raise

### Retorna dados da wallet
def get_wallet_dids(agent, initialize_agent=False):
    """
    Fetch credentials from the agent (wallet).
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    wallets = None

    # create connection and check status
    try:
        response = requests.get(
            agent.admin_endpoint
            + "/wallet/did",
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()

        wallets = response.json()["results"]
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return wallets


def create_schema_json(schema_name, schema_version, schema_attrs):
    """
    Create an Indy Schema object based on a list of attributes.
    Returns the schema as well as a template for creating credentials.
    """
    schema = {
        'name': schema_name,
        'version': schema_version,
        'attributes': schema_attrs,
    }
    creddef_template = {}
    for attr in schema_attrs:
        creddef_template[attr] = ''

    return (json.dumps(schema), json.dumps(creddef_template))


def create_schema(agent, schema_name, schema_version, schema_attrs, schema_template):
    """
    Create an Indy Schema and also store in our local database.
    Note that the agent must be running.
    """

    try:
        schema_request = {
            "schema_name": schema_name,
            "schema_version": schema_version,
            "attributes": schema_attrs,
        }
        response = agent_post_with_retry(
            agent.admin_endpoint + "/schemas",
            json.dumps(schema_request),
            headers=get_ADMIN_REQUEST_HEADERS(agent),
        )
        response.raise_for_status()
        schema_id = response.json()

        indy_schema = IndySchema(
                            ledger_schema_id = schema_id["schema_id"],
                            schema_name = schema_name,
                            schema_version = schema_version,
                            schema = schema_attrs,
                            schema_template = schema_template
                            )
        indy_schema.save()
    except:
        raise

    return indy_schema


def create_creddef(agent, indy_schema, creddef_name, creddef_template):
    """
    Create an Indy Credential Definition (VCX) and also store in our local database
    Note that the agent must be running.
    """

    revocation_registry_size = "100"
    support_revocation = True
    revocation_registry_size = int(revocation_registry_size)

    test = settings.REVOCATION

    try:
        if test == True:
            credential_definition_body = {"schema_id": indy_schema.ledger_schema_id,
                                          "support_revocation": support_revocation,
                                          "revocation_registry_size": revocation_registry_size,}
        else:
            credential_definition_body = {"schema_id": indy_schema.ledger_schema_id}

        response = agent_post_with_retry(
            agent.admin_endpoint + "/credential-definitions",
            json.dumps(credential_definition_body),
            headers=get_ADMIN_REQUEST_HEADERS(agent),
        )
        response.raise_for_status()
        cred_def_id = response.json()

        indy_creddef = IndyCredentialDefinition(
            ledger_creddef_id=cred_def_id["credential_definition_id"],
            ledger_schema=indy_schema,
            agent=agent,
            creddef_name=creddef_name,
            creddef_template=creddef_template
        )
        indy_creddef.save()

    except:
        raise

    return indy_creddef

def create_proof_request(name, description, attrs, predicates):
    """
    Create a proof request template (local database only).
    """

    proof_req_attrs = json.dumps(attrs)
    proof_req_predicates = json.dumps(predicates)
    proof_request = IndyProofRequest(
                            proof_req_name = name,
                            proof_req_description = description,
                            proof_req_attrs = proof_req_attrs,
                            proof_req_predicates = proof_req_predicates
                            )
    proof_request.save()

    return proof_request


######################################################################
# utilities to create and confirm agent-to-agent connections
######################################################################
def start_agent_if_necessary(agent, initialize_agent: bool=True, cmd: str='start', config=None) -> (AriesAgent, bool):
    # start agent if necessary

    if agent.mobile_agent or (not agent.managed_agent):
        return (agent, False)

    if initialize_agent:
        try:
            detect_process(agent.admin_endpoint, get_ADMIN_REQUEST_HEADERS(agent), start_timeout=0.0)
            # didn't start it (assume it's already running)
            return (agent, False)
        except:
            # not running, try to start
            if not config:
                config = json.loads(agent.agent_config)

            start_aca_py(agent.agent_name, config, agent.admin_endpoint, get_ADMIN_REQUEST_HEADERS(agent))

            return (agent, True)
    else:
        # didn't start it (assume it's already running)
        return (agent, False)

def request_connection_invitation(org, request_name, initialize_agent=False):
    """
    Request an Aries Connection Invitation from <partner org>.
    Creates a connection record for the requestor only 
    (receiver connection record is created when receiving the invitation).
    """

    # start the agent if requested (and necessary)
    (partner_agent, agent_started) = start_agent_if_necessary(org.agent, initialize_agent)

    # create connection and generate invitation
    try:
        response = requests.post(
                partner_agent.admin_endpoint + "/connections/create-invitation",
                headers=get_ADMIN_REQUEST_HEADERS(partner_agent),
        )
        response.raise_for_status()
        my_invitation = response.json()
        my_status = check_connection_status(partner_agent, my_invitation["connection_id"])

        connection = AgentConnection(
            guid = my_invitation["connection_id"],
            agent = partner_agent,
            partner_name = request_name,
            invitation = json.dumps(my_invitation["invitation"]),
            invitation_url = my_invitation["invitation_url"],
            status = my_status
        )
        connection.save()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(partner_agent)

    return connection


def receive_connection_invitation(agent, partner_name, invitation, initialize_agent=False):
    """
    Receive an Aries Connection Invitation.
    Creates a receiver connection record.
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    # create connection and generate invitation
    try:
        response = requests.post(
            agent.admin_endpoint
            + "/connections/receive-invitation?alias="
            + partner_name,
            invitation,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        my_connection = response.json()

        connections = AgentConnection.objects.filter(agent=agent, guid=my_connection["connection_id"]).all()
        if 0 < len(connections):
            connection = connections[0]
        else:
            connection = AgentConnection(
                guid = my_connection["connection_id"],
                agent = agent,
                partner_name = partner_name,
                invitation = invitation,
                status = my_connection["state"]
            )
        connection.save()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return connection


def get_agent_connection(agent, connection_id, initialize_agent=False):
    """
    Fetches the Connection object from the agent.
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    connection = None

    # create connection and check status
    try:
        response = requests.get(
            agent.admin_endpoint
            + "/connections/"
            + connection_id,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        connection = response.json()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return connection


def check_connection_status(agent, connection_id, initialize_agent=False):
    """
    Check status of the Connection.
    Called when an invitation has been sent and confirmation has not yet been received.
    """

    # create connection and check status
    try:
        connection = get_agent_connection(agent, connection_id, initialize_agent)

        connections = AgentConnection.objects.filter(agent=agent, guid=connection_id).all()
        if 0 < len(connections):
            my_connection = connections[0]
            my_connection.status = connection["state"]
            my_connection.save()
        else:
            my_connection = None
    except:
        raise

    return connection["state"]


def handle_agent_connections_callback(agent, topic, payload):
    """
    Handle connections processing callbacks from the agent
    """
    # TODO handle callbacks during connections protocol handshake
    # - for now only update connection status
    print(">>> callback:", agent.agent_name, topic)
    try:
        connection_id = payload["connection_id"]
        connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()
        if 0 < len(connections):
            connection = connections[0]
            connection.status = payload["state"]
            connection.save()
        return Response("{}")
    except Exception as e:
        print(e)
        return Response("{}")


def handle_agent_connections_activity_callback(agent, topic, payload):
    """
    Handle connections activity callbacks from the agent
    """
    # TODO determine use cases where this is called
    print(">>> callback:", agent.agent_name, topic)
    return Response("{}")


######################################################################
# utilities to offer, request, send and receive credentials
######################################################################


def build_credential_offer(agent, connection, credential_attrs, cred_def_id):
    credential_offer = {
            "auto_remove": False,
            "auto_issue": True,
            "comment": "Issued by " + agent.agent_name,
            "credential_preview": {
                "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
                "attributes": credential_attrs
            },
            "cred_def_id": cred_def_id,
            "connection_id": connection.guid
        }
    return credential_offer


def build_credential_definition(agent, cred_def_id):
    credential_definition = {
            "max_cred_num": 101,
            "credential_definition_id": 'JnkAjQLbFzx7TrcJWW1ACw:3:CL:9:default'
        }
    return credential_definition


def send_credential_offer(agent, connection, credential_attrs, cred_def_id, initialize_agent=False):
    """
    Send a Credential Offer.
    """
    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    try:
        credential_offer = build_credential_offer(agent, connection, credential_attrs, cred_def_id)

        response = requests.post(
            agent.admin_endpoint
            + "/issue-credential/send-offer",
            json.dumps(credential_offer),
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )

        my_cred_exchange = response.json()
        time.sleep(0.5)

        conversation = AgentConversation(
            connection = connection,
            conversation_type = CRED_EXCH_CONVERSATION,
            guid = my_cred_exchange["credential_exchange_id"],
            status = my_cred_exchange["state"])
        conversation.save()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return conversation
    

def send_credential_request(agent, conversation, initialize_agent=False):
    """
    Respond to a Credential Offer by sending a Credentia Request.
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    # create connection and generate invitation
    try:
        response = requests.post(
            agent.admin_endpoint
            + "/issue-credential/records/" + conversation.guid + "/send-request",
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()

        my_cred_exchange = response.json()
        conversation.status = my_cred_exchange["state"]
        conversation.save()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return conversation


def get_agent_conversation(agent, conversation_id, conversation_type, initialize_agent=False):
    """
    Fetches the Connection object from the agent.
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    conversation = None

    if conversation_type == CRED_EXCH_CONVERSATION:
        url_topic = "/issue-credential/records/"
    elif conversation_type == PROOF_REQ_CONVERSATION:
        url_topic = "/present-proof/records/"
    else:
        raise Exception("Invalid conversation type " + conversation_type)

    # create conversation and check status
    try:
        response = requests.get(
            agent.admin_endpoint
            + url_topic
            + conversation_id,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        conversation = response.json()
    except:
        # ignore in case the agent is deleting exchange records
        #raise
        return None
    finally:
        if agent_started:
            stop_agent(agent)

    return conversation


def check_conversation_status(agent, conversation_id, conversation_type, initialize_agent=False):
    """
    Check status of the Conversation.
    Called when a credential has been offered and/or requested and confirmation has not yet been received.
    """

    status = None

    # create connection and check status
    try:
        conversation = get_agent_conversation(agent, conversation_id, conversation_type, initialize_agent)

        conversations = AgentConversation.objects.filter(connection__agent=agent, guid=conversation_id, conversation_type=conversation_type).all()
        if 0 < len(conversations):
            my_conversation = conversations[0]
            if conversation:
                my_conversation.status = conversation["state"]
                my_conversation.save()
                status = conversation["state"]
            else:
                status = my_conversation.status
        else:
            my_conversation = None
    except:
        raise

    return status


def handle_agent_credentials_callback(agent, topic, payload):
    """
    Handle credential processing callbacks from the agent
    """
    # handle callbacks during credential exchange protocol handshake
    # - update credential status
    test = settings.REVOCATION

    state = payload["state"]

    cred_exch_id = payload["credential_exchange_id"]
    connection_id = payload["connection_id"]

    print(">>> callback:", agent.agent_name, topic, state, cred_exch_id)

    connection = AgentConnection.objects.filter(agent=agent, guid=connection_id).get()

    cred_exches = AgentConversation.objects.filter(connection__agent=agent, guid=cred_exch_id).all()

    if state == "offer_received":
        # holder receives a credential offer - create a new AgentConversation
        conversation = AgentConversation(
            connection = connection,
            conversation_type = CRED_EXCH_CONVERSATION,
            guid = cred_exch_id,
            status = state)
        conversation.save()

    elif state == "basicmessages":
        # issuer receives a credential request (no action, we have "auto submit")
        conversation = cred_exches[0]

#    elif state == "request_received":
#        # issuer receives a credential request (no action, we have "auto submit")
#        print('request_received', cred_exches)
#        conversation = cred_exches[0]
#        conversation.status = state
#        conversation.save()

    elif state == "revocation_registry":
        # holder receives a credential (no action; "auto store")
        conversation = cred_exches[0]
        conversation.status = state
        conversation.save()

    elif state == "credential_received":
        # holder receives a credential (no action; "auto store")
        conversation = cred_exches[0]
        conversation.status = state
        conversation.save()

    elif state == "credential_issued":
        # holder receives a credential (no action; "auto store")
        conversation = cred_exches[0]
        conversation.status = state
        conversation.save()

    elif state == "credential_acked":
        # issuer receives an acknowledgement that the credential was recevied (no action)

        if test == True:
            conversation = AgentConversation(
                    connection=connection,
                    conversation_type=CRED_EXCH_CONVERSATION,
                    guid=cred_exch_id,
                    status=state,
                    rev_reg_id = payload["revoc_reg_id"],
                    cred_rev_id = payload["revocation_id"])
            conversation.save()
        else:
            conversation = cred_exches[0]
            conversation.status = state
            conversation.save()
        
    elif state == "proposal_received":
        #   holder save a credential propose (no action; "auto store")
        conversation = AgentConversation(
                connection = connection,
                conversation_type = CRED_EXCH_CONVERSATION,
                guid = cred_exch_id,
                status = "proposal_received")
        conversation.save()
        
    else:
        # ignore all other statuses (but update state)
        if 0 < len(cred_exches):
            conversation = cred_exches[0]
            conversation.status = state
            conversation.save()

    return Response("{}")

def handle_message_callback(agent, topic, payload):
    """
    Handle credential processing callbacks from the agent
    """
    # handle callbacks during credential exchange protocol handshake
    # - update credential status
    test = settings.REVOCATION

    connection_id = payload["connection_id"]
    message_id = payload["message_id"]
    content = payload["content"]
    state = payload["state"]

    connection = AgentConnection.objects.filter(agent=agent, guid=connection_id).get()

    if state == "received":
        conversation = AgentMessage(
            guid = connection_id,
            connection = connection,
            message_id = message_id,
            content = content,
            state = state)
        conversation.save()

    return Response("{}")

def fetch_credentials(agent, initialize_agent=False):
    """
    Fetch credentials from the agent (wallet).
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    credentials = None

    # create connection and check status
    try:
        response = requests.get(
            agent.admin_endpoint
            + "/credentials",
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        credentials = response.json()["results"]
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return credentials

######################################################################
# utilities to request, send and receive proofs
######################################################################

def build_proof_request(agent, connection, proof_name, requested_attrs, requested_predicates):
    proof_request = {
          "connection_id": connection.guid,
          "proof_request": {
            "name": proof_name,
            "version": "1.0",
            "requested_attributes": requested_attrs,
            "requested_predicates": requested_predicates
          }
        }
    return proof_request


def build_presentation(agent, requested_attrs, requested_predicates, self_attested_attrs):
    proof_presentation = {
            "requested_attributes": requested_attrs,
            "requested_predicates": requested_predicates,
            "self_attested_attributes": self_attested_attrs
        }
    return proof_presentation



def send_proof_request(agent, connection, proof_req_name, proof_attrs, proof_predicates, initialize_agent=False):
    """
    Send an Aries Proof Request.
    """
    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    # create connection and generate invitation
    try:
        proof_request = build_proof_request(agent, connection, proof_req_name, proof_attrs, proof_predicates)

        response = requests.post(
            agent.admin_endpoint
            + "/present-proof/send-request",
            json.dumps(proof_request),
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        my_proof_request = response.json()


        conversation = AgentConversation(
            connection = connection,
            conversation_type = PROOF_REQ_CONVERSATION,
            guid = my_proof_request["presentation_exchange_id"],
            status = my_proof_request["state"])
        conversation.save()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return conversation


# note additional filters are exact match only (attr=value) to filter the allowable claims
def get_claims_for_proof_request(agent, conversation, additional_filters=None, initialize_agent=False):
    """
    For the receiver of the Proof Request (i.e. Prover) find the set of claims that can be used
    to construct a Proof.
    additional_filters must be wql format as defined:  https://github.com/hyperledger/indy-sdk/tree/master/docs/design/011-wallet-query-language
    """
    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    # create connection and generate invitation
    params = ""
    if additional_filters:
        params = "?extra_query=" + urllib.parse.quote_plus(json.dumps(additional_filters))
    try:
        response = requests.get(
            agent.admin_endpoint
            + "/present-proof/records/" + conversation.guid + "/credentials" + params,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        creds_for_proof = response.json()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return creds_for_proof


def cred_for_referent(creds_for_proof, attr, schema_id):
    """
    Find the credential for the given referent (i.e. credential id).
    """

    for cred in creds_for_proof['attrs'][attr]:
        if schema_id == cred['cred_info']['referent']:
            return cred
    return None


def send_claims_for_proof_request(agent, conversation, supplied_attrs, supplied_predicates, supplied_self_attested_attrs, initialize_agent=False):
    """
    Construct a Proof with the given set of claims and send the Proof.
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    # create connection and generate invitation
    try:
        presentation = build_presentation(agent, supplied_attrs, supplied_predicates, supplied_self_attested_attrs)
        response = requests.post(
            agent.admin_endpoint
            + "/present-proof/records/" + conversation.guid + "/send-presentation",
            json.dumps(presentation),
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        my_proof_request = response.json()

        conversation.status = my_proof_request["state"]
        conversation.save()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return conversation


def handle_agent_proof_callback(agent, topic, payload):
    """
    Handle proof request processing callbacks from the agent
    """
    # handle callbacks during proof request protocol handshake
    state = payload["state"]
    print('state->', state)

    proof_request_id = payload["presentation_exchange_id"]

    connection_id = payload["connection_id"]

    connection = AgentConnection.objects.filter(agent=agent, guid=connection_id).get()
    proof_requests = AgentConversation.objects.filter(connection__agent=agent, guid=proof_request_id).all()

    # TODO update the following as appropriate for proof requests
    if state == "request_received":
        # holder receives a credential offer - create a new AgentConversation
        if 0 == len(proof_requests):
            conversation = AgentConversation(
                connection = connection,
                conversation_type = PROOF_REQ_CONVERSATION,
                guid = proof_request_id,
                status = state)
        else:
            conversation = proof_requests[0]
            conversation.status = state

        conversation.save()

    elif state == "presentation_sent":
        # issuer receives a credential request (no action, we have "auto submit")
        conversation = proof_requests[0]
        conversation.status = state
        conversation.save()

    elif state == "presentation_received":
        # holder receives a credential (no action; "auto store")
        conversation = proof_requests[0]
        conversation.status = state
        conversation.save()

    elif state == "verified":
        # issuer receives an acknowledgement that the credential was recevied (no action)
        conversation = proof_requests[0]
        conversation.status = state
        conversation.save()

    else:
        # ignore all other statuses (but update state)
        if 0 < len(proof_requests):
            conversation = proof_requests[0]
            conversation.status = state
            conversation.save()

    return Response("{}")

def remove_credential(agent, connection_id, initialize_agent=False):
    """
    Fetch credentials from the agent (wallet).
    """

    # start the agent if requested (and necessary)     
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    credentials = None

    try:
        response = requests.delete(
            agent.admin_endpoint
            + "/credential/" + connection_id,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return credentials

def build_credential_proposal(agent, connection, credential_attrs, cred_def_id, issuer_did, schema_id, schema_issuer_did):
    credential_proposal = {
        "credential_proposal": {
            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
            "attributes": credential_attrs
        },
        'connection_id': connection.guid,
        'comment': "Issued by " + agent.agent_name,
        'schema_name': 'serpro',
        'schema_version': '1.0',
        'issuer_did': schema_issuer_did,
        'schema_issuer_did': schema_issuer_did,
        "auto_remove": False,
        'cred_def_id': cred_def_id,
        'schema_id': schema_id
    }
    return credential_proposal


def send_credential_proposal(agent, connection, credential_attrs, cred_def_id, schema, initialize_agent=False):
    """
    Send a Credential Offer.
    """

    # start the agent if requested (and necessary)

    issuer_did = schema[0].ledger_schema_id
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)
    schema_id = schema[0].ledger_schema_id
    schema_issuer_did = schema_id[:22]

    try:

        credential_proposal = build_credential_proposal(agent, connection, credential_attrs, cred_def_id, issuer_did, schema_id, schema_issuer_did)

        response = requests.post(
            agent.admin_endpoint
            + "/issue-credential/send-proposal",
            json.dumps(credential_proposal),
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )

        response.raise_for_status()

        my_cred_exchange = response.json()

        conversation = AgentConversation(
            connection = connection,
            conversation_type = CRED_EXCH_CONVERSATION,
            guid = my_cred_exchange["credential_exchange_id"],
            status = my_cred_exchange["state"])
        conversation.save()

    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return conversation


def remove_issue_credential(agent, connection_id, initialize_agent=False):
    """
    Fetch credentials from the agent (wallet).
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    credentials = None

    try:
        response = requests.post(
            agent.admin_endpoint
            + "/issue-credential/records/" + connection_id + "/remove",
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return credentials


def revoke_credential(agent, rev_reg_id, cred_rev_id, initialize_agent=False):
    """
    Revoke credencial
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    revoke_status = None

    credential_definition_body = {"rev_reg_id": rev_reg_id,
                                  "cred_rev_id": cred_rev_id,
                                  "publish": True}
    # create connection and check status
    try:
        response = requests.post(
            agent.admin_endpoint
            + "/revocation/revoke",
            json.dumps(credential_definition_body),
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        revoke_status = response
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return revoke_status

def send_simple_message(agent, conn_id, message, initialize_agent=False):
    """
    Send simple message
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    message_status = None

    message = {"content": message }
    connection = AgentConnection.objects.filter(agent=agent, guid=conn_id).get()

    # create connection and check status
    try:
        response = requests.post(
            agent.admin_endpoint
            + "/connections/" + conn_id + "/send-message",
            json.dumps(message),
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        message_status = response

    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return message_status

def delete_connection_record(agent, connection_id, initialize_agent=False):
    """
    Fetches the Connection object from the agent.
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    connection = None

    # create connection and check status
    try:
        response = requests.delete(
            agent.admin_endpoint
            + "/connections/"
            + connection_id,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        connection = response.json()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)

    return connection

def get_revoke_registry(agent, revocation_registry_id, initialize_agent=False):
    """
    Fetch credentials from the agent (wallet).
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    revoke_status = None

    try:
        response = requests.get(
            agent.admin_endpoint
            + "/revocation/registry/" + revocation_registry_id,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
        revoke_status = response.json()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return revoke_status


def remove_proof(agent, conversation_id, initialize_agent=False):
    """
    Fetch credentials from the agent (wallet).
    """

    # start the agent if requested (and necessary)
    (agent, agent_started) = start_agent_if_necessary(agent, initialize_agent)

    proofs = None

    try:
        response = requests.delete(
            agent.admin_endpoint
            + "/present-proof/records/" + conversation_id,
            headers=get_ADMIN_REQUEST_HEADERS(agent)
        )
        response.raise_for_status()
    except:
        raise
    finally:
        if agent_started:
            stop_agent(agent)
    return proofs