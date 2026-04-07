from fastapi import FastAPI

from app.core.dependencies import get_funcionario_service
from app.core.security import generate_password_hash
from app.modules.funcionario.funcionario_model import Funcionario
from app.modules.funcionario.funcionario_repository import FuncionarioRepository
from app.routers.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="TEMPUS - V 1.0.1")
app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.get("/", tags=["Root"])
def root():
    return {"HI": "Hello World"}


funcionario_master: Funcionario = Funcionario(nome="MasterClass",
                                              email="master@gmail.com",
                                              senha=generate_password_hash("123"),
                                              is_admin=True, access_funcionario=True,
                                              is_colaborador=True, access_servico=True,
                                              access_cliente=True, access_item_servico=True,
                                              access_ordem_servico=True, ativo=True,
                                              cargo="MasterClass", )
