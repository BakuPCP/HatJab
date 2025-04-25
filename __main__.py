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

    # Загрузка сохраненного цвета текста
    try:
        if os.path.exists("Scripts/color.cfg"):
            with open("Scripts/color.cfg", "r") as f:
                color = f.read().strip()
                colors = {
                    'green': '\033[92m',
                    'lightblue': '\033[94m',
                    'purple': '\033[95m',
                    'default': '\033[0m'
                }
                if color in colors:
                    print(colors[color], end='')
    except Exception as e:
        print(f"[Error] Failed to load color settings: {e}")
    show_logo()

    if not hjcheck.check_password():
        return

    # Запуск основного цикла без передачи catal
    main_loop()

if __name__ == "__main__":
    main()