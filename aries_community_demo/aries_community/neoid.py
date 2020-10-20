import requests
from django.shortcuts import redirect
from .indy_utils import *
import OpenSSL
from .agent_utils import *

def get_id_from_neoid(code, client_id, code_verifier, redirect_uri, client_secret, address):
    """
    Get id from neoid
    """
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    message = {"grant_type" : "authorization_code",
               "client_id" : client_id,
               "client_secret" : client_secret,
               "code" : code,
               "code_verifier" : code_verifier,
               "redirect_uri" : redirect_uri}


    try:
        response = requests.post(
            address + "/smartcert-api/v0/oauth/token",
            json.dumps(message),
            headers=headers,
            verify=False
        )
        status = response.raise_for_status()

    except:
        raise

    finally:
        return status

def get_code_neoid(client_id, code_challenge, code_challenge_method, redirect_uri, scope, state, login_hint, address):
    """
    Get code from neoid
    """
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    url = address + '/smartcert-api/v0/oauth/authorize/?response_type=code' \
              + '&client_id=' + client_id \
              + '&code_challenge=' + code_challenge \
              + '&code_challenge_method=' + code_challenge_method \
              + '&redirect_uri=' + redirect_uri \
              + '&scope=' + scope \
              + '&state=' + state \
              + '&login_hint=' + login_hint

    try:
        response = redirect(url, verify=False, is_redirect=True)

    except:
        raise

    return response

def get_token_neoid(client_id, client_secret, code, code_verifier_tmp, redirect_uri, address):
    """
    Get token from neoid
    """
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    message = {"client_id": client_id,
               "client_secret": client_secret,
               "code": code,
               "code_verifier": code_verifier_tmp,
               "redirect_uri": redirect_uri}

    try:
        response = requests.post(
            address + "/smartcert-api/v0/oauth/token/?grant_type=authorization_code",
            params = message,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        data = response.json()

    except:
        raise

    return data

def get_pubkey_neoid(access_token, address, cpf):
    """
    Get pubkey from neoid
    """
    headers = {'Authorization': 'Bearer' + ' ' + access_token }
    try:
        response = requests.get(
            address + "/smartcert-api/v0/oauth/certificate-discovery",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        data = response.json()
        print('data->', data["certificates"][0]["certificate"])
        coded_string = data["certificates"][0]["certificate"]

        filename = cpf + '.txt'
        fo = open(filename, 'w')
        fo.write('%s' % coded_string)
        fo.close()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(filename).read())
        certIssue = cert.get_issuer()
        print("Issuer: ", certIssue.commonName)
        pubkey = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")

    except:
        raise
    return pubkey
