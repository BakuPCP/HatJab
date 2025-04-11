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
    print("Добро пожаловать в HatJab v2.1!")
    print("Введите 'help' для списка команд\n")

def initialize_environment():
    """Инициализация окружения"""
    required_dirs = ["System", "mods", "Scripts", "Data", "catalyst"]
    for folder in required_dirs:
        os.makedirs(folder, exist_ok=True)

    if os.path.exists("System/catal.modhj"):
        if not crypto.decrypt_to_file("System/catal.modhj", "System/catal.py"):
            print("[Ошибка] Не удалось расшифровать catal.modhj")

def load_commands():
    """Загрузка команд"""
    commands_file = "Scripts/commands.txt"
    default_commands = {
        "help": "Показать список команд",
        "mods": "Список активных модов",
        "clear": "Очистить консоль",
        "settings": "Графический редактор системы",
        "exit": "Выход из программы",
        "backup": "Создать резервную копию",
        "catt": "Показать моды в catalyst",
        "version": "Показать версию системы"
    }

    if not os.path.exists(commands_file):
        try:
            with open(commands_file, "w", encoding="utf-8") as f:
                for cmd, desc in default_commands.items():
                    f.write(f"{cmd}\t| {desc}\n")
            return list(default_commands.items())
        except Exception as e:
            print(f"[Ошибка] Не удалось создать commands.txt: {e}")
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
            print(f"[Ошибка] Чтение commands.txt: {e}")
            continue

    print("[Внимание] Создаю новый файл команд")
    try:
        with open(commands_file, "w", encoding="utf-8") as f:
            for cmd, desc in default_commands.items():
                f.write(f"{cmd}\t| {desc}\n")
        return list(default_commands.items())
    except Exception as e:
        print(f"[Критично] Не удалось создать commands.txt: {e}")
        return [("help", "Показать справку"), ("exit", "Выход")]

def run_ai_editor():
    """Запуск графического редактора"""
    try:
        # Добавляем путь к модулям
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Scripts.Settings.settings import start_editor
        start_editor()
    except ImportError as e:
        print(f"[Ошибка] Не удалось импортировать редактор: {e}")
    except Exception as e:
        print(f"[Ошибка] Ошибка в работе редактора: {e}")

def main():
    """Основная функция программы"""
    initialize_environment()
    show_logo()

    if not hjcheck.check_password():
        return

    try:
        from System import catal
    except ImportError as e:
        print(f"[Ошибка] Не удалось загрузить модуль catal: {e}")
        catal = None

    commands = load_commands()

    while True:
        try:
            cmd = input("> ").strip().lower()
            if not cmd:
                continue

            if cmd == "help":
                print("\nДоступные команды:")
                max_len = max(len(c[0]) for c in commands)
                for c, d in commands:
                    print(f"  {c.ljust(max_len)} - {d}")

            elif cmd == "mods":
                hjcheck.list_mods()

            elif cmd == "catt" and catal:
                files = catal.get_mod_list()
                print("\nФайлы в catalyst:" if files else "\nПапка catalyst пуста")
                for f in sorted(files):
                    print(f"- {f}")


            elif cmd == "settings":

                try:

                    from Scripts.Settings.settings import start_editor

                    start_editor()

                except Exception as e:

                    print(f"[Ошибка] Не удалось запустить редактор: {e}")

            elif cmd == "exit":
                if catal and catal.process_mods():
                    print("\n[Система] Новые моды были установлены")

                if input("\nСохранить сессию перед выходом? (y/n): ").lower() == 'y':
                    crypto.save_session()
                    print("Сессия сохранена")

                if os.path.exists("System/catal.py"):
                    crypto.encrypt_file("System/catal.py", "System/catal.modhj")
                    print("Файл catal зашифрован")
                break

            elif cmd == "clear":
                os.system("cls" if os.name == "nt" else "clear")

            elif cmd == "backup":
                crypto.create_backup()

            elif cmd == "version":
                print("\nHatJab v1.0.5")
                print("Система управления модами с шифрованием")

            else:
                print(f"\nНеизвестная команда: {cmd}")
                print("Введите 'help' для списка команд")

        except KeyboardInterrupt:
            print("\nПрерывание (Ctrl+C)")
            if input("Завершить работу? (y/n): ").lower() == 'y':
                if os.path.exists("System/catal.py"):
                    crypto.encrypt_file("System/catal.py", "System/catal.modhj")
                break

        except Exception as e:
            print(f"\n[Ошибка] {e}")

if __name__ == "__main__":
    main()