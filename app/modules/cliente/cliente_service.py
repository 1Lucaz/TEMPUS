from sqlalchemy import Sequence

from app.core.security import password_hash, generate_password_hash
from app.modules.cliente.cliente_model import Cliente
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteResponse, ClienteUpdate
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.utils.app_exception import Conflict, BadRequest, NotFound, Unauthorized


class ClienteService:

    def __init__(self, repository: ClienteRepository):
        self.repository = repository

    def buscar_varios_cliente(self,
                              dados: ClienteResponse,
                              usuario_atual: FuncionarioResponse | ClienteResponse) -> list[Cliente]:

        if isinstance(usuario_atual, ClienteResponse):
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        elif isinstance(usuario_atual, FuncionarioResponse) and not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        else:
            condicoes_pesquisa: dict = {campo: dado for campo, dado in dados.items() if dado is not None}
            return self.repository.buscar_varios(**condicoes_pesquisa)

    def buscar_um_cliente(self,
                          dados: ClienteResponse,
                          usuario_atual: FuncionarioResponse | ClienteResponse) -> Cliente:

        if isinstance(usuario_atual, ClienteResponse):
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        elif isinstance(usuario_atual, FuncionarioResponse) and not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        condicoes_pesquisa: dict = {campo: dado for campo, dado in dados.items() if dado is not None}
        return self.repository.buscar_um(**condicoes_pesquisa)

    def buscar_todos_cliente(self,
                             usuario_atual: FuncionarioResponse | ClienteResponse) -> Sequence[Cliente]:

        if isinstance(usuario_atual, ClienteResponse):
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        elif isinstance(usuario_atual, FuncionarioResponse) and not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        return self.repository.buscar_todos()

    def criar_cliente_funcionario(self,
                                  cliente: ClienteCreate,
                                  usuario_atual: FuncionarioResponse | ClienteResponse) -> Cliente | None:

        if isinstance(usuario_atual, ClienteResponse) or isinstance(usuario_atual,
                                                                    FuncionarioResponse) and not usuario_atual.access_cliente:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if self.repository.exists_email(email=str(cliente.email)) or self.repository.exists_telefone(
                telefone=cliente.telefone):
            raise Conflict(causa="Email ou telefone já em uso")

        senha_hash = generate_password_hash(cliente.password)

        cliente_novo = Cliente(
            nome=cliente.nome,
            email=str(cliente.email),
            telefone=cliente.telefone,
            senha=senha_hash
        )

        self.repository.registrar_cliente(cliente_novo)
        return cliente_novo

    def criar_cliente_publico(self, cliente: ClienteCreate) -> Cliente:

        if self.repository.exists_email(email=str(cliente.email)) or self.repository.exists_telefone(
                telefone=cliente.telefone):
            raise Conflict(causa="Email ou telefone já em uso")

        senha_hash = generate_password_hash(cliente.password)

        cliente_novo = Cliente(
            nome=cliente.nome,
            email=str(cliente.email),
            telefone=cliente.telefone,
            senha=senha_hash
        )

        self.repository.registrar_cliente(cliente_novo)
        return cliente_novo

    def desativar_cliente_por_cliente (self,
                                      usuario_atual: ClienteResponse | FuncionarioResponse) -> Cliente | None:

        if isinstance(usuario_atual, ClienteResponse):
            return self.repository.desativar_cliente_por_cliente(usuario_atual.id)

        else:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

    def desativar_cliente_por_funcionario (self,
                                          dados_buscar: ClienteResponse | None,
                                          usuario_atual: ClienteResponse | FuncionarioResponse) -> Cliente | None:

        if isinstance(usuario_atual, FuncionarioResponse):
            if usuario_atual.access_cliente:
                return self.repository.atualizar_cliente_por_funcionario(dados_buscar=dados_buscar,
                                                                         dados_novos=dados_novos.model_dump())
            else:
                raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        else:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")


    def atualizar_cliente_por_cliente(self,
                          dados_novos: ClienteUpdate,
                          usuario_atual: ClienteResponse | FuncionarioResponse) -> Cliente | None:

        if isinstance(usuario_atual, ClienteResponse):
            return self.repository.atualizar_cliente_por_cliente (usuario_atual.id, dados_novos.model_dump())

        else:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

    def atualizar_cliente_por_funcionario(self,
                                      dados_novos: ClienteUpdate,
                                      dados_buscar: ClienteResponse | None,
                                      usuario_atual: ClienteResponse | FuncionarioResponse) -> Cliente | None:

        if isinstance(usuario_atual, FuncionarioResponse):
            if usuario_atual.access_cliente:
                return self.repository.atualizar_cliente_por_funcionario (dados_buscar=dados_buscar, dados_novos=dados_novos.model_dump())
            else:
                raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        else:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")
