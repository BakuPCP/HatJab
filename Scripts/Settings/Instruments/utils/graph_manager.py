import networkx as nx

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.pos = {}
        self.selected_node = None
        self.dragged_node = None

    def init_default_graph(self):
        """Инициализация графа по умолчанию"""
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