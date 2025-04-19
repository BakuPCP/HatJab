import os
import json
import shutil

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
            "test": "Пример команды мода"
        }
    }

    # Файл данных мода
    with open(os.path.join(CATALYST_DIR, "example_mod_d.lhj"), "w", encoding='utf-8') as f:
        json.dump(example_mod, f, indent=4, ensure_ascii=False)

    # Код мода
    with open(os.path.join(CATALYST_DIR, "example_mod.py"), "w", encoding='utf-8') as f:
        f.write("""def cmd_test():\n    print("Это тестовая команда из мода!")\n""")


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
    """Перемещает моды в папку mods без шифрования"""
    if not os.path.exists(CATALYST_DIR):
        return False

    processed = False
    for file in os.listdir(CATALYST_DIR):
        if file.endswith('.py'):
            mod_name = file.replace('.py', '')
            data_file = f"{mod_name}_d.lhj"
            data_path = os.path.join(CATALYST_DIR, data_file)

            if os.path.exists(data_path):
                # Копируем файлы мода
                shutil.copy2(
                    os.path.join(CATALYST_DIR, file),
                    os.path.join("mods", file)
                )

                # Перемещаем файл данных
                shutil.move(
                    data_path,
                    os.path.join("mods", data_file)
                )

                # Удаляем исходные файлы
                os.remove(os.path.join(CATALYST_DIR, file))
                processed = True
                print(f"[Catalyst] Мод {mod_name} установлен")

    return processed


# Инициализация при импорте
initialize()