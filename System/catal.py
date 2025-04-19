import os
import json
import shutil
from System import crypto

CATALYST_DIR = "catalyst"


def initialize():
    """Инициализация папки catalyst"""
    if not os.path.exists(CATALYST_DIR):
        os.makedirs(CATALYST_DIR)
        _create_example_mod()


def _create_example_mod():
    """Создает пример мода для демонстрации"""
    example_mod = {
        "name": "example_mod",
        "version": "1.0",
        "commands": {
            "test": "Mode example"
        }
    }

    # Файл данных мода
    with open(os.path.join(CATALYST_DIR, "example_mod_d.lhj"), "w") as f:
        json.dump(example_mod, f, indent=4)

    # Код мода
    with open(os.path.join(CATALYST_DIR, "example_mod.py"), "w") as f:
        f.write("""def cmd_test():\n    print("Test mode command!")\n""")


def get_mod_list():
    """Возвращает список файлов в папке catalyst"""
    if not os.path.exists(CATALYST_DIR):
        return []

    files = []
    for f in os.listdir(CATALYST_DIR):
        if f.endswith('.py') or f.endswith('_d.lhj'):
            files.append(f)
    return files


def process_mods():
    """Шифрует и перемещает моды в папку mods"""
    if not os.path.exists(CATALYST_DIR):
        return False

    processed = False
    for file in os.listdir(CATALYST_DIR):
        if file.endswith('.py'):
            mod_name = file.replace('.py', '')
            data_file = f"{mod_name}_d.lhj"
            data_path = os.path.join(CATALYST_DIR, data_file)

            if os.path.exists(data_path):
                # Шифруем код мода
                with open(os.path.join(CATALYST_DIR, file), "r") as f:
                    mod_code = f.read()
                crypto.encrypt_data(mod_code, f"mods/{mod_name}.modhj")

                # Перемещаем файл данных
                shutil.move(data_path, f"mods/{data_file}")

                # Удаляем исходный файл
                os.remove(os.path.join(CATALYST_DIR, file))
                processed = True
                print(f"[Catalyst] Mode {mod_name} installed")

    return processed


# Инициализация при импорте
initialize()