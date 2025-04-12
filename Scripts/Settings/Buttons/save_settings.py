import json
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk


class SaveSettingsButton:
    def __init__(self, master, editor):
        self.master = master  # Родительский фрейм для кнопки
        self.editor = editor  # Ссылка на главный редактор

    def create_button(self):
        """Создает и возвращает кнопку сохранения"""
        btn = ttk.Button(
            self.master,
            text="Save",
            command=self._save_settings
        )
        btn.pack(side=tk.LEFT, padx=5)
        return btn

    def _save_settings(self):
        """Сохраняет текущее состояние графа"""
        try:
            data = {
                "nodes": list(self.editor.graph.nodes(data=True)),
                "edges": list(self.editor.graph.edges()),
                "positions": {k: list(v) for k, v in self.editor.pos.items()}
            }

            with open("graph_settings.json", "w") as f:
                json.dump(data, f, indent=2)

            messagebox.showinfo("Success", "Graph settings saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            return False