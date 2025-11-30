from psycopg2 import sql, Error
from pydantic import EmailStr
from app.core.database import Database
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteService:

    @staticmethod
    def listar(ativo: bool | None = None, nome: str | None = None):
        listar = sql.SQL('''SELECT id, nome, email, telefone, ativo FROM cliente''')
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
    def criar_cliente(cliente: ClienteCreate):
        criar = sql.SQL ('''
                INSERT INTO cliente (nome, email, telefone, ativo)
                VALUES (%s, %s, %s, %s) RETURNING id, nome, email, telefone, ativo
                ''')
        valores = (cliente.nome, cliente.email, cliente.telefone)

        try:
            with Database() as db:
                return db.fetchone(criar, valores)

        except Error as e:
            erro = str(e)
            if "email" in erro:
                raise ValueError("EMAIL JÁ CADASTRADO")
            elif "telefone" in erro:
                raise ValueError("TELEFONE JÁ CADASTRADO")
            raise e

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = sql.SQL('''SELECT id, nome, email, telefone, ativo FROM cliente WHERE id = %s;''')
        with Database() as db:
            return db.fetchone(buscar_id, (id,))

    @staticmethod
    def atualizar(id: int, dados: ClienteUpdate):
        campos = []
        valores = []

        if dados.nome is not None:
            campos.append(sql.SQL('nome = %s'))
            valores.append(dados.nome)

        if dados.email is not None:
            campos.append(sql.SQL('email = %s'))
            valores.append(dados.email)

        if dados.telefone is not None:
            campos.append(sql.SQL('telefone = %s'))
            valores.append(dados.telefone)

        if dados.ativo is not None:
            campos.append(sql.SQL('ativo = %s'))
            valores.append(dados.ativo)

        if not campos:
            return "Nenhum dado enviado para atualização"

        valores.append(id)

        atualizar = sql.SQL('''UPDATE cliente SET {campos} WHERE id = %s
                                RETURNING id, nome, email, telefone, ativo
                            ''').format(campos=sql.SQL(', ').join(campos))

        try:
            with Database() as db:
                resultado = db.fetchone(atualizar, tuple(valores))

                if not resultado:
                    raise ValueError("CLIENTE NÃO ENCONTRADO")
                return resultado

        except Error as e:
            erro = str(e)
            if "email" in erro:
                raise ValueError("EMAIL JÁ EM USO POR OUTRO CLIENTE")
            elif "telefone" in erro:
                raise ValueError("TELEFONE JÁ EM USO POR OUTRO CLIENTE")
            raise e

    @staticmethod
    def desativar(id: int):
        desativar = '''UPDATE cliente SET ativo = FALSE WHERE id = %s 
        RETURNING id, nome, email, telefone, ativo'''

        with Database() as db:
            resultado = db.fetchone(desativar, (id,))

            if not resultado:
                raise ValueError("CLIENTE NÃO ENCONTRADO")

            return resultado