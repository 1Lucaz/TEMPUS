# funcionario_router.py

from fastapi import APIRouter, Depends

from app.core.dependencies import get_funcionario_service
from app.core.security import get_usuario_atual
from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.funcionario.funcionario_schema import (
    FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse, FuncionarioInput
)
from app.modules.funcionario.funcionario_service import FuncionarioService
from app.modules.utils.app_exception import *

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


@router.get("/buscar-um",
            response_model=FuncionarioResponse,
            status_code=status.HTTP_200_OK)
def buscar_um_funcionario(dados_buscar: FuncionarioInput,
                          service: FuncionarioService = Depends(get_funcionario_service),
                          usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_um_funcionario(dados_buscar, usuario_atual)


@router.get("/buscar-varios",
            response_model=list[FuncionarioResponse],
            status_code=status.HTTP_200_OK)
def buscar_varios_funcionarios(dados_buscar: FuncionarioInput,
                               service: FuncionarioService = Depends(get_funcionario_service),
                               usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_varios_funcionarios(dados_buscar, usuario_atual)


@router.get("/buscar-todos",
            response_model=list[FuncionarioResponse],
            status_code=status.HTTP_200_OK)
def buscar_todos_funcionarios(service: FuncionarioService = Depends(get_funcionario_service),
                              usuario_atual: ClienteResponse | FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_todos_funcionarios(usuario_atual)


@router.post("/",
             response_model=FuncionarioResponse,
             status_code=status.HTTP_201_CREATED)
def criar_funcionario(dados: FuncionarioCreate,
                      service: FuncionarioService = Depends(get_funcionario_service),
                      usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.criar_funcionario(dados, usuario_atual)


@router.patch("/atualizar/por-si",
              response_model=FuncionarioResponse,
              status_code=status.HTTP_200_OK)
def atualizar_funcionario_por_si(dados_novos: FuncionarioUpdate,
                                 service: FuncionarioService = Depends(get_funcionario_service),
                                 usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_funcionario_por_si(dados_novos=dados_novos, usuario_atual=usuario_atual)


@router.patch("/atualizar/por-funcionario",
              response_model=FuncionarioResponse,
              status_code=status.HTTP_200_OK)
def atualizar_funcionario_por_funcionario(dados_novos: FuncionarioUpdate,
                                          dados_buscar: FuncionarioInput | None = None,
                                          service: FuncionarioService = Depends(get_funcionario_service),
                                          usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_funcionario_por_funcionario(dados_novos=dados_novos,
                                                         dados_buscar=dados_buscar,
                                                         usuario_atual=usuario_atual)


@router.patch("/desativar/por-si",
              response_model=FuncionarioResponse,
              status_code=status.HTTP_200_OK)
def desativar_funcionario_por_si(service: FuncionarioService = Depends(get_funcionario_service),
                                 usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.desativar_funcionario_por_si(usuario_atual=usuario_atual)


@router.patch("/desativar/por-funcionario",
              response_model=FuncionarioResponse,
              status_code=status.HTTP_200_OK)
def desativar_funcionario_por_funcionario(dados_buscar: FuncionarioInput | None = None,
                                          service: FuncionarioService = Depends(get_funcionario_service),
                                          usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.desativar_funcionario_por_funcionario(dados_buscar=dados_buscar, usuario_atual=usuario_atual)