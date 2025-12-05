from fastapi import APIRouter, status, Body
from typing import List, Optional
from app.modules.utils.exceptions import tratar_exception
from app.modules.funcionario.funcionario_schema import FuncionarioCreate, FuncionarioUpdate, FuncionarioBase
from app.modules.funcionario.funcionario_service import FuncionarioService

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

@router.get("/", response_model=List[FuncionarioBase])
def listar_funcionarios(ativo: Optional[bool] = None, nome: Optional[str] = None):
    return FuncionarioService.listar(ativo=ativo, nome=nome)

@router.post("/", response_model=FuncionarioBase, status_code=status.HTTP_201_CREATED)
def criar_funcionario(funcionario: FuncionarioCreate):
    try:
        return FuncionarioService.criar_funcionario(funcionario)
    except Exception as e:
        tratar_exception(e)

@router.get("/{id}", response_model=FuncionarioBase)
def buscar_funcionario(id: int):
    funcionario = FuncionarioService.buscar_por_id(id)
    if not funcionario:
        tratar_exception(ValueError("FUNCIONÁRIO NÃO ENCONTRADO"))
    return funcionario

@router.put("/{id}", response_model=FuncionarioBase)
def atualizar_funcionario(id: int, dados: FuncionarioUpdate = Body (...,
                                                                    example ={})):
    try:
        return FuncionarioService.atualizar(id, dados)
    except Exception as e:
        tratar_exception(e)

@router.post("/{id}/desativar", response_model=FuncionarioBase)
def desativar_funcionario(id: int):
    try:
        return FuncionarioService.desativar(id)
    except Exception as e:
        tratar_exception(e)