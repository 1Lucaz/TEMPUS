from app.core.security import verify_password_hash, create_acess_token
from app.modules.cliente.cliente_repository import ClienteRepository
from app.modules.funcionario.funcionario_repository import FuncionarioRepository
from app.modules.utils.app_exception import Unauthorized, NotFound


class AuthService:

    def __init__(self,
                 cliente_repository: ClienteRepository,
                 funcionario_repository: FuncionarioRepository):
        self.cliente_repository = cliente_repository
        self.funcionario_repository = funcionario_repository

    def login_cliente(self, email: str, senha: str) -> dict:

        cliente = self.cliente_repository.buscar_um(email=email)

        if cliente is None:
            raise NotFound(causa="Cliente não encontrado")

        if not cliente.ativo:
            raise Unauthorized(causa="Conta desativada")

        if not verify_password_hash(senha, cliente.senha):
            raise Unauthorized(causa="Credenciais inválidas")

        token = create_acess_token({
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "ativo": cliente.ativo,
        })

        return {"access_token": token, "token_type": "bearer"}

    def login_funcionario(self, email: str, senha: str) -> dict:

        funcionario = self.funcionario_repository.buscar_um(email=email)

        if funcionario is None:
            raise NotFound(causa="Funcionário não encontrado")

        if not funcionario.ativo:
            raise Unauthorized(causa="Conta desativada")

        if not verify_password_hash(senha, funcionario.senha):
            raise Unauthorized(causa="Credenciais inválidas")

        token = create_acess_token({
            "id": funcionario.id,
            "nome": funcionario.nome,
            "email": funcionario.email,
            "cargo": funcionario.cargo,
            "ativo": funcionario.ativo,
            "is_admin": funcionario.is_admin,
            "is_colaborador": funcionario.is_colaborador,
            "access_cliente": funcionario.access_cliente,
            "access_funcionario": funcionario.access_funcionario,
            "access_servico": funcionario.access_servico,
            "access_item_servico": funcionario.access_item_servico,
            "access_ordem_servico": funcionario.access_ordem_servico,
        })

        return {"access_token": token, "token_type": "bearer"}