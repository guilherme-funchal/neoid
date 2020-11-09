from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

import operator
import pyqrcode
import sweetify
import pkce
import datetime


from urllib3.exceptions import InsecureRequestWarning #added
import requests
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#from django.views.decorators.csrf import csrf_exempt
from .forms import *
#from .models import *
#from .wallet_utils import *
from .registration_utils import *
#from .agent_utils import *
from .neoid import *
import json

USER_ROLE = getattr(settings, "DEFAULT_USER_ROLE", 'User')
ORG_ROLE = getattr(settings, "DEFAULT_ORG_ROLE", 'Admin')

###############################################################
# UI views to support user and organization registration
###############################################################

# Sign up as a site user, and create an agent
def user_signup_view(
    request,
    template=''
    ):
    """
    Create a user account with a managed agent.
    """

    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            mobile_agent = form.cleaned_data.get('mobile_agent')

            user = authenticate(username=username, password=raw_password)

            if Group.objects.filter(name=USER_ROLE).exists():
                user.groups.add(Group.objects.get(name=USER_ROLE))
            user.save()

            # create an Indy agent - derive agent name from email, and re-use raw password
            user = user_provision(user, raw_password, mobile_agent=mobile_agent)

            # TODO need to auto-login with Atria custom user
            #login(request, user)

            handle_alert(request, message=trans('User created'), type='success')
            return redirect('login')
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Sign up as an org user, and create a agent
def org_signup_view(
    request,
    template=''
    ):
    """
    Signup an Organization with a managed agent.
    Creates a user account and links to the Organization.
    """

    if request.method == 'POST':
        form = OrganizationSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            managed_agent = form.cleaned_data.get('managed_agent')
            admin_port = form.cleaned_data.get('admin_port')
            admin_endpoint = form.cleaned_data.get('admin_endpoint')
            http_port = form.cleaned_data.get('http_port')
            http_endpoint = form.cleaned_data.get('http_endpoint')
            api_key = form.cleaned_data.get('api_key')
            webhook_key = form.cleaned_data.get('webhook_key')

            user = authenticate(username=username, password=raw_password)
            user.managed_agent = False

            if Group.objects.filter(name='Admin').exists():
                user.groups.add(Group.objects.get(name='Admin'))
            user.save()

            # create and provision org, including org agent
            org_name = form.cleaned_data.get('org_name')
            org_role_name = form.cleaned_data.get('org_role_name')
            org_ico_url = form.cleaned_data.get('ico_url')
            org_role, created = AriesOrgRole.objects.get_or_create(name=org_role_name)
            org = org_signup(user, raw_password, org_name, org_role=org_role, org_ico_url=org_ico_url,
                managed_agent=managed_agent, admin_port=admin_port, admin_endpoint=admin_endpoint,
                http_port=http_port, http_endpoint=http_endpoint,
                api_key=api_key, webhook_key=webhook_key)

            # TODO need to auto-login with Atria custom user
            #login(request, user)

            return redirect('login')
    else:
        form = OrganizationSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


###############################################################
# Agent callback web service
###############################################################
TOPIC_CONNECTIONS = "connections"
TOPIC_CONNECTIONS_ACTIVITY = "connections_actvity"
TOPIC_CREDENTIALS = "issue_credential"
TOPIC_PRESENTATIONS = "present_proof"
TOPIC_GET_ACTIVE_MENU = "get-active-menu"
TOPIC_PERFORM_MENU_ACTION = "perform-menu-action"
TOPIC_PROBLEM_REPORT = "problem-report"
TOPIC_MESSAGE = "basicmessages"


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def agent_cb_view(
    request,
    cb_key,
    topic,
    format=None
    ):
    """
    Handle callbacks from the Aries agents.
    cb_key maps the callback to a specific agent.
    """
    payload = request.data

    agent = AriesAgent.objects.filter(callback_key=cb_key).get()

    if topic == TOPIC_CONNECTIONS:
        # handle connections callbacks
        return handle_agent_connections_callback(agent, topic, payload)

    elif topic == TOPIC_CONNECTIONS_ACTIVITY:
        # handle connections activity callbacks
        return handle_agent_connections_activity_callback(agent, topic, payload)

    elif topic == TOPIC_CREDENTIALS:
        # handle credentials callbacks
        return handle_agent_credentials_callback(agent, topic, payload)

    elif topic == TOPIC_PRESENTATIONS:
        # handle credentials callbacks
        return handle_agent_proof_callback(agent, topic, payload)

    elif topic == TOPIC_MESSAGE:
        # handle credentials callbacks
        return handle_message_callback(agent, topic, payload)


    # not yet handled message types
    print(">>> unhandled callback:", agent.agent_name, topic)
    return Response("{}")


###############################################################
# UI views to support Django wallet login/logoff
###############################################################
def agent_for_current_session(request):
    """
    Determine the current active agent
    """

    agent_name = request.session['agent_name']
    agent = AriesAgent.objects.filter(agent_name=agent_name).first()

    # validate it is the correct wallet
    agent_type = request.session['agent_type']
    agent_owner = request.session['agent_owner']


    if agent_type == 'user':
        # verify current user owns agent
        if agent_owner == request.user.email:
            return (agent, agent_type, agent_owner)
        raise Exception('Error agent/session config is not valid')
    elif agent_type == 'org':
        # verify current user has relationship to org that owns agent
        for org in request.user.ariesrelationship_set.all():
            if org.org.org_name == agent_owner:
                return (agent, agent_type, agent_owner)
        raise Exception('Error agent/session config is not valid')
    else:
        raise Exception('Error agent/session config is not valid')


###############################################################
# UI views to support wallet and agent UI functions
###############################################################
def profile_view(
    request,
    template='aries/profile.html'
    ):
    """
    List Connections for the current agent.
    """

# expects a agent to be opened in the current session
    (agent, agent_type, agent_owner) = agent_for_current_session(request)


    if agent_type == 'user':
        connections = AriesUser.objects.filter(email=agent_owner).all()
    else:
        name = agent_owner.split()
        first_name = name[0]
        connections = AriesUser.objects.filter(first_name=first_name).all()
    return render(request, template,
        {'agent_name': agent.agent_name, 'connections': connections})


def data_view(
    request,
    template=''
    ):
    """
    Example of user-defined view for Data tab.
    """
    return render(request, 'aries/data.html')

def wallet_view(
   request
    ):
    """
    List info about wallet.
    """
    try:
        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        wallets = get_wallet_dids(agent)
        return render(request, 'aries/wallet/list.html', {'agent_name': agent.agent_name, 'wallets': wallets})
    except:
        raise
    finally:
        pass

import importlib

def plugin_view(request, view_name):
    """
    Find and invoke user-defined view.
    These are configured in settings file.
    """

    view_function = getattr(settings, view_name)

    mod_name, func_name = view_function.rsplit('.',1)
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)

    return func(request)


