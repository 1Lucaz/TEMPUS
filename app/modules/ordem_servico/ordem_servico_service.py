from typing import Sequence

from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.ordem_servico.ordem_servico_model import OrdemServico
from app.modules.ordem_servico.ordem_servico_repository import OrdemServicoRepository
from app.modules.ordem_servico.ordem_servico_schema import OrdemCreate, OrdemUpdate, OrdemInput
from app.modules.utils.app_exception import Unauthorized, NotFound, BadRequest
from app.modules.utils.prioridade import Prioridade


class OrdemServicoService:

    def __init__(self, repository: OrdemServicoRepository, cliente_repository: ClienteRepository):
        self.repository = repository
        self.cliente_repository = cliente_repository

    def buscar_varios(self,
                      dados: OrdemInput,
                      usuario_atual: FuncionarioResponse | ClienteResponse) -> Sequence[OrdemServico] | None:

        if not isinstance(usuario_atual, FuncionarioResponse) and usuario_atual.access_ordem_servico:
            condicionais = dados.model_dump(exclude_none=True)
            return self.repository.buscar_varios(**condicionais)

        elif isinstance(usuario_atual, ClienteResponse):
            return self.repository.buscar_varios(cliente_id=usuario_atual.id)

        raise Unauthorized (causa="O que você tá fazendo por aqui? 🤔")


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
                    usuario_atual: FuncionarioResponse) -> OrdemServico:

        if not isinstance(usuario_atual, FuncionarioResponse) or not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        if not self.cliente_repository.buscar_por_id(dados.cliente_id):
            raise NotFound(causa="Cliente não existe ou está inativo")

        dados_criar = dados.model_dump()

        if "status" in dados:
            dados["status"] = str(dados["status"])

        if "prioridade" in dados:
            dados["prioridade"] = str(dados["prioridade"])

        ordem_nova = OrdemServico(**dados_criar)

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
            dados["status"] = str(dados["status"])

        if "prioridade" in dados:
            dados["prioridade"] = str(dados["prioridade"])

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

    def buscar_por_prioridade(self,
                      prioridade: Prioridade,
                      usuario_atual: FuncionarioResponse | ClienteResponse) -> Sequence [OrdemServico] | None:

        if not usuario_atual.access_ordem_servico:
            raise Unauthorized(causa="Você não está autorizado a realizar este serviço")

        ordem = self.repository.buscar_por_prioridade(prioridade)

        if ordem is None:
            raise NotFound(causa="Ordem de serviço não encontrada")

        return ordem