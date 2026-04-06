from datetime import datetime

from sqlalchemy import BIGINT, Boolean, String, Float, func, Text
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, DeclarativeBase


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Servico(Base):
    __tablename__ = "servico"

    id: Mapped[int] = mapped_column(BIGINT,
                                    primary_key=True,
                                    init=False,
                                    nullable=False,
                                    autoincrement=True)

    descricao: Mapped[str] = mapped_column(Text,
                                           nullable=False)

    valor_base: Mapped[float] = mapped_column(Float,
                                              nullable=False)

    ativo: Mapped[bool] = mapped_column(Boolean,
                                        nullable=False,
                                        default=True,
                                        server_default="TRUE")

    created_at: Mapped[datetime] = mapped_column(init=False,
                                                 server_default=func.now(),
                                                 nullable=False)

    updated_at: Mapped[datetime] = mapped_column(init=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now())