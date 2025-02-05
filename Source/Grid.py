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
    class Entry:
        def __init__(self, x_pos: int, y_pos: int, item: Tree | None = None) -> None:
            self.x_pos: int = x_pos
            self.y_pos: int = y_pos
            self.object: Tree | None = item

    def __init__(self, tree: Tree, compact_tree: bool) -> None:
        self.tree: Tree = tree
        self.grid: list[list[Grid.Entry]] = [[self.Entry(0, 0, None)]]
        self.rightmost_entries: list[int] = [-1]
        self.place_tree_on_grid(compact_tree)

    @property
    def width(self) -> int:
        return len(self.grid)

    @property
    def height(self) -> int:
        return len(self.grid[-1])

    def cell_is_empty(self, coords: tuple[int, int]) -> bool:
        return self.get_item(coords) is None

    def has_item(self, item: Tree) -> bool:
        return self.get_coords(item) != (-1, -1)

    def expand(self, new_width: int = 0, new_height: int = 0) -> None:
        for row_index in range(self.height, new_height+1):
            self.rightmost_entries.append(-1)
            for column_index, column in enumerate(self.grid):
                column.append(self.Entry(column_index, row_index))
        for column in range(self.width, new_width+1):
            self.grid.append([self.Entry(row, column) for row in range(self.height)])

    def place_item(self, coords: tuple[int, int], item: Tree | None) -> None:
        self.expand(coords[0], coords[1])
        self.grid[coords[0]][coords[1]].object = item
        if item is None:
            for i in reversed(range(self.width)):
                if self.grid[i][coords[1]].object is not None:
                    self.rightmost_entries[coords[1]] = i
                    break
        else:
            self.rightmost_entries[coords[1]] = max(self.rightmost_entries[coords[1]], coords[0])

    def get_item(self, coords: tuple[int, int]) -> Tree | None:
        return None if coords[0] >= self.width or coords[1] >= self.height else self.grid[coords[0]][coords[1]].object

    def get_coords(self, item: Tree) -> tuple[int, int]:
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell.object is item:
                    return x, y
        return -1, -1

    def get_x_coord(self, item: Tree) -> int:
        return self.get_coords(item)[0]

    def get_y_coord(self, item: Tree) -> int:
        return self.get_coords(item)[1]

    def move_item(self, old_coords: tuple[int, int], new_coords: tuple[int, int]) -> None:
        self.place_item(new_coords, self.get_item(old_coords))
        self.clear_space(old_coords)

    def clear_space(self, coords: tuple[int, int]) -> None:
        self.place_item(coords, None)

    def place_tree_on_grid(self, compact_tree: bool) -> None:
        self.place_item((0, 0), self.tree)
        for child in self.tree:
            self.place_node_on_grid(child, compact_tree)
        if self.tree.name == '':
            self.clear_space(self.get_coords(self.tree))
            for x in range(self.width):
                for y in range(self.height):
                    if self.get_item((x, y)) is not None:
                        self.move_item((x, y), (x, y - 1))

    def place_node_on_grid(self, node: Tree, compact_tree: bool) -> None:
        y_pos = self.get_y_coord(node.parent) + 1
        parents_rightest_placed_child: int = self.rightest_placed_child(node.parent)
        x_pos: int = max(
            self.rightmost_entries[y_pos]+1 if self.height > y_pos else -1, self.get_x_coord(node.parent)
            if parents_rightest_placed_child < 0 else self.get_x_coord(node.parent[parents_rightest_placed_child]) + 1
        )
        self.place_item((x_pos, y_pos), node)
        for child in node:
            self.place_node_on_grid(child,  compact_tree)

        if compact_tree:
            self.fix_node_x_position(node.parent)

        placed_child_children: int = 1 + self.rightest_placed_child(node)
        if ((placed_child_children > 0 and placed_child_children % 2 == 0 and compact_tree) or
            (placed_child_children > 1 and placed_child_children % 2 == 1 and not compact_tree)):
            current_node = node
            able_to_nudge = True
            while len(current_node) > 0:
                current_node = current_node[0]
                x_pos, y_pos = self.get_coords(current_node)
                if x_pos < 1 or not self.cell_is_empty((x_pos-1, y_pos)):
                    able_to_nudge = False
                    break
            if able_to_nudge:
                for child_to_nudge in node:
                    self.nudge_node_left(child_to_nudge)

        if not compact_tree:
            self.fix_node_x_position(node.parent)

    def nudge_node_left(self, node: Tree) -> None:
        for child in node:
            self.nudge_node_left(child)
        x_pos, y_pos = self.get_coords(node)
        self.move_item((x_pos, y_pos), (x_pos - 1, y_pos))

    def fix_node_x_position(self, node: Tree) -> None:
        if node is None:
            return
        x_pos, y_pos = self.get_coords(node)
        new_x_position = ((self.get_x_coord(node[self.rightest_placed_child(node)])
                           - self.get_x_coord(node[0])) // 2 + self.get_x_coord(node[0]))
        if x_pos != new_x_position and self.cell_is_empty((new_x_position, y_pos)):
            self.move_item((x_pos, y_pos), (new_x_position, y_pos))
            self.fix_node_x_position(node.parent)

    def rightest_placed_child(self, node: Tree) -> int:
        for i, child in enumerate(reversed(node.children)):
            if self.has_item(child):
                return len(node) - i - 1
        return -1
