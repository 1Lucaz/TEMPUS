import os
import re
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine

load_dotenv()
engine = create_engine(re.sub
                       (r'^postgresql:',
                        'postgresql+psycopg:',
                        os.getenv('DATABASE_URL')),
                       echo=True)


LocalSession = sessionmaker(bind=engine,
                            expire_on_commit=False,
                            autoflush=True)


class Database:
    def __enter__(self):
        self.session = LocalSession()
        return self.session

    def __exit__(self, exc_type, exc_value, exc_traceback):

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

def get_db():
    with Database() as db:
        yield db
