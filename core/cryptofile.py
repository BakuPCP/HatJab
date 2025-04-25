import os
from cryptography.fernet import Fernet
from core.settings_manager import settings_manager


class CryptoFile:
    def __init__(self):
        self.key_file = os.path.join("Scripts", "crypto.key")
        self._ensure_key_exists()

    def _ensure_key_exists(self):
        """Проверяет наличие ключа шифрования, создает новый если нет"""
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)

    def _get_key(self):
        """Загружает ключ шифрования"""
        with open(self.key_file, 'rb') as f:
            return f.read()

    def encrypt_file(self, file_path):
        """Шифрует файл"""
        try:
            key = self._get_key()
            fernet = Fernet(key)

            with open(file_path, 'rb') as f:
                original = f.read()

            encrypted = fernet.encrypt(original)

            with open(file_path + '.enc', 'wb') as f:
                f.write(encrypted)

            os.remove(file_path)
            return True
        except Exception as e:
            print(f"[Error] Encryption failed: {e}")
            return False

    def decrypt_file(self, file_path):
        """Дешифрует файл"""
        try:
            if not file_path.endswith('.enc'):
                print("[Error] File must have .enc extension")
                return False

            key = self._get_key()
            fernet = Fernet(key)

            with open(file_path, 'rb') as f:
                encrypted = f.read()

            decrypted = fernet.decrypt(encrypted)

            output_path = file_path[:-4]  # Удаляем .enc
            with open(output_path, 'wb') as f:
                f.write(decrypted)

            os.remove(file_path)
            return True
        except Exception as e:
            print(f"[Error] Decryption failed: {e}")
            return False


# Глобальный экземпляр для использования в других модулях
crypto_file = CryptoFile()