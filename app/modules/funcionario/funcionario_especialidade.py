from mimetypes import inited

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base (MappedAsDataclass, DeclarativeBase):
    pass

class FuncionarioEspecialidade (Base):

    __tablename__ = 'funcionario_especialidade'

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, init=False)
    funcionario_id : Mapped[int] = mapped_column(Integer, ForeignKey('funcionario.id'), nullable=False)
    especialidade_id: Mapped[str] = mapped_column(String (100), primary_key=True, nullable=False)

