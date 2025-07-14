#!/usr/bin/env python3
"""
Script para probar la conexión PostGIS desde la perspectiva de GeoServer
"""

import psycopg2
import requests

# Configuración
GEOSERVER_URL = "http://localhost:8080/geoserver"
GEOSERVER_USER = "admin"
GEOSERVER_PASS = "geoserver"
WORKSPACE = "geopamplona"
DATASTORE = "geopamplona_postgis"

# Configuraciones de PostGIS a probar
DB_CONFIGS = [
    {
        "name": "localhost:5433",
        "host": "localhost",
        "port": "5433",
        "dbname": "geopamplona",
        "user": "admin",
        "password": "admin"
    },
    {
        "name": "postgis:5432 (interno Docker)",
        "host": "postgis",
        "port": "5432",
        "dbname": "geopamplona",
        "user": "admin",
        "password": "admin"
    },
    {
        "name": "host.docker.internal:5433",
        "host": "host.docker.internal",
        "port": "5433",
        "dbname": "geopamplona",
        "user": "admin",
        "password": "admin"
    }
]

def test_postgis_connection(config):
    """Probar conexión directa a PostGIS"""
    try:
        print(f"🔍 Probando conexión: {config['name']}")
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            dbname=config['dbname'],
            user=config['user'],
            password=config['password']
        )
        cur = conn.cursor()
        
        # Probar consulta básica
        cur.execute("SELECT COUNT(*) FROM geometry_columns WHERE f_table_schema = 'public'")
        count = cur.fetchone()[0]
        
        # Probar tabla específica
        cur.execute("SELECT COUNT(*) FROM alum_pto_acometida LIMIT 1")
        table_count = cur.fetchone()[0]
        
        conn.close()
        
        print(f"   ✅ Conexión exitosa")
        print(f"   📊 Tablas espaciales: {count}")
        print(f"   📋 Registros en alum_pto_acometida: {table_count}")
        return True, config
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def update_datastore_config(working_config):
    """Actualizar configuración del datastore con la configuración que funciona"""
    try:
        print(f"\n🔧 Actualizando datastore con configuración: {working_config['name']}")
        
        url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}"
        headers = {'Content-type': 'text/xml'}
        data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <dataStore>
            <name>{DATASTORE}</name>
            <connectionParameters>
                <host>{working_config['host']}</host>
                <port>{working_config['port']}</port>
                <database>{working_config['dbname']}</database>
                <user>{working_config['user']}</user>
                <passwd>{working_config['password']}</passwd>
                <dbtype>postgis</dbtype>
                <schema>public</schema>
                <validate>true</validate>
                <Connection timeout>20</Connection timeout>
                <preparedStatements>false</preparedStatements>
            </connectionParameters>
        </dataStore>
        """
        
        response = requests.put(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), 
                               headers=headers, data=data)
        
        if response.status_code in [200, 201]:
            print("   ✅ Datastore actualizado exitosamente")
            return True
        else:
            print(f"   ❌ Error actualizando datastore: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_geoserver_layer_creation():
    """Probar crear una capa después de actualizar la configuración"""
    try:
        print(f"\n🧪 Probando crear capa después de actualización...")
        
        url = f"{GEOSERVER_URL}/rest/workspaces/{WORKSPACE}/datastores/{DATASTORE}/featuretypes"
        headers = {'Content-type': 'text/xml'}
        
        test_table = "alum_pto_acometida"
        data = f"""<?xml version="1.0" encoding="UTF-8"?>
        <featureType>
            <name>{test_table}</name>
            <nativeName>{test_table}</nativeName>
            <title>Test Layer - {test_table}</title>
            <abstract>Capa de prueba para verificar conexión</abstract>
            <srs>EPSG:4326</srs>
            <enabled>true</enabled>
            <advertised>true</advertised>
        </featureType>
        """
        
        response = requests.post(url, auth=(GEOSERVER_USER, GEOSERVER_PASS), 
                               headers=headers, data=data)
        
        if response.status_code in [200, 201]:
            print("   ✅ Capa de prueba creada exitosamente!")
            return True
        else:
            print(f"   ❌ Error creando capa: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO DE CONEXIÓN POSTGIS-GEOSERVER")
    print("=" * 60)
    
    working_config = None
    
    # Probar diferentes configuraciones de conexión
    for config in DB_CONFIGS:
        success, conf = test_postgis_connection(config)
        if success:
            working_config = conf
            break
        print()
    
    if not working_config:
        print("❌ No se pudo establecer conexión con PostGIS")
        print("💡 Verifica que el contenedor PostGIS esté ejecutándose:")
        print("   docker ps | grep postgis")
        return
    
    print(f"\n✅ Configuración de trabajo encontrada: {working_config['name']}")
    
    # Actualizar datastore con la configuración que funciona
    if update_datastore_config(working_config):
        # Probar crear una capa
        if test_geoserver_layer_creation():
            print("\n" + "=" * 60)
            print("🎉 ¡PROBLEMA SOLUCIONADO!")
            print("✅ Conexión PostGIS-GeoServer funcionando")
            print("💡 Ahora ejecuta: fix_and_publish.bat opción 1")
        else:
            print("\n❌ Aún hay problemas con la creación de capas")
    else:
        print("\n❌ No se pudo actualizar la configuración del datastore")

if __name__ == "__main__":
    main() 