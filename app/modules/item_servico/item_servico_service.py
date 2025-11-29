from psycopg2 import sql, Error
from TEMPUS.app.core.database import Database
from .item_servico_schema import ItemCreate, ItemUpdate


class ItemService:

    @staticmethod
    def listar(ativo: bool | None = None, ordem_servico_id: int | None = None):
        listar = 'SELECT id, ordem_servico_id, servico_id, valor, ativo FROM item_servico'
        campos = []
        valores = []

        if ativo is not None:
            campos.append('ativo = %s')
            valores.append(ativo)

        if ordem_servico_id:
            campos.append('ordem_servico_id = %s')
            valores.append(ordem_servico_id)

        if campos:
            listar += ' WHERE ' + ' AND '.join(campos)

        with Database() as db:
            return db.fetchall(listar, tuple(valores))

    @staticmethod
    def criar_item(item: ItemCreate):
        check_servico = 'SELECT id FROM servico WHERE id = %s AND ativo = TRUE'
        check_ordem = 'SELECT id FROM ordem_servico WHERE id = %s AND ativo = TRUE'

        criar = '''
                INSERT INTO item_servico (ordem_servico_id, servico_id, valor, ativo)
                VALUES (%s, %s, %s, %s) 
                RETURNING id, ordem_servico_id, servico_id, valor, ativo
                '''
        valores = (item.ordem_servico_id, item.servico_id, item.valor)

        try:
            with Database() as db:
                if not db.fetchone(check_servico, (item.servico_id,)):
                    raise ValueError("SERVIÇO NÃO EXISTE OU ESTÁ INATIVO")

                if not db.fetchone(check_ordem, (item.ordem_servico_id,)):
                    raise ValueError("ORDEM DE SERVIÇO NÃO EXISTE OU ESTÁ INATIVA")

                return db.fetchone(criar, valores)

        except Error as e:
            raise e

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = 'SELECT id, ordem_servico_id, servico_id, valor, ativo FROM item_servico WHERE id = %s'
        with Database() as db:
            return db.fetchone(buscar_id, (id,))

    @staticmethod
    def atualizar(id: int, dados: ItemUpdate):
        campos = []
        valores = []

        if dados.ordem_servico_id is not None:
            campos.append(sql.SQL('ordem_servico_id = %s'))
            valores.append(dados.ordem_servico_id)

        if dados.servico_id is not None:
            campos.append(sql.SQL('servico_id = %s'))
            valores.append(dados.servico_id)

        if dados.valor is not None:
            campos.append(sql.SQL('valor = %s'))
            valores.append(dados.valor)

        if dados.ativo is not None:
            campos.append(sql.SQL('ativo = %s'))
            valores.append(dados.ativo)

        if not campos:
            raise ValueError("Nenhum dado enviado para atualização")

        valores.append(id)

        atualizar = sql.SQL('''
                    UPDATE item_servico SET {campos} WHERE id = %s
                    RETURNING id, ordem_servico_id, servico_id, valor, ativo
                            ''').format(campos=sql.SQL(', ').join(campos))

        try:
            with Database() as db:
                resultado = db.fetchone(atualizar, tuple(valores))

                if not resultado:
                    raise ValueError("ITEM NÃO ENCONTRADO")
                return resultado

        except Error as e:
            raise e

    @staticmethod
    def desativar(id: int):
        desativar = '''
            UPDATE item_servico SET ativo = FALSE WHERE id = %s 
            RETURNING id, ordem_servico_id, servico_id, valor, ativo
        '''

        with Database() as db:
            resultado = db.fetchone(desativar, (id,))

            if not resultado:
                raise ValueError("ITEM NÃO ENCONTRADO")

            return resultado