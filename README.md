# Investment Funds Backend

Este es el backend para la aplicación de gestión de fondos de inversión. Provee las APIs necesarias para manejar las suscripciones y desvinculaciones de usuarios a fondos, y gestionar las transacciones financieras.

## Tecnologías Utilizadas

- **Python** (con FastAPI)
- **MongoDB** (base de datos)
- **Pydantic** (validación de datos y esquemas)
- **Uvicorn** (servidor de aplicaciones ASGI)

## Requisitos Previos

1. **Python 3.7+**
2. **MongoDB** instalado y corriendo localmente o en la nube.


## Instalación

### 1. Clona el repositorio:

 
git clone https://github.com/jijunahe/investment_funds_app.git


### 2. Ve al directorio del backend:

cd investment_funds_app_backend

### 3. Crea un entorno virtual (si quieren es opcional, pero recomendado):

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate



### 4. Instala las dependencias:

pip install -r requirements.txt


### 5. Configura las variables de entorno:

Crea un archivo .env en el directorio raíz y añade las variables de entorno necesarias:
add/.env

DB_HOST="mongodb://localhost:27017/"
DB="investment_funds_db"
ORIGINS="http://localhost:3000,http://127.0.0.1:3000"

#CONFIGURACION SMTP
EMAIL_REMITENTE="testpruebas@gmail.com"
PASSWORD_EMAIL="acaelpassword*"


### 6. Inicia el servidor:

uvicorn main:app --reload


El servidor se iniciará en http://localhost:8000.

### Endpoints Principales
### Usuarios
GET /users/{user_id}: Obtiene los detalles de un usuario por su ID.
POST /users/: Crea un nuevo usuario.
### Fondos
POST /funds/subscribe: Permite a un usuario suscribirse a un fondo.
POST /funds/unsubscribe: Permite a un usuario desvincularse de un fondo.
GET /funds: Lista todos los fondos disponibles.
### Historial
POST /funds/gettraza/{user_id}: Obtiene el historial de transacciones de un usuario específico.


investment_funds_app_backend/
│
├── app/
│   ├── models/            # Modelos de Pydantic para validación
│   ├── routes/            # Rutas para fondos y usuarios
│   ├── services/          # Lógica de negocio para suscripciones, desvinculaciones
│   └── db.py              # Configuración de la conexión a MongoDB
│
├── main.py                # Punto de entrada de la aplicación FastAPI
├── requirements.txt       # Dependencias del proyecto
└── .env                   # Variables de entorno (no incluir en control de versiones)


### Uso

Asegúrate de tener MongoDB corriendo en tu máquina o en un servicio en la nube como MongoDB Atlas.
Ejecuta la aplicación con uvicorn y visita la documentación interactiva generada automáticamente 
por FastAPI en http://localhost:8000/docs.


### Comandos Útiles
1. Iniciar el servidor con Hot Reload:

    uvicorn main:app --reload
2. Instalar nuevas dependencias:

    Si necesitas instalar nuevas dependencias, hazlo con:
    pip install nombre_paquete

    Luego actualiza el archivo requirements.txt con:
    pip freeze > requirements.txt

