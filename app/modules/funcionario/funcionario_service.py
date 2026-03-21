from app.modules.funcionario.funcionario_model import Funcionario
from app.modules.funcionario.funcionario_repository import FuncionarioRepository
from app.modules.funcionario.funcionario_schema import FuncionarioCreate
from app.modules.utils.app_exception import *
from passlib.hash import pbkdf2_sha256 as hashgenerator


class FuncionarioService:

    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def listar(self, id: int | None = None,
               ativo: bool | None = None,
               nome: str | None = None,
               email: str | None = None,
               is_admin: bool | None = None,
               is_colaborador: bool | None = None,
               telefone: str | None = None) -> list[type[Funcionario]]:

        condicoes_exigidas : dict = {   "id": id,
                                        "ativo": ativo,
                                        "nome": nome,
                                        "email": email,
                                        "telefone": telefone,
                                        "is_admin": is_admin,
                                        "is_colaborador": is_colaborador}

        condicoes_pesquisa: dict = {campo : dado for campo, dado in condicoes_exigidas.items() if dado is not None}

        return self.repository.busca_dinamica(**condicoes_pesquisa)


    def criar_funcionario(self, funcionario: FuncionarioCreate) -> Funcionario:

        if self.repository.busca_dinamica(email=str(funcionario.email)) or self.repository.busca_dinamica(telefone=funcionario.telefone):
            raise Conflict()

        funcionario_novo = Funcionario (
            nome = funcionario.nome,
            email=str(funcionario.email),
            cargo=funcionario.cargo,
            is_admin=funcionario.is_admin,
            is_colaborador=funcionario.is_colaborador,
            senha=hashgenerator.hash(funcionario.senha)
        )

        self.repository.salvar_funcionario(funcionario)
        return funcionario


    def atualizar(self,
                  id: int,
                  nome: str | None = None,
                  email: str | None = None,
                  cargo: str | None = None,
                  is_colaborador: bool | None = None,
                  is_admin: bool | None = None,
                  ) -> Funcionario | None:

        if nome is None and email is None and cargo is None and is_admin is None and is_colaborador is None:
            raise BadRequest(causa="Não há nenhum parâmetro para buscar o cliente")

        dados_novos: dict = {campo:dado for campo,dado in
                             {"nome": nome,
                              "email": email,
                              "cargo": cargo,
                              "is_colaborador":is_colaborador,
                              "is_admin": is_admin}.items() if dado is not None}


        funcionario = self.repository.buscar_por_id(id)

        if funcionario:

            if FuncionarioRepository.exists_email(dados_novos.get("email")):
                raise Conflict (causa="Este email já está em uso")

            if FuncionarioRepository.exists_telefone(dados_novos.get("telefone")):
                raise Conflict(causa="Este telefone já está em uso")

            else:
                funcionario = self.repository.atualizar_funcionario(id, dados_novos)
                return funcionario

        else:
            raise NotFound(causa="Cliente não encontrado")



    def desativar(self, id: int | None = None,
                  email: str | None = None) -> type[Funcionario]:

        if id is None and email is None:
            raise BadRequest(causa="Não há nenhum parâmetro para desativar o cliente")

        cliente = self.repository.desativar_funcionario(id=id, email=email)

        if cliente is None:
            raise NotFound(causa="Cliente não encontrado")

        return cliente