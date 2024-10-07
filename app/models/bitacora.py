from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

class Bitacora(BaseModel):
    id: ObjectId = None
    user_id: ObjectId
    fund_id: ObjectId
    accion: str  # 'Vinculado' o 'Desvinculado'
    fecha: datetime
    tipo: str # 'Traza, Notificación'
