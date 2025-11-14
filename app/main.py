from fastapi import FastAPI
from app.routers.api_router import api_router
from app.core.database import Base, engine
import app.models.cliente_model
import app.models.servico_model
import app.models.funcionario_model
import app.models.ordem_servico_model
import app.models.item_servico_model

app = FastAPI(title="Sistema de Agendamento - MVC (psycopg2)")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "API de Agendamento rodando"}
