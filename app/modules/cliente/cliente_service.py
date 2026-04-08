from app.core.security import generate_password_hash
from app.modules.cliente.cliente_model import Cliente
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteResponse, ClienteUpdate, ClienteRequest
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.utils.app_exception import Conflict, BadRequest, NotFound, Unauthorized


class ClienteService:

    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def buscar_varios_cliente(self,
                              dados: ClienteRequest,
                              usuario_atual: ClienteResponse | FuncionarioResponse):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        condicoes = dados.model_dump(exclude_none=True, exclude={"id"})

        if not condicoes:
            raise BadRequest(causa="Nenhum critério de busca informado")

        return self.repository.buscar_varios(**condicoes)

    def buscar_todos_cliente(self, usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        return self.repository.buscar_todos()

    def criar_cliente_funcionario(self,
                                  cliente_novo: ClienteCreate,
                                  usuario_atual: ClienteResponse | FuncionarioResponse):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        if self.repository.exists_email(cliente_novo.email) or self.repository.exists_telefone(cliente_novo.telefone):
            raise Conflict(causa="Email ou telefone já em uso")

        cliente_novo = Cliente(
            nome=cliente_novo.nome,
            email=str(cliente_novo.email),
            telefone=cliente_novo.telefone,
            senha=generate_password_hash(cliente_novo.senha),
            ativo=cliente_novo.ativo,
        )

        self.repository.registrar_cliente(cliente_novo)
        return cliente_novo

    def criar_cliente_publico(self, cliente: ClienteCreate):

        if self.repository.exists_email(cliente.email) or self.repository.exists_telefone(cliente.telefone):
            raise Conflict(causa="Email ou telefone já em uso")

        cliente_novo = Cliente(
            nome=cliente.nome,
            email=str(cliente.email),
            telefone=cliente.telefone,
            senha=generate_password_hash(cliente.senha)
        )

        self.repository.registrar_cliente(cliente_novo)
        return cliente_novo

    def desativar_cliente(self,
                          dados_buscar: ClienteRequest,
                          usuario_atual: ClienteResponse | FuncionarioResponse):

        if isinstance(usuario_atual, FuncionarioResponse):
            if not dados_buscar:
                raise BadRequest(causa="Você não inseriu nenhum dado de busca")

            if not usuario_atual.access_cliente:
                raise Unauthorized(causa="Você não tem permissão para isso")

            else:

                cliente = self.repository.buscar_um(**dados_buscar.model_dump(exclude_none=True))

                if cliente is None:
                    raise NotFound(causa="Nenhum cliente foi encontrado com base nesses dados")

                return self.repository.desativar_cliente(id=cliente.id,
                                                         nome_autor=usuario_atual.nome,
                                                         email_autor=str(usuario_atual.email))

        elif isinstance(usuario_atual, ClienteResponse):

            cliente = self.repository.buscar_por_id(usuario_atual.id)

            if cliente is None:
                raise NotFound(causa="Nenhum cliente foi encontrado com base nesses dados")

            return self.repository.desativar_cliente(id=cliente.id,
                                                     nome_autor=usuario_atual.nome,
                                                     email_autor=str(usuario_atual.email))

        else:
            raise Unauthorized(
                causa="Você é um negócio que não identificamos e que não deveria estar aqui. Por isso não está autorizado a realizar esta ação")

    def atualizar_cliente(self,
                          dados_novos: ClienteUpdate,
                          dados_buscar: ClienteRequest | None,
                          usuario_atual):

        if not dados_novos:
            raise BadRequest(causa="Você não inseriu nenhum dado novo")

        if isinstance(usuario_atual, FuncionarioResponse):
            if not dados_buscar:
                raise BadRequest(causa="Você não inseriu nenhum dado de busca")

            if not usuario_atual.access_cliente:
                raise Unauthorized(causa="Você não tem permissão para isso")

            else:
                cliente = self.repository.buscar_um(**dados_buscar.model_dump(exclude_none=True))

                if cliente is None:
                    raise NotFound(causa="Nenhum cliente foi encontrado com base nesses dados")

            return self.repository.atualizar_cliente(id=cliente.id,
                                                     dados_novos=dados_novos.model_dump(exclude_none=True))

        elif isinstance(usuario_atual, ClienteResponse):

            dados_novos = dados_novos.model_dump(exclude_none=True)
            cliente = self.repository.buscar_por_id(usuario_atual.id)

            if cliente is None:
                raise NotFound(causa="Nenhum cliente foi encontrado com base nesses dados")

            return self.repository.atualizar_cliente(id=cliente.id,
                                                     dados_novos=dados_novos)

        else:
            raise Unauthorized(
                causa="Você é um negócio que não identificamos e que não deveria estar aqui. Por isso não está autorizado a realizar esta ação")
