from datetime import datetime

from sqlalchemy import String, BIGINT, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass


class Base (MappedAsDataclass, DeclarativeBase):
    pass

class Cliente (Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column (BIGINT, primary_key=True, init=False, nullable=False, autoincrement=True)
    nome: Mapped[str] = mapped_column (String (255), nullable=False)
    telefone: Mapped [str] = mapped_column (String (45), unique=True)
    email: Mapped[str] = mapped_column (String(255), unique=True)
    senha: Mapped [str] = mapped_column (String(255), nullable=False)

    ativo: Mapped[bool] = mapped_column (Boolean, nullable=False, default=True, server_default="TRUE")

    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), onupdate=func.now())
    updated_by: Mapped [str] = mapped_column(String (255), init=False, nullable=False)