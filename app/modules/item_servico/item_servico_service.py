from typing import Sequence

from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.item_servico.item_servico_model import ItemServico
from app.modules.item_servico.item_servico_repository import ItemServicoRepository
from app.modules.item_servico.item_servico_schema import ItemCreate, ItemUpdate, ItemBase
from app.modules.utils.app_exception import Unauthorized, NotFound, BadRequest, Conflict


class ItemServicoService:

    def __init__(self, repository: ItemServicoRepository):
        self.repository = repository

    def buscar_varios(self,
                      dados: ItemBase,
                      usuario_atual: FuncionarioResponse) -> Sequence[ItemServico] | None:

        if not usuario_atual.access_item_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        condicionais = {campo: dado for campo, dado in dados.model_dump().items() if dado is not None}
        return self.repository.buscar_varios(**condicionais)

    def buscar_todos(self,
                     usuario_atual: FuncionarioResponse) -> Sequence[ItemServico]:

        if not usuario_atual.access_item_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        return self.repository.buscar_todos()

    def buscar_por_id(self,
                      id: int,
                      usuario_atual: FuncionarioResponse) -> ItemServico:

        if not usuario_atual.access_item_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        item = self.repository.buscar_por_id(id)

        if item is None:
            raise NotFound(causa="Item não encontrado")

        return item

    def criar_item(self,
                   dados: ItemCreate,
                   usuario_atual: FuncionarioResponse) -> ItemServico:

        if not usuario_atual.access_item_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if not self.repository.exists_servico(dados.servico_id):
            raise NotFound(causa="Serviço não existe ou está inativo")

        if not self.repository.exists_ordem_servico(dados.ordem_servico_id):
            raise NotFound(causa="Ordem de serviço não existe ou está inativa")

        item_novo = ItemServico(
            ordem_servico_id=dados.ordem_servico_id,
            servico_id=dados.servico_id,
            valor=dados.valor,
        )

        return self.repository.registrar_item(item_novo)

    def atualizar_item(self,
                       id: int,
                       dados_novos: ItemUpdate,
                       usuario_atual: FuncionarioResponse) -> ItemServico | None:

        if not usuario_atual.access_item_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        dados = dados_novos.model_dump(exclude_none=True)

        if not dados:
            raise BadRequest(causa="Nenhum dado informado para atualização")

        item = self.repository.atualizar_item(id=id, dados_novos=dados)

        if item is None:
            raise NotFound(causa="Item não encontrado")

        return item

    def desativar_item(self,
                       id: int,
                       usuario_atual: FuncionarioResponse) -> ItemServico | None:

        if not usuario_atual.access_item_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        item = self.repository.desativar_item(id=id)

        if item is None:
            raise NotFound(causa="Item não encontrado")

        return item