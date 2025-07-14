from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException, Request, Depends
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta

from services.ServiceUsers import *

SECRET_KEY = "2812-Data-Secret-Key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

PUBLIC_ROUTES = [
    "/",
    "/db-status",
    "/login",
    "/docs"
]

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload: {payload}")
        validate=validate_user_token(token)
        if "error" in validate:
            print(f"Error al validar el token: {validate['error']}")
            return None
        if not validate:
            print("Token no válido o expirado")
            return None
        
        return validate
    except PyJWTError:
        return None

async def dispatch(self, request: Request, call_next):
    # Si la ruta es pública, no se verifica el token
    if request.url.path in PUBLIC_ROUTES:
        return await call_next(request)

    # Verificación del token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"detail": "Token requerido"})

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload
    except jwt.PyJWTError:
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"detail": "Token inválido o expirado"})

    return await call_next(request)
    
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")

    token = auth.split(" ")[1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado",error= 403)
    return payload
