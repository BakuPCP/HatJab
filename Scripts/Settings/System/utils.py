import json
import os
from typing import Dict, Any

def save_positions(filepath: str, positions: Dict[str, Any]):
    """Сохранение позиций узлов в файл"""
    try:
        with open(filepath, 'w') as f:
            json.dump({k: list(v) for k, v in positions.items()}, f)
        return True
    except Exception as e:
        print(f"Error saving positions: {e}")
        return False

def load_positions(filepath: str) -> Dict[str, Any]:
    """Загрузка позиций узлов из файла"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return {k: tuple(v) for k, v in json.load(f).items()}
        except Exception as e:
            print(f"Error loading positions: {e}")
    return {}