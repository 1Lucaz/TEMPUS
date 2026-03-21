from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


class Base (MappedAsDataclass, DeclarativeBase):
    pass

class Especialidade(Base):
    __tablename__ = 'especialidade'