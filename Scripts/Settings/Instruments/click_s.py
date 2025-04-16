import tkinter as tk
from tkinter import Menu
from .utils import algo_s
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # <-- Добавлен новый импорт
import matplotlib.pyplot as plt  # <-- Добавлен новый импорт
import networkx as nx  # <-- Добавлен новый импорт


class RightClickMenu:
    def __init__(self, editor):
        self.editor = editor
        self.selected_node = None
        self.algo_viewer = algo_s.AlgorithmViewer(editor)
        self.bind_events()

    def bind_events(self):
        """Привязка события правой кнопки мыши"""
        self.editor.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        """Обработчик кликов мыши"""
        if not event.inaxes or event.button != 3:  # 3 - правая кнопка мыши
            return

        # Проверяем клик по узлу
        self.selected_node = None
        for node, (x, y) in self.editor.graph_manager.pos.items():
            from .utils.nt_help import NodeTypeHelper
            width, height = NodeTypeHelper.calculate_dimensions(self.editor, self.editor.graph_manager.graph, node)

            if (x - width / 2 <= event.xdata <= x + width / 2 and
                    y - height / 2 <= event.ydata <= y + height / 2):
                self.selected_node = node
                break

        # Создаем контекстное меню только если клик был по узлу
        if self.selected_node and hasattr(event, 'guiEvent'):
            menu = Menu(self.editor.master, tearoff=0)
            menu.add_command(label="Свойства", command=self.show_properties)  # <-- Изменена команда
            menu.add_command(label="Алгоритмы",
                             command=lambda: self.algo_viewer.show(self.selected_node))  # <-- Оставил старый вариант
            menu.post(event.guiEvent.x_root, event.guiEvent.y_root)

    def show_properties(self):
        """Показывает окно свойств узла с визуализацией связей (НОВАЯ ВЕРСИЯ)"""
        if not self.selected_node:
            return

        # Создаем новое окно
        prop_window = tk.Toplevel(self.editor.master)
        prop_window.title(f"Свойства: {self.selected_node}")
        prop_window.geometry("800x600")

        # 1. Создаем подграф для отображения
        G = self.editor.graph_manager.graph
        # Включаем выбранный узел, его соседей и предшественников
        related_nodes = [self.selected_node]
        related_nodes += list(G.successors(self.selected_node))  # Исходящие связи
        related_nodes += list(G.predecessors(self.selected_node))  # Входящие связи
        subgraph = G.subgraph(related_nodes)

        # 2. Создаем графическое представление
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.set_axis_off()
        ax.set_title(f"Связи узла: {self.selected_node}", pad=20)

        # Позиционирование с учетом типа узла
        #pos = nx.spring_layout(subgraph, seed=42, k=0.5)
        pos = {node: self.editor.graph_manager.pos[node] for node in subgraph.nodes()}

        # 3. Рисуем связи
        nx.draw_networkx_edges(
            subgraph,
            pos,
            ax=ax,
            arrows=True,
            arrowstyle='->',
            width=1.5,
            edge_color='#666666'
        )

        # 4. Рисуем узлы как прямоугольники (как в основном редакторе)
        for node, (x, y) in pos.items():
            node_type = subgraph.nodes[node].get('type', 'file')

            # Определяем цвет и размер
            if node == self.selected_node:
                color = '#e31a1c'  # Красный для выбранного узла
                width, height = 0.25, 0.15  # Больший размер
            else:
                color = '#1f78b4'  # Синий для связанных узлов
                width, height = 0.2 * (0.7 if node_type == "file" else 1.0), \
                                0.1 * (0.7 if node_type == "file" else 1.0)

            # Рисуем прямоугольник
            rect = plt.Rectangle(
                (x - width / 2, y - height / 2),
                width, height,
                facecolor=color, alpha=0.7, edgecolor='black',
                linewidth=2 if node == self.selected_node else 1
            )
            ax.add_patch(rect)

            # Добавляем текст
            label = node.split('/')[-1] if node_type == "file" else node
            ax.text(
                x, y, label,
                ha='center', va='center',
                fontsize=9 if node_type == "file" else 11,
                color='white',
                weight='bold' if node == self.selected_node else 'normal'
            )

        # 5. Добавляем информационную панель
        info_frame = tk.Frame(prop_window)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Собираем статистику
        node_type = G.nodes[self.selected_node].get('type', 'unknown')
        in_degree = G.in_degree(self.selected_node)
        out_degree = G.out_degree(self.selected_node)

        # Отображаем информацию
        tk.Label(info_frame,
                 text=f"Тип: {'📁 Папка' if node_type == 'folder' else '📄 Файл'}",
                 font='Arial 10').pack(anchor='w')
        tk.Label(info_frame,
                 text=f"Входящие связи: {in_degree}",
                 font='Arial 10').pack(anchor='w')
        tk.Label(info_frame,
                 text=f"Исходящие связи: {out_degree}",
                 font='Arial 10').pack(anchor='w')

        # 6. Встраиваем график в окно
        canvas = FigureCanvasTkAgg(fig, prop_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 7. Добавляем кнопку закрытия
        btn_frame = tk.Frame(prop_window)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(
            btn_frame,
            text="Закрыть",
            command=prop_window.destroy,
            width=15
        ).pack(side=tk.RIGHT, padx=10)