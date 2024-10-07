# app/models/funds_response.py

from pydantic import BaseModel
from bson import ObjectId

class FundsResponseAll(BaseModel):
    _id: str  # Cambiar esto a str para serializar ObjectId
    idfondo:str
    nombre: str
    valor: float
    categoria: str
     

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_mongo(cls, fund_data):
        return cls(
            _id=str(fund_data["_id"]),
            idfondo=str(fund_data["_id"]),
            nombre=fund_data["nombre"],
            valor=fund_data["valor"],
            categoria=fund_data["categoria"]  
        )
