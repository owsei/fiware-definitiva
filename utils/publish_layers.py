#!/usr/bin/env python3
"""
Script para publicar todas las capas de PostGIS en GeoServer
"""

import psycopg2
import requests
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CONFIGURACIÓN
GEOSERVER_URL = "http://localhost:8080/geoserver"
GEOSERVER_USER = "admin"
GEOSERVER_PASS = "geoserver"
WORKSPACE = "geopamplona"
DATASTORE = "geopamplona_postgis"

DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "dbname": "geopamplona",
    "user": "admin",
    "password": "admin"
}

def get_postgis_tables():
    """Obtener todas las tablas espaciales de PostGIS"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT f_table_name, f_geometry_column, type
            FROM geometry_columns
            WHERE f_table_schema = 'public'
            ORDER BY f_table_name
        """)
        tables = cur.fetchall()
        conn.close()
        return tables
    except Exception as e:
        logger.error(f"❌ Error obteniendo tablas: {e}")
        return []

def update_datastore():
    """Actualizar configuración del datastore"""
    url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}"
    headers = {'Content-type': 'text/xml'}
    
    data = f"""<?xml version="1.0" encoding="UTF-8"?>
    <dataStore>
        <name>{DATASTORE}</name>
        <connectionParameters>
            <host>{DB_CONFIG['host']}</host>
            <port>{DB_CONFIG['port']}</port>
            <database>{DB_CONFIG['dbname']}</database>
            <user>{DB_CONFIG['user']}</user>
            <passwd>{DB_CONFIG['password']}</passwd>
            <dbtype>postgis</dbtype>
            <schema>public</schema>
        </connectionParameters>
    </dataStore>
    """
    
    response = requests.put(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), 
                           headers=headers, data=data)
    
    if response.status_code in [200, 201]:
        logger.info("✅ Datastore actualizado")
        return True
    else:
        logger.error(f"❌ Error actualizando datastore: {response.status_code}")
        return False

def publish_layer(table_name):
    """Publicar una capa en GeoServer"""
    try:
        # Verificar si ya existe
        check_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}/featuretypes/{table_name}"
        check_response = requests.get(check_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
        
        if check_response.status_code == 200:
            logger.info(f"✅ Ya existe: {table_name}")
            return True
        
        # Crear nueva capa
        url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}/featuretypes"
        headers = {'Content-type': 'text/xml'}
        
        data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <featureType>
            <name>{table_name}</name>
            <nativeName>{table_name}</nativeName>
            <title>{table_name.replace('_', ' ').title()}</title>
            <abstract>Capa {table_name} importada desde PostGIS</abstract>
            <srs>EPSG:4326</srs>
            <enabled>true</enabled>
            <advertised>true</advertised>
        </featureType>
        """
        
        response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), 
                               headers=headers, data=data)
        
        if response.status_code in [200, 201]:
            logger.info(f"✅ Publicada: {table_name}")
            return True
        else:
            logger.warning(f"⚠️  Error: {table_name} - {response.status_code}")
            return False
            
    except Exception as e:
        logger.warning(f"⚠️  Error con {table_name}: {e}")
        return False

def main():
    """Función principal"""
    logger.info("📤 Publicando Capas en GeoServer")
    logger.info("=" * 50)
    
    # Actualizar datastore
    logger.info("🔧 Actualizando datastore...")
    if not update_datastore():
        logger.error("❌ No se pudo actualizar el datastore")
        return
    
    # Obtener tablas
    logger.info("📋 Obteniendo tablas de PostGIS...")
    tables = get_postgis_tables()
    
    if not tables:
        logger.error("❌ No se encontraron tablas espaciales")
        return
    
    logger.info(f"📊 Encontradas {len(tables)} tablas espaciales")
    
    # Publicar capas
    logger.info("📤 Publicando capas...")
    published = 0
    failed = 0
    
    for table_info in tables:
        table_name = table_info[0]
        if publish_layer(table_name):
            published += 1
        else:
            failed += 1
    
    # Resumen
    logger.info("=" * 50)
    logger.info("🎉 Proceso completado!")
    logger.info(f"✅ Capas publicadas: {published}")
    logger.info(f"❌ Capas que fallaron: {failed}")
    logger.info(f"📊 Total procesadas: {len(tables)}")
    logger.info("")
    logger.info("💡 Verifica en GeoServer:")
    logger.info("   http://localhost:8080/geoserver")
    logger.info("   Workspace: geopamplona")
    logger.info("=" * 50)

if __name__ == "__main__":
    main() 