from datetime import date
from psycopg2 import sql, Error
from TEMPUS.app.core.database import Database
from ordem_servico_schema import OrdemCreate, OrdemUpdate


class OrdemServicoService:

    @staticmethod
    def listar(ativo: bool | None = None, status: str | None = None, cliente_id: int | None = None,
               data_inicio: date | None = None, data_fim: date | None = None):
        listar = 'SELECT id, cliente_id, data_abertura, status, ativo FROM ordem_servico'
        campos = []
        valores = []

        if ativo is not None:
            campos.append('ativo = %s')
            valores.append(ativo)

        if status:
            campos.append('status = %s')
            valores.append(status)

        if cliente_id:
            campos.append('cliente_id = %s')
            valores.append(cliente_id)

        if data_inicio:
            campos.append('data_abertura >= %s')
            valores.append(data_inicio)

        if data_fim:
            campos.append('data_abertura <= %s')
            valores.append(data_fim)

        if campos:
            listar += ' WHERE ' + ' AND '.join(campos)

        with Database() as db:
            return db.fetchall(listar, tuple(valores))

    @staticmethod
    def criar(ordem: OrdemCreate):
        verificar_cliente = 'SELECT id FROM cliente WHERE id = %s AND ativo = %s'

        criar = '''
                INSERT INTO ordem_servico (cliente_id, data_abertura, status, ativo)
                VALUES (%s, %s, %s, %s) 
                RETURNING id, cliente_id, data_abertura, status, ativo
                '''

        valores_insert = (ordem.cliente_id, ordem.data_abertura, ordem.status.value)

        try:
            with Database() as db:
                cliente_existe = db.fetchone(verificar_cliente, (ordem.cliente_id,))

                if not cliente_existe:
                    raise ValueError("CLIENTE NÃO EXISTE OU ESTÁ INATIVO")

                return db.fetchone(criar, valores_insert)

        except Error as e:
            raise e

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = '''SELECT id, cliente_id, data_abertura, status, ativo FROM ordem_servico WHERE id = %s;'''
        with Database() as db:
            return db.fetchone(buscar_id, (id,))

    @staticmethod
    def atualizar(id: int, ordem: OrdemUpdate):
        campos = []
        valores = []

        if ordem.cliente_id is not None:
            campos.append(sql.SQL('cliente_id = %s'))
            valores.append(ordem.cliente_id)

        if ordem.data_abertura is not None:
            campos.append(sql.SQL('data_abertura = %s'))
            valores.append(ordem.data_abertura)

        if ordem.status is not None:
            campos.append(sql.SQL('status = %s'))
            valores.append(ordem.status.value)

        if ordem.ativo is not None:
            campos.append(sql.SQL('ativo = %s'))
            valores.append(ordem.ativo)

        if not campos:
            raise ValueError("Nenhum dado enviado para atualização")

        valores.append(id)

        atualizar = sql.SQL('''UPDATE ordem_servico SET {campos} WHERE id = %s
                                RETURNING id, cliente_id, data_abertura, status, ativo
                            ''').format(campos=sql.SQL(', ').join(campos))

        try:
            with Database() as db:
                resultado = db.fetchone(atualizar, tuple(valores))

                if not resultado:
                    raise ValueError("ORDEM NÃO ENCONTRADA")
                return resultado

        except Error as e:
            raise e

    @staticmethod
    def desativar(id: int):
        desativar = '''UPDATE ordem_servico SET ativo = FALSE WHERE id = %s 
        RETURNING id, cliente_id, data_abertura, status, ativo'''

        with Database() as db:
            resultado = db.fetchone(desativar, (id,))

            if not resultado:
                raise ValueError("ORDEM NÃO ENCONTRADA")

            return resultado