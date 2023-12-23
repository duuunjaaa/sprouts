class Node:
    def __init__(self, id: str) -> None:
        self.id = id
    
    def __str__(self) -> str:
        return self.id

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Node):
            return self.id == __value.id
        return False

class Boundary:
    def __init__(self, boundary_nodes: list[Node]):
        self.nodes = boundary_nodes
    
    def __str__(self) -> str:
        return ''.join([str(node) for node in self.nodes]) + '.'
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Boundary):
            return self.nodes == __value.nodes
        return False

class Region:
    def __init__(self, boundaries: list[Boundary]):
        self.boundaries = boundaries
    
    def __str__(self) -> str:
        return ''.join([str(boundary) for boundary in self.boundaries]) + '}'
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Region):
            return self.boundaries == __value.boundaries
        return False
