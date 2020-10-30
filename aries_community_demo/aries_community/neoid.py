import requests
from django.shortcuts import redirect
from .indy_utils import *
import OpenSSL
from .agent_utils import *
from .models import *

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
#       print('data->', data["certificates"][0]["certificate"])
        coded_string = data["certificates"][0]["certificate"]

        filename = cpf + '.txt'
        fo = open(filename, 'w')
        fo.write('%s' % coded_string)
        fo.close()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(filename).read())
        certIssue = cert.get_issuer()

        pubkey = OpenSSL.crypto.dump_publickey(OpenSSL.crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, open(filename).read())
        certIssue = cert.get_issuer()
        subject = cert.get_subject().CN
        compost = subject.split(":")
        nome = compost[0]
        nome = nome.split()
        first_name = nome[0].capitalize()
        last_name = nome[1].capitalize()
        cpf = compost[1]
        val = cert.get_extension(4).get_data()
        val = str(val)
        date_birth = val[48:56]
#        print(date_birth)
        email = val[234:-1]
#        print(email)
        rg = val[67:93]
#        print(rg)
        emissao = val[93:98]
#        print(emissao)
        estado_emissao = val[96:98]
#        print(estado_emissao)
        inss = val[144:156]
#        print(inss)
        titulo = val[193:205]
#        print(titulo)
        zona = val[205:208]
#        print(zona)
        secao = val[208:212]
#        print(secao)
        natural = val[212:224]
#        print(natural)
        estado = val[224:226]

        dict = {
            "first_name": first_name,
            "last_name": last_name,
            "cpf": cpf,
            "date_birth": date_birth,
            "email": email,
            "rg": rg,
            "emissao": emissao,
            "estado_emissao": estado_emissao,
            "inss": inss,
            "titulo": titulo,
            "zona": zona,
            "secao": secao,
            "estado": estado,
            "natural": natural,
            "pubkey": pubkey
        }

    except:
        raise
    return dict
