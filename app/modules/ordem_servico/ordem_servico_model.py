from datetime import datetime

from sqlalchemy import BIGINT, Boolean, ForeignKey, String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class OrdemServico(Base):
    __tablename__ = "ordem_servico"

    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        init=False,
        nullable=False,
        autoincrement=True
    )

    cliente_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("cliente.id"),
        nullable=False
    )

    data_abertura: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    prioridade: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="TRUE"
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now()
    )