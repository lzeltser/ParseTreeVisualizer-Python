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


class GraphicsSettings:
    first_canvas_width: float
    first_canvas_height: float

    side_margin: float
    top_margin: float
    cell_width: float
    cell_height: float

    min_box_width: float
    box_height_: float

    shadow_enabled: bool
    shadow_offset_top: float
    shadow_offset_side: float

    line_width: int
    outline_width: int

    compact_tree: bool

    stacked_color: tuple[int, int, int]
    unstacked_color: tuple[int, int, int]
    highlight_color: tuple[int, int, int]
    shadow_color: tuple[int, int, int]

    def __init__(self) -> None:
        self.set_to_defaults()

    def set_to_defaults(self) -> None:
        self.first_canvas_width = 1500
        self.first_canvas_height = 750

        self.side_margin = 10
        self.top_margin = 10
        self.cell_width = 100
        self.cell_height = 50

        self.min_box_width = 22.5
        self.box_height_ = 20

        self.shadow_enabled = True
        self.shadow_offset_top = 8
        self.shadow_offset_side = 8

        self.line_width = 2
        self.outline_width = 3

        self.compact_tree = False

        self.stacked_color = (0x00, 0xFF, 0x00)
        self.unstacked_color = (0xFF, 0x00, 0x00)
        self.highlight_color = (0xFF, 0xFF, 0x00)
        self.shadow_color = (0xC0, 0xC0, 0xC0)

    def canvas_width(self, grid_width: int) -> float:
        return self.cell_width * (1+grid_width) + self.side_margin

    def canvas_height(self, grid_height: int) -> float:
        return self.cell_height * (1+grid_height) + self.top_margin

    def box_width(self, text_graphic_width: float) -> float:
        return max(self.min_box_width, text_graphic_width + 2)

    def box_height(self) -> float:
        return self.box_height_

    def box_x_coord(self, x_pos: int, text_graphic_width: float) -> float:
        return self.side_margin + self.cell_width * (x_pos + 0.25) - self.box_width(text_graphic_width) / 2

    def box_y_coord(self, y_pos: int) -> float:
        return self.top_margin + self.cell_height * y_pos

    def text_x_coord(self, x_pos: int, text_graphic_width: float) -> float:
        return self.side_margin + self.cell_width * (0.25 + x_pos) - text_graphic_width / 2

    def text_y_coord(self, y_pos: int, text_graphic_height: float) -> float:
        return self.top_margin + self.cell_height * y_pos + self.box_height_ / 2 - text_graphic_height / 2

    def line_start_x_coord(self, x_pos: int) -> float:
        return self.side_margin + self.cell_width * (0.25 + x_pos)

    def line_start_y_coord(self, y_pos: int) -> float:
        return self.top_margin + self.box_height_ + self.cell_height * y_pos - 1

    def line_end_x_coord(self, x_pos: int) -> float:
        return self.side_margin + self.cell_width * (0.25 + x_pos)

    def line_end_y_coord(self, y_pos: int) -> float:
        return self.top_margin + self.cell_height * y_pos + 1

    def box_shadow_x_coord(self, x_pos: int, text_graphic_width: float) -> float:
        return self.box_x_coord(x_pos, text_graphic_width) + self.shadow_offset_side

    def box_shadow_y_coord(self, y_pos: int) -> float:
        return self.box_y_coord(y_pos) + self.shadow_offset_top

    def line_shadow_start_x_coord(self, x_pos: int) -> float:
        return self.line_start_x_coord(x_pos) + self.shadow_offset_side

    def line_shadow_start_y_coord(self, y_pos: int) -> float:
        return self.line_start_y_coord(y_pos) + self.shadow_offset_top

    def line_shadow_end_x_coord(self, x_pos: int) -> float:
        return self.line_end_x_coord(x_pos) + self.shadow_offset_side

    def line_shadow_end_y_coord(self, y_pos: int) -> float:
        return self.line_end_y_coord(y_pos) + self.shadow_offset_top

    def horizontal_scroll_bar_pos(self, x_pos: int, text_graphic_width: float) -> int:
        return int(self.box_x_coord(x_pos, text_graphic_width) + self.box_width(text_graphic_width)/2)

    def vertical_scroll_bar_pos(self, y_pos: int) -> int:
        return int(self.box_y_coord(y_pos) + self.box_height()/2)
