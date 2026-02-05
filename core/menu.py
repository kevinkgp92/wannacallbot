from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem
from colorama import Fore, Style
import requests

VERSION = '2.3 BETA'

def check_version():
    try:
        # Dummy check for now to avoid blocking
        return ""
    except:
        return ""

def create_menu(callbacks):
    """
    callbacks: dict with keys 'auto', 'porculero', 'nocturno', 'contrareembolso'
    mapped to functions.
    """
    banner = Fore.MAGENTA + Style.BRIGHT + r"""
  _____                _     _               ___    ____  
 |  __ \              | |   (_)             |__ \  |___ \ 
 | |__) |__ _ __ _   _| |__  _  __ _ _ __      ) |   __) |
 |  ___/ _ \ '__| | | | '_ \| |/ _` | '_ \    / /   |__ < 
 | |  |  __/ |  | |_| | |_) | | (_| | | | |  / /_ _ ___) |
 |_|   \___|_|   \__,_|_.__/|_|\__,_|_| |_| |____(_)____/ 
""" + Style.RESET_ALL

    menu = ConsoleMenu(banner + check_version(), "Seleccione un modo" + Style.RESET_ALL)

    item_auto = FunctionItem("Modo Automático (Llamadas)", callbacks['auto'])
    item_porculero = FunctionItem("Modo Porculero (Caos/Rápido)", callbacks['porculero'])
    item_nocturno = FunctionItem("Modo Nocturno (Disponible 24h/Noche)", callbacks['nocturno'])
    item_contrareembolso = FunctionItem("Modo Contrareembolso (Físico)", callbacks['contrareembolso'])

    menu.append_item(item_auto)
    menu.append_item(item_porculero)
    menu.append_item(item_nocturno)
    menu.append_item(item_contrareembolso)
    
    return menu
