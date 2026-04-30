from datetime import datetime
from sqlalchemy import String,BIGINT, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base


class CategoriaServico(Base):

	__tablename__ = "categoria_item_servico"

	id: Mapped[int] = mapped_column(BIGINT, init=False, nullable=False,
    	primary_key=True,
    	autoincrement=True
	)

	descricao: Mapped[str] = mapped_column(
    	String(255),
    	nullable=False
	)

	ativo: Mapped[bool] = mapped_column(
    	Boolean,
    	default=True,
        server_default="TRUE"
	)

	created_at: Mapped[datetime] = mapped_column( init=False,
    	server_default=func.now()
	)

	updated_at: Mapped[datetime] = mapped_column( init=False,
    	server_default=func.now(),
    	onupdate=func.now()
	)

