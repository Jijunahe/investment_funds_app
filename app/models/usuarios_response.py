# app/models/usuarios_response.py

from pydantic import BaseModel
from bson import ObjectId

class UsuariosResponseAll(BaseModel):
    _id: str  # Cambiar esto a str para serializar ObjectId
    idusuario:str
    nombres: str
    saldo_base: float
    email: str
    identificacion: str
     

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_mongo(cls, us_data):
        return cls(
            _id=str(us_data["_id"]),
            idusuario=str(us_data["_id"]),
            nombres=us_data["nombres"],
            saldo_base=us_data["saldo_base"],
            email=us_data["email"],  
            identificacion=us_data["identificacion"]  
        )
