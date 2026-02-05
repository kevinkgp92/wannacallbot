@echo off
title INSTALADOR DE DEPENDENCIAS (PERUBIAN BOT)
color 0B

echo ===================================================
echo    INSTALANDOLIBRERIAS FALTANTES (VITAMINAS)
echo ===================================================
echo.
echo Como tenemos un Python nuevo, esta limpio.
echo Vamos a instalarle lo necesario.
echo.

pip install customtkinter selenium webdriver-manager requests pyinstaller pillow packaging

echo.
echo ===================================================
echo    LIBRERIAS INSTALADAS. TODO LISTO.
echo ===================================================
echo.
pause
