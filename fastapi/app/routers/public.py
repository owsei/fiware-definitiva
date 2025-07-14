from typing import Union
from fastapi import Request,APIRouter
from fastapi.responses import JSONResponse
import psycopg2
import dbConfig
from fastapi import APIRouter
from middleware.JWTMiddleware import *
from services.ServiceUsers import *
import bcrypt

router = APIRouter()

# Ruta de ejemplo para verificar que la API está funcionando
@router.get("/")
def read_root():
    return {"Hello": "World"}

# Ruta para verificar el estado de la conexión a la base de datos PostGIS
@router.get("/db-status")
def db_status():
    try:
        conn = psycopg2.connect(**dbConfig.DB_CONFIG)
        conn.close()
        return {"status": "PostGIS is connected"}
    except Exception as e:
        return {"status": f"Failed to connect: {e}"}

# Login de usuario
@router.post("/login")
async def login(request: Request):
    # Lógica de autenticación
    # token = request.headers.get("Authorization")
    params = await request.json()
    # params=request.query_params
    usuario = params.get("usuario")
    print(f"usuario: {usuario}")
    password = params.get("password")
    print(f"password: {password}")

    # hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    if not usuario or not password:
        return JSONResponse(
            content={"message": "Usuario y contraseña son requeridos","error": 403},
            status_code=400
        )
    
    response = validate_user(usuario, password)
    message = response.get("message")
    if "error" in response:
        return JSONResponse(
            content={"message": message, "error": response["error"]},
            status_code=500
        )
    userValidate = response.get("user")
    jwt_token = create_access_token({"username": userValidate[1], "password": userValidate[2]})
    updateUserToken(userValidate[0], jwt_token)
    # # print(f"Token JWT generado: {jwt_Token}")
    return JSONResponse(
        content={"token": jwt_token,"idusuario": userValidate[0]},
        status_code=200
    )

# Registro de usuario
@router.post("/register")
async def register(request: Request):
    params=request.query_params
    usuario = params.get("usuario")
    password = params.get("password")

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if not usuario or not hashed_pw:
        return JSONResponse(
            content={"message": "Usuario y contraseña son requeridos"},
            status_code=400
        )
    
    if user_exists(usuario):
        return JSONResponse(
            content={"message": "El usuario ya existe"},
            status_code=400
        )
    
    #Registrar el usuario
    msg = register_user(usuario, hashed_pw)
    id = msg.get("id")
    if "error" in msg:
        return JSONResponse(
            content={"message": msg["message"], "error": msg["error"]},
            status_code=500
        )
    
    if not id:
        return JSONResponse(
            content={"message": "Error al registrar el usuario"},
            status_code=500
        )
    # Generar el token JWT
    jwt_Token = create_access_token({"sub": usuario, "password": password})
    
    print(f"Token JWT generado: {jwt_Token}")
    if not jwt_Token:
        return JSONResponse(
            content={"message": f"Error al generar el token JWT for {usuario}"},
            status_code=500
        )
    
    # Actualizar el token del usuario en la base de datos
    updateUserToken(id, jwt_Token)
    
    # print(f"Token JWT generado: {jwt_Token}")
    return JSONResponse(
        content={"message": f"Login successful for{usuario} ", "token": jwt_Token},
        status_code=200
    )