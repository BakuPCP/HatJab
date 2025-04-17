import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path


class SettingsEditor:
    def __init__(self, master):
        self.master = master
        master.title("Настройки")

        # Пути к файлам конфигурации
        self.script_dir = Path(__file__).parent
        self.settings_file = self.script_dir / "settings.cfg"
        self.commands_file = self.script_dir / "commands.txt"

        # Загрузка текущих настроек
        self.settings = self._load_settings()
        self.commands = self._load_commands()

        # Инициализация интерфейса
        self._setup_ui()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Вкладки
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка настроек
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Настройки")
        self._setup_settings_tab()

        # Вкладка команд
        self.commands_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.commands_frame, text="Команды")
        self._setup_commands_tab()

        # Панель кнопок
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            self.button_frame,
            text="Сохранить",
            command=self._save_all
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            self.button_frame,
            text="Отмена",
            command=self.master.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _setup_settings_tab(self):
        """Настройка вкладки с параметрами"""
        frame = ttk.LabelFrame(self.settings_frame, text="Параметры системы", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Тема
        ttk.Label(frame, text="Тема оформления:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "dark"))
        ttk.Combobox(
            frame,
            textvariable=self.theme_var,
            values=["light", "dark", "system"],
            state="readonly",
            width=15
        ).grid(row=0, column=1, sticky=tk.W, pady=2)

        # Язык
        ttk.Label(frame, text="Язык интерфейса:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.lang_var = tk.StringVar(value=self.settings.get("language", "ru"))
        ttk.Combobox(
            frame,
            textvariable=self.lang_var,
            values=["ru", "en"],
            state="readonly",
            width=15
        ).grid(row=1, column=1, sticky=tk.W, pady=2)

        # Автосохранение
        self.autosave_var = tk.BooleanVar(value=self.settings.get("autosave", True))
        ttk.Checkbutton(
            frame,
            text="Автосохранение",
            variable=self.autosave_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Размер шрифта
        ttk.Label(frame, text="Размер шрифта:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.font_var = tk.IntVar(value=self.settings.get("font_size", 12))
        ttk.Spinbox(
            frame,
            from_=8,
            to=24,
            textvariable=self.font_var,
            width=5
        ).grid(row=3, column=1, sticky=tk.W, pady=2)

    def _setup_commands_tab(self):
        """Настройка вкладки с командами"""
        frame = ttk.LabelFrame(self.commands_frame, text="Список команд", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Текстовое поле для команд
        self.commands_text = tk.Text(frame, width=50, height=15, wrap=tk.WORD)
        self.commands_text.pack(fill=tk.BOTH, expand=True)

        # Заполняем команды
        for cmd in self.commands:
            self.commands_text.insert(tk.END, f"{cmd}\n")

        # Подсказка
        ttk.Label(frame, text="Формат: команда|описание").pack(anchor=tk.W)

    def _load_settings(self):
        """Загрузка настроек из файла"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить настройки: {str(e)}")
                return {}
        return {}

    def _load_commands(self):
        """Загрузка команд из файла"""
        if self.commands_file.exists():
            try:
                with open(self.commands_file, "r", encoding="utf-8") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить команды: {str(e)}")
                return []
        return []

    def _save_all(self):
        """Сохранение всех изменений"""
        try:
            # Сохраняем настройки
            new_settings = {
                "theme": self.theme_var.get(),
                "language": self.lang_var.get(),
                "autosave": self.autosave_var.get(),
                "font_size": self.font_var.get()
            }

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(new_settings, f, indent=4, ensure_ascii=False)

            # Сохраняем команды
            commands = self.commands_text.get("1.0", tk.END).strip().split("\n")
            with open(self.commands_file, "w", encoding="utf-8") as f:
                f.write("\n".join([cmd.strip() for cmd in commands if cmd.strip()]))

            messagebox.showinfo("Сохранение", "Настройки успешно сохранены!")
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {str(e)}")


def start_editor():
    root = tk.Tk()
    editor = SettingsEditor(root)
    root.mainloop()


if __name__ == "__main__":
    start_editor()