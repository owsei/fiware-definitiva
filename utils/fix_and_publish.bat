@echo off
echo ========================================
echo 🔧 REPARACION Y PUBLICACION DE CAPAS
echo ========================================
echo.

echo Verificando dependencias...
python -c "import psycopg2, requests" 2>nul
if errorlevel 1 (
    echo ⚠️  Instalando dependencias...
    pip install psycopg2-binary requests
)

echo.
echo ¿Qué deseas hacer?
echo 1. Solo publicar capas existentes (RAPIDO)
echo 2. Reparar errores + publicar todo (COMPLETO)
echo.
set /p choice="Elige opción (1 o 2): "

if "%choice%"=="1" (
    echo.
    echo 📤 Publicando capas existentes en GeoServer...
    python publish_layers.py
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Ejecutando reparación completa...
    python restore_fixed.py
) else (
    echo ❌ Opción inválida
    goto end
)

echo.
echo ✅ Proceso completado!
echo 💡 Verifica en: http://localhost:8080/geoserver

:end
pause 