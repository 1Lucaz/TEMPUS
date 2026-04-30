from datetime import datetime

from sqlalchemy import BIGINT, Boolean, ForeignKey, Float, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, MappedAsDataclass

from app.core.base import Base


class ItemServico(Base):
    __tablename__ = "item_servico"

    id: Mapped[int] = mapped_column( BIGINT,
        primary_key=True,
        init=False,
        nullable=False,
        autoincrement=True
    )

    servico_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("servico.id"),
        nullable=False
    )

    categoria_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("categoria_item_servico.id"),
        nullable=False
    )

    valor: Mapped[float] = mapped_column(
        Float,
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