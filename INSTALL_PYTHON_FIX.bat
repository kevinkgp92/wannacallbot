@echo off
title INSTALADOR AUTOMATICO DE PYTHON (PARA PERUBIAN BOT)
color 0A

echo ===================================================
echo      ASISTENTE DE INSTALACION PYTHON (PARA KEVIN)
echo ===================================================
echo.
echo ESTE SCRIPT SOLUCIONARA EL PROBLEMA DE LAS DLLs.
echo.

echo [PASO 1/3] Descargando Python 3.11 (Oficial)...
echo ---------------------------------------------------
curl -L -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

if not exist python_installer.exe (
    color 0C
    echo [ERROR] No se pudo descargar el instalador. Revisa tu internet.
    pause
    exit
)

echo.
echo [PASO 2/3] Instalando Python... 
echo ---------------------------------------------------
echo IMPORTANTE: Si te sale una ventana pidiendo permiso (Si/No), dale a SI.
echo Esto puede tardar 1 o 2 minutos. Espera a que termine.
echo.

:: /passive = Muestra barra de progreso pero no pide clics
:: PrependPath=1 = AGREGA PYTHON AL PATH (Crucial)
:: InstallAllUsers=0 = Instala solo para tu usuario (menos problemas de permisos)
python_installer.exe /passive PrependPath=1 Include_test=0 PromptOnSecure=0

echo.
echo [PASO 3/3] Limpiando basura...
echo ---------------------------------------------------
del python_installer.exe

echo.
echo ===================================================
echo    INSTALACION COMPLETADA CON EXITO
echo ===================================================
echo.
echo AHORA ES NECESARIO REINICIAR TU ORDENADOR.
echo.
echo Cuando vuelvas:
echo 1. Ejecuta RESCUE_READY_GO.bat
echo 2. Prueba a generar el EXE.
echo.
pause
