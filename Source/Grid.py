"""
Parse Tree Visualizer
Copyright (C) 2024-2025 Leon Zeltser (leonzeltser at gmail dot com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from Tree import Tree


class Grid:
    def __init__(self, tree: Tree, compact_tree: bool) -> None:
        self.tree: Tree = tree
        self.grid: list[list[Tree | None]] = [[self.tree]]

        for child in self.tree:
            self.place_tree_on_grid(child, compact_tree)

        if self.tree.name == '':
            self.nudge_nodes_up()

    @property
    def width(self) -> int:
        return len(self.grid)

    @property
    def height(self) -> int:
        return len(self.grid[-1])

    @staticmethod
    def assert_coords_are_valid(coords: tuple[int, int]) -> None:
        assert coords[0] >= 0
        assert coords[1] >= 0

    def cell_is_empty(self, coords: tuple[int, int]) -> bool:
        return self.get_node(coords) is None

    def has_item(self, node: Tree) -> bool:
        return self.get_coords(node) != (-1, -1)

    def expand(self, new_width: int = 0, new_height: int = 0) -> None:
        for column in self.grid:
            column += [None] * (new_height-self.height+1)
        self.grid += [[None] * self.height] * (new_width-self.width+1)

    def place_node(self, coords: tuple[int, int], node: Tree | None) -> None:
        self.assert_coords_are_valid(coords)
        self.expand(coords[0], coords[1])
        self.grid[coords[0]][coords[1]] = node

    def get_node(self, coords: tuple[int, int]) -> Tree | None:
        self.assert_coords_are_valid(coords)
        return None if coords[0] >= self.width or coords[1] >= self.height else self.grid[coords[0]][coords[1]]

    def get_coords(self, node: Tree) -> tuple[int, int]:
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell is node:
                    return x, y
        return -1, -1

    def get_x_coord(self, node: Tree) -> int:
        return self.get_coords(node)[0]

    def get_y_coord(self, node: Tree) -> int:
        return self.get_coords(node)[1]

    def move_node(self, old_coords: tuple[int, int], new_coords: tuple[int, int]) -> None:
        self.place_node(new_coords, self.get_node(old_coords))
        self.clear_space(old_coords)

    def clear_space(self, coords: tuple[int, int]) -> None:
        self.assert_coords_are_valid(coords)
        if coords[0] < self.width and coords[1] < self.height:
            self.grid[coords[0]][coords[1]] = None

    def rightmost_mode(self, y: int) -> int:
        if y < self.height:
            for x in reversed(range(self.width)):
                if not self.cell_is_empty((x, y)):
                    return x
        return -1

    def placed_children(self, node: Tree) -> int:
        for i, child in enumerate(reversed(node.children)):
            if self.has_item(child):
                return len(node) - i
        return 0

    def nudge_node_left(self, node: Tree) -> None:
        for child in node:
            self.nudge_node_left(child)
        x_pos, y_pos = self.get_coords(node)
        self.move_node((x_pos, y_pos), (x_pos - 1, y_pos))

    def nudge_nodes_up(self) -> None:
        self.clear_space(self.get_coords(self.tree))
        for x in range(self.width):
            for y in range(self.height):
                if self.get_node((x, y)) is not None:
                    self.move_node((x, y), (x, y - 1))

    def place_tree_on_grid(self, node: Tree, compact_tree: bool) -> None:
        y_pos = self.get_y_coord(node.parent) + 1
        x_pos: int = max(self.rightmost_mode(y_pos)+1, self.get_x_coord(node.parent))
        self.place_node((x_pos, y_pos), node)
        for child in node:
            self.place_tree_on_grid(child, compact_tree)

            if compact_tree:
                self.fix_node_x_position(node)

            if ((self.placed_children(node) > 0 and self.placed_children(node) % 2 == 0 and compact_tree) or
                (self.placed_children(node) > 1 and self.placed_children(node) % 2 == 1 and not compact_tree)):
                if self.can_nudge_children(node):
                    for child_to_nudge in node:
                        self.nudge_node_left(child_to_nudge)

            if not compact_tree:
                self.fix_node_x_position(node)

    def can_nudge_children(self, node: Tree) -> bool:
        for y, x in enumerate(self.leftmost_children(node, [], 0)):
            if x < 1 or not self.cell_is_empty((x-1, y+1+self.get_y_coord(node))):
                return False
        return True

    def leftmost_children(self, node: Tree, curr_list: list[int], level: int) -> list[int]:
        curr_list += [self.width] * (level-len(curr_list)+1)
        for child in node:
            curr_list[level] = min(curr_list[level], self.get_x_coord(child))
            self.leftmost_children(child, curr_list, level+1)
        return curr_list

    def fix_node_x_position(self, node: Tree) -> None:
        x_pos, y_pos = self.get_coords(node)
        new_x_position = (
                (self.get_x_coord(node[self.placed_children(node)-1])
                 - self.get_x_coord(node[0])) // 2 + self.get_x_coord(node[0])
        )
        if x_pos != new_x_position and self.cell_is_empty((new_x_position, y_pos)):
            self.move_node((x_pos, y_pos), (new_x_position, y_pos))
            if node.parent is not None:
                self.fix_node_x_position(node.parent)
