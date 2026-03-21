from fastapi import APIRouter, Body, Depends
from app.modules.utils.app_exception import *

from app.modules.cliente.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse
from app.modules.cliente.cliente_service import ClienteService

from app.core.dependencies import get_cliente_service


router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/buscar_cliente",
            response_model=list[ClienteResponse],
            status_code=status.HTTP_200_OK)

def buscar_cliente(dados: ClienteCreate = Body(...), service: ClienteService = Depends(get_cliente_service)):
    parametros : dict = {campo:valor for campo, valor in (dados.model_dump()).items() if valor is not None}
    return service.listar(**parametros)



@router.post("/criar_cliente",
             response_model=ClienteResponse,
             status_code=status.HTTP_201_CREATED)

def criar_cliente(cliente: ClienteCreate = Body(...), service: ClienteService = Depends(get_cliente_service)):
    return service.criar_cliente(cliente)



@router.patch("/atualizar_cliente",
              response_model=ClienteResponse,
              status_code=status.HTTP_200_OK)

def atualizar_cliente(id: int, dados: ClienteUpdate = Body(...), service: ClienteService = Depends(get_cliente_service)):
    return service.atualizar(id, nome=dados.nome, email=dados.email, telefone=dados.telefone)




@router.post("/desativar_cliente",
             response_model=ClienteResponse,
             status_code=status.HTTP_200_OK)

def desativar_cliente(cliente: ClienteResponse, service: ClienteService = Depends(get_cliente_service)):
    return service.desativar(cliente)

