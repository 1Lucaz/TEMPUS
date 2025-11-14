from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Sistema de Agendamento"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:senha@localhost:5432/agendamento_db"

    class Config:
        env_file = ".env"

settings = Settings()