######################################################################
# views to create and confirm agent-to-agent connections
######################################################################
def list_connections(
    request,
    template='aries/connection/list.html'
    ):
    """
    List Connections for the current agent.
    """

    # expects a agent to be opened in the current session
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    data_source = "["

    onboard = settings.ONBOARD['ORG']

    if agent_type == 'user':
        data_source += "[{'v':'" + agent_owner + "', 'f':'" + agent_owner + "<div><br>" \
                       + \
                       '<a onclick="listOrg()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-university"></i>Organização</a>' \
                       '<a href="../connection_response" class="w3-bar-item w3-button w3-padding"><i class="fa fa-user-secret"></i>Externo</a>' \
                       + "</div>'},'','']"

        connections = AgentConnection.objects.filter(agent=agent).all()
        invitations = AgentInvitation.objects.filter(agent=agent, connecion_guid='').all()

        exclude_filter = AgentConnection.objects.filter(agent=agent).values_list('partner_name', flat=True)
        list = AriesOrganization.objects.values_list('org_name', flat=True)
        size = len(list)
        org = {}
        for organization in list:
            org[organization] = organization

        for connection in connections:
            img = "/static/serpro/o_" + connection.partner_name + ".png"

            #        data_source += "['" + connection.partner_name + "','" + agent_owner + "', ''],"


            credentials = IndyCredentialDefinition.objects.get(
            creddef_name=connection.partner_name + "-o_" + connection.partner_name)
            schema_attrs = credentials.creddef_template
            credential_name = credentials.creddef_name
            schema_attrs = json.loads(schema_attrs)

            if onboard == connection.partner_name:
                data_source += ",[{'v':'" + connection.partner_name + "', 'f':'Organização<div><br>" + \
                               '<img src =' + img + ' title = "o_serpro" alt = "o_serpro" /><br><br>' \
                               '<button  id=' + connection.guid + ' onclick="infoConnection(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-info-circle"></i></button>' \
                               + "</div>'},'" + agent_owner + "','']"
            else:
                data_source += ",[{'v':'" + connection.partner_name + "', 'f':'Organização<div><br>" + \
                               '<img src ='+ img +' title = "o_serpro" alt = "o_serpro" /><br><br>' \
                               '<button  id=' + connection.guid + ' onclick="removeConnection(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-remove"></i></button>' \
                               + "</div>'},'" + agent_owner + "','']"

        data_source += "]"
        proof = {}
        field = {}
        field2 = {}


    else:
        data_source += "[{'v':'" + agent_owner + "', 'f':'" + agent_owner + "<div><br>" \
                       + \
                       '<a id='+ agent_owner +' onclick="invitePerson()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-user"></i>Pessoa</a>' \
                       '<a href="../connection_response" class="w3-bar-item w3-button w3-padding"><i class="fa fa-user-secret"></i>Externo</a>' \
                       + "</div>'},'','']"

        connections = AgentConnection.objects.filter(agent=agent).all()
        invitations = AgentInvitation.objects.filter(agent=agent, connecion_guid='').all()

        exclude_filter = AgentConnection.objects.filter(agent=agent).values_list('partner_name', flat=True)
        list = AriesOrganization.objects.values_list('org_name', flat=True)


        size = len(list)

        org = {}
        for organization in list:
            org[organization] = organization


        proofs = IndyProofRequest.objects.filter(active="True", expiration__gte=datetime.now()).all()
        credentials = fetch_credentials(agent)
        initialize_agent = False

        proof = {}
        for prf in proofs:
            email = prf.agent
            org = prf.schema
            org = org.replace("[", "").replace("]", "").replace("'", "")
            org = 'o_'+org
            credentials = AgentConversation.objects.filter(connection__agent=org, conversation_type='CredExchange').exclude(status='credential_revoked').all()
            count = len(credentials)

            if count >= 1:
                proof[prf.proof_req_name] = prf.proof_req_name
            else:
                proof[prf.proof_req_name] = ""

        credentials = IndyCredentialDefinition.objects.get(agent__agent_name=agent.agent_name)
        credential = credentials.creddef_template
        attribs = json.loads(credential)

        field = ""
        field2 = ""

        for value in attribs:
            field += "'<label>" + value + ": </label><input id=" + value + " class=" + value + "><br><br>'"
            field2 += "document.getElementById('" + value + "').value"

        field = field.replace(">''<", ">' + '<")
        field2 = field2.replace("valuedocument", "value, document")

        for connection in connections:

            #        data_source += "['" + connection.partner_name + "','" + agent_owner + "', ''],"
            data_source += ",[{'v':'" + connection.partner_name + "', 'f':'" + connection.partner_name + "<div><br>" + \
                            '<button  id=' + connection.guid + '&connection_partner_name=' + connection.partner_name + ' onclick="sendCredential(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-file-archive-o"></i></button >' \
                            '<button  id=' + connection.guid + ' onclick="removeConnection(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-remove"></i></button>' \
                            '<button  id=' + connection.guid + ' onclick="listProof(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-refresh"></i></button >' \
                            '<button  id=' + connection.guid + ' onclick="sendMessage(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-pencil-square-o"></i></button >' \
                            + "</div>'},'" + agent_owner + "','']"

        data_source += "]"

    data = data_source

    credentials = IndySchema.objects.all()
    cont = 0
    schemas = []
    for credential in credentials:
        schema_attrs = credentials[cont].schema_template
        credential_name = credentials[cont].schema_name
        schema_attrs = json.loads(schema_attrs)
        schemas.append({"name": credential_name, "schema_attrs": schema_attrs})
        cont = cont + 1


    if agent_type == 'user':
        return render(request, template,{'agent_name': agent.agent_name, 'connections': connections, 'invitations': invitations, 'data': data, 'org': org, 'proof': proof, 'field': field, 'field2': field2, 'schemas': schemas})
    else:
        credentials = IndyCredentialDefinition.objects.filter(agent__agent_name=agent.agent_name).all()
        schema_attrs = credentials[0].creddef_template
        credential_name = credentials[0].creddef_name
        schema_attrs = json.loads(schema_attrs)

        return render(request, template,
                      {'agent_name': agent.agent_name, 'connections': connections, 'invitations': invitations,'data': data, 'org': org, 'proof': proof, 'field': field, 'field2': field2, 'schema_attrs': schema_attrs, 'credential_name': credential_name, 'proofs': proofs})


def list_connections_org(
    request,
    template='aries/connection/list_org.html'
    ):
    """
    List Connections for the current agent.
    """

    # expects a agent to be opened in the current session
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    guid = request.GET.get('connection.guid')

    data_source = "["

    data_source += "[{'v':'" + agent_owner + "', 'f':'" + agent_owner + "<div><br>" \
                   + \
                   '<a id=' + agent_owner + ' onclick="invitePerson()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-user"></i>Pessoa</a>' \
                                            '<a href="../connection_response" class="w3-bar-item w3-button w3-padding"><i class="fa fa-user-secret"></i>Externo</a>' \
                   + "</div>'},'','']"

    connections = AgentConnection.objects.filter(guid=guid).all()

    invitations = AgentInvitation.objects.filter(agent=agent, connecion_guid='').all()

    exclude_filter = AgentConnection.objects.filter(agent=agent).values_list('partner_name', flat=True)
    list = AriesOrganization.objects.values_list('org_name', flat=True)
    size = len(list)

    org = {}
    for organization in list:
        org[organization] = organization

    partners = AgentConnection.objects.get(guid=guid)
    partner_name = partners.partner_name
    now = datetime.now()
    proofs = IndyProofRequest.objects.filter(active="True", agent=partner_name, expiration__gte=datetime.now())

    proof = {}
    for prf in proofs:
        proof[prf.proof_req_name] = prf.proof_req_name

    credentials = IndyCredentialDefinition.objects.get(agent__agent_name=agent.agent_name)

    credential = credentials.creddef_template
    attribs = json.loads(credential)

    field = ""
    field2 = ""

    for value in attribs:
        field += "'<label>" + value + ": </label><input id=" + value + " class=" + value + "><br><br>'"
        field2 += "document.getElementById('" + value + "').value"

    field = field.replace(">''<", ">' + '<")
    field2 = field2.replace("valuedocument", "value, document")

    for connection in connections:
        #        data_source += "['" + connection.partner_name + "','" + agent_owner + "', ''],"
        data_source += ",[{'v':'" + connection.partner_name + "', 'f':'" + connection.partner_name + "<div><br>" + \
                       '<button  id=' + connection.guid + ' onclick="removeConnection(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-remove"></i></button >' \
                       '<button  id=' + connection.guid + ' onclick="sendMessage(this.id)"> <class="w3-bar-item w3-button w3-padding"><i class="fa fa-pencil-square-o"></i></button >' \
                       + "</div>'},'" + agent_owner + "','']"

    data_source += "]"
    form = ""

    credentials = IndyCredentialDefinition.objects.filter(agent__agent_name=agent.agent_name).all()
    schema_attrs = credentials[0].creddef_template
    credential_name = credentials[0].creddef_name
    schema_attrs = json.loads(schema_attrs)

    data = data_source

    return render(request, template,{'agent_name': agent.agent_name, 'connections': connections, 'invitations': invitations, 'data': data,'org': org, 'proof': proof, 'field': field, 'field2': field2, 'schema_attrs': schema_attrs, 'credential_name': credential_name})


def handle_connection_request_organization(request, onboard=False):
    """
    Send a Connection request and approves automatic invitation from person to organization
    """

    if onboard is False:
        id = request.GET.get('org')
    else:
        id = onboard

    partner_name_tmp = AriesOrganization.objects.filter(org_name=id).get()
    partner_name = partner_name_tmp

    # get user or org associated with this agent

    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    org = AriesOrganization.objects.filter(org_name=partner_name).get()
    partner_name = agent_owner
    target_user = get_user_model().objects.filter(email=partner_name).all()
    target_org = AriesOrganization.objects.filter(org_name=id).all()

    their_agent = target_org[0].agent

    try:
        my_connection = request_connection_invitation(org, partner_name)
        connecion_guid = my_connection.guid

        if their_agent is not None:
            their_invitation = AgentInvitation(
                agent=their_agent,
                partner_name=partner_name_tmp,
                invitation=my_connection.invitation,
                invitation_url=my_connection.invitation_url,
            )
            their_invitation.save()

        invitations = AgentInvitation.objects.filter(id=their_invitation.id).all()

        agent_name = invitations[0].agent.agent_name

        # approves automatic invitation from person to organization
        partner_name = invitations[0].partner_name

        invitation_details = invitations[0].invitation

        (agent, agent_type, agent_owner) = agent_for_current_session(request)

        orgazinational_connection = receive_connection_invitation(agent, partner_name, invitation_details)
        time.sleep(0.5)

        connecion_guid = orgazinational_connection.guid
        invitation = AgentInvitation.objects.filter(id=their_invitation.id).get()

        invitation.connecion_guid = orgazinational_connection.guid
        invitation.save()

        if my_connection.agent.agent_org.get():
            source_name = my_connection.agent.agent_org.get().org_name
            time.sleep(0.5)
        else:
            source_name = my_connection.agent.agent_user.get().email
            time.sleep(0.5)

        target_name = my_connection.partner_name

        #               institution_logo_url = 'https://anon-solutions.ca/favicon.ico'

        if onboard is False:
            handle_alert(request, message=trans('Created connection'), type='success')
            return redirect('/connections/')
        else:
            connections = AgentConnection.objects.filter(partner_name=onboard, agent=agent).all()
            my_connection = connections[0]
            schema = IndySchema.objects.filter(schema_name=onboard).all()
            connection_id = connections[0].guid
            cred_defs = IndyCredentialDefinition.objects.filter(creddef_name=onboard + "-o_" + onboard).all()
            cred_def_id = cred_defs[0].ledger_creddef_id
            connections = AriesUser.objects.filter(email=agent_owner).values()
            attributes = list(connections)

            cred_attrs = []
            schema_attrs = cred_defs[0].creddef_template
            schema_attrs = json.loads(schema_attrs)

            for attr in schema_attrs:
                field_name = 'schema_attr_' + attr
                field_value = attributes[0].get(attr)
                cred_attrs.append({"name": attr, "value": field_value})
            my_conversation = send_credential_proposal(agent, my_connection, cred_attrs, cred_def_id, schema, connection_id)
            handle_alert(request, message=trans('Created connection and credential proposal'), type='info')
            return redirect('/view_dashboard/')


    except Exception as e:
        # ignore errors for now
        print(" >>> Failed to create request for", agent.agent_name)
        print(e)
        handle_alert(request, message=trans('Failed to create connection'), type='error')
        return redirect('/connections/')


