from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    ativo = Column(Boolean, default=True)

    ordens = relationship("OrdemServico", back_populates="cliente")
