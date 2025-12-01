from psycopg2 import pool
from psycopg2.extras import RealDictCursor


class Database:
    _pool = None

    @classmethod
    def initialize(cls, dsn, minconn=1, maxconn=10):
        if cls._pool is None:
            cls._pool = pool.ThreadedConnectionPool(
                minconn=minconn,
                maxconn=maxconn,
                dsn=dsn
            )

    def __enter__(self):
        if Database._pool is None:
            raise RuntimeError("Pool de conexões não inicializado.")

        self.conn = Database._pool.getconn()
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        return self.cur

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.cur.close()
        Database._pool.putconn(self.conn)
