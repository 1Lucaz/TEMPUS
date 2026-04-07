import jwt
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from copy import deepcopy
from jwt import encode, ExpiredSignatureError, InvalidTokenError
from os import getenv

from typing import Annotated

from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.funcionario.funcionario_schema import FuncionarioResponse

SECRET_KEY : str = getenv("SECRET_KEY")
ALGORITHM : str = getenv("ALGORITHM")

#aqui está contido o salt da senha, que é gerado automaticamente pela própria lib - nois eh racki paeeehr
password_hash : PasswordHash = PasswordHash.recommended()

#aqui está contido o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



def generate_password_hash(password: str) -> str | None:
    return password_hash.hash(password)

def verify_password_hash(password_no_hash: str, password_hashed: str) -> bool:
    return password_hash.verify (password_no_hash, password_hashed)



#CRIA O TOKEN DE ACESSO - NÃO, EU NÃO USEI UM DICIONÁRIO PRA ISSO, VALEU VALEU 77 VEZES - LUIZGS
def create_acess_token (data: dict) -> str:
    to_encode : dict = deepcopy(data)
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(hours=3)

    to_encode.update ({'exp': expire})
    encoded_jwt : str = encode (payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



#DECODIFICADOR DE TOKENS -> ESSE NEGÓCIO É MUITO MASSA, GOSTEI
def decode_token(token) -> FuncionarioResponse | ClienteResponse | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if "is_colaborador" in payload:
            return FuncionarioResponse(
                nome=payload.get("nome"),
                email=payload.get("email"),
                ativo=payload.get("ativo"),
                cargo=payload.get("cargo"),

                id=payload.get("id"),

                is_admin=payload.get("is_admin"),
                is_colaborador=payload.get("is_colaborador"),

                access_funcionario=payload.get("access_funcionario"),
                access_cliente=payload.get("access_cliente"),
                access_servico=payload.get("access_servico"),
                access_item_servico=payload.get("access_item_servico"),
                access_ordem_servico=payload.get("access_ordem_servico")

            )

        elif "is_colaborador" not in payload:
            return ClienteResponse(
                nome=payload.get("nome"),
                telefone=payload.get("telefone"),
                email=payload.get("email"),
                ativo=payload.get("ativo"),
                id=payload.get("id")
            )

        else:
            raise InvalidTokenError()

    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError()

    except jwt.InvalidTokenError:
        raise InvalidTokenError()


def get_usuario_atual (token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_token(token=token)
