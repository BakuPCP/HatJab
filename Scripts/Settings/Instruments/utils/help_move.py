from ..highlight import MultiHighlighter
from ..move import NodeMover


class GroupMover:
    def __init__(self, editor):
        self.editor = editor
        self.highlighter = editor.highlighter
        self.mover = editor.mover
        self.drag_start_pos = None
        self.bind_events()

    def bind_events(self):
        """Привязка событий для перемещения группы узлов"""
        self.editor.canvas.mpl_connect('button_press_event', self.on_press)
        self.editor.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.editor.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        """Обработчик нажатия мыши"""
        if event.inaxes and event.button == 1:
            # Проверяем, есть ли выделенные узлы
            if self.highlighter.selected_nodes:
                self.drag_start_pos = (event.xdata, event.ydata)
                # Отменяем стандартное перемещение одиночного узла
                self.mover.dragged_node = None
            else:
                # Если нет выделенных узлов, разрешаем стандартное перемещение
                self.mover.on_press(event)

    def on_drag(self, event):
        """Обработчик перемещения мыши"""
        if self.drag_start_pos and event.inaxes:
            # Вычисляем смещение
            dx = event.xdata - self.drag_start_pos[0]
            dy = event.ydata - self.drag_start_pos[1]

            # Перемещаем все выделенные узлы
            for node in self.highlighter.selected_nodes:
                if node in self.editor.graph_manager.pos:
                    x, y = self.editor.graph_manager.pos[node]
                    self.editor.graph_manager.pos[node] = (x + dx, y + dy)

            # Обновляем начальную позицию для следующего перемещения
            self.drag_start_pos = (event.xdata, event.ydata)
            self.editor._draw_graph()
        else:
            # Если нет выделенных узлов, используем стандартное перемещение
            self.mover.on_drag(event)

    def on_release(self, event):
        """Обработчик отпускания мыши"""
        self.drag_start_pos = None
        self.mover.on_release(event)