@echo off
echo ===================================================
echo      BUILDING CARNEROSBOT V1.0 (ARIES EDITION)
echo ===================================================

echo [1/4] Installing requirements...
pip install -r requirements.txt --quiet
pip install phonenumbers requests beautifulsoup4 selenium-stealth undetected-chromedriver --quiet
pip install pyinstaller --quiet

echo [2/4] Cleaning old builds...
taskkill /f /im CarnerosBot_Aries.exe >nul 2>&1
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo [3/4] Compiling EXE...
if exist CarnerosBot_Aries.spec (
    echo Found spec file. Building from spec...
    python -m PyInstaller CarnerosBot_Aries.spec
) else (
    echo Spec file not found. Generatign...
    python -m PyInstaller --noconsole --onefile --name "CarnerosBot_Aries" --paths . --collect-all customtkinter --collect-all undetected_chromedriver --collect-all selenium_stealth --collect-submodules core --collect-submodules services --add-data "carnerosbot_logo.png;." --hidden-import core --hidden-import core.osint --hidden-import services --hidden-import services.manager --hidden-import services.definitions --hidden-import phonenumbers --hidden-import requests --hidden-import bs4 --hidden-import selenium_stealth --hidden-import undetected_chromedriver gui.py
)

echo [4/4] Finalizing...
if exist dist\CarnerosBot_Aries.exe (
    echo.
    echo [SUCCESS] Build generated at: dist\CarnerosBot_Aries.exe
    echo COPYING history.json if exists...
    if exist history.json copy history.json dist\
    echo.
    echo [LAUNCH] Abriendo bot automaticamente...
    start dist\CarnerosBot_Aries.exe
) else (
    echo [ERROR] Build failed.
)

pause
