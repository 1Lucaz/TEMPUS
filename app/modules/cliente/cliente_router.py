from fastapi import APIRouter, Depends

from app.core.security import get_usuario_atual
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.utils.app_exception import *

from app.modules.cliente.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse, ClienteRequest
from app.modules.cliente.cliente_service import ClienteService

from app.core.dependencies import get_cliente_service

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/buscar-varios",
             response_model=list[ClienteResponse],
             status_code=status.HTTP_200_OK)
def buscar_varios_clientes(dados_buscar: ClienteRequest,
                           service: ClienteService = Depends(get_cliente_service),
                           usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_varios_cliente(dados_buscar, usuario_atual)


@router.get("/",
            response_model=list[ClienteResponse],
            status_code=status.HTTP_200_OK)
def buscar_todos_cliente(service: ClienteService = Depends(get_cliente_service),
                         usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_todos_cliente(usuario_atual)


@router.post("/registrar-conta",
             response_model=ClienteResponse,
             status_code=status.HTTP_201_CREATED)
def criar_cliente_publico(cliente: ClienteCreate,
                          service: ClienteService = Depends(get_cliente_service)):
    return service.criar_cliente_publico(cliente)


@router.post("/registrar-funcionario",
             response_model=ClienteResponse,
             status_code=status.HTTP_201_CREATED)
def criar_cliente_funcionario(cliente: ClienteCreate,
                              service: ClienteService = Depends(get_cliente_service),
                              usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual)):
    return service.criar_cliente_funcionario(cliente, usuario_atual)


@router.patch("/atualizar",
              response_model=ClienteResponse,
              status_code=status.HTTP_200_OK)
def atualizar_por_cliente(dados_novos: ClienteUpdate,
                          service: ClienteService = Depends(get_cliente_service),
                          usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_cliente(dados_novos=dados_novos, dados_buscar=None, usuario_atual=usuario_atual)

@router.patch("/atualizar-funcionario",
              response_model=ClienteResponse,
              status_code=status.HTTP_200_OK)
def atualizar_por_funcionario   (dados_novos: ClienteUpdate,
                                dados_buscar: ClienteRequest,
                                service: ClienteService = Depends(get_cliente_service),
                                usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_cliente(dados_novos=dados_novos, dados_buscar=dados_buscar, usuario_atual=usuario_atual)


@router.patch("/desativar-funcionario",
              response_model=ClienteResponse,
              status_code=status.HTTP_200_OK)
def desativar_cliente_por_funcionario(dados_buscar: ClienteRequest,
                                      usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual),
                                      service: ClienteService = Depends(get_cliente_service)):
    return service.desativar_cliente_por_funcionario(dados_buscar, usuario_atual)


@router.patch("/desativar",
              response_model=ClienteResponse,
              status_code=status.HTTP_200_OK)
def desativar_cliente_por_cliente(usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual),
                                  service: ClienteService = Depends(get_cliente_service)):
    return service.desativar_cliente_por_cliente(usuario_atual)
