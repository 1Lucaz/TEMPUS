from sqlalchemy import Sequence

from app.core.security import password_hash, generate_password_hash
from app.modules.cliente.cliente_model import Cliente
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteResponse, ClienteUpdate, ClienteInput
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.utils.app_exception import Conflict, BadRequest, NotFound, Unauthorized


class ClienteService:

    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def buscar_varios_cliente(self, dados: ClienteInput, usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        condicoes = dados.model_dump(exclude_none=True)

        if not condicoes:
            raise BadRequest(causa="Nenhum critério de busca informado")

        return self.repository.buscar_varios(**condicoes)


    def buscar_um_cliente(self, dados: ClienteInput, usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        condicoes = dados.model_dump(exclude_none=True)

        if not condicoes:
            raise BadRequest(causa="Nenhum critério de busca informado")

        resultado = self.repository.buscar_um(**condicoes)

        if resultado is None:
            raise NotFound(causa="Cliente não encontrado")

        return resultado


    def buscar_todos_cliente(self, usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        return self.repository.buscar_todos()


    def criar_cliente_funcionario(self, cliente: ClienteCreate, usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

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


    def desativar_cliente_por_cliente(self, usuario_atual):

        if not isinstance(usuario_atual, ClienteResponse):
            raise Unauthorized(causa="Você não está autorizado")

        return self.repository.desativar_cliente_por_cliente(usuario_atual.id)

    def desativar_cliente_por_funcionario(self, dados_buscar, usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        condicoes = dados_buscar.model_dump(exclude_none=True, exclude={"ativo"})

        if not condicoes:
            raise BadRequest(causa="Nenhum critério informado")

        cliente = self.repository.desativar_cliente_por_funcionario(**condicoes)

        if cliente is None:
            raise NotFound(causa="Cliente não encontrado")

        return cliente


    def atualizar_cliente_por_cliente(self, dados_novos: ClienteUpdate, usuario_atual):

        if not isinstance(usuario_atual, ClienteResponse):
            raise Unauthorized(causa="Você não está autorizado")

        dados = dados_novos.model_dump(exclude_none=True)

        if not dados:
            raise BadRequest(causa="Nenhum dado para atualização")

        return self.repository.atualizar_cliente_por_cliente(usuario_atual.id, dados)


    def atualizar_cliente_por_funcionario(self,
                                          dados_novos: ClienteUpdate,
                                          dados_buscar: ClienteInput,
                                          usuario_atual):

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado")

        dados_novos = dados_novos.model_dump(exclude_none=True)
        dados_filtro = dados_buscar.model_dump(exclude_none=True)

        if not dados_novos:
            raise BadRequest(causa="Nenhum dado para atualização")

        if not dados_filtro:
            raise BadRequest(causa="Nenhum critério de busca informado")

        return self.repository.atualizar_cliente_por_funcionario(
            dados_novos=dados_novos,
            dados_buscar=dados_filtro
        )