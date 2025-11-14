from sqlalchemy.orm import Session
from app.models.servico_model import Servico
from app.schemas.servico_schema import ServicoCreate, ServicoUpdate

class ServicoService:
    @staticmethod
    def listar(db: Session, ativo: bool | None = None, descricao: str | None = None):
        q = db.query(Servico)
        if ativo is not None:
            q = q.filter(Servico.ativo == ativo)
        if descricao:
            q = q.filter(Servico.descricao.ilike(f"%{descricao}%"))
        return q.all()

    @staticmethod
    def criar(data: ServicoCreate, db: Session):
        payload = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        servico = Servico(**payload)
        db.add(servico)
        db.commit()
        db.refresh(servico)
        return servico

    @staticmethod
    def buscar_por_id(id: int, db: Session):
        return db.query(Servico).filter(Servico.id == id).first()

    @staticmethod
    def atualizar(id: int, data: ServicoUpdate, db: Session):
        servico = db.query(Servico).filter(Servico.id == id).first()
        if not servico:
            return None
        payload = data.model_dump(exclude_none=True) if hasattr(data, 'model_dump') else data.dict(exclude_none=True)
        for k, v in payload.items():
            setattr(servico, k, v)
        db.commit()
        db.refresh(servico)
        return servico

    @staticmethod
    def desativar(id: int, db: Session):
        servico = db.query(Servico).filter(Servico.id == id).first()
        if not servico:
            return None
        servico.ativo = False
        db.commit()
        db.refresh(servico)
        return servico
