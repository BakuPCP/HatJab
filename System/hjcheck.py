import os
import json
import bcrypt
import time
from System import crypto

MAX_ATTEMPTS = 3
COOLDOWN_TIME = 300  # 5 минут в секундах
LOCK_FILE = "Data/auth.lock"


def check_password():
    """Основная функция проверки пароля"""
    password_file = "Data/ps.dhj"
    backup_file = "Data/rep.dhj"

    # Проверка блокировки
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            lock_time = float(f.read())
        remaining = int(lock_time - time.time())
        if remaining > 0:
            print(
                f"\n[BLOCK] The system is temporarily locked. Please try again in {remaining // 60} min {remaining % 60} sec.")
            return False
        else:
            os.remove(LOCK_FILE)

    if not os.path.exists(password_file):
        return create_password()
    else:
        return verify_password()


def create_password():
    """Создание нового пароля"""
    print("\n[System] Creating a new password")
    while True:
        password = input("Enter new password: ")
        confirm = input("Confirm password: ")

        if password == confirm:
            if len(password) < 8:
                print("[Error] Password must be at least 8 characters")
                continue

            # Хеширование пароля перед шифрованием
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Шифрование и сохранение
            crypto.encrypt_data(hashed, "Data/ps.dhj")
            crypto.encrypt_data(hashed, "Data/rep.dhj")

            print("[Success] Password created successfully!")
            return True
        else:
            print("[Error] Miss. Try again.")


def check_file_encoding(filepath):
    """Проверка и исправление кодировки файла"""
    encodings = ['utf-8', 'cp1251', 'iso-8859-1']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                f.read()
            return enc
        except UnicodeDecodeError:
            continue
    return None


def verify_password():
    """Проверка существующего пароля"""
    attempts = MAX_ATTEMPTS

    while attempts > 0:
        password = input("\nEnter password: ")

        # Дешифровка хранимого пароля
        decrypted_data = crypto.decrypt_data("Data/ps.dhj")

        if decrypted_data is None:
            print("[Error] Decryption password failed. Try again.")
            attempts -= 1
            continue

        # Проверка пароля
        try:
            if bcrypt.checkpw(password.encode(), decrypted_data):
                print("[Success] Success!")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"[Error] Wrong password. Attempts: {attempts}")
                else:
                    activate_cooldown()
                    print("\n[BLOCK] Too much. System locked.")
        except Exception as e:
            print(f"[Ошибка] Password verification failed: {e}")
            attempts -= 1

    return False


def activate_cooldown():
    """Активирует временную блокировку системы"""
    unlock_time = time.time() + COOLDOWN_TIME
    with open(LOCK_FILE, "w") as f:
        f.write(str(unlock_time))
    os.chmod(LOCK_FILE, 0o600)


def list_mods():
    """Список активных модов"""
    mods_dir = "mods"
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir, exist_ok=True)

    active_mods = []
    for file in os.listdir(mods_dir):
        if file.endswith("_d.lhj"):
            mod_name = file.replace("_d.lhj", "")
            active_mods.append(mod_name)

    if active_mods:
        print("\nActive mods:")
        for mod in active_mods:
            print(f"- {mod}")
    else:
        print("\nNo active mods.")


def manage_settings():
    """Управление настройками"""
    settings_file = "Scripts/settings.cfg"

    # Загрузка или создание настроек
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            settings = json.load(f)
    else:
        settings = {
            "theme": "dark",
            "language": "ru",
            "autosave": True,
            "font_size": 12
        }

    # Отображение текущих настроек
    print("\nCurrent settings:")
    for key, value in settings.items():
        print(f"{key}: {value}")

    # Редактирование
    print("\nEditor (Press enter to skip):")
    for key in settings:
        new_value = input(f"{key} [{settings[key]}]: ")
        if new_value:
            try:
                # Автоматическое преобразование типов
                if new_value.lower() in ['true', 'false']:
                    settings[key] = new_value.lower() == 'true'
                elif new_value.isdigit():
                    settings[key] = int(new_value)
                else:
                    settings[key] = new_value
            except:
                settings[key] = new_value

    # Сохранение
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)
    print("\n[Success] Settings saved.")