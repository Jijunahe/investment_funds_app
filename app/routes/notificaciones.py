import os

from bson import ObjectId

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def enviar_notificacion(usuario_id: str, mensaje: str, db):
    user = db["users"].find_one({"_id": ObjectId(usuario_id)})

    # Configuración del servidor SMTP
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = os.getenv("EMAIL_REMITENTE")
    email_password = os.getenv("PASSWORD_EMAIL")

    # Información del correo
    email_to = user['email']
    subject = "Estimado cliente"
    body = mensaje

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Conexión al servidor SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia la conexión segura
        server.login(email_user, email_password)  # Inicia sesión en el servidor
        server.sendmail(email_user, email_to, msg.as_string())  # Envía el correo
        
        # Registro en bitácora
        db["bitacora"].insert_one({
            "accion": f"Se ha notificado al cliente: {mensaje}",
            "user_id": ObjectId(usuario_id),
            "fund_id": ObjectId(usuario_id),  # Revisa si esto está correcto
            "fecha": datetime.now(),
            "tipo": "Notificación"
        })
        print(f"Notificación enviada a {usuario_id}: {mensaje} - Fue Exitosa")
        
    except Exception as e:
        db["bitacora"].insert_one({
            "accion": f"La notificación al cliente no fue exitosa: {str(e)}",
            "user_id": ObjectId(usuario_id),
            "fund_id": ObjectId(usuario_id),  # Revisa si esto está correcto
            "fecha": datetime.now(),
            "tipo": "Notificación"
        })
        print(f"Notificación enviada a {usuario_id}: {mensaje} - No fue Exitosa")
        
    finally:
        server.quit()  # Cierra la conexión
