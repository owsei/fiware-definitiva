#!/usr/bin/env python3
"""
Script mejorado para restaurar capas solucionando errores de geometría
"""

import os
import sys
import subprocess
import psycopg2
import requests
from pathlib import Path
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

SHAPEFILES_DIR = Path("geopamplona_shp")

def import_shapefile_fixed(shapefile_path):
    """Importar shapefile con configuración mejorada para evitar errores"""
    table_name = shapefile_path.stem.lower()
    
    try:
        logger.info(f"📥 Importando {shapefile_path.name} -> {table_name}")
        
        # Comando ogr2ogr mejorado
        cmd = [
            "ogr2ogr",
            "-f", "PostgreSQL",
            f"PG:host={DB_CONFIG['host']} port={DB_CONFIG['port']} dbname={DB_CONFIG['dbname']} user={DB_CONFIG['user']} password={DB_CONFIG['password']}",
            str(shapefile_path),
            "-nln", table_name,
            "-overwrite",
            "-t_srs", "EPSG:4326",
            "-lco", "GEOMETRY_NAME=geom",
            "-nlt", "PROMOTE_TO_MULTI",  # Promover a Multi-geometrías
            "-lco", "SPATIAL_INDEX=GIST",  # Usar GIST en lugar de YES
            "-lco", "PRECISION=NO",  # Evitar problemas de precisión
            "-skipfailures"  # Continuar aunque fallen algunas geometrías
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ Importado: {table_name}")
            return True
        else:
            # Si falla, intentar con configuración más permisiva
            logger.warning(f"⚠️  Primer intento falló, probando configuración alternativa...")
            return import_shapefile_alternative(shapefile_path)
            
    except Exception as e:
        logger.error(f"❌ Error con {shapefile_path.name}: {e}")
        return False

def import_shapefile_alternative(shapefile_path):
    """Método alternativo para shapefiles problemáticos"""
    table_name = shapefile_path.stem.lower()
    
    try:
        # Comando más permisivo
        cmd = [
            "ogr2ogr",
            "-f", "PostgreSQL",
            f"PG:host={DB_CONFIG['host']} port={DB_CONFIG['port']} dbname={DB_CONFIG['dbname']} user={DB_CONFIG['user']} password={DB_CONFIG['password']}",
            str(shapefile_path),
            "-nln", table_name,
            "-overwrite",
            "-t_srs", "EPSG:4326",
            "-lco", "GEOMETRY_NAME=geom",
            "-nlt", "GEOMETRY",  # Tipo genérico de geometría
            "-lco", "SPATIAL_INDEX=NONE",  # Sin índice espacial inicialmente
            "-skipfailures",
            "-relaxedFieldNameMatch"  # Nombres de campo más flexibles
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ Importado (alternativo): {table_name}")
            # Crear índice espacial después
            create_spatial_index(table_name)
            return True
        else:
            logger.error(f"❌ Falló método alternativo para {shapefile_path.name}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error método alternativo {shapefile_path.name}: {e}")
        return False

def create_spatial_index(table_name):
    """Crear índice espacial manualmente"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Crear índice espacial
        index_name = f"idx_{table_name}_geom"
        cur.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} USING GIST (geom);")
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Índice espacial creado para {table_name}")
        
    except Exception as e:
        logger.warning(f"⚠️  No se pudo crear índice para {table_name}: {e}")

def get_failed_shapefiles():
    """Obtener lista de shapefiles que fallaron en la importación anterior"""
    failed_patterns = [
        "AMBI_Pol_TH_Energia_Edificios",
        "AMBI_Pol_TH_Energia_EdifPub", 
        "JARD_Lin_Seto",
        "JARD_Lin_Tuberia",
        "MOBI_Pol_JuegosInf",
        "MOVI_Pol_ZonasPeatonales",
        "PROY_Pol_Edificios",
        "SEGU_Lin_EsRegZonas",
        "SEGU_Pol_EsRegSector",
        "SEGU_Pol_SenHorizont",
        "TURI_Lin_RutaVerde",
        "URBA_Lin_Alineaciones",
        "URBA_Lin_InfrTelef",
        "URBA_Lin_RedViaria",
        "URBA_Pol_UsoPorSU"
    ]
    
    failed_files = []
    for pattern in failed_patterns:
        files = list(SHAPEFILES_DIR.rglob(f"{pattern}.shp"))
        failed_files.extend(files)
    
    logger.info(f"📁 Encontrados {len(failed_files)} archivos que fallaron anteriormente")
    return failed_files

def publish_all_layers_to_geoserver():
    """Publicar todas las tablas de PostGIS en GeoServer"""
    try:
        # Obtener todas las tablas espaciales
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT f_table_name
            FROM geometry_columns
            WHERE f_table_schema = 'public'
            ORDER BY f_table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        
        logger.info(f"📤 Publicando {len(tables)} capas en GeoServer...")
        
        published_count = 0
        failed_count = 0
        
        for table in tables:
            if publish_layer_to_geoserver(table):
                published_count += 1
            else:
                failed_count += 1
        
        logger.info(f"✅ Capas publicadas: {published_count}")
        logger.info(f"❌ Capas que fallaron: {failed_count}")
        
        return published_count
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo tablas: {e}")
        return 0

def publish_layer_to_geoserver(table_name):
    """Publicar una tabla como capa en GeoServer"""
    try:
        # Verificar si ya existe
        check_url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}/featuretypes/{table_name}"
        check_response = requests.get(check_url, auth=(GEOSERVER_USER, GEOSERVER_PASS))
        
        if check_response.status_code == 200:
            logger.info(f"✅ Capa ya existe: {table_name}")
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
            logger.info(f"✅ Capa publicada: {table_name}")
            return True
        else:
            logger.warning(f"⚠️  Error publicando {table_name}: {response.status_code}")
            return False
            
    except Exception as e:
        logger.warning(f"⚠️  Error con {table_name}: {e}")
        return False

def update_geoserver_datastore():
    """Actualizar configuración del datastore en GeoServer"""
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
        logger.info("✅ Datastore actualizado en GeoServer")
        return True
    else:
        logger.error(f"❌ Error actualizando datastore: {response.status_code}")
        return False

def main():
    """Función principal"""
    logger.info("🔧 Reparación de Capas y Publicación en GeoServer")
    logger.info("=" * 60)
    
    # Opción 1: Solo publicar capas existentes
    logger.info("¿Qué deseas hacer?")
    logger.info("1. Solo publicar capas existentes en GeoServer")
    logger.info("2. Reimportar capas que fallaron + publicar todas")
    logger.info("3. Ambas opciones")
    
    choice = input("Elige una opción (1-3): ").strip()
    
    if choice in ["1", "3"]:
        logger.info("📤 Publicando capas existentes en GeoServer...")
        update_geoserver_datastore()
        published = publish_all_layers_to_geoserver()
        logger.info(f"✅ Publicadas {published} capas")
    
    if choice in ["2", "3"]:
        logger.info("🔧 Reimportando capas que fallaron...")
        failed_files = get_failed_shapefiles()
        
        if failed_files:
            imported_count = 0
            for i, shapefile in enumerate(failed_files, 1):
                logger.info(f"[{i}/{len(failed_files)}] Reprocessando...")
                if import_shapefile_fixed(shapefile):
                    imported_count += 1
            
            logger.info(f"✅ Reimportadas {imported_count} de {len(failed_files)} capas")
            
            # Publicar las nuevas capas
            if imported_count > 0:
                logger.info("📤 Publicando capas reimportadas...")
                update_geoserver_datastore()
                publish_all_layers_to_geoserver()
        else:
            logger.info("ℹ️  No se encontraron archivos que fallaron")
    
    # Resumen final
    logger.info("=" * 60)
    logger.info("🎉 Proceso completado!")
    logger.info("💡 Verifica el resultado en:")
    logger.info("   - PostGIS: Tablas espaciales")
    logger.info("   - GeoServer: http://localhost:8080/geoserver")
    logger.info("   - Workspace: geopamplona")
    logger.info("=" * 60)

if __name__ == "__main__":
    main() 