import tkinter as tk
from tkinter import Menu


class RightClickMenu:
    def __init__(self, editor):
        self.editor = editor
        self.selected_node = None
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
            node_type = self.editor.graph_manager.graph.nodes[node].get('type', 'file')
            width = self.editor.node_width * (0.7 if node_type == "file" else 1.0)
            height = self.editor.node_height * (0.7 if node_type == "file" else 1.0)

            if (x - width / 2 <= event.xdata <= x + width / 2 and
                    y - height / 2 <= event.ydata <= y + height / 2):
                self.selected_node = node
                break

        # Создаем контекстное меню только если клик был по узлу
        if self.selected_node and hasattr(event, 'guiEvent'):
            menu = Menu(self.editor.master, tearoff=0)
            menu.add_command(label="Свойства", command=self.show_properties)
            menu.post(event.guiEvent.x_root, event.guiEvent.y_root)

    def show_properties(self):
        """Показывает окно свойств узла"""
        if not self.selected_node:
            return

        prop_window = tk.Toplevel(self.editor.master)
        prop_window.title(f"Свойства: {self.selected_node}")
        prop_window.geometry("300x200")

        # Основная информация об узле
        tk.Label(prop_window, text=f"Имя узла: {self.selected_node}").pack(pady=5)

        node_type = self.editor.graph_manager.graph.nodes[self.selected_node].get('type', 'unknown')
        tk.Label(prop_window, text=f"Тип: {node_type}").pack(pady=5)

        # Здесь можно добавить другие свойства
        tk.Label(prop_window, text="Дополнительные свойства:").pack(pady=10)