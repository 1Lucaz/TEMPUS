import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


#dados do db encontram-se arquivo properties.py
load_dotenv()
engine = create_engine (os.getenv('DATABASE_URL'), pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        raise Exception
    finally:
        db.close()

class Database:
    def __enter__ (self):
        self.session = SessionLocal()
        return self.session

    def __exit__ (self, exc_type, exc_value, exc_traceback):

        try:
            if exc_type:
                self.session.rollback()
                raise f"ERRO DO TIPO - {exc_type} | MENSAGEM -> {exc_value}"

            else:
                try:
                    self.session.commit()

                except Exception:
                    self.session.rollback()
                    raise f"ERRO DO TIPO - {exc_type} | MENSAGEM -> {exc_value}"

        finally:
            self.session.close()

