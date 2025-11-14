from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_session
from app.schemas.ordem_servico_schema import OrdemCreate, OrdemUpdate, OrdemResponse
from app.services.ordem_servico_service import OrdemServicoService

router = APIRouter(prefix="/ordens", tags=["Ordens"])

@router.post("/", response_model=OrdemResponse)
def criar_ordem(data: OrdemCreate, db: Session = Depends(get_session)):
    try:
        return OrdemServicoService.criar(data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[OrdemResponse])
def listar_ordens(status: str | None = None, cliente_id: int | None = None, data_inicio: str | None = None, data_fim: str | None = None, ativo: bool | None = None, db: Session = Depends(get_session)):
    return OrdemServicoService.listar(db, ativo, status, cliente_id, data_inicio, data_fim)

@router.get("/{id}", response_model=OrdemResponse)
def obter_ordem(id: int, db: Session = Depends(get_session)):
    ordem = OrdemServicoService.buscar_por_id(id, db)
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")
    return ordem

@router.put("/{id}", response_model=OrdemResponse)
def atualizar_ordem(id: int, data: OrdemUpdate, db: Session = Depends(get_session)):
    ordem = OrdemServicoService.atualizar(id, data, db)
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")
    return ordem

@router.post("/{id}/desativar")
def desativar_ordem(id: int, db: Session = Depends(get_session)):
    ordem = OrdemServicoService.desativar(id, db)
    if not ordem:
        raise HTTPException(status_code=404, detail="Ordem não encontrada")
    return {"id": ordem.id, "ativo": ordem.ativo}
