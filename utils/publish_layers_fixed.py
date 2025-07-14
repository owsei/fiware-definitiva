#!/usr/bin/env python3
"""
Script corregido para publicar todas las capas de PostGIS en GeoServer
Usa la configuración Docker correcta
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

# Configuración PostGIS (desde el host)
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

def ensure_datastore_config():
    """Asegurar que el datastore esté configurado correctamente"""
    try:
        logger.info("🔧 Verificando configuración del datastore...")
        
        # Verificar si existe
        check_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}"
        response = requests.get(check_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
        
        if response.status_code != 200:
            logger.info("🔧 Recreando datastore...")
            create_datastore()
        else:
            logger.info("✅ Datastore existe")
        
        return True
    except Exception as e:
        logger.error(f"❌ Error verificando datastore: {e}")
        return False

def create_datastore():
    """Crear datastore con configuración Docker correcta"""
    try:
        # Eliminar si existe
        delete_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}?recurse=true"
        requests.delete(delete_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
        
        # Crear nuevo
        url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores"
        headers = {'Content-type': 'text/xml'}
        data = f"""<?xml version="1.0" encoding="UTF-8"?>
<dataStore>
    <name>{DATASTORE}</name>
    <connectionParameters>
        <entry key="host">postgis</entry>
        <entry key="port">5432</entry>
        <entry key="database">geopamplona</entry>
        <entry key="user">admin</entry>
        <entry key="passwd">admin</entry>
        <entry key="dbtype">postgis</entry>
        <entry key="schema">public</entry>
        <entry key="Expose primary keys">true</entry>
        <entry key="validate connections">true</entry>
        <entry key="Connection timeout">20</entry>
    </connectionParameters>
</dataStore>"""
        
        response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), 
                               headers=headers, data=data)
        
        if response.status_code in [200, 201]:
            logger.info("✅ Datastore recreado exitosamente")
            return True
        else:
            logger.error(f"❌ Error creando datastore: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
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
        
        # Generar título más legible
        title = table_name.replace('_', ' ').title()
        
        data = f"""<?xml version="1.0" encoding="UTF-8"?>
<featureType>
    <name>{table_name}</name>
    <nativeName>{table_name}</nativeName>
    <title>{title}</title>
    <abstract>Capa {title} importada desde PostGIS</abstract>
    <srs>EPSG:4326</srs>
    <enabled>true</enabled>
    <advertised>true</advertised>
</featureType>"""
        
        response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), 
                               headers=headers, data=data)
        
        if response.status_code in [200, 201]:
            logger.info(f"✅ Publicada: {table_name}")
            return True
        else:
            logger.warning(f"⚠️  Error: {table_name} - {response.status_code}")
            if response.text:
                logger.debug(f"   Respuesta: {response.text[:200]}...")
            return False
            
    except Exception as e:
        logger.warning(f"⚠️  Error con {table_name}: {e}")
        return False

def publish_in_batches(tables, batch_size=10):
    """Publicar capas en lotes para mejor rendimiento"""
    total_tables = len(tables)
    published = 0
    failed = 0
    
    for i in range(0, total_tables, batch_size):
        batch = tables[i:i + batch_size]
        logger.info(f"📦 Procesando lote {i//batch_size + 1} ({len(batch)} capas)...")
        
        for table_info in batch:
            table_name = table_info[0]
            if publish_layer(table_name):
                published += 1
            else:
                failed += 1
        
        # Progreso
        progress = ((i + len(batch)) / total_tables) * 100
        logger.info(f"📊 Progreso: {progress:.1f}% ({published} publicadas, {failed} fallaron)")
    
    return published, failed

def main():
    """Función principal"""
    logger.info("📤 Publicando Capas en GeoServer (VERSIÓN CORREGIDA)")
    logger.info("=" * 60)
    
    # Verificar y configurar datastore
    logger.info("🔧 Configurando datastore...")
    if not ensure_datastore_config():
        logger.error("❌ No se pudo configurar el datastore")
        return
    
    # Obtener tablas
    logger.info("📋 Obteniendo tablas de PostGIS...")
    tables = get_postgis_tables()
    
    if not tables:
        logger.error("❌ No se encontraron tablas espaciales")
        return
    
    logger.info(f"📊 Encontradas {len(tables)} tablas espaciales")
    
    # Publicar capas en lotes
    logger.info("📤 Publicando capas en lotes...")
    published, failed = publish_in_batches(tables, batch_size=5)
    
    # Resumen
    logger.info("=" * 60)
    logger.info("🎉 Proceso completado!")
    logger.info(f"✅ Capas publicadas: {published}")
    logger.info(f"❌ Capas que fallaron: {failed}")
    logger.info(f"📊 Total procesadas: {len(tables)}")
    logger.info(f"📈 Tasa de éxito: {(published/len(tables)*100):.1f}%")
    logger.info("")
    logger.info("💡 Verifica en GeoServer:")
    logger.info("   http://localhost:8080/geoserver")
    logger.info("   Workspace: geopamplona")
    logger.info("=" * 60)

if __name__ == "__main__":
    main() 