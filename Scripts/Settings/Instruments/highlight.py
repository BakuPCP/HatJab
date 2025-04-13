class MultiHighlighter:
    def __init__(self, editor):
        self.editor = editor
        self.selected_nodes = set()
        self.shift_pressed = False
        self._bind_events()

    def _bind_events(self):
        """Привязка всех необходимых событий"""
        # События мыши
        self.editor.canvas.mpl_connect('button_press_event', self._on_click)


        # События клавиатуры
        self.editor.canvas.get_tk_widget().bind('<Shift_L>', lambda e: self._set_shift_state(True))
        self.editor.canvas.get_tk_widget().bind('<KeyRelease-Shift_L>', lambda e: self._set_shift_state(False))
        self.editor.canvas.get_tk_widget().bind('<Shift_R>', lambda e: self._set_shift_state(True))
        self.editor.canvas.get_tk_widget().bind('<KeyRelease-Shift_R>', lambda e: self._set_shift_state(False))

    def _set_shift_state(self, state):
        """Устанавливает состояние клавиши Shift"""
        self.shift_pressed = state

    def _on_click(self, event):
        if not event.inaxes or event.button != 1:
            return

        clicked_node = None  # Инициализируем переменную заранее

        for node, (x, y) in self.editor.graph_manager.pos.items():
            node_type = self.editor.graph_manager.graph.nodes[node].get('type', 'file')
            #width = self.editor.node_width * (0.7 if node_type == "file" else 1.0)
            #height = self.editor.node_height * (0.7 if node_type == "file" else 1.0)
            from .utils.nt_help import NodeTypeHelper
            width, height = NodeTypeHelper.calculate_dimensions(self.editor, self.editor.graph_manager.graph, node)

            if (abs(x - event.xdata) < width / 2 and abs(y - event.ydata) < height / 2):
                clicked_node = node
                break

        # Теперь clicked_node всегда определена (может быть None)
        if clicked_node is not None:  # Явная проверка на None
            if self.shift_pressed:
                if clicked_node in self.selected_nodes:
                    self.selected_nodes.remove(clicked_node)
                else:
                    self.selected_nodes.add(clicked_node)
            else:
                self.selected_nodes = {clicked_node}

            self._update_display()

    def _update_display(self):
        for node in self.editor.graph_manager.graph.nodes():  # Изменено здесь
            if node in self.selected_nodes:
                self.editor.graph_manager.graph.nodes[node]['color'] = self.editor.selected_color  # И здесь
            elif 'color' in self.editor.graph_manager.graph.nodes[node]:  # И здесь
                del self.editor.graph_manager.graph.nodes[node]['color']  # И здесь

        self.editor._draw_graph()