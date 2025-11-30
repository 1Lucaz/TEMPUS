from psycopg2 import sql, Error
from app.core.database import Database
from app.modules.servico.servico_schema import ServicoCreate, ServicoUpdate


class ServicoService:

    @staticmethod
    def listar(ativo: bool | None = None, descricao: str | None = None):
        listar = 'SELECT id, descricao, valor_base, ativo FROM servico'
        campos = []
        valores = []

        if ativo is not None:
            campos.append('ativo = %s')
            valores.append(ativo)

        if descricao:
            campos.append('descricao ILIKE %s')
            valores.append(f"%{descricao}%")

        if campos:
            listar += ' WHERE ' + ' AND '.join(campos)

        with Database() as db:
            return db.fetchall(listar, tuple(valores))

    @staticmethod
    def criar_servico(servico: ServicoCreate):
        criar = '''
                INSERT INTO servico (descricao, valor_base, ativo)
                VALUES (%s, %s, TRUE) 
                RETURNING id, descricao, valor_base, ativo
                '''
        valores = (servico.descricao, servico.valor_base)

        try:
            with Database() as db:
                return db.fetchone(criar, valores)

        except Error as e:
            raise e

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = 'SELECT id, descricao, valor_base, ativo FROM servico WHERE id = %s'
        with Database() as db:
            return db.fetchone(buscar_id, (id,))

    @staticmethod
    def atualizar(id: int, servico: ServicoUpdate):
        campos = []
        valores = []

        if servico.descricao is not None:
            campos.append(sql.SQL('descricao = %s'))
            valores.append(servico.descricao)

        if servico.valor_base is not None:
            campos.append(sql.SQL('valor_base = %s'))
            valores.append(servico.valor_base)


        if not campos:
            raise ValueError("Nenhum dado enviado para atualização")

        valores.append(id)

        atualizar = sql.SQL('''UPDATE servico SET {campos} WHERE id = %s
                                RETURNING id, descricao, valor_base, ativo
                            ''').format(campos=sql.SQL(', ').join(campos))

        try:
            with Database() as db:
                resultado = db.fetchone(atualizar, tuple(valores))

                if not resultado:
                    raise ValueError("SERVIÇO NÃO ENCONTRADO")
                return resultado

        except Error as e:
            raise e

    @staticmethod
    def desativar(id: int):
        desativar = '''
            UPDATE servico SET ativo = FALSE WHERE id = %s 
            RETURNING id, descricao, valor_base, ativo
        '''

        with Database() as db:
            resultado = db.fetchone(desativar, (id,))

            if not resultado:
                raise ValueError("SERVIÇO NÃO ENCONTRADO")

            return resultado