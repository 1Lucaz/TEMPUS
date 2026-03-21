from app.core.security import password_hash, generate_password_hash
from app.modules.cliente.cliente_model import Cliente
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteResponse
from app.modules.utils.app_exception import Conflict, BadRequest, NotFound



class ClienteService:

    def __init__ (self, repository: ClienteRepository):
        self.repository = repository

    def listar(self, id: int | None = None,
               ativo: bool | None = None,
               nome: str | None = None,
               email: str | None = None,
               telefone: str | None = None) -> list [Cliente]:

        condicoes_exigidas : dict = {"id": id, "ativo": ativo, "nome": nome, "email": email, "telefone": telefone}
        condicoes_pesquisa: dict = {campo : dado for campo, dado in condicoes_exigidas.items() if dado is not None}

        return self.repository.busca_dinamica(**condicoes_pesquisa)


    def criar_cliente(self, cliente: ClienteCreate) -> Cliente:

        if self.repository.busca_dinamica(email=str(cliente.email)) or self.repository.busca_dinamica(telefone=cliente.telefone):
            raise Conflict()

        senha_hash = generate_password_hash(cliente.password)

        cliente_novo = Cliente (
            nome = cliente.nome,
            email=str(cliente.email),
            telefone=cliente.telefone,
            senha=senha_hash
        )

        self.repository.salvar_cliente(cliente_novo)
        return cliente_novo


    def atualizar(self,
                  id: int,
                  nome: str | None = None,
                  email: str | None = None,
                  telefone: str | None = None) -> Cliente | None:

        if nome is None and email is None and telefone is None:
            raise BadRequest(causa="Não há nenhum parâmetro para buscar o cliente")

        dados_novos: dict = {campo : dado for campo, dado in
                             {"nome": nome, "email": email, "telefone": telefone}.items() if dado is not None}


        cliente = self.repository.buscar_por_id(id)

        if cliente:

            if ClienteRepository.exists_email(dados_novos.get("email")):
                raise Conflict (causa="Este email já está em uso")

            if ClienteRepository.exists_telefone(dados_novos.get("telefone")):
                raise Conflict(causa="Este telefone já está em uso")

            else:
                cliente = self.repository.atualizar_cliente(id, dados_novos)
                return cliente

        else:
            raise NotFound(causa="Cliente não encontrado")



    def desativar(self, cliente: ClienteResponse) -> type[Cliente]:

        if cliente.id is None and cliente.email is None and cliente.telefone is None:
            raise BadRequest(causa="Não há nenhum parâmetro para desativar o cliente")

        cliente = self.repository.desativar_cliente(id=cliente.id, email=cliente.email, telefone=cliente.telefone)

        if cliente is None:
            raise NotFound(causa="Cliente não encontrado")

        if not cliente.ativo:
            raise Conflict(causa="Cliente já desativado")

        return cliente


