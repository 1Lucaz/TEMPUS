from fastapi import APIRouter
from TEMPUS.app.modules.cliente import cliente_router
from TEMPUS.app.modules.funcionario import funcionario_router
from TEMPUS.app.modules.item_servico import item_servico_router
from TEMPUS.app.modules.ordem_servico import ordem_servico_router
from TEMPUS.app.modules.servico import servico_router


api_router = APIRouter()
api_router.include_router(cliente_router.router)
api_router.include_router(funcionario_router.router)
api_router.include_router(item_servico_router.router)
api_router.include_router(ordem_servico_router.router)
api_router.include_router(servico_router.router)
