from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.auth_service import AuthService
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_service import ClienteService
from app.modules.funcionario.funcionario_repository import FuncionarioRepository
from app.modules.funcionario.funcionario_service import FuncionarioService


#INVERSÃO DE DEPENDÊNCIAS PARA O SERVICE E ROUTES, APENAS O REPOSITORY CONHECE AS REGRAS DO BANCO

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(
        cliente_repository=ClienteRepository(db),
        funcionario_repository=FuncionarioRepository(db)
    )

def get_cliente_repository (db: Session = Depends(get_db)) -> ClienteRepository:
    return ClienteRepository(db)

def get_cliente_service (repository: ClienteRepository = Depends(get_cliente_repository)) -> ClienteService:
    return ClienteService(repository)



def get_funcionario_repository (db: Session = Depends(get_db)) -> FuncionarioRepository:
    return FuncionarioRepository(db)

def get_funcionario_service (repository: FuncionarioRepository = Depends (get_funcionario_repository)) -> FuncionarioService:
    return FuncionarioService(repository)
