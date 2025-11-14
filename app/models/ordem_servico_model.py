from sqlalchemy import Column, Integer, ForeignKey, Date, String, Boolean
from app.core.database import Base
from sqlalchemy.orm import relationship

class OrdemServico(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=True)
    data_abertura = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default='aberta')
    ativo = Column(Boolean, default=True)

    cliente = relationship("Cliente", back_populates="ordens")
    funcionario = relationship("Funcionario", back_populates="ordens")
    itens = relationship("ItemServico", back_populates="ordem", cascade='all, delete-orphan')
