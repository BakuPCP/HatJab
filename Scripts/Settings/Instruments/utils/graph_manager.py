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
        main_nodes = ["System", "mods", "Scripts", "Data", "main", "Settings", "Buttons", "Instriments", "utils"]
        for node in main_nodes:
            self.graph.add_node(node, type="folder")

        # Файлы как узлы
        file_nodes = {
           "System": ["crypto.py", "hjcheck.py"],
            "mods": ["example.mod", "weather.mod"],
            "Scripts": ["commands.txt", "settings.cfg", "__init__.py", "launch.py", "graph.settings.json"],
            "Data": ["keys.dhj", "session.seshj", "ps.dhj"],
            "main": ["main.py"],
            "Settings": ["__init__.py", "settings.py", "Buttons", "Instruments"],
            "Buttons" : ["__init.py", "save_settings.py"],
            "Instruments": ["utils", "__init.py", "click_s.py", "highlight.py", "move.py"],
            "utils": ["__init__.py", "algo_s.py", "debug_m.py", "graph_manager.py", "help_move.py", "nt_help.py"],
        }

        # Добавляем файлы и связи
        for parent, files in file_nodes.items():
            for file in files:
                self.graph.add_node(f"{parent}/{file}", type="file")
                self.graph.add_edge(parent, f"{parent}/{file}")

        # Основные связи между папками
        self.graph.add_edges_from([
            ("main", "System"), ("main", "mods"),
            ("main", "Scripts"), ("Scripts", "Data"),
            ("Scripts", "Settings"), ("Settings", "Buttons"),
            ("Settings", "Instruments"), ("Instruments", "utils"),
        ])

        # Позиционирование
        self.pos = nx.spring_layout(self.graph, k=0.5, seed=42)