from fastapi import APIRouter, Depends

from app.core.dependencies import get_servico_service
from app.core.security import get_usuario_atual
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.servico.servico_schema import ServicoCreate, ServicoUpdate, ServicoBase
from app.modules.servico.servico_service import ServicoService
from app.modules.utils.app_exception import *

router = APIRouter(prefix="/servicos", tags=["Serviços"])


@router.get("/",
            response_model=list[ServicoBase],
            status_code=status.HTTP_200_OK)
def buscar_todos_servicos(service: ServicoService = Depends(get_servico_service),
                          usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_todos(usuario_atual)


@router.get("/buscar",
            response_model=list[ServicoBase],
            status_code=status.HTTP_200_OK)
def buscar_varios_servicos(dados_buscar: ServicoBase,
                           service: ServicoService = Depends(get_servico_service),
                           usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_varios(dados_buscar, usuario_atual)


@router.get("/{id}",
            response_model=ServicoBase,
            status_code=status.HTTP_200_OK)
def buscar_servico_por_id(id: int,
                          service: ServicoService = Depends(get_servico_service),
                          usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_por_id(id, usuario_atual)


@router.post("/",
             response_model=ServicoBase,
             status_code=status.HTTP_201_CREATED)
def criar_servico(dados: ServicoCreate,
                  service: ServicoService = Depends(get_servico_service),
                  usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.criar_servico(dados, usuario_atual)


@router.patch("/{id}",
              response_model=ServicoBase,
              status_code=status.HTTP_200_OK)
def atualizar_servico(id: int,
                      dados_novos: ServicoUpdate,
                      service: ServicoService = Depends(get_servico_service),
                      usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_servico(id=id, dados_novos=dados_novos, usuario_atual=usuario_atual)


@router.patch("/{id}/desativar",
              response_model=ServicoBase,
              status_code=status.HTTP_200_OK)
def desativar_servico(id: int,
                      service: ServicoService = Depends(get_servico_service),
                      usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.desativar_servico(id=id, usuario_atual=usuario_atual)