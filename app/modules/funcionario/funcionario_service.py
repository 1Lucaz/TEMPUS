from psycopg2 import sql, Error
from app.core.database import Database
from app.modules.funcionario.funcionario_schema import FuncionarioCreate, FuncionarioUpdate

class FuncionarioService:

    @staticmethod
    def listar(ativo: bool | None = None, nome: str | None = None):
        listar = 'SELECT id, nome, cargo, ativo FROM funcionario'
        campos = []
        valores = []

        if ativo is not None:
            campos.append('ativo = %s')
            valores.append(ativo)

        if nome:
            campos.append('nome ILIKE %s')
            valores.append(nome)

        if campos:
            listar += ' WHERE ' + ' AND '.join(campos)

        with Database() as db:
            return db.fetchall(listar, tuple(valores))

    @staticmethod
    def criar_funcionario(funcionario: FuncionarioCreate):
        criar = '''
                INSERT INTO funcionario (nome, cargo, ativo)
                VALUES (%s, %s, %s) RETURNING id, nome, cargo, ativo
                '''
        valores = (funcionario.nome, funcionario.cargo)

        try:
            with Database() as db:
                return db.fetchone(criar, valores)

        except Error as e:
            raise e

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = '''SELECT id, nome, cargo, ativo FROM funcionario WHERE id = %s;'''
        with Database() as db:
            return db.fetchone(buscar_id, (id,))

    @staticmethod
    def atualizar(id: int, funcionario: FuncionarioUpdate):
        campos = []
        valores = []

        if funcionario.nome is not None:
            campos.append(sql.SQL('nome = %s'))
            valores.append(funcionario.nome)

        if funcionario.cargo is not None:
            campos.append(sql.SQL('cargo = %s'))
            valores.append(funcionario.cargo)

        if funcionario.ativo is not None:
            campos.append(sql.SQL('ativo = %s'))
            valores.append(funcionario.ativo)

        if not campos:
            raise ValueError("Nenhum dado enviado para atualização")

        valores.append(id)

        atualizar = sql.SQL('''UPDATE funcionario SET {campos} WHERE id = %s
                                RETURNING id, nome, cargo, ativo
                            ''').format(campos=sql.SQL(', ').join(campos))

        try:
            with Database() as db:
                resultado = db.fetchone(atualizar, tuple(valores))

                if not resultado:
                    raise ValueError("FUNCIONÁRIO NÃO ENCONTRADO")
                return resultado

        except Error as e:
            raise e

    @staticmethod
    def desativar(id: int):
        desativar = '''UPDATE funcionario SET ativo = FALSE WHERE id = %s 
        RETURNING id, nome, cargo, ativo'''

        with Database() as db:
            resultado = db.fetchone(desativar, (id,))

            if not resultado:
                raise ValueError("FUNCIONÁRIO NÃO ENCONTRADO")

            return resultado