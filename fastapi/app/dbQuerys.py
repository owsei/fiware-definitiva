import psycopg2
from typing import Optional, Union
from fastapi import HTTPException
from fastapi import FastAPI
from sqlalchemy import Sequence 
import dbConfig

def selectOne(query: str,values='') -> Optional[tuple]:
    try:
        conn = psycopg2.connect(**dbConfig.DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(query,values)
            result = cur.fetchone()
        if result :
            return result
        else:
            return None
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    
def select(query: str,values: Union[Sequence, None] = None) -> Optional[list[tuple]]:
    try:
        conn = psycopg2.connect(**dbConfig.DB_CONFIG)
        with conn.cursor() as cur:
            if values:
                cur.execute(query, (values,))
            else:
                cur.execute(query)
            result = cur.fetchall()
            return result if result else None
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    
def selectAll(query: str) -> Optional[tuple]:
    try:
        conn = psycopg2.connect(**dbConfig.DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(query)
            result =[fila[0] for fila in cur.fetchall()]
        if result :
            # print(result)
            return result
        else:
            return None
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    
def insert(query: str,values) -> Optional[tuple]:
    try:
        conn = psycopg2.connect(**dbConfig.DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(query,values)
            id = cur.fetchone()[0]
        return {"message": "Insertado correctamente","id": id}
    except Exception as e:
        print(f"Error al insertar: {e}")
        return {"message": "Error al insertar", "error": str(e)}
    finally:
        conn.commit()
        conn.close()

def update(query: str,values) -> Optional[tuple]:
    try:
        conn = psycopg2.connect(**dbConfig.DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(query,values)
        return {"message": "Insertado correctamente"}
    except Exception as e:
        print(f"Error al insertar: {e}")
        return {"message": "Error al insertar", "error": str(e)}
    finally:
        conn.commit()
        conn.close()