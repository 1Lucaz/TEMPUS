from fastapi import FastAPI
from app.core.settings import DB_URL
from app.core.database import Database
from app.routers.api_router import api_router
app = FastAPI(title="Sistema de Agendamento - V 1.1")

app.include_router(api_router, prefix="/api")

Database.initialize(
    dsn=DB_URL,
    minconn=1,
    maxconn=10
)
@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "API de Agendamento rodando"}