def handle_connection_request(
    request,
    form_template='aries/connection/request.html',
    response_template='aries/connection/form_connection_info.html'
    ):
    """
    Send a Connection request (i.e. an Invitation).
    """

    email = request.GET.get('email')

    target_user = get_user_model().objects.filter(email=email).all()


    # get user or org associated with this agent
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    their_agent = target_user[0].agent
    org = AriesOrganization.objects.filter(org_name=agent_owner).get()

    try:
        my_connection = request_connection_invitation(org, email)

        if their_agent is not None:
            their_invitation = AgentInvitation(
                agent=their_agent,
                partner_name=agent_owner,
                invitation=my_connection.invitation,
                invitation_url=my_connection.invitation_url,
            )
            their_invitation.save()

        if my_connection.agent.agent_org.get():
            source_name = my_connection.agent.agent_org.get().org_name
        else:
            source_name = my_connection.agent.agent_user.get().email
        target_name = my_connection.partner_name
        #               institution_logo_url = 'https://anon-solutions.ca/favicon.ico'

        handle_alert(request, message=trans('Invitation created') , type='success')
        return redirect('/connections/')

    except Exception as e:
        # ignore errors for now
        print(" >>> Failed to create request for", agent.agent_name)
        print(e)
        handle_alert(request, message=trans('Invitation not created'), type='error')
        return redirect('/connections/')


def handle_connection_response(
    request,
    form_template='aries/connection/response.html',
    response_template='aries/form_response.html'
    ):
    """
    Respond to (Accept) a Connection request.
    """

    if request.method=='POST':
        form = SendConnectionResponseForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': trans('Form error'), 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            invitation_id = cd.get('invitation_id')
            partner_name = cd.get('partner_name')
            invitation_details = cd.get('invitation_details')
            invitation_url = cd.get('invitation_url')


            # get user or org associated with this agent
            (agent, agent_type, agent_owner) = agent_for_current_session(request)

            # set agent password
            # TODO vcx_config['something'] = raw_password

            # build the connection and get the invitation data back
            try:
                my_connection = receive_connection_invitation(agent, partner_name, invitation_details)
                invitation = AgentInvitation.objects.filter(id=invitation_id, agent=agent).get()
                invitation.connecion_guid = my_connection.guid
                invitation.save()

#               return render(request, response_template, {'msg': trans('Updated conversation for') + ' ' + agent.agent_name})
                handle_alert(request, message=trans('Updated conversation'), type='success')
                return redirect('/connections/')

            except IndyError:
                # ignore errors for now
                print(" >>> Failed to update request for", agent.agent_name)
                return render(request, 'aries/form_response.html', {'msg': 'Failed to update request for ' + agent.agent_name})

    else:
        # find connection request
        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        invitation_id = request.GET.get('id', None)
        invitations = []
        if invitation_id:
            invitations = AgentInvitation.objects.filter(id=invitation_id, agent=agent).all()
        if len(invitations) > 0:
            form = SendConnectionResponseForm(initial={ 'invitation_id': invitation_id,
                                                        'agent_name': invitations[0].agent.agent_name, 
                                                        'partner_name': invitations[0].partner_name, 
                                                        'invitation_details': invitations[0].invitation,
                                                        'invitation_url': invitations[0].invitation_url,
                                                         })
        else:
            (agent, agent_type, agent_owner) = agent_for_current_session(request)
            form = SendConnectionResponseForm(initial={'invitation_id': 0, 'agent_name': agent.agent_name})

        return render(request, form_template, {'form': form, 'invitation_id': invitation_id})
    

def poll_connection_status(
    request,
    form_template='aries/connection/status.html',
    response_template='aries/form_response.html'
    ):
    """
    Poll Connection status (normally a background task).
    """

    if request.method=='POST':
        form = PollConnectionStatusForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')

            # log out of current agent, if any
            (agent, agent_type, agent_owner) = agent_for_current_session(request)

            # set agent password
            # TODO vcx_config['something'] = raw_password

            connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()

            # TODO validate connection id
            my_connection = connections[0]

            # validate connection and get the updated status
            try:
                my_state = check_connection_status(agent, my_connection.guid)

                return render(request, response_template, {'msg': trans('Updated conversation for') + ' ' + agent.agent_name + ', ' + my_connection.partner_name})
            except Exception as e:
                # ignore errors for now
                print(" >>> Failed to update request for", agent.agent_name, e)
                return render(request, 'aries/form_response.html', {'msg': 'Failed to update request for ' + agent.agent_name})

    else:
        # find connection request
        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        connection_id = request.GET.get('id', None)
        connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()

        form = PollConnectionStatusForm(initial={ 'connection_id': connection_id,
                                                  'agent_name': connections[0].agent.agent_name })

        return render(request, form_template, {'form': form})


