import os
import sys
from System import crypto
from .commands import load_commands
from core.settings_manager import settings_manager

def handle_command(cmd, commands, catal=None):
    """Обработка команд"""
    if not cmd:
        return True

    if cmd == "get gui":
        try:
            from gui_launcher import launch_gui
            launch_gui()
            return False  # Закрыть консоль после запуска GUI
        except Exception as e:
            print(f"[Error] Failed to launch GUI: {e}")
            return True

    if cmd == "help":
        print("\nCommands:")
        max_len = max(len(c[0]) for c in commands)
        for c, d in commands:
            print(f"  {c.ljust(max_len)} - {d}")

    elif cmd == "mods":
        from System import hjcheck
        hjcheck.list_mods()

    elif cmd.startswith("settings --first-start"):
        mode = cmd.split()[-1].lower()
        if mode in ["gui", "console"]:
            new_settings = settings_manager.settings.copy()
            new_settings["first_start"] = mode
            if settings_manager.save_settings(new_settings):
                print(f"\nStartup mode set to: {mode}")
            else:
                print("\nFailed to save settings")
        else:
            print("\nInvalid mode. Use 'gui' or 'console'")

    elif cmd.startswith("settings text color"):

        color = cmd.split()[-1].lower()

        if settings_manager.save_color(color):

            colors = {

                'green': '\033[92m',

                'lightblue': '\033[94m',

                'purple': '\033[95m',

                'default': '\033[0m'

            }

            print(f"{colors[color]}Text color changed to {color}{colors['default']}")

        else:

            print("Available colors: green, lightblue, purple, default")

    elif cmd == "catt" and catal:
        files = catal.get_mod_list()
        print("\nFile in catalyst:" if files else "\nFolder catalyst is empty")
        for f in sorted(files):
            print(f"- {f}")

    elif cmd == "settings":
        try:
            from Scripts.settings import start_editor
            start_editor()
        except Exception as e:
            print(f"[Error] Failed to start GUI settings editor: {e}")


    elif cmd == "exit":

        if catal and catal.process_mods():
            print("\n[System] New mods installed")

        if input("\nSave session before exit? (y/n): ").lower() == 'y':
            crypto.save_session()

            print("Session saved")
            return False



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

    return True


def main_loop(catal=None):
    """Основной цикл программы"""
    # Проверяем режим первого запуска
    if settings_manager.first_start_mode == "gui":
        try:
            from gui_launcher import launch_gui
            launch_gui()
            return
        except Exception as e:
            print(f"[Error] Failed to launch GUI: {e}")
            print("Falling back to console mode")

    commands = load_commands()

    while True:
        try:
            cmd = input("> ").strip().lower()
            if not handle_command(cmd, commands, catal):
                break

        except KeyboardInterrupt:
            print("\nПрерывание (Ctrl+C)")
            if input("Terminate program? (y/n): ").lower() == 'y':
                if os.path.exists("System/catal.py"):
                    crypto.encrypt_file("System/catal.py", "System/catal.modhj")
                break

        except Exception as e:
            print(f"\n[Error] {e}")