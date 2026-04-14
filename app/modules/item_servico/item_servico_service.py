from typing import Sequence, Union
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.item_servico.item_servico_model import ItemServico
from app.modules.item_servico.item_servico_repository import ItemServicoRepository
from app.modules.item_servico.item_servico_schema import ItemCreate, ItemUpdate, ItemInput
from app.modules.utils.app_exception import Unauthorized, NotFound, BadRequest


class ItemServicoService:
    def __init__(self, repository: ItemServicoRepository):
        self.repository = repository

    def buscar_varios(self,
                      dados: ItemInput,
                      usuario: FuncionarioResponse | ClienteResponse) -> Sequence[ItemServico]:
        if isinstance(usuario, FuncionarioResponse):
            if not usuario.access_item_servico:
                raise Unauthorized(causa="Acesso negado aos itens de serviço")
            return self.repository.buscar_varios(ordem_id=dados.ordem_servico_id, servico_id=dados.servico_id,
                                                 ativo=dados.ativo)

        return self.repository.buscar_varios(cliente_id=usuario.id, ativo=True)

    def buscar_todos(self, usuario: FuncionarioResponse | ClienteResponse) -> Sequence[ItemServico]:
        if isinstance(usuario, ClienteResponse) or not usuario.access_item_servico:
            raise Unauthorized(causa="Acesso restrito a funcionários autorizados")
        return self.repository.buscar_todos()

    def buscar_por_id(self, id: int, usuario: FuncionarioResponse | ClienteResponse) -> ItemServico:
        if isinstance(usuario, FuncionarioResponse):
            if not usuario.access_item_servico:
                raise Unauthorized(causa="Acesso negado")
            item = self.repository.buscar_por_id(id)
        else:
            item = self.repository.buscar_um(id=id, cliente_id=usuario.id)

        if not item:
            raise NotFound(causa="Item não encontrado ou acesso negado")
        return item

    def criar_item(self, dados: ItemCreate, usuario: FuncionarioResponse) -> ItemServico:
        if not usuario.access_item_servico:
            raise Unauthorized(causa="SEM PERMISSÃO PLAYBOYYY")
        if not self.repository.exists_servico(dados.servico_id):
            raise NotFound(causa="Serviço inválido")
        if not self.repository.exists_ordem_servico(dados.ordem_servico_id):
            raise NotFound(causa="Ordem de serviço inválida")

        return self.repository.registrar_item(ItemServico(
            ordem_servico_id=dados.ordem_servico_id,
            servico_id=dados.servico_id,
            valor=dados.valor
        ))

    def atualizar_item(self, id: int, dados_novos: ItemUpdate, usuario: FuncionarioResponse) -> ItemServico:
        if not usuario.access_item_servico:
            raise Unauthorized(causa="Permissão insuficiente")

        payload = dados_novos.model_dump(exclude_none=True)
        if not payload:
            raise BadRequest(causa="Dados ausentes")

        item = self.repository.atualizar_item(id, payload)
        if not item:
            raise NotFound(causa="Item inexistente")
        return item

    def desativar_item(self, id: int, usuario: FuncionarioResponse) -> ItemServico:
        if not usuario.access_item_servico or not isinstance(usuario, FuncionarioResponse):
            raise Unauthorized(causa="Permissão insuficiente")
        item = self.repository.buscar_um(id)
        if not item:
            raise NotFound(causa="Item inexistente")
        else:
            return self.repository.desativar_item(item.id)
