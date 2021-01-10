from enum import Enum
import json
from datetime import datetime, timedelta
import os.path
import os


class AuthType(Enum):
    NoAuth = 0
    UserPass = 1
    OAuth = 2


class AuthCode(Enum):
    Success = 1
    BadPassword = 2
    BadUsername = 3
    BadUnknown = 4


class AuthState(Enum):
    NotLogged = 0
    Logged = 1
    Expired = 2


class Authenticator:
    def __init__(self, authtype: AuthType):
        self.name: str = None
        self.type: AuthType = authtype
        self.state: AuthState = AuthState.NotLogged

    def save(self, credentials: dict):
        os.makedirs(f'Settings/Plugin/{self.name}', exist_ok=True)
        auth_file = f'Settings/Plugin/{self.name}/auth.json'
        with open(auth_file, 'w+') as json_file:
            json.dump(credentials, json_file, indent=1)

    def load(self)-> dict:
        auth_file = f'Settings/Plugin/{self.name}/auth.json'
        if os.path.exists(auth_file):
            with open(auth_file) as file:
                return json.load(file)
        else:
            return None