def connection_qr_code(
    request,
    token
    ):
    """
    Display a QR code for the given invitation.
    """

    # find connection for requested token
    connections = AgentInvitation.objects.filter(id=token).all()
    if 0 == len(connections):
        return render(request, 'aries/form_response.html', {'msg': 'No connection found'})

    connection = connections[0]
    qr = pyqrcode.create(connection.invitation_url)
    path_to_image = '/tmp/'+token+'-qr-offer.png'
    qr.png(path_to_image, scale=2, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
    image_data = open(path_to_image, "rb").read()


    # serialize to HTTP response
    response = HttpResponse(image_data, content_type="image/png")

    #image.save(response, "PNG")
    return response
#    return response


######################################################################
# views to offer, request, send and receive credentials
######################################################################
def check_connection_messages(
    request,
    form_template='aries/connection/check_messages.html',
    response_template='aries/form_response.html'
    ):
    """
    Poll Connections for outstanding messages (normally a background task).
    """

    if request.method=='POST':
        form = PollConnectionStatusForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')

            # log out of current wallet, if any
            (agent, agent_type, agent_owner) = agent_for_current_session(request)
    
            if connection_id > 0:
                connections = AgentConnection.objects.filter(wallet=wallet, id=connection_id).all()
            else:
                connections = AgentConnection.objects.filter(wallet=wallet).all()

            total_count = 0
            for connection in connections:
                # check for outstanding, un-received messages - add to outstanding conversations
                if connection.connection_type == 'Inbound':
                    msg_count = handle_inbound_messages(wallet, connection)
                    total_count = total_count + msg_count

            return render(request, response_template, {'msg': 'Received message count = ' + str(total_count)})

    else:
        # find connection request
        connection_id = request.GET.get('connection_id', None)
        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        if connection_id:
            connections = AgentConnection.objects.filter(wallet=wallet, id=connection_id).all()
        else:
            connection_id = 0
            connections = AgentConnection.objects.filter(wallet=wallet).all()
        # TODO validate connection id
        form = PollConnectionStatusForm(initial={ 'connection_id': connection_id,
                                                  'wallet_name': connections[0].wallet.wallet_name })

        return render(request, form_template, {'form': form})


def list_conversations(
    request,
    template='aries/conversation/list.html'
    ):
    """
    List Conversations for the current wallet.
    """

    # expects a wallet to be opened in the current session
    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    conversations = AgentConversation.objects.filter(connection__agent=agent).all()
    messages = AgentMessage.objects.filter(connection__agent=agent).all()

    agent_type = request.session['agent_type']

    return render(request, template, {'agent_name': agent.agent_name, 'conversations': conversations, 'agent_type': agent_type, 'messages': messages})

def handle_select_credential_offer(
    request,
    form_template='aries/credential/select_offer.html',
    response_template='aries/credential/offer.html'
    ):
    """
    Select a Credential Definition and display a form to enter Credential Offer information.
    """

    if request.method=='POST':
        form = SelectCredentialOfferForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')
            cred_def = cd.get('cred_def')
            partner_name = cd.get('partner_name')

            credential_name = cred_def.creddef_name
            cred_def_id = cred_def.ledger_creddef_id

            # log out of current wallet, if any
            (agent, agent_type, agent_owner) = agent_for_current_session(request)

            connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()

            # TODO validate connection id
            schema_attrs = cred_def.creddef_template
            form = SendCredentialOfferForm(initial={ 'connection_id': connection_id,
                                                     'agent_name': connections[0].agent.agent_name,
                                                     'partner_name': partner_name,
                                                     'cred_def': cred_def_id,
                                                     'schema_attrs': schema_attrs,
                                                     'credential_name': credential_name })
            return render(request, response_template, {'form': form})

    else:
        # find conversation request

        connection_id = request.GET.get('connection_id', None)

        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()

        partner_name = connections[0].partner_name


        connection = connections[0]
        partner_credentials = AgentConversation.objects.filter(connection=connection, revoked='').all()
        test = len(partner_credentials)


        if test > 0:

            for partner_credential in partner_credentials:
                guid = partner_credential.guid
                cred = AgentConversation.objects.filter(guid=guid).get()

                if cred.status == 'credential_acked':
                    handle_alert(request, message=trans('Recipient already has an active credential'), type='error')
                    return redirect('/connections/')
                elif cred.status == 'offer_sent':
                    handle_alert(request, message=trans('Recipient have credencial waiting to aprove'), type='error')
                    return redirect('/connections/')

        #If number of IndyCredentialDefinition equal one don't need to choose

        credential = IndyCredentialDefinition.objects.filter(agent__agent_name=agent.agent_name).all()

        cont = len(credential)

        if cont == 1:
            form = SendCredentialOfferForm(initial={'connection_id': connection_id,
                                                    'agent_name': agent.agent_name,
                                                    'partner_name': connections[0].partner_name,
                                                    'cred_def': credential[0].ledger_creddef_id,
                                                    'schema_attrs': credential[0].creddef_template,
                                                    'credential_name': credential[0].creddef_name})
            return render(request, response_template, {'form': form})
        else:
        # TODO validate connection id
            form = SelectCredentialOfferForm(initial={ 'connection_id': connection_id,
                                                    'partner_name': connections[0].partner_name,
                                                    'agent_name': connections[0].agent.agent_name})

            return render(request, form_template, {'form': form})

def handle_credential_offer(
    request
    ):
    """
    Send a Credential Offer.
    """
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    data = request.POST
    credential_name = request.POST.get("credential_name")
    connection_id = request.POST.get("connection_id")
    partner_name = request.POST.get("partner_name")

    connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()
    my_connection = connections[0]


    cred_defs = IndyCredentialDefinition.objects.filter(creddef_name=credential_name, agent=agent).all()
    cred_def = cred_defs[0]
    cred_def_id = cred_def.ledger_creddef_id

    cred_attrs = []
    for attr, value in data.items():
        if not attr.find("schema_attr_"):
            attr = attr.replace("schema_attr_", "")
            cred_attrs.append({"name": attr, "value": value})


    partner_credentials = AgentConversation.objects.filter(connection=my_connection, conversation_type='CredExchange').exclude(status='credential_revoked').all()

    try:
        if len(partner_credentials) == 0:
            my_conversation = send_credential_offer(agent, my_connection, cred_attrs, cred_def_id)
            handle_alert(request, message=trans('Updated conversation'), type='success')
            return redirect('/connections/')
        else:
            handle_alert(request, message=trans('Recipient already has an active credential'), type='error')
            return redirect('/connections/')
    except:
        # ignore errors for now
        handle_alert(request, message=trans('Failed to update conversation'), type='error')
        return redirect('/connections/')

def handle_credential_import(
    request
    ):
    """
    Send a Credential Offer.
    """
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    connection_id = request.GET.get('connection_id', None)
    connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()
    my_connection = connections[0]
    email = my_connection.email

    agent_name = str(agent)
    credential_name = agent_owner + "-" + agent_name

    cred_defs = IndyCredentialDefinition.objects.filter(creddef_name=credential_name, agent=agent).all()
    cred_def = cred_defs[0]
    cred_def_id = cred_def.ledger_creddef_id

    user = AriesUser.objects.filter(email=email).all()


def handle_alert(request, message, type):
    if type == 'success':
        sweetify.success(request, title='', text=message, persistent=True, backdrop=False,icon='success')
    if type == 'error':
        sweetify.success(request, title='', text=message, persistent=True, backdrop=False,icon='error')
    if type == 'info':
        sweetify.success(request, title='', text=message, persistent=True, backdrop=False,icon='info')
    if type == 'warning':
        sweetify.success(request, title='', text=message, persistent=True, backdrop=False,icon='warning')
    if type == 'question':
        sweetify.success(request, title='', text=message, persistent=True, backdrop=False,icon='question')

def handle_cred_offer_response(request):
    """
    Respond to a Credential Offer by sending a Credential Request.
    """

    conversation_id = request.GET.get('conversation_id', None)

    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    
    # find conversation request


    try:
        conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()
        my_conversation = conversations[0]
        # TODO validate conversation id
        my_connection = my_conversation.connection

        my_conversation = send_credential_request(agent, my_conversation)
        time.sleep(0.5)
        credentials = fetch_credentials(agent)
        handle_alert(request, message=trans('accepted credential'), type='success')
        return redirect('/conversations/')

    except:
        handle_alert(request, message=trans('accepted not credential '), type='error')
        return redirect('/conversations/')
    finally:
        pass


######################################################################
# views to request, send and receive proofs
######################################################################
def handle_select_proof_request(
    request,
    form_template='aries/proof/select_request.html',
    response_template='aries/proof/send_request.html',
    template='aries/form_response.html'
    ):
    """
    Select a Proof Request to send, based on the templates available in the database.
    """

    proof_request = request.POST.get("proof")
    connection_id = request.POST.get("connection_id")

    partner_agent = AgentConnection.objects.get(guid=connection_id)
    partner_name = partner_agent.partner_name

    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()
    # TODO validate connection id
    connection = connections[0]

    proof = IndyProofRequest.objects.get(proof_req_name=proof_request)

    proof_req_attrs = proof.proof_req_attrs

    proof_req_predicates = proof.proof_req_predicates

    # selective attribute substitutions
    institution_did = get_public_did(agent)
    proof_req_attrs = proof_req_attrs.replace('$ISSUER_DID', institution_did)
    proof_req_predicates = proof_req_predicates.replace('$ISSUER_DID', institution_did)

    proof_form = SendProofRequestForm(initial={
        'agent_name': connection.agent.agent_name,
        'connection_id': connection_id,
        'partner_name': partner_name,
        'proof_name': proof.proof_req_name,
        'proof_attrs': proof_req_attrs,
        'proof_predicates': proof_req_predicates})


    if proof_req_predicates == '[]':
        proof_req_attrs = json.loads(proof_req_attrs)

        requested_attrs = {}

        test = settings.REVOCATION

        if test == True:
            clk = int(time.time() - 1)
            revoked = {
                "to": clk,
                "from": clk
            }

            for requested_attr in proof_req_attrs:
                referent = requested_attr["name"] + "_referent"
                requested_attrs[referent] = requested_attr
                requested_attrs[referent].update(non_revoked=revoked)

        else:
            for requested_attr in proof_req_attrs:
                referent = requested_attr["name"] + "_referent"
                requested_attrs[referent] = requested_attr

        requested_predicates = {}

        try:
            conversation = send_proof_request(agent, connection, proof.proof_req_name, requested_attrs, requested_predicates)
            handle_alert(request, message=trans('Proof request was sent'), type='success')
            return redirect('/connections/')
        except:
            # ignore errors for now
            handle_alert(request, message=trans('Proof request not sent'), type='error')
            return redirect('/connections/')
    else:
        return render(request, response_template, {'form': proof_form})


def handle_send_proof_request(
    request,
    template='aries/form_response.html'
    ):
    """
    Send a Proof Request for the selected Proof Request.
    User can edit the requested attributes and predicates.
    """

    if request.method=='POST':
        form = SendProofRequestForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')
            proof_name = cd.get('proof_name')
            proof_attrs = cd.get('proof_attrs')
            proof_predicates = cd.get('proof_predicates')

            (agent, agent_type, agent_owner) = agent_for_current_session(request)
    
            connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()
            # TODO validate connection id
            my_connection = connections[0]

            proof_req_attrs = json.loads(proof_attrs)
            proof_req_predicates = json.loads(proof_predicates)

            requested_attrs = {}
            for requested_attr in proof_req_attrs:
                referent = requested_attr["name"] + "_referent"
                requested_attrs[referent] = requested_attr
            requested_predicates = {}
            for requested_predicate in proof_req_predicates:
                referent = requested_predicate["name"] + "_referent"
                requested_predicates[referent] = requested_predicate

            # build the proof request and send
            try:
                conversation = send_proof_request(agent, my_connection, proof_name, requested_attrs, requested_predicates)

#               return render(request, template, {'msg': trans('Updated conversation for') + ' ' + agent.agent_name})
                handle_alert(request, message=trans('Proof request was sent to'), type='success')
                return redirect('/connections/')

            except:
                # ignore errors for now
                print(" >>> Failed to update conversation for", agent.agent_name)
                handle_alert(request, message=trans('Failed to update conversation'), type='error')
                return redirect('/connections/')

    else:
        return render(request, 'aries/form_response.html', {'msg': 'Method not allowed'})

def handle_proof_req_response(
        request,
        form_template='aries/proof/send_response.html',
        response_template='aries/proof/select_claims.html',
        template='aries/form_response.html'
):
    """
    First stage in responding to a Proof Request - confirm to search for claims.
    """

    if request.method == 'POST':
        form = SendProofReqResponseForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:

            cd = form.cleaned_data
            conversation_id = cd.get('conversation_id')
            proof_req_name = cd.get('proof_req_name')

            (agent, agent_type, agent_owner) = agent_for_current_session(request)
            test = settings.REVOCATION
            # find conversation request
            conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()
            my_conversation = conversations[0]
            # TODO validate conversation id
            # TODO validate connection id
            my_connection = my_conversation.connection

            # find claims for this proof request and display for the user
            try:
                val = []
                attr = []
                supplied_attrs = {}
                data = {}
                supplied_predicates = {}
                supplied_self_attested_attrs = {}

                proof_request = get_agent_conversation(agent, conversation_id, PROOF_REQ_CONVERSATION)

                credentials = get_claims_for_proof_request(agent, my_conversation)

                if len(credentials) == 0:
                    return render(request, 'aries/form_response.html',{'msg': 'No credential with valid data ' + agent.agent_name})
                else:
                    connections = AgentConnection.objects.filter(agent=agent).all()


                    for connection in connections:

                        for credential in credentials:
                            value = credential['cred_info']['referent']
                            # fetch revoked credentials

                            if test == True:
                                cred_rev_id = credential['cred_info']['cred_rev_id']
                                rev_reg_id = credential['cred_info']['rev_reg_id']
                                states = AgentConversation.objects.filter(connection=connection, cred_rev_id=cred_rev_id, rev_reg_id=rev_reg_id).all()

                                for state in states:
                                    tmp = AgentConversation.objects.filter(guid=state.guid).get()
                                    credential['cred_info']['state'] = state.status
                                    credential['cred_info']['revoked'] = state.revoked

                    size = 0

                    #Remove revoked from credentials

                    if test == True:
                        if settings.ALERT_REVOKED_CREDENTIALS == True:
                            for i in range(len(credentials)):
                               if credentials[i]['cred_info']['state'] != "credential_revoked":
                                   data = credentials[i]
                                   size = size + 1
                        else:
                            data = credentials
                            size = size + 1

                    if len(data) == 0:
                        handle_alert(request, message=trans('You have a revoked credential, please check'),type='error')
                        return redirect('/conversations/')
                    else:
                        if size == 1:
                            for referent in proof_request["presentation_request"]["requested_attributes"]:
                                supplied_attrs[referent] = {"cred_id": value, "revealed": True}

                            proof_data = send_claims_for_proof_request(agent, my_conversation, supplied_attrs, supplied_predicates, supplied_self_attested_attrs)
                            handle_alert(request, message=trans('Sent proof request'), type='success')
                            return redirect('/conversations/')

                        else:
                            form = SelectProofReqClaimsForm(initial={
                                'conversation_id': conversation_id,
                                'agent_name': my_connection.agent.agent_name,
                                'from_partner_name': my_connection.partner_name,
                                'proof_req_name': proof_req_name,
                                'selected_claims': data,
                                'proof_request': proof_request,
                            })
                            return render(request, response_template, {'form': form})
            except Exception as e:
                # ignore errors for now
                print(" >>> Failed to find claims for", agent.agent_name, e)
                return render(request, 'aries/form_response.html',
                                {'msg': 'Failed to find claims for ' + agent.agent_name})

    else:
        # find conversation request, fill in form details
        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        conversation_id = request.GET.get('conversation_id', None)
        conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()
        # TODO validate conversation id
        conversation = conversations[0]
        # TODO validate connection id
        connection = conversation.connection
        proof_request = get_agent_conversation(agent, conversation_id, PROOF_REQ_CONVERSATION)

        for referent in proof_request["presentation_request"]["requested_attributes"]:

            form = SendProofReqResponseForm(initial={
                'conversation_id': conversation_id,
                'agent_name': agent.agent_name,
                'from_partner_name': connection.partner_name,
                'proof_req_name': proof_request['presentation_request']['name'],
            })

    return render(request, form_template, {'form': form})

def handle_proof_select_claims(
    request,
    template='aries/form_response.html'
    ):
    """
    Select claims to construct Proof for Proof Request.
    """

    if request.method=='POST':
        form = SelectProofReqClaimsForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            conversation_id = cd.get('conversation_id')
            proof_req_name = cd.get('proof_req_name')

            (agent, agent_type, agent_owner) = agent_for_current_session(request)


            # find conversation request
            conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()
            # TODO validate conversation id
            my_conversation = conversations[0]
            requested_proof = get_agent_conversation(agent, conversation_id, PROOF_REQ_CONVERSATION)
            # TODO validate connection id
            my_connection = my_conversation.connection

            # get selected attributes for proof request
            supplied_attrs = {}
            supplied_predicates = {}
            supplied_self_attested_attrs = {}

            # build array of credential id's (from wallet)
            for referent in requested_proof["presentation_request"]["requested_attributes"]:
                field_name = 'proof_req_attr_' + referent
                value = request.POST.get(field_name)
                if value.startswith('ref::'):
                    supplied_attrs[referent] = { "cred_id": value[5:], "revealed": True }
                else:
                    supplied_self_attested_attrs[referent] = value
            for referent in requested_proof["presentation_request"]["requested_predicates"]:
                field_name = 'proof_req_attr_' + referent
                value = request.POST.get(field_name)
                if value.startswith('ref::'):
                    supplied_predicates[referent] = { "cred_id": value[5:] }
                else:
                    # shouldn't happen ...
                    supplied_predicates[referent] = { "cred_id": value }

            # send claims for this proof request to requestor
            try:
#               proof_data = send_claims_for_proof_request(agent, my_conversation, supplied_attrs, supplied_predicates, supplied_self_attested_attrs)

                return render(request, template, {'msg': trans('Sent proof request for') + ' ' + agent.agent_name})
            except Exception as e:
                # ignore errors for now
                print(" >>> Failed to find claims for", agent.agent_name, e)
                return render(request, 'aries/form_response.html', {'msg': 'Failed to find claims for ' + agent.agent_name})

    else:
        return render(request, 'aries/form_response.html', {'msg': 'Method not allowed'})

def handle_view_proof(
    request,
    template='aries/proof/view_proof.html',
    template_request_received='aries/proof/view_proof_request_receive.html'
    ):
    """
    View the Proof sent by the Prover.
    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    conversation_id = request.GET.get('conversation_id', None)
    conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()

    # TODO validate conversation id
    conversation = conversations[0]

    requested_proof = get_agent_conversation(agent, conversation_id, PROOF_REQ_CONVERSATION)

    screen = {}

    test = settings.REVOCATION

    if agent_type == 'org':
        if test == True:
            revoked = requested_proof["verified"]
            if revoked == 'false':
                conversation.status = "credential_revoked"
                conversation.save()

    if requested_proof["state"] == "request_received":
        name = (requested_proof["presentation_request"]["name"])
        for attr, value in requested_proof["presentation_request"]["requested_attributes"].items():
            attr = attr.replace('_referent', '')
            screen[attr] = value

        html = '<h4><p style="text-align:left;">'

#        for x, y in screen.items():
        for x, y in sorted(screen.items(), key=lambda x: x[0]):
            html += '- ' + str(x).upper() + '<br>'
        html += '</p>'
        sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='info', width=600)
        return redirect('/conversations/')


    if requested_proof["state"] == "verified":

        value = requested_proof["presentation"]["requested_proof"]["revealed_attrs"]
        value = str(value)

        if  value.find("{}") == -1:
            for attr, value in requested_proof["presentation"]["requested_proof"]["revealed_attrs"].items():
                attr = attr.replace('_referent', '')
                attr = attr.capitalize()
                screen[attr] = value

            for attr, value in requested_proof["presentation"]["requested_proof"]["revealed_attrs"].items():
                value["identifier"] = requested_proof["presentation"]["identifiers"][value["sub_proof_index"]]

            if test == True:
                html = '<h4><p style="text-align:left;">'
#               for x, y in screen.items():
# Order screen dict
                for x, y in sorted(screen.items(), key=lambda x: x[0]):
                    html += '<b>' + x.upper()  + '</b>' + ' : ' + y['raw'] + '<br>'
                html += '</p>'
            sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='info', width=600)
            return redirect('/conversations/')
        if value.find("{}") == 0:

            for attr, value in requested_proof["presentation"]["requested_proof"]["self_attested_attrs"].items():
                attr = attr.replace('_referent', '')
                attr = attr.capitalize()
                screen[attr] = value

            if test == True:
                print('aqui3')
                html = '<h4><p style="text-align:left;">'

#               for x, y in screen.items():
# Order screen dict
                for x, y in sorted(screen.items(), key=lambda x: x[0]):
                    x = x.upper()
                    html += '<b>' +  x + '</b>' + ' : ' + y + '<br>'
                html += '</p>'


            sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='info', width=600)
            return redirect('/conversations/')
        else:
            return render(request, template, {'conversation': conversation, 'proof': requested_proof, 'screen': screen})

def handle_view_proof_sent(
    request
    ):
    """
    View the Proof sent by the Prover.
    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    conversation_id = request.GET.get('conversation_id', None)


    conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()

    # TODO validate conversation id
    conversation = conversations[0]

    requested_proof = get_agent_conversation(agent, conversation_id, PROOF_REQ_CONVERSATION)
    screen = {}

    for attr, value in requested_proof["presentation"]["requested_proof"]["self_attested_attrs"].items():
        attr = attr.replace('_referent', '')
        screen[attr] = value

    html = '<h4><p style="text-align:left;">'
#    for x, y in screen.items():
    for x, y in sorted(screen.items(), key=lambda x: x[0]):
        html += '<b>' + x.upper() + '</b>' + ' : ' + y + '<br>'
    html += '</p>'
    sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='info', width=600)
    return redirect('/conversations/')


