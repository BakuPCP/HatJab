import os
import sys
import io
import json
from System import hjcheck, crypto

# Настройка кодировки системы
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def show_logo():
    logo = r"""
██╗  ██╗ █████╗ ████████╗     ██╗  █████╗ ██████╗  
██║  ██║██╔══██╗╚══██╔══╝     ██║ ██╔══██╗██╔══██╗  
███████║███████║   ██║        ██║ ███████║██████╔╝  
██╔══██║██╔══██║   ██║   ██   ██║ ██╔══██║██╔══██╗  
██║  ██║██║  ██║   ██║   ╚█████╔╝ ██║  ██║██████╔╝  
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚════╝  ╚═╝  ╚═╝╚═════╝  
"""
    print(logo)
    print("Welcome to HatJab v1.0.5!")
    print("Type 'help' to view commands\n")

def initialize_environment():
    """Инициализация окружения"""
    required_dirs = ["System", "mods", "Scripts", "Data", "catalyst"]
    for folder in required_dirs:
        os.makedirs(folder, exist_ok=True)

    if os.path.exists("System/catal.modhj"):
        if not crypto.decrypt_to_file("System/catal.modhj", "System/catal.py"):
            print("[Error] Unable to decrypt catal.modhj")

def load_commands():
    """Загрузка команд"""
    commands_file = "Scripts/commands.txt"
    default_commands = {
        "help": "Show command list",
        "mods": "Show mods list",
        "clear": "Clear console",
        "settings": "System settings",
        "exit": "Exit",
        "backup": "Create backup",
        "catt": "Show mods in catalyst",
        "version": "System version"
    }

    if not os.path.exists(commands_file):
        try:
            with open(commands_file, "w", encoding="utf-8") as f:
                for cmd, desc in default_commands.items():
                    f.write(f"{cmd}\t| {desc}\n")
            return list(default_commands.items())
        except Exception as e:
            print(f"[Error] Failed to create commands.txt: {e}")
            return list(default_commands.items())

    encodings = ['utf-8', 'cp1251', 'utf-16-le']
    for encoding in encodings:
        try:
            commands = []
            with open(commands_file, "r", encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("\t| ")
                        if len(parts) >= 2:
                            commands.append((parts[0], " | ".join(parts[1:])))
            if commands:
                return commands
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"[Error] Reading commands.txt: {e}")
            continue

    print("[NOTICE] Creating new command file...")
    try:
        with open(commands_file, "w", encoding="utf-8") as f:
            for cmd, desc in default_commands.items():
                f.write(f"{cmd}\t| {desc}\n")
        return list(default_commands.items())
    except Exception as e:
        print(f"[CRITICAL] Failed to create commands.txt: {e}")
        return [("help", "Показать справку"), ("exit", "Выход")]

def run_ai_editor():
    """Запуск графического редактора"""
    try:
        # Добавляем путь к модулям
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Scripts.settings import start_editor
        start_editor()
    except ImportError as e:
        print(f"[Error] Failed to import editor: {e}")
    except Exception as e:
        print(f"[Error] Editor malfunction: {e}")

def main():
    """Основная функция программы"""
    initialize_environment()
    show_logo()

    if not hjcheck.check_password():
        return

    try:
        from System import catal
    except ImportError as e:
        print(f"[Error] Failed to load module catal: {e}")
        catal = None

    commands = load_commands()

    while True:
        try:
            cmd = input("> ").strip().lower()
            if not cmd:
                continue

            if cmd == "help":
                print("\nCommands:")
                max_len = max(len(c[0]) for c in commands)
                for c, d in commands:
                    print(f"  {c.ljust(max_len)} - {d}")

            elif cmd == "mods":
                hjcheck.list_mods()

            elif cmd == "catt" and catal:
                files = catal.get_mod_list()
                print("\nFile in catalyst:" if files else "\nFolder catalyst is empty")
                for f in sorted(files):
                    print(f"- {f}")



            elif cmd == "settings":

                print("\nChoose settings editor:")

                print("1. Console")

                print("2. GUI")

                choice = input("Select (1-2): ").strip()

                if choice == "1":

                    try:

                        from Scripts.console_settings import ConsoleSettingsEditor

                        editor = ConsoleSettingsEditor()

                        editor.run()

                    except Exception as e:

                        print(f"[Error] Failed to start console: {e}")

                elif choice == "2":

                    try:

                        from Scripts.settings import start_editor

                        start_editor()

                    except Exception as e:

                        print(f"[Error] Failed to start GUI: {e}")

                else:

                    print("Invalid choice, returning to main menu")

            elif cmd == "exit":
                if catal and catal.process_mods():
                    print("\n[System] New mods installed")

                if input("\nSave session before exit? (y/n): ").lower() == 'y':
                    crypto.save_session()
                    print("Session saved")

                if os.path.exists("System/catal.py"):
                    crypto.encrypt_file("System/catal.py", "System/catal.modhj")
                    print("File catal encrypted")
                break

            elif cmd == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            elif cmd == "backup":
                crypto.create_backup()

            elif cmd == "version":
                print("\nHatJab v1.0.5")
                print("Mod & Encryption management System")

            else:
                print(f"\nUnknown command: {cmd}")
                print("Type 'help' to view commands")

        except KeyboardInterrupt:
            print("\nПрерывание (Ctrl+C)")
            if input("Terminate program? (y/n): ").lower() == 'y':
                if os.path.exists("System/catal.py"):
                    crypto.encrypt_file("System/catal.py", "System/catal.modhj")
                break

        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()