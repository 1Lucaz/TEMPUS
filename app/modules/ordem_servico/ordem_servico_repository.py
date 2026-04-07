from datetime import date
from typing import Sequence, cast

from sqlalchemy.orm import Session
from sqlalchemy import select, exists

from app.modules.ordem_servico.ordem_servico_model import OrdemServico


class OrdemServicoRepository:

    def __init__(self, db: Session):
        self.db = db

    def registrar_ordem(self, ordem: OrdemServico) -> OrdemServico:
        self.db.add(ordem)
        return ordem

    def atualizar_ordem(self, id: int, dados_novos: dict) -> OrdemServico | None:

        if not dados_novos:
            return None

        ordem = cast(OrdemServico | None, self.db.get(OrdemServico, id))

        if ordem is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(ordem, campo):
                setattr(ordem, campo, valor)

        return ordem

    def buscar_um(self,
                  id: int | None = None,
                  cliente_id: int | None = None,
                  status: str | None = None,
                  ativo: bool | None = None,
                  data_inicio: date | None = None,
                  data_fim: date | None = None) -> OrdemServico | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(OrdemServico).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "ativo":
                consulta = consulta.where(OrdemServico.ativo.is_(dado))

            elif campo == "data_inicio":
                consulta = consulta.where(OrdemServico.data_abertura >= dado)

            elif campo == "data_fim":
                consulta = consulta.where(OrdemServico.data_abertura <= dado)

            else:
                coluna = getattr(OrdemServico, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalar_one_or_none()

    def buscar_varios(self,
                      id: int | None = None,
                      cliente_id: int | None = None,
                      status: str | None = None,
                      ativo: bool | None = None,
                      data_inicio: date | None = None,
                      data_fim: date | None = None) -> Sequence[OrdemServico] | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(OrdemServico).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "ativo":
                consulta = consulta.where(OrdemServico.ativo.is_(dado))

            elif campo == "data_inicio":
                consulta = consulta.where(OrdemServico.data_abertura >= dado)

            elif campo == "data_fim":
                consulta = consulta.where(OrdemServico.data_abertura <= dado)

            else:
                coluna = getattr(OrdemServico, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalars().all()

    def buscar_todos(self) -> Sequence[OrdemServico]:
        return self.db.execute(select(OrdemServico)).scalars().all()

    def buscar_por_id(self, id: int) -> OrdemServico | None:

        if id is None:
            return None

        return cast(OrdemServico | None, self.db.get(OrdemServico, id, with_for_update=True))

    def desativar_ordem(self, id: int) -> OrdemServico | None:

        if id is None:
            return None

        ordem = cast(OrdemServico | None, self.db.get(OrdemServico, id, with_for_update=True))

        if ordem is None:
            return None

        ordem.ativo = False
        return ordem

    def exists_cliente(self, cliente_id: int) -> bool:
        consulta = select(exists().where(OrdemServico.cliente_id == cliente_id))
        return self.db.execute(consulta).scalar()