from typing import Union
from fastapi import Request,APIRouter,HTTPException,Depends
from middleware.JWTMiddleware import *

import services.servicePostGIS as servicePostGIS

router = APIRouter(
    prefix="/api", # 👈 Prefijo para todas las rutas de este router
    dependencies=[Depends(get_current_user)]  # 👈 Esto es como aplicar middleware solo a este router
)

@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None,user=Depends(get_current_user)):
    return {"item_id": item_id, "q": q}


# Endpoint para obtener un GeoJSON de una tabla espacial.
@router.get("/getgeojson/{table_name}")
def get_geojson(table_name: str,user=Depends(get_current_user)):
    print (f"Obteniendo GeoJSON de la tabla: {table_name}")
    geojson = servicePostGIS.get_geojson_from_table(table_name)
    if geojson:
        return geojson
    else:
        raise HTTPException(status_code=404, detail="No se encontraron datos o la tabla no existe")
    
#Tablas de postgis de las capasa de Geopamplona
@router.get("/tablesgeopamplona")
def get_tables_geopamplona(user=Depends(get_current_user)):
    print (f"Obteniendo tablas de la base de datos")
    tables = servicePostGIS.get_tables_geopamplona()
    if tables:
        # print (f"Tablas obtenidas: {tables}")
        # print(tables)
        return tables
    else:
        raise HTTPException(status_code=404, detail="No se encontraron tablas o la base de datos no existe")



@router.get("/getcatastrolayers/{municipio}/{poligono}/{parcela}")
def get_catastro_layers(municipio: int, poligono: int, parcela: int,user=Depends(get_current_user)):
    print(f"Obteniendo capas catastrales para municipio: {municipio}, poligono: {poligono}, parcela: {parcela}")
    layers = servicePostGIS.getCatastroLayers(municipio, poligono, parcela)
    if layers:
        return layers
    else:
        raise HTTPException(status_code=404, detail="No se encontraron capas catastrales o la consulta es incorrecta")

@router.get("/buscadorDireccion/{direccion}")
def buscador_direccion(direccion: str,user=Depends(get_current_user)):
    print(f"Buscando dirección: {direccion}")
    results = servicePostGIS.buscadorDireccion(direccion)
    if results:
        return results
    else:
        raise HTTPException(status_code=404, detail="No se encontraron resultados para la dirección proporcionada")


@router.get("/logout")
async def logout(request: Request):
    # Lógica de autenticación
    # token = request.headers.get("Authorization")
    params=request.query_params
    idUsuario = params.get("idUsuario")
    print(f"idUsuario: {idUsuario}")
        
    logout(idUsuario)
    # print(f"Token JWT generado: {jwt_Token}")
    return JSONResponse(
        content={"message": "Login successful", "token": create_access_token({"sub": idUsuario})},
        status_code=200
    )