from psycopg2 import sql, Error
from app.core.database import Database
from app.modules.cliente.cliente_schema import ClienteCreate, ClienteUpdate


class ClienteService:

    @staticmethod
    def listar(ativo: bool | None = None, nome: str | None = None):
        listar = sql.SQL('''
            SELECT id, nome, email, telefone, ativo 
            FROM cliente
        ''')
        campos = []
        valores = []

        if ativo is not None:
            campos.append(sql.SQL('ativo = %s'))
            valores.append(ativo)

        if nome:
            campos.append(sql.SQL('nome ILIKE %s'))
            valores.append(f"%{nome}%")

        if campos:
            listar += sql.SQL(' WHERE ') + sql.SQL(' AND ').join(campos)

        with Database() as db:
            db.execute(listar, tuple(valores))
            return db.fetchall()

    @staticmethod
    def criar_cliente(cliente: ClienteCreate):
        criar = sql.SQL('''
            INSERT INTO cliente (nome, email, telefone, ativo)
            VALUES (%s, %s, %s, TRUE)
            RETURNING id, nome, email, telefone, ativo
        ''')
        valores = (cliente.nome, cliente.email, cliente.telefone)

        try:
            with Database() as db:
                db.execute(criar, valores)
                return db.fetchone()

        except Error as e:
            erro = str(e).lower()

            if "email" in erro:
                raise ValueError("EMAIL JÁ CADASTRADO")
            if "telefone" in erro:
                raise ValueError("TELEFONE JÁ CADASTRADO")

            raise e

    @staticmethod
    def buscar_por_id(id: int):
        buscar_id = sql.SQL('''
            SELECT id, nome, email, telefone, ativo
            FROM cliente
            WHERE id = %s
        ''')
        with Database() as db:
            db.execute(buscar_id, (id,))
            return db.fetchone()

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
            raise ValueError("Nenhum dado enviado para atualização")

        valores.append(id)

        atualizar = sql.SQL('''
            UPDATE cliente
            SET {campos}
            WHERE id = %s
            RETURNING id, nome, email, telefone, ativo
        ''').format(campos=sql.SQL(', ').join(campos))

        try:
            with Database() as db:
                db.execute(atualizar, tuple(valores))
                resultado = db.fetchone()

                if not resultado:
                    raise ValueError("CLIENTE NÃO ENCONTRADO")

                return resultado

        except Error as e:
            erro = str(e).lower()

            if "email" in erro:
                raise ValueError("EMAIL JÁ EM USO POR OUTRO CLIENTE")
            if "telefone" in erro:
                raise ValueError("TELEFONE JÁ EM USO POR OUTRO CLIENTE")

            raise e

    @staticmethod
    def desativar(id: int):
        desativar = sql.SQL('''
            UPDATE cliente
            SET ativo = FALSE
            WHERE id = %s
            RETURNING id, nome, email, telefone, ativo
        ''')
        with Database() as db:
            db.execute(desativar, (id,))
            resultado = db.fetchone()

            if not resultado:
                raise ValueError("CLIENTE NÃO ENCONTRADO")

            return resultado
