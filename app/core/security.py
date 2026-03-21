from pwdlib import PasswordHash as passhash, PasswordHash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from copy import deepcopy
from jwt import encode
from os import getenv


SECRET_KEY : str = getenv("SECRET_KEY")

#aqui está contido o salt da senha, que é gerado automaticamente pela própria lib - nois eh racki paeeehr
password_hash : PasswordHash = passhash.recommended()

#gera o hash da s
def generate_password_hash(password: str) -> str:
    return password_hash.hash(password)

def get_verify_password_hash(password: str, ) -> bool:
    return password_hash.verify(password, )

'''criar o token de acesso'''
def create_acess_token (data: dict) -> str:
    to_encode : dict = deepcopy(data)
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes = 60)

    to_encode.update ({'exp': expire})
    encoded_jwt : str = encode (payload=to_encode, key=SECRET_KEY, algorithm='HS256' )
    return encoded_jwt

