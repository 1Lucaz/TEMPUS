from pydantic_settings import BaseSettings

class Settings (BaseSettings):
    APP_NAME: str = "Sistema de Agendamento"
    DATABASE_URL: str

    class Config:
        env_file = "settings.py"
