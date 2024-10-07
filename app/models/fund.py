# app/models/fund.py

from pydantic import BaseModel

class Fund(BaseModel):
    #id: str  # ID único, lo puede manejar MongoDB automáticamente
    nombre: str
    valor: float
    categoria: str
