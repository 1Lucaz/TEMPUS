from typing import Sequence

from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.ordem_servico.ordem_servico_model import OrdemServico
from app.modules.ordem_servico.ordem_servico_repository import OrdemServicoRepository
from app.modules.ordem_servico.ordem_servico_schema import OrdemCreate, OrdemUpdate, OrdemInput
from app.modules.utils.app_exception import Unauthorized, NotFound, BadRequest


class OrdemServicoService:

    def __init__(self, repository: OrdemServicoRepository, cliente_repository: ClienteRepository):
        self.repository = repository
        self.cliente_repository = cliente_repository

    def buscar_varios(self,
                      dados: OrdemInput,
                      usuario_atual: FuncionarioResponse | ClienteResponse) -> Sequence[OrdemServico] | None:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        condicionais = dados.model_dump(exclude_none=True)
        return self.repository.buscar_varios(**condicionais)

    def buscar_todos(self,
                     usuario_atual: FuncionarioResponse | ClienteResponse) -> Sequence[OrdemServico]:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        return self.repository.buscar_todos()

    def buscar_por_id(self,
                      id: int,
                      usuario_atual: FuncionarioResponse | ClienteResponse) -> OrdemServico:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        ordem = self.repository.buscar_por_id(id)

        if ordem is None:
            raise NotFound(causa="Ordem de serviço não encontrada")

        return ordem

    def criar_ordem(self,
                    dados: OrdemCreate,
                    usuario_atual: FuncionarioResponse | ClienteResponse) -> OrdemServico:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if not self.cliente_repository.buscar_por_id(dados.cliente_id):
            raise NotFound(causa="Cliente não existe ou está inativo")

        ordem_nova = OrdemServico(
            cliente_id=dados.cliente_id,
            data_abertura=dados.data_abertura,
            status=dados.status.value,
        )

        return self.repository.registrar_ordem(ordem_nova)

    def atualizar_ordem(self,
                        id: int,
                        dados_novos: OrdemUpdate,
                        usuario_atual: FuncionarioResponse) -> OrdemServico | None:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        dados = dados_novos.model_dump(exclude_none=True)

        if not dados:
            raise BadRequest(causa="Nenhum dado informado para atualização")

        if "status" in dados:
            dados["status"] = dados["status"].value

        ordem = self.repository.atualizar_ordem(id=id, dados_novos=dados)

        if ordem is None:
            raise NotFound(causa="Ordem de serviço não encontrada")

        return ordem

    def desativar_ordem(self,
                        id: int,
                        usuario_atual: FuncionarioResponse) -> OrdemServico | None:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        ordem = self.repository.desativar_ordem(id=id)

        if ordem is None:
            raise NotFound(causa="Ordem de serviço não encontrada")

        return ordem