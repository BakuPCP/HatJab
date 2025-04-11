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
                f"\n[Блокировка] Система временно заблокирована. Попробуйте через {remaining // 60} мин {remaining % 60} сек.")
            return False
        else:
            os.remove(LOCK_FILE)

    if not os.path.exists(password_file):
        return create_password()
    else:
        return verify_password()


def create_password():
    """Создание нового пароля"""
    print("\n[Система] Создание нового пароля")
    while True:
        password = input("Введите новый пароль: ")
        confirm = input("Подтвердите пароль: ")

        if password == confirm:
            if len(password) < 8:
                print("[Ошибка] Пароль должен содержать минимум 8 символов")
                continue

            # Хеширование пароля перед шифрованием
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            # Шифрование и сохранение
            crypto.encrypt_data(hashed, "Data/ps.dhj")
            crypto.encrypt_data(hashed, "Data/rep.dhj")

            print("[Успех] Пароль успешно создан!")
            return True
        else:
            print("[Ошибка] Пароли не совпадают. Попробуйте снова.")


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
        password = input("\nВведите пароль: ")

        # Дешифровка хранимого пароля
        decrypted_data = crypto.decrypt_data("Data/ps.dhj")

        if decrypted_data is None:
            print("[Ошибка] Не удалось дешифровать пароль. Попробуйте снова.")
            attempts -= 1
            continue

        # Проверка пароля
        try:
            if bcrypt.checkpw(password.encode(), decrypted_data):
                print("[Успех] Авторизация прошла успешно!")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"[Ошибка] Неверный пароль. Осталось попыток: {attempts}")
                else:
                    activate_cooldown()
                    print("\n[Блокировка] Превышено количество попыток. Система заблокирована на 5 минут.")
        except Exception as e:
            print(f"[Ошибка] Ошибка проверки пароля: {e}")
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
        print("\nАктивные моды:")
        for mod in active_mods:
            print(f"- {mod}")
    else:
        print("\nНет активных модов.")


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
    print("\nТекущие настройки:")
    for key, value in settings.items():
        print(f"{key}: {value}")

    # Редактирование
    print("\nРедактирование (оставьте пустым чтобы пропустить):")
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
    print("\n[Успех] Настройки сохранены.")