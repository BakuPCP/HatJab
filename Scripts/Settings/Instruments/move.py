class NodeMover:
    def __init__(self, editor):
        self.editor = editor
        self.dragged_node = None
        self.bind_events()

    def bind_events(self):
        """Привязка событий перемещения"""
        self.editor.canvas.mpl_connect('button_press_event', self.on_press)
        self.editor.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.editor.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.inaxes and event.button == 1:
            for node, (x, y) in self.editor.graph_manager.pos.items():  # Изменено здесь
                width = self.editor.node_width * (0.7 if self.editor.graph_manager.graph.nodes[node].get('type') == "file" else 1.0)  # И здесь
                height = self.editor.node_height * (0.7 if self.editor.graph_manager.graph.nodes[node].get('type') == "file" else 1.0)  # И здесь

                if (abs(x - event.xdata) < width/2 and abs(y - event.ydata) < height/2):
                    self.dragged_node = node
                    break

    def on_drag(self, event):
        if self.dragged_node and event.inaxes:
            self.editor.graph_manager.pos[self.dragged_node] = (event.xdata, event.ydata)  # Изменено здесь
            self.editor._draw_graph()

    def on_release(self, event):
        """Обработчик отпускания мыши"""
        self.dragged_node = None