import psycopg2.pool
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool, SimpleConnectionPool
from TEMPUS import settings as settings

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME
)

class Database:

    @staticmethod
    def commit (consulta: str, parametros: tuple = None):
        conn = pool.getconn()
        cursor = conn.cursor()

        try:
            cursor.execute(consulta, parametros)
            conn.commit()

        except Exception as e:
            if conn:
                conn.rollback()
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                pool.putconn(conn)

    @staticmethod
    def fetchone(consulta: str, parametros: tuple = None):
        conn = pool.getconn()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(consulta, parametros)
            result = cursor.fetchone()
            return result

        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                pool.putconn(conn)

    @staticmethod
    def fetchall(consulta: str, parametros: tuple = None):
        conn = pool.getconn()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute(consulta, parametros)
            result = (cursor.fetchall())
            return result

        except Exception as e:
            raise e

        finally:
            if cursor:
                cursor.close()
            if conn:
                pool.putconn(conn)







