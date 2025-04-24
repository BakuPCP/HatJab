import os
import sys
from System import crypto
from .commands import load_commands
from core.settings_manager import settings_manager
from .autocomplete import init_autocomplete, disable_autocomplete

def restart_program():
    """Перезапускает программу"""
    python = sys.executable
    os.execl(python, python, *sys.argv)

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

    elif cmd.startswith("settings alias"):
        args = cmd.split()[2:]

        if not args or args[0] == "help":
            print("\nUsage:")
            print("  settings alias list          - Show all aliases")
            print("  settings alias [name=cmd]   - Create alias")
            print("  settings alias [name]=      - Remove alias")
            return True

        # Обработка list
        if args[0] == "list":
            aliases = settings_manager.handle_aliases("list")
            print("\nAliases:" if aliases else "\nNo aliases defined")
            for name, cmd in aliases.items():
                print(f"  {name.ljust(10)} = {cmd}")
            return True

        # Обработка добавления/удаления
        if "=" in args[0]:
            alias, _, command = args[0].partition("=")
            if not alias:
                print("\nError: Alias name cannot be empty")
                return True

            if command:  # Добавление
                if settings_manager.handle_aliases("set", alias, command):
                    print(f"\nAlias set: {alias} = {command}")
                else:
                    print("\nFailed to set alias")
            else:  # Удаление
                if settings_manager.handle_aliases("remove", alias):
                    print(f"\nAlias removed: {alias}")
                else:
                    print("\nAlias not found")
        else:
            print("\nInvalid syntax. Use 'name=command'")

    elif cmd.startswith("settings autosave"):
        args = cmd.split()[2:]

        if not args or args[0] == "help":
            print("\nUsage:")
            print("  settings autosave on [interval]  - Enable autosave (optional interval in minutes)")
            print("  settings autosave off           - Disable autosave")
            return True

        new_settings = settings_manager.settings.copy()

        if args[0] == "on":
            new_settings["autosave"] = True
            if len(args) > 1 and args[1].isdigit():
                new_settings["autosave_interval"] = int(args[1])
            print("\nAutosave enabled" +
                  (
                      f" with {new_settings['autosave_interval']} min interval" if 'autosave_interval' in new_settings else ""))

        elif args[0] == "off":
            new_settings["autosave"] = False
            print("\nAutosave disabled")

        else:
            print("\nInvalid argument. Use 'on' or 'off'")
            return True

        if settings_manager.save_settings(new_settings):
            print("Settings saved")
        else:
            print("Failed to save settings")

    elif cmd.startswith("settings autocomplete"):
        args = cmd.split()[2:]
        if not args or args[0] not in ["on", "off"]:
            print("\nUsage: settings autocomplete [on/off]")
            return True

        enabled = args[0] == "on"
        if settings_manager.set_autocomplete(enabled):
            if enabled:
                init_autocomplete([cmd[0] for cmd in commands])
                print("\nAutocomplete: ON (press TAB)")
            else:
                disable_autocomplete()
                print("\nAutocomplete: OFF")
        else:
            print("\nFailed to save settings")

    elif cmd.startswith("settings env"):
        args = cmd.split()[2:]

        if not args or args[0] == "help":
            print("\nUsage:")
            print("  settings env list                   - Show all variables")
            print("  settings env get [VAR]              - Get value")
            print("  settings env set [VAR] [VALUE]      - Set value")
            print("  settings env unset [VAR]            - Remove variable")
            return True

        action = args[0]
        result = None

        if action == "list":
            env_vars = settings_manager.handle_env_vars("list")
            print("\nEnvironment variables:")
            for k, v in env_vars.items():
                print(f"  {k}={v}")

        elif action == "get" and len(args) >= 2:
            value = settings_manager.handle_env_vars("get", args[1])
            print(f"\n{args[1]}={value}")

        elif action == "set" and len(args) >= 3:
            if settings_manager.handle_env_vars("set", args[1], " ".join(args[2:])):
                print(f"\nSet: {args[1]}={' '.join(args[2:])}")
            else:
                print("\nSetting error")

        elif action == "unset" and len(args) >= 2:
            if settings_manager.handle_env_vars("unset", args[1]):
                print(f"\nRemoved: {args[1]}")
            else:
                print("\nRemoval error")

        else:
            print("\nInvalid arguments. Use 'settings env help'")

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

    elif cmd == "reboot":
        print("\n[System] Restarting program...")
        if catal and catal.process_mods():
            print("[System] New mods installed before restart")
        restart_program()
        return False

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
    """Основной цикл программы с поддержкой автодополнения"""
    # Проверяем режим первого запуска
    global init_autocomplete
    if settings_manager.first_start_mode == "gui":
        try:
            from gui_launcher import launch_gui
            launch_gui()
            return
        except Exception as e:
            print(f"[Error] Failed to launch GUI: {e}")
            print("Falling back to console mode")

    commands = load_commands()

    # Инициализация автодополнения (НОВЫЙ БЛОК)
    try:
        if settings_manager.get_autocomplete():
            from .autocomplete import init_autocomplete
            command_names = [cmd[0] for cmd in commands]
            init_autocomplete(command_names)
    except Exception as e:
        print(f"[Warning] Autocomplete init failed: {e}")

    while True:
        try:
            # Получение ввода с поддержкой алиасов
            user_input = input("> ").strip()
            aliases = settings_manager.handle_aliases("list")
            cmd = aliases.get(user_input.split()[0], user_input)

            # Обработка команды автодополнения (НОВЫЙ ОБРАБОТЧИК)
            if cmd.startswith("settings autocomplete"):
                args = cmd.split()[2:]
                if not args or args[0] not in ["on", "off"]:
                    print("\nUsage: settings autocomplete [on/off]")
                    continue

                enabled = args[0] == "on"
                if settings_manager.set_autocomplete(enabled):
                    if enabled:
                        init_autocomplete([cmd[0] for cmd in commands])
                        print("\nAutocomplete: ON (press TAB)")
                    else:
                        from .autocomplete import disable_autocomplete
                        disable_autocomplete()
                        print("\nAutocomplete: OFF")
                else:
                    print("\nFailed to save settings")
                continue

            # Стандартная обработка команд
            if not handle_command(cmd.lower(), commands, catal):
                break

        except KeyboardInterrupt:
            print("\nПрерывание (Ctrl+C)")
            if input("Terminate program? (y/n): ").lower() == 'y':
                if os.path.exists("System/catal.py"):
                    crypto.encrypt_file("System/catal.py", "System/catal.modhj")
                break
        except Exception as e:
            print(f"\n[Error] {e}")