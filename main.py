import sys
import argparse
from colorama import init
from core.inputs import InputHandler
from core.menu import create_menu
from services.manager import ServiceManager

# Initialize colorama
init()

# Force utf-8 for windows console
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Habilitar el modo debug (datos falsos)")
    args = parser.parse_args()

    # 1. Get User Data
    input_handler = InputHandler(debug=args.debug)
    user_data = input_handler.get_user_data()

    # 2. Initialize Service Manager
    manager = ServiceManager(user_data)

    # 3. Create Menu with Callbacks
    # Define wrappers to match menu callback signature if needed, or just pass methods
    def run_auto():
        manager.run_auto()
        input("Presione ENTER para continuar...")

    def run_porculero():
        manager.run_porculero()
        input("Presione ENTER para continuar...")

    def run_nocturno():
        manager.run_nocturno()
        input("Presione ENTER para continuar...")

    def run_contrareembolso():
        manager.run_contrareembolso()
        input("Presione ENTER para continuar...")

    callbacks = {
        'auto': run_auto,
        'porculero': run_porculero,
        'nocturno': run_nocturno,
        'contrareembolso': run_contrareembolso
    }
    
    menu = create_menu(callbacks)
    
    # 4. Show Menu
    menu.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        sys.exit(0)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n[CRITICAL ERROR] {e}")
        input("Presione ENTER para salir...")
        sys.exit(1)