def handle_view_credential(
    request,
    template='aries/credential/view_credential.html'
    ):
    """
    View the Proof sent by the Prover.
    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    conversation_guid = request.GET.get('conversation_guid', None)
    org = request.GET.get('org', None)

    credentials = fetch_credentials(agent)
    connections = AgentConnection.objects.filter(guid=conversation_guid).all()

    conversations = AgentConversation.objects.get(connection=connections[0], status="credential_acked")
    rev_reg_id = conversations.rev_reg_id

    for credential in credentials:
        rev_reg_id_cred = credential['rev_reg_id']
        if rev_reg_id == rev_reg_id_cred:
            html = '<h4><p style="text-align:left;">'
            html += '<b>' + 'EMISSOR' + '</b>' + ' : ' + org + '<br>'
            for attr, value in credential["attrs"].items():
                html += '<b>' + attr.upper()  + '</b>' + ' : ' + value + '<br>'
            html += '</p>'

    sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='info', width=400)
    return redirect('/conversations/')

######################################################################
# views to list wallet credentials
######################################################################
def form_response(request):
    """
    Generic response page.
    """

    msg = request.GET.get('msg', None)
    msg_txt = request.GET.get('msg_txt', None)
    return render(request, 'aries/form_response.html', {'msg': msg, 'msg_txt': msg_txt})


def list_wallet_credentials(
    request,
    template='aries/credential/list.html',
    ):
    """
    List all credentials in the current wallet.
    """

    try:
        (agent, agent_type, agent_owner) = agent_for_current_session(request)

        credentials = fetch_credentials(agent)
        print('credentials->', credentials)

#        for credential in credentials:

        test = settings.REVOCATION
        cred = len(credentials)

        count = 0

        if test == True and cred != 0:
        # Insert field with information of revocation

            connections = AgentConnection.objects.filter(agent=agent).all()

            for connection in connections:
                objects = AgentConnection.objects.filter(agent=connection.agent, partner_name=connection.partner_name).get()

                if settings.ALERT_REVOKED_CREDENTIALS == True:
                    for credential in credentials:
                        cred_rev_id = credential['cred_rev_id']
                        rev_reg_id = credential['rev_reg_id']
                        states = AgentConversation.objects.filter(connection=objects, cred_rev_id=cred_rev_id, rev_reg_id=rev_reg_id).all()

                        for state in states:
                            tmp = AgentConversation.objects.filter(guid=state.guid).get()
                            credential['state'] = tmp.status
                            credential['revoked'] = tmp.revoked
                            credential['schema_id'] = connection.partner_name

        else:
#           credentials = fetch_credentials(agent)

            for credential in credentials:
                partner_name = credentials[count]['schema_id']
                partner_name = partner_name.split(":")
                partner_name = partner_name[2]
                credentials[count]['schema_id'] = partner_name
                count += 1
        return render(request, template, {'agent_name': agent.agent_name, 'credentials': credentials})
    except:
        raise
    finally:
        pass

#Remove connection in database
def handle_remove_connection(request):
    """
    Select a Proof Request to send, based on the templates available in the database.
    """

    # find conversation request
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    connection_id = request.GET.get('connection_id', None)
    connection = AgentConnection.objects.filter(guid=connection_id, agent=agent).get()
    partner_name= connection.partner_name
    agent_name = connection.agent.agent_name
    invitation = connection.invitation
    guid = connection.guid


    try:
        guid_partner_agent_owner = AgentConnection.objects.filter(partner_name=agent_owner, invitation=invitation).get()

        if guid_partner_agent_owner is not None and connection is not None:
            connection.delete()
            guid_partner_agent_owner.delete()
            handle_alert(request, message=trans('Connection removed'), type='success')
            return redirect('/connections/')

    except:
        handle_alert(request, message=trans('Connection not removed '), type='error')
        return redirect('/connections/')
    finally:
        pass


#Function created to allow updating of information in the user's profile
def handle_update_user(
    request,
    form_template='aries/request_update.html',
    response_template='aries/profile.html'
    ):
    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    
    if agent_type == 'user':
    	connections = AriesUser.objects.get(email=agent_owner)
    else:
        name = agent_owner.split()
        first_name = name[0]
        connections = AriesUser.objects.get(first_name=first_name)
        define = AriesUser.objects.filter(first_name=first_name).get()
        
        if define.agent is None:
            define.agent = agent
            define.save()


    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            connections.first_name = cd.get('first_name')
            connections.last_name = cd.get('last_name')
            connections.date_birth = cd.get('date_birth')
            connections.cpf = cd.get('cpf')
            ori_photo = cd.get('ori_photo')
            new_photo = cd.get('new_photo')
            password1 = cd.get('password1')

            if new_photo is None:
                connections.photo = cd.get('ori_photo')
            else:
                connections.photo = cd.get('new_photo')

            if password1 != '':
                connections.set_password(password1)

        connections.save()

        connections = AriesUser.objects.filter(email=agent_owner).all()
        return render(request, response_template,
                      {'agent_name': agent.agent_name, 'connections': connections})

    else:
        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        form = UserUpdateForm(initial={'agent_name': agent})
        return render(request, form_template, {'form': form})
    
def handle_remove_credentials(
    request,
    form_template='aries/credential/form_remove_credential.html',
    response_template='aries/credential/list.html'
    ):
    """
    Select a Proof Request to send, based on the templates available in the database.
    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    
    try:
        connection_id = request.GET.get('connection_id', None)
        credentials = remove_credential(agent, connection_id)
        handle_alert(request, message=trans('Credential removed'), type='success')
        return redirect('/credentials/')

    except:
        handle_alert(request, message=trans('Credential not removed'), type='error')
        return redirect('/credentials/')
    finally:
        pass


