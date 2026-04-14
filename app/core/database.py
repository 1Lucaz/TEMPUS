import os
import re
from dotenv import load_dotenv
from app.core.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine

load_dotenv()
engine = create_async_engine(re.sub
                             (r'^postgresql:',
                              'postgresql+psycopg:',
                              os.getenv('DATABASE_URL')),
                             echo=True)


async def get_session() -> AsyncSession | None:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


AsyncLocalSession = async_sessionmaker(bind=get_session(),
                                       expire_on_commit=False,
                                       autoflush=True)


class Database:
    def __enter__(self):
        self.session = AsyncLocalSession()
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


async def get_db():
    with Database() as db:
        yield db
