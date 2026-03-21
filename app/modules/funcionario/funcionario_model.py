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
    telefone: Mapped[str] = mapped_column(String(50), nullable=False)
    senha : Mapped[str] = mapped_column (String (255), nullable=False)
    cargo : Mapped[str] = mapped_column (String (255), nullable=False)

    especialidadde: Mapped [list] = mapped_column (nullable=True)

    ativo : Mapped[bool] = mapped_column (Boolean, nullable=False, server_default = "TRUE")

    is_admin : Mapped[bool] = mapped_column (Boolean, nullable=False)
    is_colaborador: Mapped[bool] = mapped_column(Boolean, default="TRUE", server_default="TRUE")

    created_at: Mapped[datetime] = mapped_column (init=False, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column (init=False, server_default=func.now(), onupdate=func.now())
