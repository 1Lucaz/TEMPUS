from typing import Sequence

from app.core.security import generate_password_hash
from app.modules.funcionario.funcionario_model import Funcionario
from app.modules.funcionario.funcionario_repository import FuncionarioRepository
from app.modules.funcionario.funcionario_schema import FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse
from app.modules.utils.app_exception import Conflict, BadRequest, NotFound, Unauthorized


class FuncionarioService:

    def __init__(self, repository: FuncionarioRepository):
        self.repository = repository

    def buscar_um_funcionario(self,
                              dados: FuncionarioResponse,
                              usuario_atual: FuncionarioResponse) -> Funcionario:

        if not usuario_atual.access_funcionario:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        condicoes_pesquisa = {campo: dado for campo, dado in dados.model_dump().items() if dado is not None}
        return self.repository.buscar_um(**condicoes_pesquisa)

    def buscar_varios_funcionarios(self,
                                   dados: FuncionarioResponse,
                                   usuario_atual: FuncionarioResponse) -> Sequence[Funcionario]:

        if not usuario_atual.access_funcionario:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        condicoes_pesquisa = {campo: dado for campo, dado in dados.model_dump().items() if dado is not None}
        return self.repository.buscar_varios(**condicoes_pesquisa)

    def buscar_todos_funcionarios(self,
                                  usuario_atual: FuncionarioResponse) -> Sequence[Funcionario]:

        if not usuario_atual.access_funcionario:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        return self.repository.buscar_todos()

    def criar_funcionario(self,
                          dados: FuncionarioCreate,
                          usuario_atual: FuncionarioResponse) -> Funcionario:

        if not usuario_atual.is_admin:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if self.repository.exists_email(email=str(dados.email)):
            raise Conflict(causa="Email já em uso")

        funcionario_novo = Funcionario(
            nome=dados.nome,
            email=str(dados.email),
            cargo=dados.cargo,
            senha=generate_password_hash(dados.senha),
            is_admin=dados.is_admin,
            is_colaborador=dados.is_colaborador,
            access_cliente=dados.access_cliente,
            access_funcionario=dados.access_funcionario,
            access_servico=dados.access_servico,
            access_item_servico=dados.access_item_servico,
            access_ordem_servico=dados.access_ordem_servico,
        )

        return self.repository.registrar_funcionario(funcionario_novo)

    def atualizar_funcionario_por_si(self,
                                     dados_novos: FuncionarioUpdate,
                                     usuario_atual: FuncionarioResponse) -> Funcionario | None:

        dados = dados_novos.model_dump(exclude_none=True)

        if not dados:
            raise BadRequest(causa="Nenhum dado informado para atualização")

        if "email" in dados and self.repository.exists_email(email=dados["email"]):
            raise Conflict(causa="Email já em uso")

        return self.repository.atualizar_funcionario_por_si(id=usuario_atual.id, dados_novos=dados)

    def atualizar_funcionario_por_funcionario(self,
                                              dados_novos: FuncionarioUpdate,
                                              dados_buscar: FuncionarioResponse | None,
                                              usuario_atual: FuncionarioResponse) -> Funcionario | None:

        if not usuario_atual.access_funcionario:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        dados = dados_novos.model_dump(exclude_none=True)

        if not dados:
            raise BadRequest(causa="Nenhum dado informado para atualização")

        if "email" in dados and self.repository.exists_email(email=dados["email"]):
            raise Conflict(causa="Email já em uso")

        return self.repository.atualizar_funcionario_por_funcionario(
            dados_novos=dados,
            dados_buscar=dados_buscar.model_dump(exclude_none=True) if dados_buscar else None
        )

    def desativar_funcionario_por_si(self,
                                     usuario_atual: FuncionarioResponse) -> Funcionario | None:

        resultado = self.repository.desativar_funcionario_por_si(id=usuario_atual.id)

        if resultado is None:
            raise NotFound(causa="Funcionário não encontrado")

        return resultado

    def desativar_funcionario_por_funcionario(self,
                                              dados_buscar: FuncionarioResponse | None,
                                              usuario_atual: FuncionarioResponse) -> Funcionario | None:

        if not usuario_atual.access_funcionario:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if dados_buscar is None:
            raise BadRequest(causa="Nenhum dado informado para busca")

        dados = dados_buscar.model_dump(exclude_none=True)

        resultado = self.repository.desativar_funcionario_por_funcionario(
            id=dados.get("id"),
            email=dados.get("email"),
            telefone=dados.get("telefone")
        )

        if resultado is None:
            raise NotFound(causa="Funcionário não encontrado")

        return resultado