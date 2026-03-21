from fastapi import APIRouter, status, Body, Depends
from typing import List, Optional

from app.core.dependencies import get_funcionario_service
from app.modules.funcionario.funcionario_schema import FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse
from app.modules.funcionario.funcionario_service import FuncionarioService

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

@router.get("/", response_model=List[FuncionarioResponse])
def listar_funcionarios(funcionario: FuncionarioResponse = Depends (get_funcionario_service)):
    return FuncionarioService.listar(ativo=ativo, nome=nome, is_admin=)

@router.post("/", response_model=FuncionarioResponse, status_code=status.HTTP_201_CREATED)
def criar_funcionario(funcionario: FuncionarioCreate, service: FuncionarioService = Depends (get_funcionario_service)):
    return service.criar_funcionario(funcionario)

@router.get("/buscar_funcionario", response_model=FuncionarioResponse)
def buscar_funcionario(dados: FuncionarioCreate, service: FuncionarioService = Depends (get_funcionario_service)):
    service.criar_funcionario()

@router.patch("/atualizar_funcionario", response_model=FuncionarioResponse)
def atualizar_funcionario(id: int, dados: FuncionarioUpdate, service: FuncionarioService = Depends (get_funcionario_service)):
    return service.atualizar(id,
                             cargo=dados.novo_cargo,
                             nome=dados.novo_nome,
                             email=dados.novo_email,
                             is_admin=dados.is_admin)

@router.post("/desativar_funcionario", response_model=FuncionarioResponse)
def desativar_funcionario(id: int, dados:FuncionarioCreate, service: FuncionarioService = Depends (get_funcionario_service)):
    return service.desativar(id, email= str(dados.email))
