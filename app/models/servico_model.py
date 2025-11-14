from sqlalchemy import Column, Integer, String, Numeric, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255), nullable=False)
    valor_base = Column(Numeric(10,2), nullable=False, default=0.0)
    ativo = Column(Boolean, default=True)

    itens = relationship("ItemServico", back_populates="servico")
