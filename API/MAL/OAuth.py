import os
import json
from datetime import datetime, timedelta
import secrets
import webbrowser
from urllib.parse import urlencode
import requests
import json
from .api import *

class OAuth:
    def __init__(self):
        self.authorize_url = URL_AUTH
        self.access_token_url = URL_TOKEN
        self.code_verifier = self.code_challenge = ''
        self.auth_file = ''
        self.client_id = ''
        self.token_type = ''
        self.token = ''

    def service(self, auth_file, client_file=None):
        self.code_verifier = self.code_challenge = secrets.token_urlsafe(100)[:128]
        self.auth_file = auth_file
        if os.path.exists(auth_file):
            self.refresh_token()
            return True
        else:
            with open(client_file, 'r') as file:
                self.client_id = file.read().replace('\n', '')
            return self.get_authorize_url()

    def get_authorize_url(self):
        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "code_challenge": self.code_challenge,
            "state": "RequestID42",
        }
        return self.authorize_url + "?" + urlencode(auth_params)

    def auth_session(self, code):
        if code == {}:
            raise ValueError("Code given can not be empty")

        token_params = {
            "client_id": self.client_id,
            "code": code,
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(self.access_token_url, data=token_params)

        if not token_response.ok:
            raise RuntimeError('Could not acquire token')

        print('token acquired')
        token_json = json.loads(token_response.content)

        token_expire_time = datetime.now() + timedelta(0, token_json['expires_in'])

        self.token = token_json['access_token']
        self.token_type = token_json['token_type']

        auth_data = {
            'client_id': self.client_id,
            'token_type': token_json['token_type'],
            'expire_time': token_expire_time,
            'access_token': token_json['access_token'],
            'refresh_token': token_json['refresh_token'],
        }
        self.save_credentials(auth_data)
        return

    def save_credentials(self, credentials):
        self.client_id = credentials['client_id']
        self.token_type = credentials['token_type']
        self.token = credentials['access_token']

        with open(self.auth_file, 'w') as json_file:
            def datetime_serializer(o):
                if isinstance(o, datetime):
                    return o.__str__()
            json.dump(credentials, json_file, indent=1, default=datetime_serializer)

    def refresh_token(self):
        with open(self.auth_file) as file:
            data = json.load(file)
        expire_time = data['expire_time']

        expire_time_datetime = datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
        token_validity = (expire_time_datetime - datetime.now()).total_seconds()
        expired = int(token_validity) <= 60
        client_id = data['client_id']
        token_type = data['token_type']
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        token_params = {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        if expired:
            token_response = requests.post(self.access_token_url, data=token_params)
            if token_response.ok:
                data = json.loads(token_response.content)
                expire_time = datetime.now() + timedelta(0, data['expires_in'])
            else:
                print(token_response.content)
                raise RuntimeError('Could not acquire token')

        auth_data = {
            'client_id': client_id,
            'token_type': data['token_type'],
            'expire_time': expire_time,
            'access_token': data['access_token'],
            'refresh_token': data['refresh_token'],
        }

        self.save_credentials(auth_data)
        return

    def get_header(self):
        self.refresh_token()
        return str(self.token_type + " " + self.token)



