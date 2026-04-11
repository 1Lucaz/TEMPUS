from typing import Sequence

from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.servico.servico_model import Servico
from app.modules.servico.servico_repository import ServicoRepository
from app.modules.servico.servico_schema import ServicoCreate, ServicoUpdate, ServicoResponse, ServicoInput
from app.modules.utils.app_exception import Unauthorized, NotFound, BadRequest, Conflict


class ServicoService:

    def __init__(self, repository: ServicoRepository):
        self.repository = repository

    def buscar_varios(self,
                      dados: ServicoInput,
                      usuario_atual: FuncionarioResponse) -> Sequence[Servico] | None:

        if not usuario_atual.access_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        condicionais = {campo: dado for campo, dado in dados.model_dump().items() if dado is not None}
        return self.repository.buscar_varios(**condicionais)

    def buscar_todos(self, usuario_atual: FuncionarioResponse) -> Sequence[Servico]:

        if not usuario_atual.access_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        return self.repository.buscar_todos()

    def buscar_por_id(self, id: int, usuario_atual: FuncionarioResponse) -> Servico:

        if not usuario_atual.access_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        servico = self.repository.buscar_por_id(id)

        if servico is None:
            raise NotFound(causa="Serviço não encontrado")

        return servico

    def criar_servico(self, dados: ServicoCreate, usuario_atual: FuncionarioResponse) -> Servico:

        if not usuario_atual.access_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if self.repository.exists_descricao(dados.descricao):
            raise Conflict(causa="Já existe um serviço com esta descrição")

        servico_novo = Servico(
            descricao=dados.descricao,
            valor_base=dados.valor_base,
        )

        return self.repository.registrar_servico(servico_novo)

    def atualizar_servico(self,
                          id: int,
                          dados_novos: ServicoUpdate,
                          usuario_atual: FuncionarioResponse) -> Servico | None:

        if not usuario_atual.access_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        dados = dados_novos.model_dump(exclude_none=True)

        if not dados:
            raise BadRequest(causa="Nenhum dado informado para atualização")

        servico = self.repository.atualizar_servico(id=id, dados_novos=dados)

        if servico is None:
            raise NotFound(causa="Serviço não encontrado")

        return servico

    def desativar_servico(self,
                          dados_buscar: ServicoInput,
                          usuario_atual: FuncionarioResponse) -> Servico | None:

        if not usuario_atual.access_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        servico = self.repository.desativar_servico()

        if servico is None:
            raise NotFound(causa="Serviço não encontrado")

        return servico