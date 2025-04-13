import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from .Instruments.move import NodeMover
from .Instruments.highlight import MultiHighlighter
from .Instruments.utils.graph_manager import GraphManager


class FileNodeEditor:
    def __init__(self, master):
        self.master = master
        master.title("File Node Editor")

        # 1. Инициализация менеджера графа
        self.graph_manager = GraphManager()
        self.graph = self.graph_manager.graph  # Алиас для удобства
        self.pos = self.graph_manager.pos

        # 2. Инициализация фреймов
        self._init_frames()

        # 3. Настройки отображения
        self.node_width = 0.2
        self.node_height = 0.1
        self.font_size = 10
        self.node_color = "#1f78b4"
        self.selected_color = "#e31a1c"

        # 4. Инициализация графа
        self.graph_manager.init_default_graph()

        # 5. Инициализация элементов интерфейса
        self._init_buttons()
        self._draw_graph()

        # 6. Инициализация инструментов
        from .Instruments.move import NodeMover
        from .Instruments.highlight import MultiHighlighter
        self.mover = NodeMover(self)
        self.highlighter = MultiHighlighter(self)

    def _init_frames(self):
        """Инициализация всех фреймов интерфейса"""
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Панель инструментов (теперь создается в первую очередь)
        self.toolbar_frame = ttk.Frame(self.main_frame)
        self.toolbar_frame.pack(fill=tk.X, pady=5)

        # Графическая область
        self.figure = plt.figure(figsize=(10, 8))
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



        self.highlighter = MultiHighlighter(self)

    def _init_buttons(self):
        """Инициализация кнопок"""
        from .Buttons.save_settings import SaveSettingsButton
        self.save_button = SaveSettingsButton(self.toolbar_frame, self)
        self.save_button.create_button()

    def _init_graph(self):
        """Инициализация базовой структуры"""
        # Основные узлы
        main_nodes = ["System", "mods", "Scripts", "Data", "main"]
        for node in main_nodes:
            self.graph.add_node(node, type="folder")

        # Файлы как узлы
        file_nodes = {
            "System": ["crypto.py", "hjcheck.py"],
            "mods": ["example.mod", "weather.mod"],
            "Scripts": ["commands.txt", "settings.cfg"],
            "Data": ["keys.dat", "session.ses"],
            "main": ["main.py"]
        }

        # Добавляем файлы и связи
        for parent, files in file_nodes.items():
            for file in files:
                self.graph.add_node(f"{parent}/{file}", type="file")
                self.graph.add_edge(parent, f"{parent}/{file}")

        # Основные связи между папками
        self.graph.add_edges_from([
            ("main", "System"), ("main", "mods"),
            ("main", "Scripts"), ("Scripts", "Data")
        ])

        # Позиционирование
        self.pos = nx.spring_layout(self.graph, k=0.5, seed=42)

    def _setup_ui(self):




        """Настройка интерфейса"""
        # Основной фрейм
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Панель кнопок сверху
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)

        # Добавляем кнопку сохранения
        self.save_button = SaveSettingsButton(self.toolbar_frame, self)
        self.save_button.create_button()

        # Графическая область
        self.figure = plt.figure(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Панель управления
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=5)

        ttk.Button(self.control_frame, text="Refresh", command=self._draw_graph).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="Reset Layout", command=self._reset_layout).pack(side=tk.LEFT)

        # Привязка событий
        self.canvas.mpl_connect('button_press_event', self._on_press)
        self.canvas.mpl_connect('motion_notify_event', self._on_drag)
        self.canvas.mpl_connect('button_release_event', self._on_release)

    def _draw_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_axis_off()

        # Используем graph_manager вместо прямого доступа
        nx.draw_networkx_edges(
            self.graph_manager.graph,  # Изменено здесь
            self.graph_manager.pos,  # И здесь
            ax=ax,
            arrows=True,
            arrowstyle='->',
            width=1.5
        )

        for node, (x, y) in self.graph_manager.pos.items():  # Изменено здесь
            node_type = self.graph_manager.graph.nodes[node].get('type', 'file')  # И здесь
            color = self.graph_manager.graph.nodes[node].get('color', self.node_color)  # И здесь

            width = self.node_width * (0.7 if node_type == "file" else 1.0)
            height = self.node_height * (0.7 if node_type == "file" else 1.0)

            rect = Rectangle(
                (x - width / 2, y - height / 2),
                width, height,
                facecolor=color, alpha=0.7, edgecolor='black'
            )
            ax.add_patch(rect)

            label = node.split('/')[-1] if node_type == "file" else node
            ax.text(x, y, label, ha='center', va='center',
                    fontsize=self.font_size - 2 if node_type == "file" else self.font_size,
                    color='white')

        self.canvas.draw()

    def _on_press(self, event):
        """Обработчик нажатия мыши"""
        if event.inaxes and event.button == 1:
            for node, (x, y) in self.pos.items():
                width = self.node_width * (0.7 if self.graph.nodes[node].get('type') == "file" else 1.0)
                height = self.node_height * (0.7 if self.graph.nodes[node].get('type') == "file" else 1.0)

                if (abs(x - event.xdata) < width / 2 and abs(y - event.ydata) < height / 2):
                    self.selected_node = node
                    self.dragged_node = node
                    self._draw_graph()
                    break

    def _on_drag(self, event):
        """Обработчик перемещения мыши"""
        if self.dragged_node and event.inaxes:
            self.pos[self.dragged_node] = (event.xdata, event.ydata)
            self._draw_graph()

    def _on_release(self, event):
        """Обработчик отпускания мыши"""
        self.dragged_node = None

    def _reset_layout(self):
        """Сброс расположения узлов"""
        self.pos = nx.spring_layout(self.graph, k=0.5)
        self._draw_graph()


def start_editor():
    root = tk.Tk()
    editor = FileNodeEditor(root)
    root.mainloop()

if __name__ == "__main__":
    start_editor()