import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend
import shutil
from datetime import datetime

# Глобальные переменные для ключей
RSA_PRIVATE_KEY = None
RSA_PUBLIC_KEY = None


def generate_rsa_keys():
    """Генерация и сохранение RSA ключей"""
    global RSA_PRIVATE_KEY, RSA_PUBLIC_KEY

    key_file = "Data/rsa_keys.keyhj"
    try:
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                RSA_PRIVATE_KEY = serialization.load_pem_private_key(
                    f.read(), password=None, backend=default_backend())
                RSA_PUBLIC_KEY = RSA_PRIVATE_KEY.public_key()
        else:
            RSA_PRIVATE_KEY = rsa.generate_private_key(
                public_exponent=65537, key_size=2048, backend=default_backend())
            RSA_PUBLIC_KEY = RSA_PRIVATE_KEY.public_key()

            with open(key_file, "wb") as f:
                f.write(RSA_PRIVATE_KEY.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            os.chmod(key_file, 0o600)
    except Exception as e:
        print(f"[CRITICAL] Key generation error: {e}")
        raise


def encrypt_data(data, output_file):
    """Шифрование данных с использованием RSA+AES"""
    if not isinstance(data, bytes):
        data = str(data).encode('utf-8')

    if RSA_PRIVATE_KEY is None:
        generate_rsa_keys()

    try:
        # Генерация AES ключа
        aes_key = os.urandom(32)
        iv = os.urandom(16)

        # Шифрование данных
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        encrypted = encryptor.update(padder.update(data) + padder.finalize()) + encryptor.finalize()

        # Шифрование ключа
        encrypted_key = RSA_PUBLIC_KEY.encrypt(
            aes_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Сохранение
        with open(output_file, "wb") as f:
            f.write(base64.b64encode(encrypted_key) + b"\n")
            f.write(base64.b64encode(iv) + b"\n")
            f.write(base64.b64encode(encrypted))
        os.chmod(output_file, 0o600)
        return True
    except Exception as e:
        print(f"[Error] Encryption failed: {e}")
        return False


def decrypt_data(input_file, output_file=None):
    """Дешифрование данных"""
    if RSA_PRIVATE_KEY is None:
        generate_rsa_keys()

    try:
        with open(input_file, "rb") as f:
            encrypted_key = base64.b64decode(f.readline().strip())
            iv = base64.b64decode(f.readline().strip())
            encrypted = base64.b64decode(f.readline().strip())

        # Расшифровка ключа
        aes_key = RSA_PRIVATE_KEY.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Расшифровка данных
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(decryptor.update(encrypted) + decryptor.finalize()) + unpadder.finalize()

        if output_file:
            with open(output_file, "wb") as f:
                f.write(data)
            os.chmod(output_file, 0o600)
            return True
        return data
    except Exception as e:
        print(f"[Error] Decryption failed: {e}")
        return None


def encrypt_file(src, dst):
    """Шифрование файла"""
    try:
        with open(src, "rb") as f:
            data = f.read()
        if encrypt_data(data, dst):
            os.remove(src)
            return True
        return False
    except Exception as e:
        print(f"[Error] Encryption files failed: {e}")
        return False


def decrypt_to_file(src, dst):
    """Дешифрование в файл"""
    data = decrypt_data(src)
    if data:
        try:
            with open(dst, "wb") as f:
                f.write(data)
            os.chmod(dst, 0o600)
            return True
        except Exception as e:
            print(f"[Error] Decryption files failed: {e}")
    return False


def save_session():
    """Сохранение сессии"""
    session = {
        "mods": [],
        "settings": {},
        "history": []
    }
    if not encrypt_data(json.dumps(session), "Data/session.seshj"):
        print("[Error] Failed to save session")


def create_backup():
    """Создание резервной копии"""
    backup_dir = "Backups"
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"

    try:
        # Важные файлы для резервирования
        important_files = [
            "Data/ps.dhj",
            "Data/rep.dhj",
            "Data/session.seshj",
            "Data/rsa_keys.keyhj",
            "Scripts/commands.txt",
            "Scripts/settings.cfg"
        ]

        # Создаем временную папку
        temp_dir = f"temp_backup_{timestamp}"
        os.makedirs(temp_dir, exist_ok=True)

        # Копируем файлы
        for file in important_files:
            if os.path.exists(file):
                shutil.copy2(file, os.path.join(temp_dir, os.path.basename(file)))

        # Создаем архив
        shutil.make_archive(os.path.join(backup_dir, backup_name), "zip", temp_dir)
        shutil.rmtree(temp_dir)

        print(f"\n[Success] Backup {backup_name}.zip created")
        return True
    except Exception as e:
        print(f"\n[Error] Backup creation failed: {e}")
        return False


# Инициализация ключей при запуске
generate_rsa_keys()