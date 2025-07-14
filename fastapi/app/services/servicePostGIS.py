import psycopg2
from typing import Optional
from fastapi import HTTPException
from fastapi import FastAPI 
import dbConfig
import dbQuerys

# Funcion de obtencion de datos de tabla espacial
def get_geojson_from_table(table_name: str) -> Optional[dict]:
    query = f"""select  json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(ST_SetSRID(geom, 4326))::json,
                'properties', to_jsonb(t) - 'geom'"""
    if table_name=="ambi_pto_calidadaire":
        query =query +" || jsonb_build_object('temperatura', sc.temperatura)"
    
    query=query+f" ))) AS geojson from {table_name} t"""

    if table_name=="ambi_pto_calidadaire":
        query= query + " inner join orion.sensores_calidad sc on sc.idsensor = t.gid;"

    print(query)
    result = dbQuerys.select(query)
    if result and result[0]:
        return result[0]
    else:
        return []
    
# Endpoint para obtener tablas de la base de datos
def get_tables_geopamplona() -> Optional[list]:
    query= f"""SELECT table_name 
               FROM information_schema.tables 
               WHERE table_schema = 'public' 
                 AND table_type = 'BASE TABLE'
               order by table_name;"""
    print(query)
    result = dbQuerys.selectAll(query)
    return result


def getCatastroLayers(municipo,poligono,parcela) -> Optional[list]:
    query = f"""select  json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(t.geom)::json,
                        'properties', to_jsonb(t) - 'geom' ))) AS geojson 
                        from (
                        select (planta_num * 3) as altura,planta_num,* 
                        from (select  *,
                                case 
                                    when vuu.planta = 'Sótano-6' then -6
                                    when vuu.planta = 'Sótano-5' then -5
                                    when vuu.planta = 'Sótano-4' then -4
                                    when vuu.planta = 'Sótano-3' then -3
                                    when vuu.planta = 'Sótano-2' then -2
                                    when vuu.planta = 'Sótano-1' then -1
                                    when vuu.planta = 'Bajo' then 0
                                    when vuu.planta = 'Entresuelo' then 1
                                    when vuu.planta = 'Primero' then 2
                                    when vuu.planta = 'Segundo' then 3
                                    when vuu.planta = 'Tercero' then 4
                                    when vuu.planta = 'Cuarto' then 5
                                    when vuu.planta = 'Quinto' then 6
                                    when vuu.planta = 'Sexto' then 7
                                    when vuu.planta = 'Séptimo' then 8
                                    when vuu.planta = 'Octavo' then 9
                                    when vuu.planta = 'Noveno' then 10
                                    when vuu.planta = 'Décimo' then 11
                                    when vuu.planta = 'Undécimo' then 12
                                    when vuu.planta = 'Duodécimo' then 13
                                    when vuu.planta = 'Decimotercero' then 14
                                    when vuu.planta = 'Decimocuarto' then 15
                                    when vuu.planta = 'Decimoquinto' then 16
                                    when vuu.planta = 'Decimosexto' then 17
                                    when vuu.planta = 'Decimoséptimo' then 18
                                    when vuu.planta = 'Decimoctavo' then 19
                                    when vuu.planta = 'Decimoctavo' then 20
                                    when vuu.planta = 'Decimoctavo' then 21
                                    when vuu.planta = 'Decimoctavo' then 22
                                    when vuu.planta = 'Decimoctavo' then 23
                                    when vuu.planta = 'Decimonoveno' then 24
                            end as planta_num
                        from vista_union_uu vuu ) as c
                        where c.municipio ={municipo} and c.poligono ={poligono} and c.parcela = {parcela}
                        and c.planta_num is not null
                        order by planta_num,subarea
                ) as t"""
    print(query)
    result = dbQuerys.select(query)
    print(f"Resultado de la consulta: {result}")
    if result and result[0]:
        return result[0]
    else:
        return []

def buscadorDireccion(direccion: str) -> Optional[list]:
    query = 'select  distinct calle,municipio,poligono,parcela from vista_union_uu vuu where vuu.calle like %s order by 3'
    print(query)
    result = dbQuerys.select(query,'%'+direccion.upper()+'%')
    print(f"Resultado de la consulta: {result}")
    return result if result else []

