from sqlalchemy.orm import Session
from app.models.cliente_model import Cliente
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate

class ClienteService:
    @staticmethod
    def listar(db: Session, ativo: bool | None = None, nome: str | None = None):
        q = db.query(Cliente)
        if ativo is not None:
            q = q.filter(Cliente.ativo == ativo)
        if nome:
            q = q.filter(Cliente.nome.ilike(f"%{nome}%"))
        return q.all()

    @staticmethod
    def criar(data: ClienteCreate, db: Session):
        payload = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        cliente = Cliente(**payload)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def buscar_por_id(id: int, db: Session):
        return db.query(Cliente).filter(Cliente.id == id).first()

    @staticmethod
    def atualizar(id: int, data: ClienteUpdate, db: Session):
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            return None
        payload = data.model_dump(exclude_none=True) if hasattr(data, 'model_dump') else data.dict(exclude_none=True)
        for k, v in payload.items():
            setattr(cliente, k, v)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def desativar(id: int, db: Session):
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            return None
        cliente.ativo = False
        db.commit()
        db.refresh(cliente)
        return cliente
