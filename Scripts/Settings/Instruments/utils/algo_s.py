import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AlgorithmViewer:
    def __init__(self, editor):
        self.editor = editor
        self.window = None
        self.algo_color = "#2ca02c"  # Зеленый цвет для алгоритмов

    def show(self, node_name):
        """Простое окно с алгоритмами"""
        if self.window and tk.Toplevel.winfo_exists(self.window):
            self.window.destroy()

        self.window = tk.Toplevel(self.editor.master)
        self.window.title(f"Алгоритмы: {node_name}")

        # Примерные алгоритмы
        algorithms = ["Сортировка", "Поиск", "Оптимизация", "Анализ"]

        # Простой список
        for i, algo in enumerate(algorithms):
            ttk.Label(self.window, text=algo).pack(pady=2)

        # Кнопка визуализации
        ttk.Button(self.window, text="Показать граф",
                   command=lambda: self._show_algo_graph(node_name, algorithms)).pack(pady=10)

    def _show_algo_graph(self, node_name, algorithms):
        """Простая визуализация алгоритмов как узлов"""
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        # Создаем мини-граф
        G = nx.DiGraph()
        G.add_node(node_name, color=self.editor.node_color)

        for algo in algorithms:
            G.add_node(algo, color=self.algo_color)
            G.add_edge(node_name, algo)

        # Позиционирование
        pos = nx.spring_layout(G)

        # Рисуем
        colors = [G.nodes[n].get('color', '#1f78b4') for n in G.nodes()]
        nx.draw(G, pos, ax=ax, node_color=colors, with_labels=True)

        # Встраиваем в окно
        canvas = FigureCanvasTkAgg(fig, self.window)
        canvas.get_tk_widget().pack()
        canvas.draw()