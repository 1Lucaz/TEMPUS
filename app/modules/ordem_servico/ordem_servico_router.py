from fastapi import APIRouter, Depends

from app.core.dependencies import get_ordem_servico_service
from app.core.security import get_usuario_atual
from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.ordem_servico.ordem_servico_schema import OrdemCreate, OrdemUpdate, OrdemBase, OrdemInput
from app.modules.ordem_servico.ordem_servico_service import OrdemServicoService
from app.modules.utils.app_exception import *

router = APIRouter(prefix="/ordens", tags=["Ordens de Serviço"])


@router.get("/",
            response_model=list[OrdemBase],
            status_code=status.HTTP_200_OK)
def buscar_todos_ordens(service: OrdemServicoService = Depends(get_ordem_servico_service),
                        usuario_atual: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.buscar_todos(usuario_atual)


@router.get("/buscar",
            response_model=list[OrdemBase],
            status_code=status.HTTP_200_OK)
def buscar_varios_ordens(dados_buscar: OrdemInput,
                         service: OrdemServicoService = Depends(get_ordem_servico_service),
                         usuario_atual: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.buscar_varios(dados_buscar, usuario_atual)


@router.get("/{id}",
            response_model=OrdemBase,
            status_code=status.HTTP_200_OK)
def buscar_ordem_por_id(id: int,
                        service: OrdemServicoService = Depends(get_ordem_servico_service),
                        usuario_atual: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.buscar_por_id(id, usuario_atual)


@router.post("/",
             response_model=OrdemBase,
             status_code=status.HTTP_201_CREATED)
def criar_ordem(dados: OrdemCreate,
                service: OrdemServicoService = Depends(get_ordem_servico_service),
                usuario_atual: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.criar_ordem(dados, usuario_atual)


@router.patch("/{id}",
              response_model=OrdemBase,
              status_code=status.HTTP_200_OK)
def atualizar_ordem(id: int,
                    dados_novos: OrdemUpdate,
                    service: OrdemServicoService = Depends(get_ordem_servico_service),
                    usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_ordem(id=id, dados_novos=dados_novos, usuario_atual=usuario_atual)


@router.patch("/{id}/desativar",
              response_model=OrdemBase,
              status_code=status.HTTP_200_OK)
def desativar_ordem(id: int,
                    service: OrdemServicoService = Depends(get_ordem_servico_service),
                    usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.desativar_ordem(id=id, usuario_atual=usuario_atual)