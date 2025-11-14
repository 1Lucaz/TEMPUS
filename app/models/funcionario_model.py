from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    cargo = Column(String(255), nullable=True)
    ativo = Column(Boolean, default=True)

    ordens = relationship("OrdemServico", back_populates="funcionario")
