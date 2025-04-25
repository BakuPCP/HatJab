import importlib
import os
from core.settings_manager import settings_manager


class ModsManager:
    def __init__(self):
        self.mods_dir = "mods"
        self.available_mods = self._discover_mods()
        self.loaded_mods = {}

    def refresh_mods_list(self):
        """Обновляет список доступных модов"""
        self.available_mods = self._discover_mods()

    def _discover_mods(self):
        """Рекурсивно ищет моды во всех подпапках директории mods"""
        mods = {}
        if not os.path.exists(self.mods_dir):
            print(f"[ERROR] Папка модов не найдена: {self.mods_dir}")
            return mods

        for root, dirs, files in os.walk(self.mods_dir):
            # Пропускаем служебные папки
            dirs[:] = [d for d in dirs if not d.startswith('_')]

            for file in files:
                if file.endswith('.py') and not file.startswith('_'):
                    mod_name = file[:-3]  # Убираем .py
                    mod_path = os.path.join(root, file)

                    # Формируем имя мода с учетом подпапок (например: test.testmode)
                    rel_path = os.path.relpath(root, self.mods_dir)
                    if rel_path != '.':
                        mod_name = f"{rel_path.replace(os.sep, '.')}.{mod_name}"

                    mods[mod_name] = mod_path

        print(f"[DEBUG] Найдены моды: {mods}")  # Для отладки
        return mods

    def load_mod(self, mod_name):
        """Загружает указанный мод с учетом подпапок"""
        if mod_name not in self.available_mods:
            print(f"[Mod Error] Мод '{mod_name}' не найден")
            return False

        try:
            # Преобразуем путь в python-импорт (заменяем \ на .)
            import_name = f"mods.{mod_name.replace(os.sep, '.')}"
            mod = importlib.import_module(import_name)
            self.loaded_mods[mod_name] = mod
            return True
        except Exception as e:
            print(f"[Mod Error] Ошибка загрузки мода '{mod_name}': {e}")
            return False

    def execute_mod_command(self, cmd):
        """Обрабатывает команду мода (формат: 'modname:args')"""
        if ':' not in cmd:
            print("[Mod Error] Неверный формат команды. Используйте: modname:command")
            return None

        mod_name, command = cmd.split(':', 1)

        if mod_name not in self.available_mods:
            print(f"[Mod Error] Мод '{mod_name}' не найден")
            return None

        if mod_name not in self.loaded_mods:
            if not self.load_mod(mod_name):
                return None

        try:
            if hasattr(self.loaded_mods[mod_name], 'execute'):
                # Передаем команду как строку и возвращаем результат
                return self.loaded_mods[mod_name].execute(command)
            else:
                print(f"[Mod Error] Мод '{mod_name}' не имеет функции execute()")
                return None
        except Exception as e:
            print(f"[Mod Error] Ошибка выполнения мода '{mod_name}': {e}")
            return None

    def get_available_mods(self):
        """Возвращает список доступных модов с их расположением"""
        mods_list = []
        for mod_name, mod_path in self.available_mods.items():
            mods_list.append({
                'name': mod_name,
                'path': mod_path,
                'loaded': mod_name in self.loaded_mods
            })
        return mods_list


# Глобальный экземпляр менеджера модов
mods_manager = ModsManager()