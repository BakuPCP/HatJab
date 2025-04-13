class NodeTypeHelper:
    @staticmethod
    def get_node_type(graph, node, default='file'):
        """Безопасно получает тип узла"""
        return graph.nodes[node].get('type', default)

    @staticmethod
    def calculate_dimensions(editor, graph, node):
        """Вычисляет ширину и высоту узла с проверкой типа"""
        node_type = NodeTypeHelper.get_node_type(graph, node)
        width = editor.node_width * (0.7 if node_type == "file" else 1.0)
        height = editor.node_height * (0.7 if node_type == "file" else 1.0)
        return width, height