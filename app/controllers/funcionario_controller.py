from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.schemas.funcionario_schema import FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse
from app.services.funcionario_service import FuncionarioService

router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])

@router.post("/", response_model=FuncionarioResponse)
def criar_funcionario(data: FuncionarioCreate, db: Session = Depends(get_session)):
    try:
        return FuncionarioService.criar(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[FuncionarioResponse])
def listar_funcionarios(ativo: bool | None = None, cargo: str | None = None, db: Session = Depends(get_session)):
    return FuncionarioService.listar(db, ativo, cargo)

@router.get("/{id}", response_model=FuncionarioResponse)
def obter_funcionario(id: int, db: Session = Depends(get_session)):
    funcionario = FuncionarioService.buscar_por_id(id, db)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario não encontrado")
    return funcionario

@router.put("/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(id: int, data: FuncionarioUpdate, db: Session = Depends(get_session)):
    funcionario = FuncionarioService.atualizar(id, data, db)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario não encontrado")
    return funcionario

@router.post("/{id}/desativar")
def desativar_funcionario(id: int, db: Session = Depends(get_session)):
    funcionario = FuncionarioService.desativar(id, db)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario não encontrado")
    return {"id": funcionario.id, "ativo": funcionario.ativo}
