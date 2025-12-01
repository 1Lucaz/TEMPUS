from psycopg2 import sql, Error
from app.core.database import Database
from app.modules.funcionario.funcionario_schema import FuncionarioCreate, FuncionarioUpdate


class FuncionarioService:

    @staticmethod
    def listar(ativo: bool | None = None, nome: str | None = None):
        listar = '''
            SELECT id, nome, cargo, ativo 
            FROM funcionario
        '''
        campos = []
        valores = []

        if ativo is not None:
            campos.append('ativo = %s')
            valores.append(ativo)

        if nome:
            campos.append('nome ILIKE %s')
            valores.append(f"%{nome}%")

        if campos:
            listar += ' WHERE ' + ' AND '.join(campos)

        with Database() as db:
            db.execute(listar, tuple(valores))
            return db.fetchall()

    @staticmethod
    def criar_funcionario(funcionario: FuncionarioCreate):
        criar = '''
            INSERT INTO funcionario (nome, cargo, ativo)
            VALUES (%s, %s, TRUE)
            RETURNING id, nome, cargo, ativo
        '''
        valores = (funcionario.nome, funcionario.cargo)

        with Database() as db:
            db.execute(criar, valores)
            return db.fetchone()

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = '''
            SELECT id, nome, cargo, ativo 
            FROM funcionario 
            WHERE id = %s
        '''
        with Database() as db:
            db.execute(buscar_id, (id,))
            return db.fetchone()

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

        atualizar = sql.SQL('''
            UPDATE funcionario 
            SET {campos}
            WHERE id = %s
            RETURNING id, nome, cargo, ativo
        ''').format(campos=sql.SQL(', ').join(campos))

        with Database() as db:
            db.execute(atualizar, tuple(valores))
            resultado = db.fetchone()

            if not resultado:
                raise ValueError("FUNCIONÁRIO NÃO ENCONTRADO")

            return resultado

    @staticmethod
    def desativar(id: int):
        desativar = '''
            UPDATE funcionario 
            SET ativo = FALSE 
            WHERE id = %s
            RETURNING id, nome, cargo, ativo
        '''

        with Database() as db:
            db.execute(desativar, (id,))
            resultado = db.fetchone()

            if not resultado:
                raise ValueError("FUNCIONÁRIO NÃO ENCONTRADO")

            return resultado
