import os
import sys
import io
from System import hjcheck, crypto
from core.environment import initialize_environment
from core.logo import show_logo
from core.main_loop import main_loop

# Настройка кодировки системы
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    """Основная функция программы"""
    initialize_environment()
    show_logo()

    if not hjcheck.check_password():
        return

    try:
        from System import catal
    except ImportError as e:
        print(f"[Error] Failed to load module catal: {e}")
        catal = None

    main_loop(catal)

if __name__ == "__main__":
    main()