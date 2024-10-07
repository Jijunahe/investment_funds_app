# app/models/bitacora_response.py

from pydantic import BaseModel
from bson import ObjectId

class BitacoraResponse(BaseModel):
    _id: str  # Cambiar esto a str para serializar ObjectId
    idbitacora:str
    accion: str
    fund: object  # Mantener como object si no necesitas validación adicional
    fecha: str
    tipo: str
    

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_mongo(cls, bitacora_data,  fund):
        return cls(
            _id=str(bitacora_data["_id"]),
            idbitacora=str(bitacora_data["_id"]),
            accion=bitacora_data["accion"],
            fund={"nombre":fund["nombre"],"valor":fund["valor"],"categoria":fund["categoria"]},
            fecha=bitacora_data["fecha"].isoformat(), # Convertir a ISO format
            tipo=bitacora_data.get("tipo", "Traza") 
         )