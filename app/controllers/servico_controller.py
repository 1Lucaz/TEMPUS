from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.schemas.servico_schema import ServicoCreate, ServicoUpdate, ServicoResponse
from app.services.servico_service import ServicoService

router = APIRouter(prefix="/servicos", tags=["Servicos"])

@router.post("/", response_model=ServicoResponse)
def criar_servico(data: ServicoCreate, db: Session = Depends(get_session)):
    try:
        return ServicoService.criar(data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ServicoResponse])
def listar_servicos(ativo: bool | None = None, descricao: str | None = None, db: Session = Depends(get_session)):
    return ServicoService.listar(db, ativo, descricao)

@router.get("/{id}", response_model=ServicoResponse)
def obter_servico(id: int, db: Session = Depends(get_session)):
    servico = ServicoService.buscar_por_id(id, db)
    if not servico:
        raise HTTPException(status_code=404, detail="Servico não encontrado")
    return servico

@router.put("/{id}", response_model=ServicoResponse)
def atualizar_servico(id: int, data: ServicoUpdate, db: Session = Depends(get_session)):
    servico = ServicoService.atualizar(id, data, db)
    if not servico:
        raise HTTPException(status_code=404, detail="Servico não encontrado")
    return servico

@router.post("/{id}/desativar")
def desativar_servico(id: int, db: Session = Depends(get_session)):
    servico = ServicoService.desativar(id, db)
    if not servico:
        raise HTTPException(status_code=404, detail="Servico não encontrado")
    return { "id": servico.id, "ativo": servico.ativo }