def handle_revoke_credentials(
    request,
    form_template='aries/credential/form_revoke_credential.html',
    response_template='aries/credential/list.html'
    ):
    """
    Select a Proof Request to send, based on the templates available in the database.
    """



    if request.method=='POST':
        form = RevokeCredentialForm(request.POST)

        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            (agent, agent_type, agent_owner) = agent_for_current_session(request)

            cd = form.cleaned_data
            connection_id = cd.get('referent')

            credentials = fetch_credentials(agent)
            cred_rev_id = credentials[0]['cred_rev_id']
            rev_reg_id = credentials[0]['rev_reg_id']
            revoke_id = revoke_credential(agent, rev_reg_id, cred_rev_id)

            return list_wallet_credentials(
                request
            )

    else:
        # find conversation request
        (connection, agent_type, agent_owner) = agent_for_current_session(request)
        connection_id = request.GET.get('connection_id', None)
        form = RevokeCredentialForm(initial={'connection_id': connection_id,
                                               'referent': connection_id,
                                               'agent_name': connection_id})

        return render(request, form_template, {'form': form})


def handle_send_message(request):
    """
           Send simple message
    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    connection_id = request.GET.get('connection_id', None)
    message = request.GET.get('message')

    try:
        message_status = send_simple_message(agent, connection_id, message)
        handle_alert(request, message=trans('Message sent'), type='success')
        return redirect('/connections/')

    except:
        handle_alert(request, message=trans('Message not sent'), type='error')
        return redirect('/connections/')
    finally:
        pass



def handle_credential_proposal(request):
    """
    Send a Credential proposal.
    """

    data = request.POST
    connection_id = request.POST.get("connection_id")
    cred_def_id = request.POST.get("cred_def_id")
    partner_name = request.POST.get("partner_name")
    credential_name = request.POST.get("credential_name")
    schema_attrs = request.POST.get("schema_attrs")

    cred_attrs = []
    for attr, value in data.items():
        if not attr.find("schema_attr_"):
            attr = attr.replace("schema_attr_", "")
            cred_attrs.append({"name": attr, "value": value})

    (agent, agent_type, agent_owner) = agent_for_current_session(request)
    connections = AgentConnection.objects.filter(guid=connection_id).all()

    # TODO validate connection id
    my_connection = connections[0]

    cred_defs = IndyCredentialDefinition.objects.filter(agent='o_' + partner_name).all()

    cred_def_id = cred_defs[0].ledger_creddef_id
    schema_name = cred_defs[0].ledger_schema
    cred_def = cred_defs[0]
    schema = IndySchema.objects.filter(schema_name=schema_name).all()

    try:
        my_conversation = send_credential_proposal(agent, my_connection, cred_attrs, cred_def_id, schema, connection_id)
        handle_alert(request, message=trans('Credential proposal sent'), type='success')
        return redirect('/connections/')
    except:
        # ignore errors for now
        print(" >>> Failed to update conversation for", agent.agent_name)
        handle_alert(request, message=trans('Credential proposal not sent'), type='error')
        return redirect('/connections/')


def handle_select_credential_proposal(
    request,
    form_template='aries/credential/select_proposal.html',
    response_exist = 'aries/credential/exist.html',
    response_template='aries/credential/proposal.html'
    ):
    """
    Select a Credential Definition and display a form to enter Credential Offer information.
    """

    if request.method=='POST':
        form = CredentialProposalForm(request.POST)
        if not form.is_valid():
            return render(request, 'aries/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            (agent, agent_type, agent_owner) = agent_for_current_session(request)
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')
            partner_name = cd.get('partner_name')
            credential_name = cd.get('credential_name')
            agent_name = cd.get('agent_name')

            query = IndyCredentialDefinition.objects.filter(id=credential_name).all()
            credential_name = query[0].creddef_name
            cred_def_id = query[0].ledger_creddef_id

            # log out of current wallet, if any
            (agent, agent_type, agent_owner) = agent_for_current_session(request)

            connections = AgentConnection.objects.filter(guid=connection_id).all()
            schema_attrs = query[0].creddef_template

            form = SendCredentialProposalForm(initial={'connection_id': connection_id,
                                                    'agent_name': connections[0].agent.agent_name,
                                                    'partner_name': partner_name,
                                                    'cred_def': cred_def_id,
                                                    'schema_attrs': schema_attrs,
                                                    'credential_name': credential_name})

            return render(request, response_template, {'form': form})

    else:
        # find conversation request
        connection_id = request.GET.get('connection_id', None)
        connection_partner_id = request.GET.get('connection_partner_name', None)
        
        connection_partner_id = connection_partner_id.lower()
        connection_partner_id = connection_partner_id.replace(" ", "_")

        connection_destination_id = AgentConnection.objects.filter(agent='o_'+connection_partner_id).all()

        connection_destination = connection_destination_id[0].guid

        (agent, agent_type, agent_owner) = agent_for_current_session(request)
        connections = AgentConnection.objects.filter(guid=connection_id, agent=agent).all()

        agent_target = AriesUser.objects.filter(email=agent_owner).all()
        credentials = fetch_credentials(agent_target[0].agent)

        # If number of IndyCredentialDefinition equal one don't need to choose
        credentialdef = IndyCredentialDefinition.objects.filter(agent__agent_name='o_' + connection_partner_id).all()
        cont = len(credentialdef)

        if cont == 1:
            form = SendCredentialProposalForm(initial={'connection_id': connection_id,
                                                    'agent_name': agent.agent_name,
                                                    'partner_name': connection_partner_id,
                                                    'cred_def': credentialdef[0].ledger_creddef_id,
                                                    'schema_attrs': credentialdef[0].creddef_template,
                                                    'credential_name': credentialdef[0].creddef_name})
            return render(request, response_template, {'form': form})
        else:
            form = CredentialProposalForm(initial={'connection_id': connection_id,
                                                'partner_name': connection_partner_id,
                                                'agent_name': 'o_'+ connection_partner_id})

            return render(request, form_template, {'form': form})

def handle_cred_proposal_response(request):
    """
    Respond to a Credential Offer by sending a Credential Request.
    """
    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    conversation_id = request.GET.get('conversation_id', None)
    conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()

    # TODO validate conversation id
    conversation = conversations[0]
    agent_conversation = get_agent_conversation(agent, conversation_id, CRED_EXCH_CONVERSATION)
    proposed_attrs = agent_conversation["credential_proposal_dict"]["credential_proposal"]["attributes"]

    cred_attrs = {}

    for i in range(len(proposed_attrs)):
        cred_attrs[proposed_attrs[i]["name"]] = proposed_attrs[i]["value"]
    # TODO validate connection id

    connection = conversation.connection
    cred_def_id = agent_conversation['credential_proposal_dict']['cred_def_id']
    schema_id = agent_conversation['credential_proposal_dict']['schema_id']

    my_connection = AgentConnection.objects.filter(agent=agent, partner_name=connection.partner_name).all()

    schema_attrs = cred_attrs
    cred_attrs_tmp = []
    for attr in schema_attrs:
        cred_attrs_tmp.append({"name": attr, "value": schema_attrs[attr]})

    try:
        my_conversation = send_credential_offer(agent, my_connection[0], cred_attrs_tmp, cred_def_id)
        
        #Remove credential proposal
        clean_credentials_prop = remove_issue_credential(agent, conversation_id)
        clean_conversations_prop = AgentConversation.objects.filter(guid=conversation_id).delete()

        handle_alert(request, message=trans('Credential sent'), type='success')
        return redirect('/conversations/')
    except:
        # ignore errors for now
        print(" >>> Failed to update conversation for", agent.agent_name)
        handle_alert(request, message=trans('Credential not sent'), type='error')
        return redirect('/conversations/')
    finally:
        pass


def handle_cred_proposal_show(
    request
    ):
    """
    List all credentials in the current wallet.
    """

    try:

        conversation_id = request.GET.get('conversation_id', None)

        (agent, agent_type, agent_owner) = agent_for_current_session(request)

        conversations = AgentConversation.objects.filter(guid=conversation_id, connection__agent=agent).all()
        conversation = conversations[0]

        agent_conversation = get_agent_conversation(agent, conversation_id, CRED_EXCH_CONVERSATION)
        proposed_attrs = agent_conversation["credential_proposal_dict"]["credential_proposal"]["attributes"]

        cred_attrs = {}
        for i in range(len(proposed_attrs)):
            cred_attrs[proposed_attrs[i]["name"]] = proposed_attrs[i]["value"]
        # TODO validate connection id

        html = '<h4><p style="text-align:left;">'
#       for x, y in cred_attrs.items():
        for x, y in sorted(cred_attrs.items(), key=lambda x: x[0]):
            html += '<b>' + x.upper() + '</b>' + ' : ' + y + '<br>'
        html += '</p>'

        sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='info', width=600)
        return redirect('/conversations/')

        connection = conversation.connection
        cred_def_id = agent_conversation['credential_proposal_dict']['cred_def_id']
        schema_id = agent_conversation['credential_proposal_dict']['schema_id']

#       return render(request, 'aries/credential/list_view.html', {'conversation_id': conversation_id, 'partner_name': connection.partner_name, 'proposed_attrs' : proposed_attrs})
    except:
        raise
    finally:
        pass


def handle_message_show(
    request
    ):
    """
    List all messages to user.
    """

    try:

        message_id = request.GET.get('message_id', None)

        (agent, agent_type, agent_owner) = agent_for_current_session(request)

        message = AgentMessage.objects.filter(message_id=message_id).get()
        message_id = message.message_id
        date = message.date
        content = message.content
        state = message.state
        connection = message.connection
        message.state = "read"
        message.save()

        html = '<h4><p style="text-align:left;">'
        html += '<b>'
        html += trans('Sender') + '</b> : ' + str(connection.partner_name) + '<br>'
        html += '<b>'
        html += trans('Date') + '</b> : ' + str(date) + '<br>'
        html += '<b>'
        html += trans('Message') + '</b> : ' + content + '<br>'
        sweetify.success(request, title='', html=html, persistent=True, backdrop=False, icon='success', width=600)
        return redirect('/conversations/')

#       return render(request, 'aries/conversation/messages.html', {'connection': connection, 'message_id': message_id, 'date': date, 'content': content, 'state': state})

    except:
        raise
    finally:
        pass

def handle_message_remove(
    request
    ):
    """
    List all messages to user.
    """

    try:

        message_id = request.GET.get('message_id', None)

        (agent, agent_type, agent_owner) = agent_for_current_session(request)

        message = AgentMessage.objects.filter(message_id=message_id).all()
        conversation = messages[0]

        return render(request, 'aries/conversation/messages.html', {'messages': message})
    except:
        raise
    finally:
        pass

def handle_cred_proposal_delete(request):
#    """
#    Respond to a Creden    tial Offer by sending a Credential Request.
#    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    try:
        conversation_id = request.GET.get('conversation_id', None)
        credentials = remove_issue_credential(agent, conversation_id)
        conversations = AgentConversation.objects.filter(guid=conversation_id).delete()
        handle_alert(request, message=trans('Credential proposal remove'), type='success')
        return redirect('/conversations/')
    except:
        raise
    finally:
        pass

