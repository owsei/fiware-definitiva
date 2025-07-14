@echo off
echo ========================================
echo  Instalacion de GDAL/OGR para Windows
echo ========================================
echo.

echo Verificando si GDAL ya esta instalado...
ogr2ogr --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GDAL ya esta instalado
    ogr2ogr --version
    echo.
    echo Presiona cualquier tecla para continuar con la restauracion...
    pause >nul
    goto :restore
)

echo ❌ GDAL no encontrado. Instalando...
echo.

echo Opcion 1: Instalar con conda (recomendado si tienes Anaconda/Miniconda)
echo conda install -c conda-forge gdal
echo.

echo Opcion 2: Descargar OSGeo4W (instalador independiente)
echo https://trac.osgeo.org/osgeo4w/
echo.

echo Opcion 3: Instalar con pip (puede ser problematico)
echo pip install gdal
echo.

echo ¿Que opcion prefieres?
echo [1] Intentar con conda
echo [2] Abrir pagina de OSGeo4W
echo [3] Intentar con pip
echo [4] Salir y instalar manualmente
echo.

set /p choice="Elige una opcion (1-4): "

if "%choice%"=="1" goto :conda
if "%choice%"=="2" goto :osgeo
if "%choice%"=="3" goto :pip
if "%choice%"=="4" goto :manual
goto :invalid

:conda
echo.
echo Instalando GDAL con conda...
conda install -c conda-forge gdal -y
if %errorlevel% equ 0 (
    echo ✅ GDAL instalado exitosamente con conda
    goto :verify
) else (
    echo ❌ Error instalando con conda
    goto :osgeo
)

:pip
echo.
echo Instalando GDAL con pip...
pip install gdal
if %errorlevel% equ 0 (
    echo ✅ GDAL instalado exitosamente con pip
    goto :verify
) else (
    echo ❌ Error instalando con pip
    goto :osgeo
)

:osgeo
echo.
echo Abriendo pagina de OSGeo4W...
start https://trac.osgeo.org/osgeo4w/
echo.
echo Por favor:
echo 1. Descarga OSGeo4W64 Setup
echo 2. Ejecuta el instalador
echo 3. Selecciona "Express Install"
echo 4. Instala GDAL
echo 5. Reinicia esta ventana de comandos
echo.
echo Presiona cualquier tecla cuando hayas terminado...
pause >nul
goto :verify

:manual
echo.
echo Instalacion manual requerida.
echo Visita: https://gdal.org/download.html
echo O: https://trac.osgeo.org/osgeo4w/
echo.
echo Despues de instalar, reinicia la ventana de comandos y ejecuta:
echo python restore_simple.py
echo.
pause
exit /b 1

:invalid
echo Opcion invalida. Intentalo de nuevo.
goto :choice

:verify
echo.
echo Verificando instalacion...
ogr2ogr --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GDAL instalado correctamente
    ogr2ogr --version
    goto :restore
) else (
    echo ❌ GDAL aun no funciona. Puede necesitar reiniciar la ventana de comandos.
    echo.
    echo Intenta:
    echo 1. Cerrar esta ventana
    echo 2. Abrir una nueva ventana de comandos
    echo 3. Ejecutar: python restore_simple.py
    pause
    exit /b 1
)

:restore
echo.
echo ========================================
echo  Ejecutando restauracion de capas
echo ========================================
python restore_simple.py

echo.
echo ========================================
echo  Proceso completado
echo ========================================
pause 