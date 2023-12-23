from Game import Game
from sprouts.SproutsAction import SproutsAction
from sprouts.SproutsAction import TwoBoundaryMove, OneBoundaryMove
from sprouts.SproutsState import Region, Boundary, Node


class SproutsGame(Game):
    state: list[Region]
    num_nodes: int
    player: int
    done: bool
    def __init__(self, num_nodes: int):
        new_region = []
        for i in range(num_nodes):
            node = Node(str(i))
            new_region.append(Boundary([node]))
        self.state = [Region(new_region)]
        self.num_nodes = num_nodes
        self.player = 0
        self.done = False

    def __count_occurances_in_state(self, node: Node) -> int:
        count = 0
        for region in self.state:
            for boundary in region.boundaries:
                count += boundary.nodes.count(node)
        return count

    def __powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]

    def __get_valid_one_boundary_actions(self, region: Region, boundary: Boundary) -> list[SproutsAction]:
        valid_actions = []
        valid_ij_choices = []
        for i in range(0, len(boundary.nodes)):
            # i can be chosen if it occurs <= 2 times in the boundary
            if self.__count_occurances_in_state(boundary.nodes[i]) > 2:
                continue
            for j in range(i, len(boundary.nodes)):
                # j can be chosen if it occurs <= 2 times in the boundary
                if self.__count_occurances_in_state(boundary.nodes[j]) > 2:
                    continue
                if i == j:
                    # This is a valid move only if xi occurs only once in the boundary
                    if self.__count_occurances_in_state(boundary.nodes[i]) == 1:
                        valid_ij_choices.append((i, j))
                else:
                    valid_ij_choices.append((i, j))

        boundaries_without_boundary = [x for x in region.boundaries if x != boundary]
        for i, j in valid_ij_choices:
            # Create the new node
            new_node = Node(str(self.num_nodes))

            # Combine each ij choice with each subset of the boundaries
            for subset in self.__powerset(boundaries_without_boundary):
                included_boundaries = []
                excluded_boundaries = []
                for b in subset:
                    if b == boundary:
                        continue
                    included_boundaries.append(b)
                for b in region.boundaries:
                    if b in subset or b == boundary:
                        continue
                    excluded_boundaries.append(b)
                valid_actions.append(OneBoundaryMove(region, boundary, i, j, included_boundaries, excluded_boundaries, new_node))
        return valid_actions
            
    def __get_valid_two_boundary_actions(self, region: Region) -> list[SproutsAction]:
        valid_actions = []
        for b1_index in range(len(region.boundaries)):
            boundary1 = region.boundaries[b1_index]
            for b2_index in range(b1_index+1, len(region.boundaries)):
                boundary2 = region.boundaries[b2_index]
                for i in range(len(boundary1.nodes)):
                    # i can be chosen if it occurs <= 2 times in the boundary
                    if self.__count_occurances_in_state(boundary1.nodes[i]) > 2:
                        continue
                    for j in range(len(boundary2.nodes)):
                        # j can be chosen if it occurs <= 2 times in the boundary
                        if self.__count_occurances_in_state(boundary2.nodes[j]) > 2:
                            continue
                        # Create the new node
                        new_node = Node(str(self.num_nodes))

                        valid_actions.append(TwoBoundaryMove(region, boundary1, boundary2, i, j, new_node))
        return valid_actions

    def __get_valid_actions_inside_region(self, region: Region) -> list[SproutsAction]:
        valid_actions = []
        for boundary in region.boundaries:
            valid_actions.extend(self.__get_valid_one_boundary_actions(region, boundary))
        valid_actions.extend(self.__get_valid_two_boundary_actions(region))
        return valid_actions

    def get_valid_actions(self) -> list[SproutsAction]:
        valid_actions = []
        for region in self.state:
            valid_actions.extend(self.__get_valid_actions_inside_region(region))
        return valid_actions
    
    def __is_done(self) -> bool:
        return self.get_valid_actions() == []
    
    def get_state_value(self) -> float:
        if self.done:
            # If the game is done and player 0 is next to play
            # player 0 has lost, return -1 else return 1
            return -1 if self.player == 0 else 1
        return 0

    def step(self, action: SproutsAction) -> tuple[any, bool, float]:
        if isinstance(action, TwoBoundaryMove):
            # A two boundary move just joins two boundaries into one
            # First boundary is: x1, x2, ..., xm
            # Second boundary is: y1, y2, ..., yn
            # i,j are the indices of the nodes in the boundaries
            # The new boundary is: x1, ..., xi, new_node, yj, ..., yn, y1, ..., yj, new_node, xi, ..., xm

            # Remove the old boundaries
            # Find the region from the action and remove boundaries
            action_region = [x for x in self.state if x == action.region][0]
            action_region.boundaries.remove(action.boundary1)
            action_region.boundaries.remove(action.boundary2)

            # Create the new boundary
            new_boundary = []
            new_boundary.extend(action.boundary1.nodes[:action.i+1])
            new_boundary.append(action.new_node)
            if len(action.boundary2.nodes) > 1:
                new_boundary.extend(action.boundary2.nodes[action.j:])
            new_boundary.extend(action.boundary2.nodes[:action.j+1])
            new_boundary.append(action.new_node)
            if len(action.boundary1.nodes) > 1:
                new_boundary.extend(action.boundary1.nodes[action.i:])

            # Add the new boundary
            action_region.boundaries.append(Boundary(new_boundary))

        elif isinstance(action, OneBoundaryMove):
            # A one boundary move splits the region into two regions
            # x1, x2, ..., xn is the current boundary
            # The first new boundary is b1 = x1, ..., xi, new_node, xj, ..., xn
            # The second new boundary is b2 = xi, ..., xj, new_node
            # The two new regions are:
            # b1, B1 where B1 are boundaries taken inside the first new boundary
            # b2, B2 where B2 are boundaries taken outside the first new boundary
            
            # Remove the old region
            for region in self.state:
                if region == action.region:
                    self.state.remove(region)
                    break

            # Create the first new boundary
            new_boundary1 = []
            for k in range(action.i+1):
                new_boundary1.append(action.boundary.nodes[k])
            new_boundary1.append(action.new_node)

            if len(action.boundary.nodes) > 1:
                for k in range(action.j, len(action.boundary.nodes)):
                    new_boundary1.append(action.boundary.nodes[k])
            
            # Create the second new boundary
            new_boundary2 = []
            for k in range(action.i, action.j+1):
                new_boundary2.append(action.boundary.nodes[k])
            new_boundary2.append(action.new_node)

            # Create the first new region
            new_region1 = []
            for boundary in action.included_boundaries:
                new_region1.append(boundary)
            new_region1.append(Boundary(new_boundary1))

            # Create the second new region
            new_region2 = []
            for boundary in action.excluded_boundaries:
                new_region2.append(boundary)
            new_region2.append(Boundary(new_boundary2))

            # Add the two new regions
            self.state.append(Region(new_region1))
            self.state.append(Region(new_region2))
        
        self.num_nodes += 1
        self.player = 1 - self.player

        # Order of these two lines is important!
        self.done = self.__is_done()
        state_value = self.get_state_value()

        return self.state, self.done, state_value

    def render(self):
        for region in self.state:
            print(region)
        print('-------------')        