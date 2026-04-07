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

    def atualizar_item(self, id: int, dados_novos: dict) -> ItemServico | None:

        if not dados_novos:
            return None

        item = cast(ItemServico | None, self.db.get(ItemServico, id))

        if item is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(item, campo):
                setattr(item, campo, valor)

        return item

    def buscar_um(self,
                  id: int | None = None,
                  ordem_servico_id: int | None = None,
                  servico_id: int | None = None,
                  valor: float | None = None,
                  ativo: bool | None = None) -> ItemServico | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(ItemServico).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "ativo":
                consulta = consulta.where(ItemServico.ativo.is_(dado))
            else:
                coluna = getattr(ItemServico, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalar_one_or_none()

    def buscar_varios(self,
                      id: int | None = None,
                      ordem_servico_id: int | None = None,
                      servico_id: int | None = None,
                      valor: float | None = None,
                      ativo: bool | None = None) -> Sequence[ItemServico] | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(ItemServico).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "ativo":
                consulta = consulta.where(ItemServico.ativo.is_(dado))
            else:
                coluna = getattr(ItemServico, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalars().all()

    def buscar_todos(self) -> Sequence[ItemServico]:
        return self.db.execute(select(ItemServico)).scalars().all()

    def buscar_por_id(self, id: int) -> ItemServico | None:

        if id is None:
            return None

        return cast(ItemServico | None, self.db.get(ItemServico, id, with_for_update=True))

    def desativar_item(self, id: int) -> ItemServico | None:

        if id is None:
            return None

        item = cast(ItemServico | None, self.db.get(ItemServico, id, with_for_update=True))

        if item is None:
            return None

        item.ativo = False
        return item

    def exists_servico(self, servico_id: int) -> bool:
        consulta = select(exists().where(ItemServico.servico_id == servico_id))
        return self.db.execute(consulta).scalar()

    def exists_ordem_servico(self, ordem_servico_id: int) -> bool:
        consulta = select(exists().where(ItemServico.ordem_servico_id == ordem_servico_id))
        return self.db.execute(consulta).scalar()