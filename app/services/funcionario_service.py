from sqlalchemy.orm import Session
from app.models.funcionario_model import Funcionario
from app.schemas.funcionario_schema import FuncionarioCreate, FuncionarioUpdate

class FuncionarioService:
    @staticmethod
    def listar(db: Session, ativo: bool | None = None, cargo: str | None = None):
        q = db.query(Funcionario)
        if ativo is not None:
            q = q.filter(Funcionario.ativo == ativo)
        if cargo:
            q = q.filter(Funcionario.cargo.ilike(f"%{cargo}%"))
        return q.all()

    @staticmethod
    def criar(data: FuncionarioCreate, db: Session):
        payload = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        funcionario = Funcionario(**payload)
        funcionario.ativo = True
        db.add(funcionario)
        db.commit()
        db.refresh(funcionario)
        return funcionario

    @staticmethod
    def buscar_por_id(id: int, db: Session):
        return db.query(Funcionario).filter(Funcionario.id == id).first()

    @staticmethod
    def atualizar(id: int, data: FuncionarioUpdate, db: Session):
        funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
        if not funcionario:
            return None
        payload = data.model_dump(exclude_none=True) if hasattr(data, 'model_dump') else data.dict(exclude_none=True)
        for k, v in payload.items():
            setattr(funcionario, k, v)
        db.commit()
        db.refresh(funcionario)
        return funcionario

    @staticmethod
    def desativar(id: int, db: Session):
        funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
        if not funcionario:
            return None
        funcionario.ativo = False
        db.commit()
        db.refresh(funcionario)
        return funcionario
