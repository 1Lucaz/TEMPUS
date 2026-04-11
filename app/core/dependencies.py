from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth.auth_service import AuthService
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.cliente.cliente_service import ClienteService
from app.modules.funcionario.funcionario_repository import FuncionarioRepository
from app.modules.funcionario.funcionario_service import FuncionarioService
from app.modules.item_servico.item_servico_repository import ItemServicoRepository
from app.modules.item_servico.item_servico_service import ItemServico, ItemServicoService
from app.modules.ordem_servico.ordem_servico_repository import OrdemServicoRepository
from app.modules.ordem_servico.ordem_servico_service import OrdemServicoService
from app.modules.servico.servico_repository import ServicoRepository
from app.modules.servico.servico_service import ServicoService


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


def get_item_servico_repository (db: Session = Depends(get_db)) -> ItemServicoRepository:
    return ItemServicoRepository(db)

def get_item_servico_service (repository: ItemServicoRepository = Depends(get_item_servico_repository)) -> ItemServicoService:
    return ItemServicoService(repository)


def get_ordem_servico_repository (db: Session = Depends(get_db)) -> OrdemServicoRepository:
    return OrdemServicoRepository(db)

def get_ordem_servico_service (ordem_repository: OrdemServicoRepository = Depends(get_ordem_servico_repository),
                               cliente_repository: ClienteRepository = Depends(get_cliente_repository)) -> OrdemServicoService:
    return OrdemServicoService(ordem_repository, cliente_repository)


def get_servico_repository (db: Session = Depends(get_db)) -> ServicoRepository:
    return ServicoRepository(db)

def get_servico_service (repository: ServicoRepository = Depends(get_servico_repository)) -> ServicoService:
    return ServicoService(repository)