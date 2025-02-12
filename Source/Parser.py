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

from __future__ import annotations
from collections.abc import Iterable

from Grammar import Grammar
import HTML
from Tree import Tree


class Parser:
    grammar: Grammar
    tree: Tree | None
    current_node: Tree | None
    parse_stack: list[ParseStackFrame]
    token_stream: list[Grammar.Token]
    finished_parsing: bool
    code: list[str]
    last_highlighted_line: int

    class ParseStackFrame:
        def __init__(self, node: Tree) -> None:
            self.node = node

    def input_grammar(self, description: str) -> None:
        self.grammar = Grammar(description)
        self.generate_rules()

    def new_code(self, code: str) -> None:
        self.token_stream = self.grammar.lexer(code)

    def node_on_stack(self, node: Tree) -> bool:
        for item in self.parse_stack:
            if node is item.node:
                return True
        return False

    def make_html(self) -> str:
        return HTML.Code.make_html(self.code)

    def token_stream_to_str(self) -> str:
        return ' '.join(map(lambda x: x.image, self.token_stream))

    def generate_rules(self) -> None: ...
    def step(self) -> None: ...
    def parse_stack_to_str(self) -> str: ...
    def reset(self) -> None: ...


class TableParser(Parser):
    curr_highlighted_row: int
    last_highlighted_row: int
    curr_highlighted_col: int
    last_highlighted_col: int

    def table_height(self) -> int: ...
    def table_width(self) -> int: ...
    def table_top_row(self) -> Iterable[str]: ...
    def table_left_col(self) -> Iterable[str]: ...
    def get_table(self) -> Iterable[Iterable[str]]: ...

    def input_grammar(self, description: str) -> None:
        super().input_grammar(description)
        self.code = self.grammar.make_list()

    def highlight_line(self, line: int) -> None:
        self.last_highlighted_line = HTML.Code.highlighted_line = line

    @staticmethod
    def remove_highlight() -> None:
        HTML.Code.highlighted_line = -1
