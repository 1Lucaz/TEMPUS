from fastapi import FastAPI
from .routers.api_router import api_router

app = FastAPI(title="Sistema de Agendamento - MVC ")

app.include_router(api_router, prefix="/api/v1.1")

@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "API de Agendamento rodando"}
