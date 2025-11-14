from sqlalchemy import Column, Integer, ForeignKey, Numeric, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class ItemServico(Base):
    __tablename__ = "itens_servico"

    id = Column(Integer, primary_key=True, index=True)
    ordem_servico_id = Column(Integer, ForeignKey('ordens_servico.id'), nullable=False)
    servico_id = Column(Integer, ForeignKey('servicos.id'), nullable=False)
    valor = Column(Numeric(10,2), nullable=False, default=0.0)
    ativo = Column(Boolean, default=True)

    ordem = relationship("OrdemServico", back_populates="itens")
    servico = relationship("Servico", back_populates="itens")
