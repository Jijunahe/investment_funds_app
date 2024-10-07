from pydantic import BaseModel, EmailStr

class User(BaseModel):
    _id: str
    id: str
    nombres: str
    email: EmailStr
    identificacion: str
    saldo_base: float
