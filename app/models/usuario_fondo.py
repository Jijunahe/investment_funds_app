from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

class UsuarioFondo(BaseModel):
    user_id: str
    fund_id: str
    estado: str  # 'Activo' o 'Desvinculado'
    fecha_vinculacion: datetime
    fecha_desvinculacion: datetime = None
