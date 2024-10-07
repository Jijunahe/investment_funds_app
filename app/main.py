# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importa CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.fund_routes import router as fund_router
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# Configuración de CORS
origins = os.getenv("ORIGINS").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes especificados
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(user_router)
app.include_router(fund_router)

@app.get("/")
def read_root():
    return {"message": "API de Fondos de Inversión"}
