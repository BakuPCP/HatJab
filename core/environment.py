import os

def initialize_environment():
    """Инициализация окружения"""
    required_dirs = ["System", "mods", "Scripts", "Data"]
    for folder in required_dirs:
        os.makedirs(folder, exist_ok=True)