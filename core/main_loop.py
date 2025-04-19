import os
import sys
from System import crypto
from .commands import load_commands


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

    elif cmd.startswith("settings text color"):
        # Обработка изменения цвета текста
        color = cmd.split()[-1].lower()
        colors = {
            'green': '\033[92m',
            'lightblue': '\033[94m',
            'purple': '\033[95m',
            'default': '\033[0m'
        }

        if color in colors:
            # Сохраняем настройки цвета
            try:
                with open("Scripts/color.cfg", "w") as f:
                    f.write(color)
                print(f"{colors[color]}Text color changed to {color}{colors['default']}")
            except Exception as e:
                print(f"[Error] Failed to save color settings: {e}")
        else:
            print("Available colors: green, lightblue, purple, default")

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