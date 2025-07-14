import uvicorn
from typing import Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import middleware.JWTMiddleware
from routers import public, protected

# python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Inicializa FastAPI
app = FastAPI()


# Configuración de CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public.router)
app.include_router(protected.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)





