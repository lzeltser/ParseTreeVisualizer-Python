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


class Code:
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
        return (Code.highlight_start + add_escape_sequences(text).removeprefix(Code.highlight_line_code) +
                Code.highlight_end) if text.startswith(Code.highlight_line_code) else add_escape_sequences(text)

    @staticmethod
    def make_html(text: list[str]) -> str:
        return Code.html_start + '<br>'.join(map(Code.add_escape_sequences, text)) + Code.html_end

    @staticmethod
    def highlight_line(line: str) -> str:
        return Code.highlight_line_code + line

    @staticmethod
    def remove_highlight(line: str) -> str:
        return line.removeprefix(Code.highlight_line_code)
