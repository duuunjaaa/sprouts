from Action import Action
from sprouts.SproutsState import Region, Boundary, Node

class SproutsAction(Action):
    def __init__(self, region: Region) -> None:
        self.region = region

class TwoBoundaryMove(SproutsAction):
    """
    A move that connects two boundaries together

    Attributes:
        boundary1 (Boundary): The first boundary
        boundary2 (Boundary): The second boundary
        i (int): The index of the node in boundary1
        j (int): The index of the node in boundary2
        new_node (Node): The new node that is added between the two selected nodes
    """
    def __init__(self, region: Region, boundary1: Boundary, boundary2: Boundary, i: int, j: int, new_node: Node) -> None:
        super().__init__(region)
        self.boundary1 = boundary1
        self.boundary2 = boundary2
        self.i = i
        self.j = j
        self.new_node = new_node
    
    def __str__(self) -> str:
        return f"TwoBoundaryMove: Boundary1: {self.boundary1}, Boundary2: {self.boundary2}, i: {self.i}, j: {self.j}, new_node: {self.new_node}"

class OneBoundaryMove(SproutsAction):
    """
    A move that adds a new node to a boundary

    Attributes:
        boundary (Boundary): The boundary to add the new node to
        i (int): The index of the first node in the boundary
        j (int): The index of the second node in the boundary
        included_boundaries (list[Boundary]): The boundaries that are "inside"
        excluded_boundaries (list[Boundary]): The boundaries that are left "outside"
        new_node (Node): The new node that is added to the boundary
    """
    def __init__(self, region: Region, boundary: Boundary, i: int, j: int, 
                 included_boundaries: list[Boundary], excluded_boundaries: list[Boundary],
                 new_node: Node) -> None:
        super().__init__(region)
        self.boundary = boundary
        self.i = i
        self.j = j
        self.included_boundaries = included_boundaries
        self.excluded_boundaries = excluded_boundaries
        self.new_node = new_node

    def __str__(self) -> str:
        included_str = ''.join([str(b) for b in self.included_boundaries])
        excluded_str = ''.join([str(b) for b in self.excluded_boundaries])
        return f"OneBoundaryMove: Boundary: {self.boundary}, i: {self.i}, j: {self.j}, \
        included_boundaries: {included_str}, excluded_boundaries: {excluded_str}, new_node: {self.new_node}"