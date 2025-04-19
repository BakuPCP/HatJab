import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path


class SettingsEditor:
    def __init__(self, master):
        self.master = master
        master.title("Settings")

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
        # Создаем основной фрейм
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Применяем текущую тему
        self.apply_theme(self.settings.get("theme", "dark"))

        # Вкладки
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка настроек
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self._setup_settings_tab()

        # Вкладка команд
        self.commands_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.commands_frame, text="Commands")
        self._setup_commands_tab()

        # Панель кнопок
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            self.button_frame,
            text="Save",
            command=self._save_all
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            self.button_frame,
            text="Cancel",
            command=self.master.destroy
        ).pack(side=tk.RIGHT, padx=5)

    def _setup_settings_tab(self):
        """Настройка вкладки с параметрами"""
        frame = ttk.LabelFrame(self.settings_frame, text="System parameters", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Тема
        ttk.Label(frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "dark"))
        theme_combobox = ttk.Combobox(
            frame,
            textvariable=self.theme_var,
            values=["light", "dark"],
            state="readonly",
            width=15
        )
        theme_combobox.grid(row=0, column=1, sticky=tk.W, pady=2)
        self.theme_var.trace_add('write', lambda *args: self.apply_theme(self.theme_var.get()))

        # Язык
        #ttk.Label(frame, text="Interface language:").grid(row=1, column=0, sticky=tk.W, pady=2)
        #self.lang_var = tk.StringVar(value=self.settings.get("language", "ru"))
        #ttk.Combobox(
         #   frame,
          #  textvariable=self.lang_var,
           # values=["ru", "en"],
            #state="readonly",
            #width=15
        #).grid(row=1, column=1, sticky=tk.W, pady=2)

        # Автосохранение
        self.autosave_var = tk.BooleanVar(value=self.settings.get("autosave", True))
        ttk.Checkbutton(
            frame,
            text="Autosave",
            variable=self.autosave_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)

        # Размер шрифта
        ttk.Label(frame, text="Font size:").grid(row=3, column=0, sticky=tk.W, pady=2)
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
        frame = ttk.LabelFrame(self.commands_frame, text="Commands list", padding="10")
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Текстовое поле для команд
        self.commands_text = tk.Text(frame, width=50, height=15, wrap=tk.WORD)
        self.commands_text.pack(fill=tk.BOTH, expand=True)

        # Заполняем команды
        for cmd in self.commands:
            self.commands_text.insert(tk.END, f"{cmd}\n")

        # Подсказка
        ttk.Label(frame, text="Form: command|description").pack(anchor=tk.W)

    def apply_theme(self, theme):
        """Применение цветовой темы ко всему интерфейсу"""
        if theme == "light":
            main_bg = "#E0E0E0"  # Пепельный (основной фон)
            frame_bg = "#C0C0C0"  # Чуть темнее для рамок
            fg_color = "#000000"  # Черный текст
            entry_bg = "#FFFFFF"  # Белый для полей ввода
        else:
            main_bg = "#424242"  # Темно-серый (основной фон)
            frame_bg = "#616161"  # Чуть светлее для рамок
            fg_color = "#FFFFFF"  # Белый текст
            entry_bg = "#303030"  # Темный для полей ввода

        # Настраиваем основной фон окна
        self.master.configure(bg=main_bg)

        # Создаем и настраиваем стили для ttk виджетов
        style = ttk.Style()
        style.theme_use('default')

        # Основные стили
        style.configure('.', background=main_bg, foreground=fg_color)
        style.configure('TFrame', background=main_bg)
        style.configure('TLabel', background=main_bg, foreground=fg_color)
        style.configure('TButton', background=main_bg, foreground=fg_color)
        style.configure('TCombobox', fieldbackground=entry_bg, foreground=fg_color)
        style.configure('TCheckbutton', background=main_bg, foreground=fg_color)
        style.configure('TLabelframe', background=frame_bg, foreground=fg_color)
        style.configure('TLabelframe.Label', background=frame_bg, foreground=fg_color)

        # Обновляем текстовые поля
        if hasattr(self, 'commands_text'):
            self.commands_text.configure(
                bg=entry_bg,
                fg=fg_color,
                insertbackground=fg_color,
                selectbackground=fg_color,
                selectforeground=entry_bg
            )

    def _load_settings(self):
        """Загрузка настроек из файла"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to install settings: {str(e)}")
                return {"theme": "dark","autosave": True, "font_size": 12}
        return {"theme": "dark","autosave": True, "font_size": 12}

    def _load_commands(self):
        """Загрузка команд из файла"""
        if self.commands_file.exists():
            try:
                with open(self.commands_file, "r", encoding="utf-8") as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to install commands: {str(e)}")
                return []
        return []

    def _save_all(self):
        """Сохранение всех изменений"""
        try:
            # Сохраняем настройки
            new_settings = {
                "theme": self.theme_var.get(),
                #"language": self.lang_var.get(),
                "autosave": self.autosave_var.get(),
                "font_size": self.font_var.get()
            }

            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(new_settings, f, indent=4, ensure_ascii=False)

            # Сохраняем команды
            commands = self.commands_text.get("1.0", tk.END).strip().split("\n")
            with open(self.commands_file, "w", encoding="utf-8") as f:
                f.write("\n".join([cmd.strip() for cmd in commands if cmd.strip()]))

            messagebox.showinfo("Save", "Settings saved successfully!")
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")


def start_editor():
    root = tk.Tk()
    editor = SettingsEditor(root)
    root.mainloop()


if __name__ == "__main__":
    start_editor()