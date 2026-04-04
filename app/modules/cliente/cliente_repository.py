from typing import Sequence, cast

from app.modules.cliente.cliente_model import Cliente
from sqlalchemy.orm import Session
from sqlalchemy import select, exists


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        return cliente

    def atualizar_cliente_por_cliente   (self,
                                        id: int | None,
                                        dados_novos: dict) -> Cliente | None:

        if not dados_novos:
            return None

        cliente_antigo = cast (Cliente | None, self.db.get(Cliente, id))

        if cliente_antigo is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(cliente_antigo, campo):
                setattr(cliente_antigo, campo, valor)

        return cliente_antigo

    def atualizar_cliente_por_funcionario(self,
                                          dados_novos: dict,
                                          dados_buscar: dict | None) -> Cliente | None:

        if not dados_novos or not dados_buscar:
            return None

        if dados_buscar.get("id"):
            cliente_antigo = self.db.get(Cliente, dados_buscar.get("id"))
        else:
            cliente_antigo = self.buscar_um(**dados_buscar)

        if cliente_antigo is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(cliente_antigo, campo):
                setattr(cliente_antigo, campo, valor)

        return cliente_antigo

    def buscar_um   (self,
                    nome: str | None = None,
                    email: str | None = None,
                    telefone: str | None = None,
                    ativo: bool | None = None) -> Cliente | None:

        condicionais = {campo: dado for campo, dado in locals().items() if dado is not None and campo != "self"}

        consulta = select(Cliente).with_for_update(True)

        for campo, dado in condicionais.items():

            if dado is None:
                pass

            elif campo == "nome":
                consulta = consulta.where(Cliente.nome.ilike(f"%{dado}%"))

            elif campo == "ativo":
                consulta = consulta.where(Cliente.ativo.is_(dado))

            else:
                coluna = getattr(Cliente, campo)
                consulta = consulta.where(coluna == dado)

        if not condicionais:
            return None

        return self.db.execute(consulta).scalar_one_or_none()

    def buscar_varios   (self,
                        nome: str | None = None,
                        email: str | None = None,
                        telefone: str | None = None,
                        ativo: bool | None = None) -> Sequence[Cliente] | None:

        condicionais = {campo: dado for campo, dado in locals().items() if dado is not None and campo != "self"}

        consulta = select(Cliente).with_for_update(True)

        for campo, dado in condicionais.items():

            if campo == "nome":
                consulta = consulta.where(Cliente.nome.ilike(f"%{dado}%"))

            elif campo == "ativo":
                consulta = consulta.where(Cliente.ativo.is_(dado))

            else:
                coluna = getattr(Cliente, campo)
                consulta = consulta.where(coluna == dado)

        if not condicionais:
            return None

        return self.db.execute(consulta).scalars().all()

    '''
    a buscar_varios pode buscar um ou vários clientes e, devido a confiabilidade, a função desativar foi limitada
    para efetuar isso apenas quando for retornado um único e inequívoco registro, evitando que mais de um cliente possa 
    ser desativado a cada requisição. Ass: Lucas
    '''

    def buscar_todos(self) -> Sequence[Cliente]:
        return self.db.execute(select(Cliente)).scalars().all()

    def desativar_cliente_por_cliente (self,
                          id: int | None = None) -> Cliente | None:

        if id:
            cliente = cast(Cliente | None, self.db.get(Cliente, id, with_for_update=True))

            if cliente is None:
                return None

            cliente.ativo = False
            return cliente


    def desativar_cliente_por_funcionario(self,
                          id: int | None = None,
                          email: str | None = None,
                          telefone: str | None = None) -> Cliente | None:

        condicionais = {campo: dado for campo, dado in locals().items() if dado is not None and campo != "self"}

        if not condicionais:
            return None

        if id:
            cliente = cast (Cliente | None, self.db.get(Cliente, id, with_for_update=True))

            if cliente is None:
                return None

            cliente.ativo = False
            return cliente


        elif id is None:
            cliente = self.buscar_um(email=email, telefone=telefone)

            if cliente is None:
                return None

            cliente.ativo = False

            return cliente

        return None

    def buscar_por_id(self, id: int) -> Cliente | None:

        if id is None:
            return None

        else:
            cliente = self.db.get(Cliente, id, with_for_update=True)

            if cliente is None:
                return None
            else:
                return cliente

    def exists_email(self, email: str | None = None) -> bool:
        consulta = select(exists().where(Cliente.email == email))
        return self.db.execute(consulta).scalar()

    def exists_telefone(self, telefone: str | None = None) -> bool:
        consulta = select(exists().where(Cliente.telefone == telefone))
        return self.db.execute(consulta).scalar()
