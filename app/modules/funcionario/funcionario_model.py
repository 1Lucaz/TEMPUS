from datetime import datetime

from sqlalchemy import String, BIGINT, Boolean, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, MappedAsDataclass

class Base (MappedAsDataclass, DeclarativeBase):
    pass

class Funcionario(Base):
    __tablename__ = 'funcionario'

    id : Mapped [int] = mapped_column (BIGINT, init=False, nullable=False, primary_key=True, autoincrement=True)

    nome : Mapped[str] = mapped_column (String (255), nullable=False)
    email : Mapped[str] = mapped_column (String (255), nullable=False)
    senha : Mapped[str] = mapped_column (String (255), nullable=False)
    cargo : Mapped[str] = mapped_column (String (255), nullable=False)

    is_admin : Mapped[bool] = mapped_column (Boolean, nullable=False)

    #acessar o perfil de outro cliente
    access_cliente: Mapped [bool] = mapped_column(Boolean, nullable=False)

    # acessar o perfil de outro cliente
    access_funcionario: Mapped [bool] = mapped_column(Boolean, nullable=False)

    # acessar o servico
    access_servico: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # acessar o item_servico
    access_item_servico: Mapped[bool] = mapped_column(Boolean, nullable=False)

    #acessar o ordem_serviço
    access_ordem_servico: Mapped[bool] = mapped_column(Boolean, nullable=False)

    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="TRUE")
    is_colaborador: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="TRUE")

    created_at: Mapped[datetime] = mapped_column (init=False, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column (init=False, server_default=func.now(), onupdate=func.now())
