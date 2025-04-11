from typing import Dict, Any, Optional
from tkinter import messagebox


class NodeEditor:
    def __init__(self, graph_manager):
        self.gm = graph_manager
        self.selected_node = None

    def select_node(self, node_name: Optional[str]) -> Dict[str, Any]:
        """Выбор узла для редактирования"""
        self.selected_node = node_name
        return self.get_node_properties(node_name) if node_name else {}

    def get_node_properties(self, node_name: str) -> Dict[str, Any]:
        """Получение свойств узла"""
        return dict(self.gm.graph.nodes[node_name]) if node_name in self.gm.graph else {}

    def update_node(self, node_name: str, properties: Dict[str, Any]) -> bool:
        """Обновление свойств узла"""
        if node_name in self.gm.graph:
            self.gm.graph.nodes[node_name].update(properties)
            return True
        return False

    def delete_node(self, node_name: str) -> bool:
        """Удаление узла с подтверждением"""
        if node_name not in self.gm.graph or node_name in ['main', 'crypto']:
            return False

        if messagebox.askyesno("Подтверждение", f"Удалить узел '{node_name}' и все связи?"):
            self.gm.graph.remove_node(node_name)
            if self.selected_node == node_name:
                self.selected_node = None
            return True
        return False