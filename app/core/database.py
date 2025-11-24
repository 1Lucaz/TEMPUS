from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from TEMPUS import settings

pool = ThreadedConnectionPool (dsn=settings.DATABASE_URL, )

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







