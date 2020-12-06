from Core.Plugins.Base.Auth.Authentication import *
import secrets
from urllib.parse import urlencode
import requests
import json
import time


class OAuth(Authenticator):
    def __init__(self, name: str, client_id: str, url_auth: str, url_token: str):
        super().__init__(AuthType.OAuth)
        self.name: str = name
        self.client_id: str = client_id
        self.code_verifier = self.code_challenge = secrets.token_urlsafe(100)[:128]
        self.url_auth = url_auth
        self.url_token = url_token
        self.token: str = None
        self.token_type: str = None
        self.token_refresh: str = None
        self.token_expire_time: int = 0
        self.check_auth()


    def url(self)-> str:
        #self.code_verifier = self.code_challenge = secrets.token_urlsafe(100)[:128]
        auth_params: dict = {
            "response_type": "code",
            "client_id": self.client_id,
            "code_challenge": self.code_challenge,
            "code_challenge_method": 'plain',
            "state": "RequestID42",
        }
        print(self.code_challenge)
        url = self.url_auth + "?" + urlencode(auth_params)
        return url

    def code(self, code: str) -> AuthCode:
        token_params: dict = {
            "client_id": self.client_id,
            "code": code,
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code",
        }
        token_response = requests.post(self.url_token, token_params)

        if not token_response.ok:
            return AuthCode.BadUnknown

        token_json = json.loads(token_response.content)

        self.token_expire_time = int(time.time()) + int(token_json['expires_in'])

        self.token = token_json['access_token']
        self.token_type = token_json['token_type']
        self.token_refresh = token_json['refresh_token']

        auth_data = {
            'client_id': self.client_id,
            'token_type': self.token_type,
            'expire_time': self.token_expire_time,
            'access_token': self.token,
            'refresh_token': self.token_refresh,
        }

        self.save(auth_data)
        self.state = AuthState.Logged

    def check_auth(self):
        auth_data = self.load()
        if auth_data is not None:
            self.client_id = auth_data['client_id']
            self.token_type = auth_data['token_type']
            self.token_expire_time = auth_data['expire_time']
            self.token = auth_data['access_token']
            self.token_refresh = auth_data['refresh_token']

            if self.token_valid(self.token_expire_time):
                self.state = AuthState.Logged
                return True
            else:
                self.state = AuthState.Expired
                return False
        else:
            self.state = AuthState.NotLogged
            return False

    def token_valid(self, expire_time):
        return time.time() <= expire_time

    def refresh_token(self):
        token_params = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "refresh_token": self.token_refresh,
        }
        token_response = requests.post(self.url_token, data=token_params)
        if token_response.ok:
            token_json = json.loads(token_response.content)
            self.token_expire_time = int(time.time()) + int(token_json['expires_in'])
        else:
            return AuthCode.BadUnknown

        self.client_id = token_json['client_id']
        self.token_type = token_json['token_type']
        self.token_expire_time = token_json['expire_time']
        self.token = token_json['access_token']
        self.token_refresh = token_json['refresh_token']

        auth_data = {
            'client_id': self.client_id,
            'token_type': self.token_type,
            'expire_time': self.token_expire_time,
            'access_token': self.token,
            'refresh_token': self.token_refresh,
        }

        self.save(auth_data)
        self.state = AuthState.Logged
        return AuthCode.Success
