from fastapi import FastAPI
from app.routers.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TEMPUS - V 1.0.1")
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.get("/", tags=["Root"])
def root():
    return {"HI": "Hello World"}


