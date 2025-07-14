#!/usr/bin/env python3
"""
Script para verificar el estado actual de PostGIS y GeoServer
antes de ejecutar la restauración de capas.
"""

import psycopg2
import requests
import json
from pathlib import Path

# Configuración
DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "dbname": "geopamplona",
    "user": "admin",
    "password": "admin"
}

GEOSERVER_URL = "http://localhost:8080/geoserver"
GEOSERVER_USER = "admin"
GEOSERVER_PASS = "geoserver"
WORKSPACE = "geopamplona"

def check_postgis_status():
    """Verificar estado de PostGIS"""
    print("🔍 Verificando PostGIS...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Contar tablas espaciales
        cur.execute("""
            SELECT COUNT(*) FROM geometry_columns 
            WHERE f_table_schema = 'public'
        """)
        table_count = cur.fetchone()[0]
        
        # Listar tablas
        cur.execute("""
            SELECT f_table_name FROM geometry_columns 
            WHERE f_table_schema = 'public'
            ORDER BY f_table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        print(f"✅ PostGIS conectado exitosamente")
        print(f"📊 Tablas espaciales encontradas: {table_count}")
        
        if tables:
            print("📋 Tablas actuales:")
            for i, table in enumerate(tables, 1):
                print(f"   {i:2d}. {table}")
        else:
            print("⚠️  No hay tablas espaciales en PostGIS")
        
        conn.close()
        return table_count, tables
        
    except Exception as e:
        print(f"❌ Error conectando a PostGIS: {e}")
        return 0, []

def check_geoserver_status():
    """Verificar estado de GeoServer"""
    print("\n🔍 Verificando GeoServer...")
    try:
        # Verificar conexión
        response = requests.get(f"{GEOSERVER_URL}/rest/about/version", 
                              auth=(GEOSERVER_USER, GEOSERVER_PASS))
        
        if response.status_code != 200:
            print(f"❌ Error conectando a GeoServer: {response.status_code}")
            return 0, []
        
        print("✅ GeoServer conectado exitosamente")
        
        # Obtener capas del workspace
        response = requests.get(f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/layers", 
                              auth=(GEOSERVER_USER, GEOSERVER_PASS),
                              headers={'Accept': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            layers = []
            if 'layers' in data and 'layer' in data['layers']:
                layer_list = data['layers']['layer']
                if isinstance(layer_list, list):
                    layers = [layer['name'] for layer in layer_list]
                else:
                    layers = [layer_list['name']]
            
            print(f"📊 Capas publicadas en workspace '{WORKSPACE}': {len(layers)}")
            
            if layers:
                print("📋 Capas actuales:")
                for i, layer in enumerate(sorted(layers), 1):
                    print(f"   {i:2d}. {layer}")
            else:
                print("⚠️  No hay capas publicadas en el workspace")
            
            return len(layers), layers
        else:
            print(f"⚠️  No se pudo obtener lista de capas: {response.status_code}")
            return 0, []
            
    except Exception as e:
        print(f"❌ Error conectando a GeoServer: {e}")
        return 0, []

def check_shapefiles():
    """Verificar archivos shapefile disponibles"""
    print("\n🔍 Verificando archivos shapefile...")
    
    shapefiles_dir = Path("geopamplona_shp")
    if not shapefiles_dir.exists():
        print(f"❌ Directorio no encontrado: {shapefiles_dir}")
        return 0, []
    
    shapefiles = list(shapefiles_dir.rglob("*.shp"))
    print(f"✅ Directorio encontrado: {shapefiles_dir}")
    print(f"📊 Archivos shapefile disponibles: {len(shapefiles)}")
    
    if shapefiles:
        print("📋 Algunos archivos encontrados:")
        for i, shp in enumerate(sorted(shapefiles)[:10], 1):
            print(f"   {i:2d}. {shp.name}")
        if len(shapefiles) > 10:
            print(f"   ... y {len(shapefiles) - 10} más")
    
    return len(shapefiles), shapefiles

def main():
    """Función principal"""
    print("=" * 60)
    print("  VERIFICACIÓN DE ESTADO - PostGIS/GeoServer")
    print("=" * 60)
    
    # Verificar PostGIS
    postgis_count, postgis_tables = check_postgis_status()
    
    # Verificar GeoServer
    geoserver_count, geoserver_layers = check_geoserver_status()
    
    # Verificar shapefiles
    shapefile_count, shapefiles = check_shapefiles()
    
    # Resumen
    print("\n" + "=" * 60)
    print("  RESUMEN DEL ESTADO ACTUAL")
    print("=" * 60)
    print(f"📊 PostGIS tablas espaciales:     {postgis_count:3d}")
    print(f"📊 GeoServer capas publicadas:    {geoserver_count:3d}")
    print(f"📊 Archivos shapefile disponibles: {shapefile_count:3d}")
    
    # Análisis
    print("\n📈 ANÁLISIS:")
    if postgis_count < 50:
        print("⚠️  PostGIS tiene pocas tablas - se necesita restauración")
    else:
        print("✅ PostGIS parece tener un número adecuado de tablas")
    
    if geoserver_count < 100:
        print("⚠️  GeoServer tiene pocas capas publicadas")
    else:
        print("✅ GeoServer tiene un buen número de capas")
    
    if shapefile_count > 100:
        print("✅ Hay suficientes archivos shapefile para la restauración")
    else:
        print("⚠️  Pocos archivos shapefile disponibles")
    
    # Recomendación
    print("\n💡 RECOMENDACIÓN:")
    if postgis_count < shapefile_count // 2:
        print("🚀 Se recomienda ejecutar la restauración completa")
        print("   Ejecuta: python restore_layers.py")
    else:
        print("✅ El sistema parece estar en buen estado")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 