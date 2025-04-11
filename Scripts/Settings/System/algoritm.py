import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
from typing import Dict, List


class AlgorithmVisualizer:
    def __init__(self, parent_frame):
        self.frame = ttk.Frame(parent_frame)
        self.algorithm_file = "Scripts/Settings/System/algorithm_data.json"
        self.algorithm_data = self._load_algorithm_data()

        self._setup_ui()

    def _load_algorithm_data(self) -> Dict:
        """Загрузка данных об алгоритмах"""
        default_data = {
            "startup": [
                "1. Инициализация окружения",
                "2. Загрузка конфигураций",
                "3. Проверка пароля",
                "4. Загрузка модулей"
            ],
            "command_processing": [
                "1. Получение команды",
                "2. Валидация ввода",
                "3. Поиск обработчика",
                "4. Выполнение",
                "5. Логирование"
            ],
            "mod_loading": [
                "1. Проверка подписи",
                "2. Верификация кода",
                "3. Загрузка в песочницу",
                "4. Регистрация команд"
            ]
        }

        if os.path.exists(self.algorithm_file):
            try:
                with open(self.algorithm_file, 'r') as f:
                    return json.load(f)
            except:
                return default_data
        return default_data

    def _save_algorithm_data(self):
        """Сохранение данных об алгоритмах"""
        with open(self.algorithm_file, 'w') as f:
            json.dump(self.algorithm_data, f, indent=4)

    def _setup_ui(self):
        """Настройка интерфейса вкладки"""
        # Основные элементы
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Создаем вкладки для каждого алгоритма
        self._create_tab("startup", "Запуск системы")
        self._create_tab("command_processing", "Обработка команд")
        self._create_tab("mod_loading", "Загрузка модов")

        # Кнопка сохранения
        ttk.Button(self.frame, text="Сохранить изменения",
                   command=self._save_algorithm_data).pack(pady=10)

    def _create_tab(self, algo_key: str, title: str):
        """Создание вкладки для конкретного алгоритма"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)

        # Текстовое поле с прокруткой
        text_area = scrolledtext.ScrolledText(tab, wrap=tk.WORD, width=60, height=15)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Заполняем данными
        text_area.insert(tk.END, "\n".join(self.algorithm_data[algo_key]))

        # Привязка события изменения
        text_area.bind("<FocusOut>", lambda e, k=algo_key: self._update_algorithm_data(k, text_area.get("1.0", tk.END)))

    def _update_algorithm_data(self, algo_key: str, text: str):
        """Обновление данных алгоритма"""
        steps = [step.strip() for step in text.split("\n") if step.strip()]
        self.algorithm_data[algo_key] = steps

    def get_frame(self):
        """Возвращает фрейм для встраивания"""
        return self.frame