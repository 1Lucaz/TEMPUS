from sqlalchemy.orm import Session
from app.modules.funcionario.funcionario_model import Funcionario


class FuncionarioRepository:

    def __init__(self, db: Session):
        self.db = db

    def salvar_funcionario(self, funcionario: Funcionario) -> Funcionario:
        self.db.add(funcionario)
        self.db.flush()
        return funcionario

    def atualizar_funcionario(self,
                            id: int,
                            dados_novos: dict) -> type[Funcionario] | None:

        if id is None or dados_novos is None:
            return None

        funcionario_antigo = self.db.get(Funcionario, id)

        if funcionario_antigo is None:
            return None

        for campo, valor in dados_novos.items():
            if hasattr(funcionario_antigo, campo):
                setattr(funcionario_antigo, campo, valor)

        self.db.flush()
        return funcionario_antigo


    def busca_dinamica (self,
                        nome: str | None = None,
                        email: str | None = None,
                        telefone:str | None = None,
                        ativo: bool | None = None,
                        is_admin: bool | None = None) -> list [type[Funcionario]]:


        query = self.db.query(Funcionario)

        condicionais : dict = {"nome": nome,
                               "email": email,
                               "telefone": telefone,
                               "ativo": ativo,
                               "is_admin": is_admin}

        for campo, dado in condicionais.items():

            if dado is None:
                continue

            if campo == "nome":
                coluna = getattr(Funcionario, campo)
                query = query.filter(coluna.ilike(f"%{dado}%"))

            else:
                query = query.filter_by(**{campo: dado})

        return query.all()



    '''
    a busca dinâmica pode buscar um ou vários clientes e, devido a confiabilidade, a função desativar foi limitada
    para efetuar isso apenas quando for retornado um único e inequívoco registro, evitando que mais de um cliente possa 
    ser desativado a cada requisição. Ass: Lucas
    '''

    def desativar_funcionario(self,
                            id: int | None = None,
                            email: str | None = None,
                            telefone: str | None = None) -> type[Funcionario] | None:

        condicionais = {"id": id, "email": email, "telefone": telefone}

        if email is None and telefone is None and id is None:
            return None

        if id is not None:
            funcionario = self.db.get(Funcionario, id)

        else:

            funcionario = self.db.query(Funcionario)

            for campo, dado in condicionais.items():
                if dado is None:
                    continue

                else:
                    funcionario = funcionario.query(Funcionario).filter_by(**{campo: dado})

            funcionario = funcionario.first()

        if funcionario is None:
            return None

        else:
            funcionario.ativo = False
            self.db.flush()
            return funcionario


    def buscar_por_id (self, id: int) -> type[Funcionario] | None:

        if id is None:
            return None

        else:
            funcionario = self.db.get(Funcionario, id)

            if funcionario is None:
                return None
            else:
                return funcionario


    def exists_email (self, email:str | None = None) -> bool:
        return self.db.query(Funcionario).filter_by(email=email).exists().scalar()

    def exists_telefone(self, telefone: str | None = None) -> bool:
        return self.db.query(Funcionario).filter_by(telefone=telefone).exists().scalar()
