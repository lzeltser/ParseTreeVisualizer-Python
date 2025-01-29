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

from typing import Any


def add_escape_sequences(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


class StackTrace:
    html_start: str = r"""<!DOCTYPE HTML>
<html><head><meta charset="utf-8" /><style type="text/css">
p { white-space: pre-wrap; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; }
</style></head><body align="center" style=" font-family:'Segoe UI', sans-serif; font-size:9pt; font-weight:400; font-style:normal;">
<table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="0" cellpadding="0">
<tr><td><p align="right" style=" color:#00ff00;">"""
    html_middle: str = r"""</span></p></td><td><p align="left">   """
    html_end: str = r"""</p></td></tr></table></body></html>"""

    @staticmethod
    def make_html(stack_text: list[str], token_text: list[str]) -> str:
        return (StackTrace.html_start + '<br>'.join(map(add_escape_sequences, stack_text)) +
                StackTrace.html_middle + '<br>   '.join(map(add_escape_sequences, token_text)) + StackTrace.html_end)


class RDCode:
    html_start: str = r"""<!DOCTYPE HTML>
<html><head><meta charset="utf-8" /><style type="text/css">
p { white-space: pre-wrap; }
</style></head><body style=" font-family:'Courier New', monospace; font-size:9pt; font-weight:400; font-style:normal;"><p>"""
    html_end: str = r"""</p></body></html>"""
    highlight_line_code: str = r"""+==HIGHLIGHT_THIS_LINE=="""
    highlight_start: str = r"""<highlight style="background-color:red;">"""
    highlight_end: str = r""" </highlight>"""

    @staticmethod
    def add_escape_sequences(text: str) -> str:
        return (RDCode.highlight_start + add_escape_sequences(text).removeprefix(RDCode.highlight_line_code) +
                RDCode.highlight_end) if text.startswith(RDCode.highlight_line_code) else add_escape_sequences(text)

    @staticmethod
    def make_html(text: list[str]) -> str:
        return RDCode.html_start + '<br>'.join(map(RDCode.add_escape_sequences, text)) + RDCode.html_end

    @staticmethod
    def highlight_line(line: str) -> str:
        return RDCode.highlight_line_code + line

    @staticmethod
    def remove_highlight(line: str) -> str:
        return line.removeprefix(RDCode.highlight_line_code)


class Table:
    html_start: str = r"""<!DOCTYPE HTML>
<html><head><meta charset="utf-8" /><style type="text/css">
p { white-space: pre-wrap; }
.top_row { text-align:center; color:#ff0000; background-color:#dcdcdc; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; position:sticky; top:0; z-index:2; }
.top_row_highlighted { text-align:center; color:#ff0000; background-color:#b4b4b4; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; position:sticky; top:0; z-index:2; }
.left_col { text-align:center; color:#ff0000; background-color:#dcdcdc; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; position:sticky; left:0; z-index:1; }
.left_col_highlighted { text-align:center; color:#ff0000; background-color:#b4b4b4; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; position:sticky; left:0; z-index:1; }
.cell_normal { text-align:center; background-color:#ffffff; }
.cell_highlighted { text-align:center; background-color:#e6e6e6; }
.cell_double_highlighted { text-align:center; background-color:#aaaaaa; }
</style></head><body style=" font-family: 'Segoe UI', sans-serif; font-size:9pt; font-weight:400; font-style:normal;"><table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" align="center" cellspacing="0" cellpadding="0">"""
    html_end: str = r"""</table></body></html>"""

    row_start: str = r"""<tr>"""
    row_end: str = r"""</tr>"""

    cell_start_1: str = r"""<td class=" """
    cell_start_2: str = r""" "><p align="center">  """
    cell_end: str = r"""  </p></td>"""

    cell_style_top_row: str = r"""top_row"""
    cell_style_top_row_hl: str = r"""top_row_highlighted"""
    cell_style_left_col: str = r"""left_col"""
    cell_style_left_col_hl: str = r"""left_col_highlighted"""
    cell_style_normal: str = r"""cell_normal"""
    cell_style_hl: str = r"""cell_highlighted"""
    cell_style_2_hl: str = r"""cell_double_highlighted"""

    @staticmethod
    def write_cell(style: str, content: Any = '') -> str:
        return (Table.cell_start_1 + style + Table.cell_start_2
                + add_escape_sequences(str('' if str(content) == '-1' else content)) + Table.cell_end)

    @staticmethod
    def write_row(first_style: str, main_style: str, hl_style: str, first_item: Any, other_items: list, hl_col: int) -> str:
        text: str = Table.row_start
        text += Table.write_cell(first_style, first_item)
        for i, item in enumerate(other_items):
            text += Table.write_cell(hl_style if i == hl_col else main_style, item)
        text += Table.row_end
        return text

    @staticmethod
    def write_table(left_col: list, top_row: list, table: list[list], hl_row: int = -1, hl_col: int = -1) -> str:
        text: str = Table.html_start
        text += Table.write_row(Table.cell_style_normal, Table.cell_style_top_row, Table.cell_style_top_row_hl, '', top_row, hl_col)
        for r, row in enumerate(table):
            text += Table.row_start
            text += Table.write_cell(Table.cell_style_left_col_hl if r == hl_row else Table.cell_style_left_col, left_col[r])
            for c, cell in enumerate(row):
                this_style: str
                if r == hl_row and c == hl_col:
                    this_style = Table.cell_style_2_hl
                elif r == hl_row or c == hl_col:
                    this_style = Table.cell_style_hl
                else:
                    this_style = Table.cell_style_normal
                text += Table.write_cell(this_style, cell)
            text += Table.row_end

        text += Table.html_end
        return text
