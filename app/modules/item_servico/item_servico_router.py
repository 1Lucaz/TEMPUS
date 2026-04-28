from fastapi import APIRouter, Depends, status
from typing import Union
from app.core.dependencies import get_item_servico_service
from app.core.security import get_usuario_atual
from app.modules.funcionario.funcionario_schema import FuncionarioResponse
from app.modules.cliente.cliente_schema import ClienteResponse
from app.modules.item_servico.item_servico_service import ItemServicoService
from app.modules.item_servico.item_servico_schema import ItemCreate, ItemUpdate, ItemResponse, ItemInput

router = APIRouter(prefix="/itens", tags=["Itens de Serviço"])

@router.get("/", response_model=list[ItemResponse])
def buscar_todos_itens(service: ItemServicoService = Depends(get_item_servico_service),
                       usuario: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.buscar_todos(usuario)

@router.post("/buscar", response_model=list[ItemResponse])
def buscar_varios_itens(dados_buscar: ItemInput,
                        service: ItemServicoService = Depends(get_item_servico_service),
                        usuario: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.buscar_varios(dados_buscar, usuario)

@router.get("/{id}", response_model=ItemResponse)
def buscar_item_por_id(id: int,
                       service: ItemServicoService = Depends(get_item_servico_service),
                       usuario: FuncionarioResponse | ClienteResponse = Depends(get_usuario_atual)):
    return service.buscar_por_id(id, usuario)

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def criar_item(dados: ItemCreate,
               service: ItemServicoService = Depends(get_item_servico_service),
               usuario: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.criar_item(dados, usuario)

@router.patch("/{id}", response_model=ItemResponse)
def atualizar_item(id: int, dados_novos: ItemUpdate,
                   service: ItemServicoService = Depends(get_item_servico_service),
                   usuario: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.atualizar_item(id, dados_novos, usuario)

@router.patch("/{id}/desativar", response_model=ItemResponse)
def desativar_item(id: int,
                   service: ItemServicoService = Depends(get_item_servico_service),
                   usuario: FuncionarioResponse = Depends(get_usuario_atual)):
    return service.desativar_item(id, usuario)