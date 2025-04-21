import json
import os
from pathlib import Path
from typing import Dict, Any
import tkinter.messagebox as messagebox


class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.script_dir = Path(__file__).parent.parent
        self.settings_file = self.script_dir / "Scripts" / "settings.cfg"
        self.commands_file = self.script_dir / "Scripts" / "commands.txt"
        self.color_file = self.script_dir / "Scripts" / "color.cfg"

        # Загружаем настройки при инициализации
        self._settings = self._load_settings()
        self._commands = self._load_commands()
        self._color = self._load_color()

    @property
    def settings(self) -> Dict[str, Any]:
        """Возвращает текущие настройки"""
        return self._settings

    @property
    def commands(self) -> list:
        """Возвращает список команд"""
        return self._commands

    @property
    def color(self) -> str:
        """Возвращает текущий цвет текста"""
        return self._color

    @property
    def first_start_mode(self) -> str:
        """Возвращает режим первого запуска"""
        return self._settings.get("first_start", "console")

    def _load_settings(self) -> Dict[str, Any]:
        """Загружает настройки из файла"""
        default_settings = {
            "theme": "dark",
            "autosave": True,
            "autosave_interval": 5,
            "font_size": 12,
            "first_start": "console",
            "env_vars": {}
        }

        if not self.settings_file.exists():
            return default_settings

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                # Объединяем с настройками по умолчанию на случай, если в файле нет каких-то полей
                return {**default_settings, **loaded}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
            return default_settings

    def handle_env_vars(self, action: str, key: str = None, value: str = None) -> Any:
        """Обрабатывает операции с переменными окружения"""
        env_vars = self._settings.get("env_vars", {})

        if action == "list":
            return env_vars

        elif action == "get":
            return env_vars.get(key, "")

        elif action == "set":
            if not key:
                return False
            env_vars[key] = value
            self._settings["env_vars"] = env_vars
            return self.save_settings(self._settings)

        elif action == "unset":
            if key in env_vars:
                del env_vars[key]
                self._settings["env_vars"] = env_vars
                return self.save_settings(self._settings)
            return False

        return False

    def _load_commands(self) -> list:
        """Загружает команды из файла"""
        if not self.commands_file.exists():
            return []

        try:
            with open(self.commands_file, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load commands: {str(e)}")
            return []

    def _load_color(self) -> str:
        """Загружает цвет текста из файла"""
        if not self.color_file.exists():
            return "default"

        try:
            with open(self.color_file, "r", encoding="utf-8") as f:
                color = f.read().strip().lower()
                return color if color in ["green", "lightblue", "purple", "default"] else "default"
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load color settings: {str(e)}")
            return "default"

    def save_settings(self, new_settings: Dict[str, Any]) -> bool:
        """Сохраняет настройки в файл"""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(new_settings, f, indent=4, ensure_ascii=False)
            self._settings = new_settings
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            return False

    def save_commands(self, commands: list) -> bool:
        """Сохраняет команды в файл"""
        try:
            with open(self.commands_file, "w", encoding="utf-8") as f:
                f.write("\n".join([cmd.strip() for cmd in commands if cmd.strip()]))
            self._commands = commands
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save commands: {str(e)}")
            return False

    def save_color(self, color: str) -> bool:
        """Сохраняет цвет текста в файл"""
        if color not in ["green", "lightblue", "purple", "default"]:
            return False

        try:
            with open(self.color_file, "w", encoding="utf-8") as f:
                f.write(color)
            self._color = color
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save color: {str(e)}")
            return False

    def apply_theme(self, widget, theme: str):
        """Применяет тему к виджету"""
        if theme == "light":
            bg = "#E0E0E0"
            fg = "#000000"
            entry_bg = "#FFFFFF"
            frame_bg = "#C0C0C0"
        else:
            bg = "#424242"
            fg = "#FFFFFF"
            entry_bg = "#303030"
            frame_bg = "#616161"

        widget.configure(bg=bg)

        if hasattr(widget, 'children'):
            for child in widget.children.values():
                self.apply_theme(child, theme)

        # Специальные настройки для разных виджетов
        if isinstance(widget, tk.Text) or isinstance(widget, tk.Entry):
            widget.configure(bg=entry_bg, fg=fg, insertbackground=fg)
        elif isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
            widget.configure(bg=frame_bg)


# Создаем глобальный экземпляр менеджера настроек
settings_manager = SettingsManager()