def handle_view_dashboard(
    request,
    template='aries/conversation/list_dashboard.html',
    ):
    """
    View dashboard for the current wallet.
    """
    if 'neoid' in request.session:
        del request.session['neoid']


    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    headers = get_ADMIN_REQUEST_HEADERS(agent)

    if agent_type == 'user':
        onboard = settings.ONBOARD['ACTIVE']
        if onboard == True:
            org = settings.ONBOARD['ORG']
            target_user = get_user_model().objects.filter(email=agent_owner).all()
            target_org = AriesOrganization.objects.filter(org_name=org).all()
            their_agent = target_org[0].agent

            filter = AgentConnection.objects.filter(agent=agent, partner_name=org)

            if not filter:
                return handle_connection_request_organization(request, org)


            # connections = AgentConnection.objects.filter(partner_name=org, agent=agent).all()
            # my_connection = connections[0]
            # schema = IndySchema.objects.filter(schema_name=org).all()
            # connection_id = connections[0].guid
            # cred_defs = IndyCredentialDefinition.objects.filter(creddef_name=org + "-o_" + org).all()
            # cred_def_id = cred_defs[0].ledger_creddef_id
            #
            # connections = AriesUser.objects.filter(email=agent_owner).values()
            # attributes = list(connections)
            #
            # cred_attrs = []
            # schema_attrs = cred_defs[0].creddef_template
            # schema_attrs = json.loads(schema_attrs)
            #
            # for attr in schema_attrs:
            #     field_name = 'schema_attr_' + attr
            #     field_value = attributes[0].get(attr)
            #     cred_attrs.append({"name": attr, "value": field_value})
            # my_conversation = send_credential_proposal(agent, my_connection, cred_attrs, cred_def_id, schema, connection_id)


    conversations = AgentConversation.objects.filter(connection__agent=agent).all()

    credential_acked = 0
    proposal_sent = 0
    proposal_acked = 0
    offer_received = 0
    request_received = 0
    request_sent = 0
    presentation_sent = 0
    presentation_acked = 0
    proposal_received = 0
    proof_verified = 0

    for conversation in conversations:
            if conversation.status == 'credential_acked':
                credential_acked = credential_acked + 1
            if conversation.status == 'proposal_sent':
                proposal_sent = proposal_sent + 1
            if conversation.status == 'proposal_received':
                proposal_received = proposal_sent + 1
            if conversation.status == 'verified':
                presentation_acked = presentation_acked + 1
            if conversation.status == 'presentation_acked':
                presentation_acked = presentation_acked + 1

    count_message = len(conversations)
    connections = AgentConnection.objects.filter(agent=agent).all()
    count_connections = len(connections)
    credentials = fetch_credentials(agent)
    count_credentials = len(credentials)

    data = "["
    data += "['Credencial reconhecida'" + ', ' + str(credential_acked) + ']' + ','
    data += "['Proposta enviada'" + ', ' + str(proposal_sent) + ']' + ','
    data += "['Proposta recebida'" + ', ' + str(proposal_received) + ']' + ','
    data += "['Prova recebida'" + ', ' + str(presentation_acked) + ']' + ','
    data += "]"

    return render(request, template, {'agent_name': agent.agent_name,
                                      'count_message': count_message,
                                      'count_connections': count_connections,
                                      'credential_acked' : credential_acked,
                                      'proposal_sent' : proposal_sent,
                                      'proposal_received' : proposal_received,
                                      'proposal_acked' : proposal_acked,
                                      'offer_received' : offer_received,
                                      'request_received' : request_received,
                                      'request_sent' : request_sent,
                                      'presentation_sent' : presentation_sent,
                                      'presentation_acked' : presentation_acked,
                                      'count_credentials': count_credentials,
                                      'data' : data})


