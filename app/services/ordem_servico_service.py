from sqlalchemy.orm import Session
from app.models.ordem_servico_model import OrdemServico
from app.models.cliente_model import Cliente
from app.schemas.ordem_servico_schema import OrdemCreate, OrdemUpdate
from fastapi import HTTPException
from datetime import date

class OrdemServicoService:
    @staticmethod
    def listar(db: Session, ativo: bool | None = None, status: str | None = None, cliente_id: int | None = None, data_inicio: date | None = None, data_fim: date | None = None):
        q = db.query(OrdemServico)
        if ativo is not None:
            q = q.filter(OrdemServico.ativo == ativo)
        if status:
            q = q.filter(OrdemServico.status == status)
        if cliente_id:
            q = q.filter(OrdemServico.cliente_id == cliente_id)
        if data_inicio:
            q = q.filter(OrdemServico.data_abertura >= data_inicio)
        if data_fim:
            q = q.filter(OrdemServico.data_abertura <= data_fim)
        return q.all()

    @staticmethod
    def criar(data: OrdemCreate, db: Session):
        payload = data.model_dump() if hasattr(data, "model_dump") else data.dict()
        cliente = db.query(Cliente).filter(Cliente.id == payload["cliente_id"], Cliente.ativo == True).first()
        if not cliente:
            raise HTTPException(status_code=400, detail="Cliente não existe ou está inativo")

        ordem = OrdemServico(
            cliente_id=payload["cliente_id"],
            funcionario_id=payload.get("funcionario_id"),
            data_abertura=payload["data_abertura"],
            status=payload.get("status", "aberta"),
            ativo=True
        )
        db.add(ordem)
        db.commit()
        db.refresh(ordem)
        return ordem

    @staticmethod
    def buscar_por_id(id: int, db: Session):
        ordem = db.query(OrdemServico).filter(OrdemServico.id == id).first()
        if not ordem:
            raise HTTPException(status_code=404, detail="Ordem não encontrada")
        return ordem

    @staticmethod
    def atualizar(id: int, data: OrdemUpdate, db: Session):
        ordem = db.query(OrdemServico).filter(OrdemServico.id == id).first()
        if not ordem:
            raise HTTPException(status_code=404, detail="Ordem não encontrada")
        payload = data.model_dump(exclude_none=True) if hasattr(data, "model_dump") else data.dict(exclude_none=True)
        for k, v in payload.items():
            setattr(ordem, k, v)
        db.commit()
        db.refresh(ordem)
        return ordem

    @staticmethod
    def desativar(id: int, db: Session):
        ordem = db.query(OrdemServico).filter(OrdemServico.id == id).first()
        if not ordem:
            raise HTTPException(status_code=404, detail="Ordem não encontrada")
        ordem.ativo = False
        db.commit()
        db.refresh(ordem)
        return ordem
