from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_item_servico_service
from app.core.security import get_usuario_atual
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.item_servico.item_servico_service import ItemServicoService
from app.modules.item_servico.item_servico_schema import ItemCreate, ItemUpdate, ItemBase


router = APIRouter(prefix="/itens", tags=["Itens de Serviço"])

@router.get("/",
            response_model=list[ItemBase],
            status_code=status.HTTP_200_OK)
def buscar_todos_itens(service: ItemServicoService = Depends(get_item_servico_service),
                       usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_todos(usuario_atual)


@router.get("/buscar",
            response_model=list[ItemBase],
            status_code=status.HTTP_200_OK)
def buscar_varios_itens(dados_buscar: ItemBase,
                        service: ItemServicoService = Depends(get_item_servico_service),
                        usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_varios(dados_buscar, usuario_atual)


@router.get("/{id}",
            response_model=ItemBase,
            status_code=status.HTTP_200_OK)
def buscar_item_por_id(id: int,
                       service: ItemServicoService = Depends(get_item_servico_service),
                       usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.buscar_por_id(id, usuario_atual)


@router.post("/",
             response_model=ItemBase,
             status_code=status.HTTP_201_CREATED)
def criar_item(dados: ItemCreate,
               service: ItemServicoService = Depends(get_item_servico_service),
               usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.criar_item(dados, usuario_atual)


@router.patch("/{id}",
              response_model=ItemBase,
              status_code=status.HTTP_200_OK)
def atualizar_item(id: int,
                   dados_novos: ItemUpdate,
                   service: ItemServicoService = Depends(get_item_servico_service),
                   usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_item(id=id, dados_novos=dados_novos, usuario_atual=usuario_atual)


@router.patch("/{id}/desativar",
              response_model=ItemBase,
              status_code=status.HTTP_200_OK)
def desativar_item(id: int,
                   service: ItemServicoService = Depends(get_item_servico_service),
                   usuario_atual: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.desativar_item(id=id, usuario_atual=usuario_atual)