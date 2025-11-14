from sqlalchemy.orm import Session
from app.models.item_servico_model import ItemServico
from app.models.ordem_servico_model import OrdemServico
from app.models.servico_model import Servico
from app.schemas.item_servico_schema import ItemCreate

class ItemServicoService:
    @staticmethod
    def listar(db: Session, ativo: bool | None = None, ordem_servico_id: int | None = None):
        q = db.query(ItemServico)
        if ativo is not None:
            q = q.filter(ItemServico.ativo == ativo)
        if ordem_servico_id:
            q = q.filter(ItemServico.ordem_servico_id == ordem_servico_id)
        return q.all()

    @staticmethod
    def criar(ordem_id: int, data: ItemCreate, db: Session):
        payload = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        servico = db.query(Servico).filter(Servico.id == payload['servico_id'], Servico.ativo == True).first()
        ordem = db.query(OrdemServico).filter(OrdemServico.id == ordem_id, OrdemServico.ativo == True).first()
        if not servico or not ordem:
            raise ValueError('referencia_invalida')
        item = ItemServico(ordem_servico_id=ordem_id, servico_id=payload['servico_id'], valor=payload['valor'])
        item.ativo = True
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def buscar_por_id(id: int, db: Session):
        return db.query(ItemServico).filter(ItemServico.id == id).first()

    @staticmethod
    def atualizar(id: int, valor: float, db: Session):
        item = db.query(ItemServico).filter(ItemServico.id == id).first()
        if not item:
            return None
        item.valor = valor
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def desativar(id: int, db: Session):
        item = db.query(ItemServico).filter(ItemServico.id == id).first()
        if not item:
            return None
        item.ativo = False
        db.commit()
        db.refresh(item)
        return item
