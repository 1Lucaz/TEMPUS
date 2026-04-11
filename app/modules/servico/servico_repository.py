from typing import Sequence, cast

from sqlalchemy.orm import Session
from sqlalchemy import select, exists

from app.modules.servico.servico_model import Servico


class ServicoRepository:

    def __init__(self, db: Session):
        self.db = db

    def registrar_servico(self, servico: Servico) -> Servico:
        self.db.add(servico)
        return servico

    def atualizar_servico(self, id: int, dados_novos: dict) -> Servico | None:

        if not dados_novos:
            return None

        servico = cast(Servico | None, self.db.get(Servico, id))

        if servico is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(servico, campo):
                setattr(servico, campo, valor)

        return servico

    def buscar_um(self,
                  descricao: str | None = None,
                  ativo: bool | None = None) -> Servico | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(Servico).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "descricao":
                consulta = consulta.where(Servico.descricao.ilike(f"%{dado}%"))

            elif campo == "ativo":
                consulta = consulta.where(Servico.ativo.is_(dado))

            else:
                coluna = getattr(Servico, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalar_one_or_none()

    def buscar_varios(self,
                      descricao: str | None = None,
                      ativo: bool | None = None) -> Sequence[Servico] | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(Servico).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "descricao":
                consulta = consulta.where(Servico.descricao.ilike(f"%{dado}%"))

            elif campo == "ativo":
                consulta = consulta.where(Servico.ativo.is_(dado))

        return self.db.execute(consulta).scalars().all()

    def buscar_todos(self) -> Sequence[Servico]:
        return self.db.execute(select(Servico)).scalars().all()

    def buscar_por_id(self, id: int) -> Servico | None:

        if id is None:
            return None

        return cast(Servico | None, self.db.get(Servico, id, with_for_update=True))

    def desativar_servico(self, id: int | None = None,
                          descricao: str | None = None,
                          ativo : bool | None = None) -> Servico | None:

        if id is None or descricao is None or ativo is None:
            return None

        if id:
            servico = cast(Servico | None, self.db.get(Servico, id, with_for_update=True))

        else:
            servico = cast (Servico | None, self.buscar_um(descricao, ativo))

        if servico is None:
            return None

        servico.ativo = False
        return servico

    def exists_descricao(self, descricao: str) -> bool:
        consulta = select(exists().where(Servico.descricao == descricao))
        return self.db.execute(consulta).scalar()