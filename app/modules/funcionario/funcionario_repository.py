from typing import Sequence, cast

from sqlalchemy.orm import Session
from sqlalchemy import select, exists

from app.modules.funcionario.funcionario_model import Funcionario


class FuncionarioRepository:

    def __init__(self, db: Session):
        self.db = db


    def registrar_funcionario(self, funcionario: Funcionario) -> Funcionario:
        self.db.add(funcionario)
        self.db.flush()
        return funcionario


    def atualizar_funcionario_por_si(self,
                                     id: int,
                                     dados_novos: dict) -> Funcionario | None:

        if not dados_novos:
            return None

        funcionario = cast(Funcionario | None, self.db.get(Funcionario, id))

        if funcionario is None:
            return None

        campos_permitidos = {"nome", "email", "telefone", "senha"}

        for campo, valor in dados_novos.items():
            if campo in campos_permitidos and hasattr(funcionario, campo):
                setattr(funcionario, campo, valor)

        return funcionario

    def atualizar_funcionario_por_funcionario(self,
                                              dados_novos: dict,
                                              dados_buscar: dict | None) -> Funcionario | None:

        if not dados_novos or not dados_buscar:
            return None

        if "id" in dados_buscar:
            funcionario = cast(Funcionario | None, self.db.get(Funcionario, dados_buscar["id"]))
        else:
            funcionario = self.buscar_um(**dados_buscar)

        if funcionario is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(funcionario, campo):
                setattr(funcionario, campo, valor)

        return funcionario


    def buscar_um(self,
                  nome: str | None = None,
                  email: str | None = None,
                  ativo: bool | None = None,
                  is_admin: bool | None = None) -> Funcionario | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(Funcionario).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "nome":
                consulta = consulta.where(Funcionario.nome.ilike(f"%{dado}%"))

            elif campo == "ativo":
                consulta = consulta.where(Funcionario.ativo.is_(dado))

            elif campo == "is_admin":
                consulta = consulta.where(Funcionario.is_admin.is_(dado))

            else:
                coluna = getattr(Funcionario, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalar_one_or_none()

    def buscar_varios(self,
                      nome: str | None = None,
                      email: str | None = None,
                      ativo: bool | None = None,
                      is_admin: bool | None = None) -> Sequence[Funcionario] | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        consulta = select(Funcionario).with_for_update()

        for campo, dado in condicionais.items():

            if campo == "nome":
                consulta = consulta.where(Funcionario.nome.ilike(f"%{dado}%"))

            elif campo in ("ativo", "is_admin"):
                coluna = getattr(Funcionario, campo)
                consulta = consulta.where(coluna.is_(dado))

            else:
                coluna = getattr(Funcionario, campo)
                consulta = consulta.where(coluna == dado)

        return self.db.execute(consulta).scalars().all()

    def buscar_todos(self) -> Sequence[Funcionario]:
        return self.db.execute(select(Funcionario)).scalars().all()

    def buscar_por_id(self, id: int) -> Funcionario | None:

        if id is None:
            return None

        return cast(Funcionario | None, self.db.get(Funcionario, id, with_for_update=True))


    '''
    buscar_varios pode retornar múltiplos registros, portanto desativar foi
    restrito a buscar_um — garantindo que apenas um funcionário seja afetado
    por requisição. Ass: Lucas
    '''

    def desativar_funcionario_por_si(self, id: int) -> Funcionario | None:

        funcionario = cast(Funcionario | None, self.db.get(Funcionario, id, with_for_update=True))

        if funcionario is None:
            return None

        funcionario.ativo = False
        return funcionario

    def desativar_funcionario_por_funcionario(self,
                                              id: int | None = None,
                                              email: str | None = None) -> Funcionario | None:

        condicionais = {campo: dado for campo, dado in locals().items()
                        if dado is not None and campo != "self"}

        if not condicionais:
            return None

        if id:
            funcionario = cast(Funcionario | None, self.db.get(Funcionario, id, with_for_update=True))
        else:
            funcionario = self.buscar_um(email=email)

        if funcionario is None:
            return None

        funcionario.ativo = False
        return funcionario


    def exists_email(self, email: str | None = None) -> bool:
        consulta = select(exists().where(Funcionario.email == email))
        return self.db.execute(consulta).scalar()

    def exists_telefone(self, telefone: str | None = None) -> bool:
        consulta = select(exists().where(Funcionario.telefone == telefone))
        return self.db.execute(consulta).scalar()