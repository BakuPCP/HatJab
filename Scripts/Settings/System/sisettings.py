import tkinter as tk
from tkinter import ttk
import json
import os
from typing import Dict


class SISettingsEditor:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.settings_file = "Scripts/Settings/sisettings.json"
        self.settings = self._load_settings()

        self._setup_ui()

    def _load_settings(self) -> Dict:
        """Загрузка настроек из файла"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return {
            "autosave": True,
            "theme": "dark",
            "node_color": "#1f78b4",
            "font_size": 10
        }

    def _save_settings(self):
        """Сохранение настроек в файл"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def _setup_ui(self):
        """Настройка интерфейса вкладки"""
        # Настройки внешнего вида
        ttk.Label(self.frame, text="Настройки системы", font=('Helvetica', 12, 'bold')).grid(row=0, columnspan=2,
                                                                                             pady=10)

        # Автосохранение
        self.autosave_var = tk.BooleanVar(value=self.settings["autosave"])
        ttk.Checkbutton(self.frame, text="Автосохранение",
                        variable=self.autosave_var,
                        command=self._update_autosave).grid(row=1, column=0, sticky='w', padx=10)

        # Тема
        ttk.Label(self.frame, text="Тема интерфейса:").grid(row=2, column=0, sticky='w', padx=10)
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        themes = ttk.Combobox(self.frame, textvariable=self.theme_var,
                              values=["dark", "light", "system"])
        themes.grid(row=2, column=1, sticky='ew', padx=10)
        themes.bind("<<ComboboxSelected>>", self._update_theme)

        # Цвет узлов
        ttk.Label(self.frame, text="Цвет узлов:").grid(row=3, column=0, sticky='w', padx=10)
        self.color_var = tk.StringVar(value=self.settings["node_color"])
        ttk.Entry(self.frame, textvariable=self.color_var, width=10).grid(row=3, column=1, sticky='w', padx=10)

        # Размер шрифта
        ttk.Label(self.frame, text="Размер шрифта:").grid(row=4, column=0, sticky='w', padx=10)
        self.font_var = tk.IntVar(value=self.settings["font_size"])
        ttk.Spinbox(self.frame, from_=8, to=16, textvariable=self.font_var,
                    width=5, command=self._update_font).grid(row=4, column=1, sticky='w', padx=10)

        # Кнопка сохранения
        ttk.Button(self.frame, text="Применить все",
                   command=self._apply_all).grid(row=5, columnspan=2, pady=10)

    def _update_autosave(self):
        self.settings["autosave"] = self.autosave_var.get()
        self._save_settings()

    def _update_theme(self, event=None):
        self.settings["theme"] = self.theme_var.get()
        self._save_settings()

    def _update_font(self):
        self.settings["font_size"] = self.font_var.get()
        self._save_settings()

    def _apply_all(self):
        """Применение всех настроек"""
        self.settings.update({
            "autosave": self.autosave_var.get(),
            "theme": self.theme_var.get(),
            "node_color": self.color_var.get(),
            "font_size": self.font_var.get()
        })
        self._save_settings()
        tk.messagebox.showinfo("Успех", "Настройки применены!\nПерезапустите редактор для полного обновления.")

    def get_frame(self):
        """Возвращает фрейм для встраивания"""
        return self.frame