def handle_cred_revoke(request):
    """
    Revoke credential
    """

    conversation_id = request.GET.get('conversation_id', None)

    try:

        cred_rev_id = request.GET.get('cred_rev_id', None)
        rev_reg_id = request.GET.get('rev_reg_id', None)

        (agent, agent_type, agent_owner) = agent_for_current_session(request)

        revoke_status = revoke_credential(agent, rev_reg_id, cred_rev_id)
        revoke_status = get_revoke_registry(agent, rev_reg_id)
        connections = AgentConversation.objects.filter(guid=conversation_id).get()
        conversation_id = connections.connection.guid

        message = trans('Revoked credential') + " " + conversation_id + " " + agent_owner + " " + cred_rev_id + " " + rev_reg_id
        message_status = send_simple_message(agent, conversation_id, message)

        conversations = AgentConversation.objects.filter(rev_reg_id=rev_reg_id, cred_rev_id=cred_rev_id).all()

        for conversation in conversations:
            update = AgentConversation.objects.filter(guid=conversation.guid).get()
            update.status = "credential_revoked"
            update.revoked = datetime.now()
            update.save()

        handle_alert(request, message=trans('Credential revoked'), type='success')
        return redirect('/conversations/')

    except:
        handle_alert(request, message=trans('Credential not revoked'), type='error')
        return redirect('/conversations/')
    finally:
        pass


def oauth2(request):
    """
    Login in NeoID server
    """
    cpf =  request.POST.get("cpf")
    code = request.POST.get("code")

    code_verifier = pkce.generate_code_verifier(length=128)
    code_challenge = pkce.get_code_challenge(code_verifier)

    scope = "single_signature"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    client_id = settings.NEOID['CLIENT_ID']
    code_challenge_method = "S256"
    redirect_uri = settings.NEOID['REDIRECT_HOST']  + settings.NEOID['REDIRECT_URI']
    address = settings.NEOID['ADDRESS']
    client_secret = settings.NEOID['CLIENT_SECRET']
    state = "aut"

    login_hint = cpf

    try:
        if code == "None":
            request.session['cpf'] = cpf
            request.session['agent_type'] = 'user'

            response = get_code_neoid(client_id, code_challenge, code_challenge_method, redirect_uri, scope, state, login_hint, address)
            request.session['code_verifier'] = code_verifier
            return response
        else:
            code = request.GET.get('code', None)
            state = request.GET.get('state', None)
            cpf = request.session['cpf']
            code_verifier_tmp = request.session['code_verifier']
            data = get_token_neoid(client_id, client_secret, code, code_verifier_tmp, redirect_uri, address)
            access_token = data['access_token']
            dict = get_pubkey_neoid(access_token, address, cpf)
            password = dict['cpf']
            email = dict['email']
            mobile_agent = False

            connections = AriesUser.objects.filter(email=email).all()

            if connections:
                print('User exist')
            else:
                new_user = AriesUser(
                    email = email,
                    first_name = dict['first_name'],
                    last_name = dict['last_name'],
                    date_birth = dict['date_birth'],
                    cpf = dict['cpf'],
                    pubkey = dict['pubkey'],
                    rg = dict['rg'],
                    emissao = dict['emissao'],
                    estado_emissao = dict['estado_emissao'],
                    inss = dict['inss'],
                    titulo = dict['titulo'],
                    zona = dict['zona'],
                    secao = dict['secao'],
                    natural = dict['natural'],
                    estado = dict['estado']
                )

                new_user.set_password(password)
                new_user.save()

                if Group.objects.filter(name=USER_ROLE).exists():
                    new_user.groups.add(Group.objects.get(name=USER_ROLE))
                new_user.save()

                user = authenticate(username=email, password=password)

                # create an Indy agent - derive agent name from email, and re-use raw password

                user = user_provision(user, password, mobile_agent=mobile_agent)

            request.session['agent_name'] = email
            request.session['neoid'] = data

            cpf_neoid = dict['cpf']

            if cpf == cpf_neoid:
                user = authenticate(email=email)
                login(request, user)
                return redirect('/view_dashboard/')
            else:
                handle_alert(request, message=trans('Usuario com CPF diferente'), type='error')
                return redirect('/')

    except:
        handle_alert(request, message=trans('Usuario não existe'), type='error')
        return redirect('/')

def handle_proofs(request, template='aries/proof/list.html'):
    """
    handle proofs from user
    """

    (agent, agent_type, agent_owner) = agent_for_current_session(request)

    if request.method == 'POST':
        proof_req_name = request.POST.get("proof_req_name")
        test = IndyProofRequest.objects.filter(proof_req_name = proof_req_name)

        if not test:
            proof_req_description = request.POST.get("proof_req_description")
            proof_req_attrs = request.POST.getlist("proof_req_attrs")
            schema = str(request.POST.getlist("schema"))
            schema = schema.replace("[]'", "")
            proof_req_predicates = request.POST.get("proof_req_predicates")

            val = "["
            for attrib in proof_req_attrs:
                val += '{"name"' + ':' + '"' + attrib + '"}'
            val = val.replace("}{", "},{")
            val += "]"

            store = IndyProofRequest.objects.create(
                proof_req_name=proof_req_name,
                agent=agent_owner,
                schema=schema,
                proof_req_description=proof_req_description,
                proof_req_attrs=val,
                proof_req_predicates='[]',
                creation=datetime.now(),
                expiration=datetime.now() + timedelta(days=365)
            )
            handle_alert(request, message=trans('Consent Created'), type='success')
            return redirect('/proofs/')
        else:
            handle_alert(request, message=trans('Name exist, please change it'), type='error')
            return redirect('/proofs/')

    else:
        proofs = IndyProofRequest.objects.filter(agent = agent_owner)

        proof = {}


        exclude_filter = AgentConnection.objects.filter(agent=agent).values_list('partner_name', flat=True)
        orgs_filter = IndySchema.objects.values_list('schema_name', flat=True)
        orgs = IndySchema.objects.filter(schema_name__in=exclude_filter)
#       orgs = IndySchema.objects.all()

        connections = AgentConnection.objects.filter(agent=agent).all()

        schemas = []
        proof = {}
        for prf in proofs:
            proof[prf.proof_req_name] = prf.proof_req_name

        for org in orgs:
            data = IndySchema.objects.get(schema_name = org)
            schemas.append({"org": data.schema_name, "attr": data.schema})

        for prf in proofs:
            proof[prf.proof_req_name] = prf.proof_req_name

        return render(request, template, {'proofs': proofs, 'orgs': orgs, 'schemas': schemas, 'agent': agent_owner})

def handle_proof_remove(request):
    """
    Remove proof from user
    """
    id = request.GET.get('id', None)
    proof = IndyProofRequest.objects.filter(id=id)
    proof.delete()
    handle_alert(request, message=trans('Connection removed'), type='success')
    return redirect('/proofs/')

def handle_proof_state(request):
    """
    State proof from user
    """
    id = request.GET.get('id', None)
    state = request.GET.get('state', None)
    proof = IndyProofRequest.objects.get(id=id)

    if proof.active == True:
        proof.active = "False"
        state = "not active"
    else:
        proof.active = "True"
        state = "active"
    proof.save()
    handle_alert(request, message=trans('Defined state'), type='success')
    return redirect('/proofs/')



