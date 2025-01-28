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


class Grid[T]:
    class Entry:
        def __init__(self, x_pos: int, y_pos: int, item: T | None = None) -> None:
            self.x_pos: int = x_pos
            self.y_pos: int = y_pos
            self.object: T | None = item

    def __init__(self) -> None:
        self.grid: list[list[Grid.Entry]] = [[self.Entry(0, 0, None)]]
        self.rightmost_entries: list[int] = [-1]

    @property
    def width(self) -> int:
        return len(self.grid)

    @property
    def height(self) -> int:
        return len(self.grid[-1])

    def cell_is_empty(self, coords: tuple[int, int]) -> bool:
        return self.get_item(coords) is None

    def has_item(self, item: T) -> bool:
        return self.get_item_coords(item) != (-1, -1)

    def expand(self, new_width: int = 0, new_height: int = 0) -> None:
        for row_index in range(self.height, new_height+1):
            self.rightmost_entries.append(-1)
            for column_index, column in enumerate(self.grid):
                column.append(self.Entry(column_index, row_index))
        for column in range(self.width, new_width+1):
            self.grid.append([self.Entry(row, column) for row in range(self.height)])

    def place_item(self, coords: tuple[int, int], item: T | None) -> None:
        self.expand(coords[0], coords[1])
        self.grid[coords[0]][coords[1]].object = item
        if item is None:
            for i in reversed(range(self.width)):
                if self.grid[i][coords[1]].object is not None:
                    self.rightmost_entries[coords[1]] = i
                    break
        else:
            self.rightmost_entries[coords[1]] = max(self.rightmost_entries[coords[1]], coords[0])

    def get_item(self, coords: tuple[int, int]) -> T | None:
        return None if coords[0] >= self.width or coords[1] >= self.height else self.grid[coords[0]][coords[1]].object

    def get_item_coords(self, item: T) -> tuple[int, int]:
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                if cell.object is item:
                    return x, y
        return -1, -1

    def get_item_x_coord(self, item: T) -> int:
        return self.get_item_coords(item)[0]

    def get_item_y_coord(self, item: T) -> int:
        return self.get_item_coords(item)[1]

    def move_item(self, old_coords: tuple[int, int], new_coords: tuple[int, int]) -> None:
        self.place_item(new_coords, self.get_item(old_coords))
        self.clear_space(old_coords)

    def clear_space(self, coords: tuple[int, int]) -> None:
        self.place_item(coords, None)
