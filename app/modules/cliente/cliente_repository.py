from app.modules.cliente.cliente_model import Cliente
from sqlalchemy.orm import Session

class ClienteRepository:

    def __init__ (self, db: Session):
        self.db = db

    def salvar_cliente(self, cliente: Cliente) -> Cliente:
        self.db.add(cliente)
        self.db.flush()
        return cliente

    def atualizar_cliente(self,
                            id: int,
                            dados_novos: dict) -> type[Cliente] | None:

        if id is None or dados_novos is None:
            return None

        cliente_antigo = self.db.get(Cliente, id)

        if cliente_antigo is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(cliente_antigo, campo):
                setattr(cliente_antigo, campo, valor)

        self.db.flush()
        return cliente_antigo


    def busca_dinamica (self,
                         nome: str | None = None,
                         email: str | None = None,
                         telefone: str | None = None,
                         ativo: bool | None = None) -> list [Cliente]:


        query = self.db.query(Cliente)

        condicionais : dict = {"nome": nome, "email": email, "telefone": telefone, "ativo": ativo}

        for campo, dado in condicionais.items():

            if dado is None:
                continue

            if campo == "nome":
                coluna = getattr(Cliente, campo)
                query = query.filter(coluna.ilike(f"%{dado}%"))

            else:
                query = query.filter_by(**{campo: dado})

        return query.all()

    def


    '''
    a busca dinâmica pode buscar um ou vários clientes e, devido a confiabilidade, a função desativar foi limitada
    para efetuar isso apenas quando for retornado um único e inequívoco registro, evitando que mais de um cliente possa 
    ser desativado a cada requisição. Ass: Lucas
    '''

    def desativar_cliente(self,
                            id: int | None = None,
                            email: str | None = None,
                            telefone: str | None = None) -> type[Cliente] | None:

        condicionais = {"id": id, "email": email, "telefone": telefone}

        if email is None and telefone is None and id is None:
            return None

        if id is not None:
            cliente = self.db.get(Cliente, id)

        else:

            cliente = self.db.query(Cliente)

            for campo, dado in condicionais.items():
                if dado is None:
                    continue

                else:
                    cliente = cliente.query(Cliente).filter_by(**{campo: dado})

            cliente = cliente.first()

        if cliente is None:
            return None

        if not cliente.ativo:
            return Cliente

        else:
            cliente.ativo = False
            self.db.flush()
            return cliente


    def buscar_por_id (self, id: int) -> type[Cliente] | None:

        if id is None:
            return None

        else:
            cliente = self.db.get(Cliente, id)

            if cliente is None:
                return None
            else:
                return cliente


    def exists_email (self, email:str | None = None) -> bool:
        return self.db.query(Cliente).filter_by(email=email).exists().scalar()

    def exists_telefone(self, telefone: str | None = None) -> bool:
        return self.db.query(Cliente).filter_by(telefone=telefone).exists().scalar()