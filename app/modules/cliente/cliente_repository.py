from typing import Sequence, cast

from app.modules.cliente.cliente_model import Cliente
from sqlalchemy.orm import Session
from sqlalchemy import select, exists


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.flush()
        return cliente

    def atualizar_cliente(self,
                          id: int,
                          dados_novos: dict,
                          nome_autor: str | None,
                          email_autor: str | None) -> Cliente | None:

        cliente_antigo = cast(Cliente | None, self.db.get(Cliente, id))

        if cliente_antigo is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(cliente_antigo, campo):
                setattr(cliente_antigo, campo, valor)

        cliente_antigo.updated_by = f"atualizado por - NOME: {nome_autor} | EMAIL: {email_autor}"

        return cliente_antigo

    def buscar_um(self,
                  id: int | None = None,
                  nome: str | None = None,
                  email: str | None = None,
                  telefone: str | None = None,
                  ativo: bool | None = None) -> Cliente | None:

        condicionais = {campo: dado for campo, dado in locals().items() if dado is not None and campo != "self"}

        consulta = select(Cliente).with_for_update()

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

    def buscar_varios(self,
                      nome: str | None = None,
                      email: str | None = None,
                      telefone: str | None = None,
                      ativo: bool | None = None) -> Sequence[Cliente] | None:

        condicionais = {campo: dado for campo, dado in locals().items() if dado is not None and campo != "self"}

        consulta = select(Cliente).with_for_update()

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

    def desativar_cliente(self,
                          id: int | None = None,
                          nome_autor: str | None = None,
                          email_autor: str | None = None) -> Cliente | None:

        if id:
            cliente = cast(Cliente | None, self.db.get(Cliente, id, with_for_update=True))

            if cliente is None:
                return None

            cliente.ativo = False
            cliente.updated_by = f"atualizado por - NOME: {nome_autor} | EMAIL: {email_autor}"
            return cliente

        else:
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
