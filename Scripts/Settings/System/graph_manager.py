import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any


class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions = {}
        self._init_base_graph()

    def _init_base_graph(self):
        """Инициализация базовой структуры HatJab"""
        core_components = ["main", "hjcheck", "crypto", "catal"]
        for comp in core_components:
            self.graph.add_node(comp, type="core", locked=False)

        edges = [
            ("main", "hjcheck"), ("main", "crypto"),
            ("main", "catal"), ("hjcheck", "crypto")
        ]
        self.graph.add_edges_from(edges)
        self.positions = nx.spring_layout(self.graph)

    def add_node(self, name: str, node_type: str, **attrs):
        """Добавление нового узла"""
        attrs.update({"type": node_type, "locked": False})
        self.graph.add_node(name, **attrs)
        self.positions[name] = (0, 0)  # Временная позиция

    def draw_graph(self, ax, selected_node: str = None):
        """Отрисовка графа на matplotlib axes"""
        # Очистка и настройка
        ax.clear()

        # Разделение узлов по типам
        core_nodes = [n for n, d in self.graph.nodes(data=True)
                      if d.get('type') == 'core']
        user_nodes = [n for n in self.graph.nodes()
                      if n not in core_nodes]

        # Рисуем узлы
        nx.draw_networkx_nodes(
            self.graph, self.positions, nodelist=core_nodes,
            ax=ax, node_size=2500, node_color='#2b7bb9'
        )
        nx.draw_networkx_nodes(
            self.graph, self.positions, nodelist=user_nodes,
            ax=ax, node_size=2000, node_color='#7bccc4'
        )

        # Выделение выбранного узла
        if selected_node and selected_node in self.positions:
            nx.draw_networkx_nodes(
                self.graph, self.positions, nodelist=[selected_node],
                ax=ax, node_size=2800, node_color='#f03b20'
            )

        # Отрисовка связей
        nx.draw_networkx_edges(
            self.graph, self.positions, ax=ax,
            arrows=True, arrowstyle='->', width=2
        )

        # Подписи
        nx.draw_networkx_labels(
            self.graph, self.positions, ax=ax,
            font_size=10, font_weight='bold'
        )