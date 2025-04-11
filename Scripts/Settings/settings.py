import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import networkx as nx
import os
import json
from typing import Dict, List, Optional
from .System.sisettings import SISettingsEditor


class AIGraphEditor:
    def __init__(self, master):
        self.master = master
        master.title("HatJab Advanced Editor")

        # Инициализация состояния
        self.graph = nx.DiGraph()
        self.pos = {}
        self.dragged_node = None
        self.selected_node = None
        self.node_files = {}
        self._init_graph()
        self._scan_files()

        # Настройки отображения
        self.node_width = 0.15
        self.node_height = 0.1
        self.font_size = 10
        self.node_color = "#1f78b4"
        self.selected_color = "#e31a1c"

        # Создание интерфейса
        self._setup_main_ui()
        self._setup_graph_tab()
        self._setup_settings_tab()
        self._bind_events()

        # Первоначальная отрисовка
        self._draw_graph()
        self._update_info()

    def _setup_main_ui(self):
        """Создание основного интерфейса с вкладками"""
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка графа
        self.graph_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_tab, text="System Graph")

        # Вкладка настроек
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="SI Settings")

    def _setup_graph_tab(self):
        """Настройка вкладки с графом"""
        # Основные фреймы
        self.main_frame = ttk.Frame(self.graph_tab)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = ttk.Frame(self.main_frame)
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Node Contents")
        self.control_frame = ttk.Frame(self.main_frame, width=250)

        self.graph_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.info_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        self.control_frame.grid(row=0, column=2, sticky="ns", padx=5, pady=5)

        self.main_frame.columnconfigure(0, weight=1)

        # Графическая область
        self.figure = plt.figure(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Информационная панель
        self.info_text = tk.Text(self.info_frame, width=30, height=15)
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Панель управления
        ttk.Button(self.control_frame, text="Refresh",
                   command=self._update_display).pack(pady=5, fill=tk.X)
        ttk.Button(self.control_frame, text="Add Node",
                   command=self._add_node_dialog).pack(pady=5, fill=tk.X)
        ttk.Button(self.control_frame, text="Delete Node",
                   command=self._delete_node).pack(pady=5, fill=tk.X)
        ttk.Button(self.control_frame, text="Reset Layout",
                   command=self._reset_layout).pack(pady=5, fill=tk.X)

    def _setup_settings_tab(self):
        """Настройка вкладки с SI Settings"""
        self.si_editor = SISettingsEditor(self.settings_tab)
        self.si_editor.get_frame().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _init_graph(self):
        """Инициализация графа системы"""
        components = [
            "System", "mods", "catalyst", "Scripts",
            "Data", "main", "config"
        ]
        for comp in components:
            self.graph.add_node(comp, type="folder", locked=False)

        edges = [
            ("main", "System"), ("main", "mods"),
            ("main", "Scripts"), ("System", "catalyst"),
            ("Scripts", "Data"), ("config", "main")
        ]
        self.graph.add_edges_from(edges)
        self.pos = nx.spring_layout(self.graph, k=1.5, seed=42)

    def _scan_files(self):
        """Сканирование файлов для каждого узла"""
        self.node_files = {
            "System": ["__init__.py", "crypto.py", "hjcheck.py", "catal.py"],
            "mods": ["example_mod.modhj", "weather_mod.modhj"],
            "catalyst": ["new_mod.py", "mod_config.lhj"],
            "Scripts": ["commands.txt", "settings.cfg"],
            "Data": ["rsa_keys.keyhj", "session.seshj"],
            "main": ["main.py"],
            "config": ["config.ini"]
        }

    def _draw_graph(self):
        """Отрисовка графа с квадратными узлами"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_axis_off()

        # Рисуем связи
        nx.draw_networkx_edges(
            self.graph, self.pos, ax=ax,
            arrows=True, arrowstyle='->', width=1.5
        )

        # Рисуем квадратные узлы
        for node, (x, y) in self.pos.items():
            color = self.node_color if node != self.selected_node else self.selected_color
            rect = Rectangle(
                (x - self.node_width / 2, y - self.node_height / 2),
                self.node_width, self.node_height,
                facecolor=color, alpha=0.7, edgecolor='black'
            )
            ax.add_patch(rect)

            # Текст узла
            ax.text(x, y, node,
                    ha='center', va='center',
                    fontsize=self.font_size, color='white')

        self.canvas.draw()

    def _update_info(self):
        """Обновление информационной панели"""
        self.info_text.delete(1.0, tk.END)
        if self.selected_node:
            files = self.node_files.get(self.selected_node, [])
            self.info_text.insert(tk.END, f"Node: {self.selected_node}\n\nFiles:\n")
            for file in files:
                self.info_text.insert(tk.END, f"- {file}\n")
        else:
            self.info_text.insert(tk.END, "Select a node to view contents")

    def _bind_events(self):
        """Привязка обработчиков событий"""
        self.canvas.mpl_connect('button_press_event', self._on_press)
        self.canvas.mpl_connect('motion_notify_event', self._on_drag)
        self.canvas.mpl_connect('button_release_event', self._on_release)
        self.master.bind("<Button-3>", self._on_right_click)
        self.master.bind("<Control-s>", lambda e: self._save_settings())

    def _on_press(self, event):
        """Обработчик нажатия ЛКМ"""
        if event.inaxes and event.button == 1:
            for node, (x, y) in self.pos.items():
                if (abs(x - event.xdata) < self.node_width / 2 and
                        abs(y - event.ydata) < self.node_height / 2):
                    if not self.graph.nodes[node].get('locked', False):
                        self.dragged_node = node
                    self.selected_node = node
                    self._draw_graph()
                    self._update_info()
                    break

    def _on_drag(self, event):
        """Обработчик перемещения мыши"""
        if self.dragged_node and event.inaxes:
            self.pos[self.dragged_node] = (event.xdata, event.ydata)
            self._draw_graph()

    def _on_release(self, event):
        """Обработчик отпускания ЛКМ"""
        self.dragged_node = None

    def _on_right_click(self, event):
        """Обработчик ПКМ"""
        if self.selected_node:
            menu = tk.Menu(self.master, tearoff=0)
            menu.add_command(label="Show Files", command=self._show_files)
            menu.add_command(label="Add File", command=self._add_file_dialog)
            menu.add_separator()
            menu.add_command(label="Lock Node", command=self._toggle_lock)
            menu.post(event.x_root, event.y_root)

    def _show_files(self):
        """Показать файлы узла"""
        if self.selected_node:
            files = self.node_files.get(self.selected_node, [])
            message = "\n".join(files) if files else "No files"
            messagebox.showinfo(
                f"Files in {self.selected_node}",
                message
            )

    def _add_file_dialog(self):
        """Диалог добавления файла"""
        if not self.selected_node:
            return

        dialog = tk.Toplevel(self.master)
        dialog.title(f"Add file to {self.selected_node}")

        ttk.Label(dialog, text="Filename:").pack(pady=5)
        entry = ttk.Entry(dialog, width=30)
        entry.pack(pady=5)

        def add_file():
            filename = entry.get()
            if filename:
                if self.selected_node not in self.node_files:
                    self.node_files[self.selected_node] = []
                self.node_files[self.selected_node].append(filename)
                self._update_info()
                dialog.destroy()

        ttk.Button(dialog, text="Add", command=add_file).pack(pady=5)

    def _update_display(self):
        """Обновить отображение"""
        self._draw_graph()
        self._update_info()

    def _add_node_dialog(self):
        """Диалог добавления узла"""
        dialog = tk.Toplevel(self.master)
        dialog.title("Add Node")

        ttk.Label(dialog, text="Node Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(dialog, text="Type:").grid(row=1, column=0, padx=5, pady=5)
        type_var = tk.StringVar(value="folder")
        ttk.Combobox(dialog, textvariable=type_var,
                     values=["folder", "module", "config"]).grid(row=1, column=1, padx=5, pady=5)

        def add_node():
            name = name_entry.get()
            if name and name not in self.graph.nodes:
                self.graph.add_node(name, type=type_var.get(), locked=False)
                self.pos[name] = (0, 0)
                self.node_files[name] = []
                self._update_display()
                dialog.destroy()

        ttk.Button(dialog, text="Add", command=add_node).grid(row=2, columnspan=2, pady=5)

    def _delete_node(self):
        """Удалить выбранный узел"""
        if self.selected_node and self.selected_node not in ['main', 'System']:
            if messagebox.askyesno("Confirm", f"Delete node '{self.selected_node}'?"):
                self.graph.remove_node(self.selected_node)
                if self.selected_node in self.node_files:
                    del self.node_files[self.selected_node]
                self.selected_node = None
                self._update_display()

    def _toggle_lock(self):
        """Закрепить/открепить узел"""
        if self.selected_node:
            locked = not self.graph.nodes[self.selected_node].get('locked', False)
            self.graph.nodes[self.selected_node]['locked'] = locked
            if locked:
                self.dragged_node = None
            messagebox.showinfo("Info", f"Node {'locked' if locked else 'unlocked'}")

    def _reset_layout(self):
        """Сбросить расположение узлов"""
        self.pos = nx.spring_layout(self.graph, k=1.5)
        self._draw_graph()

    def _save_settings(self):
        """Сохранение всех настроек"""
        self.si_editor._apply_all()
        messagebox.showinfo("Success", "All settings saved")


def start_editor():
    """Запуск редактора"""
    root = tk.Tk()
    editor = AIGraphEditor(root)
    root.mainloop()


if __name__ == "__main__":
    start_editor()