from fastapi import APIRouter
from TEMPUS.modules import cliente_controller, servico_controller, funcionario_controller, ordem_servico_controller, item_servico_controller

api_router = APIRouter()
api_router.include_router(cliente_controller.router)
api_router.include_router(servico_controller.router)
api_router.include_router(funcionario_controller.router)
api_router.include_router(ordem_servico_controller.router)
api_router.include_router(item_servico_controller.router)
