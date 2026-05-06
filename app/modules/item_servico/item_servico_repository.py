from typing import Sequence, cast
from sqlalchemy.orm import Session
from sqlalchemy import select, exists

from app.modules.item_servico.item_servico_model import ItemServico

class ItemServicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def registrar_item(self, item: ItemServico) -> ItemServico:
        self.db.add(item)
        self.db.flush()
        return item

    def atualizar_item(self,
                       id: int,
                       dados_novos: dict) -> ItemServico | None:
        item = cast(ItemServico | None, self.db.get(ItemServico, id))
        if not item:
            return None
        for campo, valor in dados_novos.items():
            if hasattr(item, campo):
                setattr(item, campo, valor)
        return item

    def buscar_um(self,
                  id: int | None = None,
                  descricao: str | None = None,
                  categoria_id: int | None = None,
                  ativo: bool | None = None) -> ItemServico | None:
        consulta = select(ItemServico)
        if descricao:
            consulta = consulta.where(ItemServico.descricao.ilike(descricao))
        if id:
            consulta = consulta.where(ItemServico.id == id)
        if categoria_id:
            consulta = consulta.where(ItemServico.categoria_id == categoria_id)
        if ativo:
            consulta = consulta.where(ItemServico.ativo == ativo)
        return self.db.execute(consulta).scalar_one_or_none()

    def buscar_varios(self,
                      id: int | None = None,
                      categoria_id: int | None = None,
                      ativo: bool | None = None) -> Sequence[ItemServico]:
        consulta = select(ItemServico)
        if id:
            consulta = consulta.where(ItemServico.id == id)
        if categoria_id:
            consulta = consulta.where(ItemServico.categoria_id == categoria_id)
        if ativo is not None:
            consulta = consulta.where(ItemServico.ativo == ativo)
        return self.db.execute(consulta).scalars().all()

    def buscar_todos(self) -> Sequence[ItemServico]:
        return self.db.execute(select(ItemServico)).scalars().all()

    def buscar_por_id(self, id: int) -> ItemServico | None:
        return cast(ItemServico | None, self.db.get(ItemServico, id))

    def desativar_item(self, id: int) -> ItemServico | None:
        item = self.buscar_por_id(id)
        if item:
            item.ativo = False
        else:
            return None

    def exists_item(self, categoria_id: int | None = None, descricao: str | None = None) -> bool:

        consulta = self.db.execute
        if categoria_id:
            consulta = consulta(select(exists().where(ItemServico.categoria_id == categoria_id))).scalar()
        if descricao:
            consulta = consulta(select(exists().where(ItemServico.descricao.ilike(descricao)))).scalar()
        else:
            return False

        return consulta
