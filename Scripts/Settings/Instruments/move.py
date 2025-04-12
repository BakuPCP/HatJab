class NodeMover:
    def __init__(self, editor):
        self.editor = editor
        self.dragged_node = None

    def bind_events(self):
        """Привязка событий перемещения"""
        self.editor.canvas.mpl_connect('button_press_event', self.on_press)
        self.editor.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.editor.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        """Обработчик нажатия мыши"""
        if event.inaxes and event.button == 1:  # Левая кнопка мыши
            for node, (x, y) in self.editor.pos.items():
                if (abs(x - event.xdata) < self.editor.node_width / 2 and
                        abs(y - event.ydata) < self.editor.node_height / 2):
                    self.dragged_node = node
                    self.editor.selected_node = node
                    self.editor._draw_graph()
                    break

    def on_drag(self, event):
        """Обработчик перемещения мыши"""
        if self.dragged_node and event.inaxes:
            self.editor.pos[self.dragged_node] = (event.xdata, event.ydata)
            self.editor._draw_graph()

    def on_release(self, event):
        """Обработчик отпускания мыши"""
        self.dragged_node = None