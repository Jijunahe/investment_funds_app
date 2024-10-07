# app/routes/fund_routes.py

from fastapi import APIRouter, Depends, HTTPException
from app.models.fund import Fund
from app.database.db import get_db
from app.models.usuario_fondo import UsuarioFondo
from app.models.fund_response import FundResponse 
from app.models.bitacora_response import BitacoraResponse 
from app.models.funds_response import FundsResponseAll
from bson.objectid import ObjectId
from bson import ObjectId
from datetime import datetime
from .notificaciones import enviar_notificacion
from typing import List

router = APIRouter()

@router.post("/funds/", response_model=Fund)
async def create_fund(fund: Fund):
    db = get_db()
    fund_dict = fund.dict()
    fund_dict['_id'] = ObjectId()  # Usar ObjectId para MongoDB
    db.funds.insert_one(fund_dict)
    return fund

@router.get("/funds/{fund_id}", response_model=Fund)
async def get_fund(fund_id: str):
    db = get_db()
    fund = db.funds.find_one({"_id": ObjectId(fund_id)})
    if not fund:
        raise HTTPException(status_code=404, detail="El Fondo no existe")
    fund['_id'] = str(fund['_id'])  # Convertir ObjectId a string
    return fund

@router.post("/funds",response_model=List[FundsResponseAll])
async def get_fund(db = Depends(get_db)) -> List[FundsResponseAll]:
    db = get_db()
    funds = db.funds.find()
    if not funds:
        raise HTTPException(status_code=404, detail="No hay fondos")
    
    fundall = []
    for fund in funds:
        fundall.append(FundsResponseAll.from_mongo(fund))
  
    return fundall 


@router.put("/funds/{fund_id}", response_model=Fund)
async def update_fund(fund_id: str, fund: Fund):
    db = get_db()
    updated_fund = db.funds.find_one_and_update(
        {"_id": ObjectId(fund_id)},
        {"$set": fund.dict()},
        return_document=True
    )
    if not updated_fund:
        raise HTTPException(status_code=404, detail="El Fondo no existe")
    updated_fund['_id'] = str(updated_fund['_id'])  # Convertir ObjectId a string
    return updated_fund

@router.delete("/funds/{fund_id}", response_model=dict)
async def delete_fund(fund_id: str):
    db = get_db()
    result = db.funds.delete_one({"_id": ObjectId(fund_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="El Fondo no existe")
    return {"detail": "Fund deleted successfully"}


# Suscribir usuario a un fondo
@router.post("/funds/subscribe/")
async def subscribe_user_to_fund(user_id: str, fund_id: str, db = Depends(get_db)):
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    fund = db["funds"].find_one({"_id": ObjectId(fund_id)})
    user_fund = db["usuarios_fondos"].find_one({"user_id": ObjectId(user_id),"fund_id":ObjectId(fund_id),"estado":"Vinculado"})

    if not user or not fund:
        raise HTTPException(status_code=404, detail="El cliente o el Fono no se encuentran registrados")
    
    if user_fund:
        raise HTTPException(status_code=400, detail="Ya se encuentra vinculado a este fondo")

    if user['saldo_base'] < fund['valor']:
        raise HTTPException(status_code=400, detail=f"No tiene saldo disponible para vincularse al fondo {fund['nombre']}")

    # Descontar valor del fondo del saldo del usuario
    db["users"].update_one({"_id": ObjectId(user_id)}, {"$inc": {"saldo_base": -fund["valor"]}})

    # Insertar en la tabla intermedia usuarios_fondos
    db["usuarios_fondos"].insert_one({
        "user_id": ObjectId(user_id),
        "fund_id": ObjectId(fund_id),
        "estado": "Vinculado",
        "fecha_vinculacion": datetime.now()
    })

    # Registrar en la bitácora
    db["bitacora"].insert_one({
        "accion": "Suscripción",
        "user_id": ObjectId(user_id),
        "fund_id": ObjectId(fund_id),
        "fecha": datetime.now(),
        "tipo":"Traza"
    })
    mensaje="La subscripción ha sido exitosa"
    enviar_notificacion(user_id,mensaje,db)
    return {"message": mensaje}

# Desvincular usuario de un fondo
@router.post("/funds/unsubscribe/")
async def unsubscribe_user_from_fund(user_id: str, fund_id: str, db = Depends(get_db)):
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    fund = db["funds"].find_one({"_id": ObjectId(fund_id)})
    user_fund = db["usuarios_fondos"].find_one({"user_id": ObjectId(user_id), "fund_id": ObjectId(fund_id), "estado": "Vinculado"})

    if not user or not fund or not user_fund:
        raise HTTPException(status_code=404, detail="El cliente, Fondo, or subscripción no existen")

    # Devolver el valor del fondo al saldo del usuario
    db["users"].update_one({"_id": ObjectId(user_id)}, {"$inc": {"saldo_base": fund["valor"]}})

    # Actualizar estado en la tabla intermedia usuarios_fondos a "Desvinculado"
    db["usuarios_fondos"].update_one({"_id": user_fund["_id"]}, {"$set": {"estado": "Desvinculado", "fecha_desvinculacion": datetime.now()}})

    # Registrar en la bitácora
    db["bitacora"].insert_one({
        "accion": "Desvinculación",
        "user_id": ObjectId(user_id),
        "fund_id": ObjectId(fund_id),
        "fecha": datetime.now(),
        "tipo":"Traza"
    })
    mensaje="Se ha desvinculado con éxito"
    enviar_notificacion(user_id,mensaje,db)
    return {"message": mensaje}
    

 # Obtener Fondos suscritos
@router.post("/funds/getfunds/", response_model=List[FundResponse]) 
async def get_funds_user(user_id: str, db = Depends(get_db)) -> List[FundResponse]:
    try:
        user_id_obj = ObjectId(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="El user_id no es válido")

    user = db["users"].find_one({"_id": user_id_obj})
    user_funds = db["usuarios_fondos"].find({"user_id": user_id_obj, "estado": "Vinculado"})

    if not user or user_funds is None:
        raise HTTPException(status_code=404, detail="El cliente o suscripción no existen")

    foundsxusuario = []
    for user_fund in user_funds:
        fund = db["funds"].find_one({"_id": ObjectId(user_fund["fund_id"])})
        if fund:
            # Método from_mongo para crear la instancia de FundResponse
            foundsxusuario.append(FundResponse.from_mongo(fund, user_fund["fecha_vinculacion"].isoformat()))
  
    return foundsxusuario
 # Obtener Bitacora
@router.post("/funds/gettraza/", response_model=List[BitacoraResponse])
async def gettraza(user_id: str, db = Depends(get_db)) -> List[BitacoraResponse]:
    user = db["users"].find_one({"_id": ObjectId(user_id)})
   
    bitacoras = db["bitacora"].find({"user_id": ObjectId(user_id)})

    if not user or not bitacoras:
        raise HTTPException(status_code=404, detail="El cliente o bitacora no existen")

     
    bitacoraxusuario = []
    for bitacora in bitacoras:
        fund = db["funds"].find_one({"_id": ObjectId(bitacora["fund_id"])})
        if fund:
            # Método from_mongo para crear la instancia de FundResponse
            bitacoraxusuario.append(BitacoraResponse.from_mongo(bitacora,fund))
  
    return bitacoraxusuario