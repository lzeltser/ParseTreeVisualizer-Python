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

stack_trace_beginning_text: str = r"""<!DOCTYPE HTML>
<html><head><meta charset="utf-8" /><style type="text/css">
p { white-space: pre-wrap; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; }
</style></head><body align="center" style=" font-family:'Segoe UI', sans-serif; font-size:9pt; font-weight:400; font-style:normal;">
<table border="0" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="0" cellpadding="0">
<tr><td><p align="right" style=" color:#00ff00;">"""
stack_trace_middle_text: str = r"""</span></p></td>
<td><p align="left">"""
stack_trace_end_text: str = r"""</p></td></tr></table></body></html>"""

recursive_descent_beginning_text: str = r"""<!DOCTYPE HTML>
<html><head><meta charset="utf-8" /><style type="text/css">
p { white-space: pre-wrap; }
</style></head><body style=" font-family:'Courier New', monospace; font-size:9pt; font-weight:400; font-style:normal;"><p>"""
recursive_descent_end_text: str = r"""</p></body></html>"""

recursive_descent_highlight_start: str = r"""<highlight style="background-color:red;">"""
recursive_descent_highlight_end: str = r""" </highlight>"""

table_beginning_text: str = r"""<!DOCTYPE HTML>
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
table_row_beginning: str = r"""<tr>"""
table_cell_start_part1: str = r"""<td class=" """
cell_style_top_row: str = r"""top_row"""
cell_style_top_row_hl: str = r"""top_row_highlighted"""
cell_style_left_col: str = r"""left_col"""
cell_style_left_col_hl: str = r"""left_col_highlighted"""
cell_style_normal: str = r"""cell_normal"""
cell_style_hl: str = r"""cell_highlighted"""
cell_style_2_hl: str = r"""cell_double_highlighted"""
table_cell_start_part2: str = r""" "><p align="center">  """
table_cell_end: str = r"""  </p></td>"""
table_row_end: str = r"""</tr>"""
table_end_text: str = r"""</table></body></html>"""
