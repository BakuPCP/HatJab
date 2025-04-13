import tkinter as tk
from tkinter import messagebox


class DebugHelper:
    def __init__(self, editor):
        self.editor = editor
        self.debug_window = None
       # self._setup_debug_tools()

    #def _setup_debug_tools(self):
       # """Добавляет кнопку отладки в интерфейс"""
        #debug_btn = tk.Button(
         #   self.editor.toolbar_frame,
          #  text="Debug",
           # command=self.toggle_debug
        #)
        #debug_btn.pack(side=tk.LEFT, padx=5)

    def toggle_debug(self):
        """Переключает окно отладки"""
        if self.debug_window and tk.Toplevel.winfo_exists(self.debug_window):
            self.debug_window.destroy()
            self.debug_window = None
        else:
            self.show_debug_info()

    def show_debug_info(self):
        """Показывает информацию для отладки"""
        self.debug_window = tk.Toplevel(self.editor.master)
        self.debug_window.title("Debug Info")

        # Основная информация
        tk.Label(self.debug_window, text="Current State:", font='Arial 10 bold').pack(pady=5)

        # Информация о графе
        graph_info = f"Nodes: {len(self.editor.graph_manager.graph.nodes)}\n" \
                     f"Edges: {len(self.editor.graph_manager.graph.edges)}"
        tk.Label(self.debug_window, text=graph_info).pack(pady=5)

        # Кнопка для дампа данных
        tk.Button(
            self.debug_window,
            text="Dump Graph Data",
            command=self.dump_graph_data
        ).pack(pady=10)

    def dump_graph_data(self):
        """Выводит полные данные графа"""
        data = {
            "nodes": list(self.editor.graph_manager.graph.nodes(data=True)),
            "edges": list(self.editor.graph_manager.graph.edges()),
            "positions": dict(self.editor.graph_manager.pos)
        }
        messagebox.showinfo("Graph Data", str(data))