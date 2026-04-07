import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from app.core.base import Base

#dados do db encontram-se arquivo properties.py
load_dotenv()
engine = create_engine (os.getenv('DATABASE_URL'), pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)

def init_db():
    inspector = inspect(engine)
    Base.metadata.drop_all(engine)
    tabelas_existentes = set(inspector.get_table_names())
    tabelas_models = set(Base.metadata.tables.keys())

    tabelas_restantes = tabelas_models - tabelas_existentes

    if tabelas_restantes:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(bind=engine)
    else:
        print("[DB] Banco de dados OK.")

class Database:
    def __enter__ (self):
        self.session = SessionLocal()
        return self.session

    def __exit__ (self, exc_type, exc_value, exc_traceback):

        try:
            if exc_type:
                self.session.rollback()
                raise

            else:
                try:
                    self.session.commit()

                except Exception:
                    self.session.rollback()
                    raise

        finally:
            self.session.close()


async def get_db ():
    with Database() as db:
        yield db