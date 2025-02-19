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


class UsesGrammar:
    grammar: Grammar


class Parser(UsesGrammar):
    tree: Tree | None
    current_node: Tree | None
    parse_stack: list[BaseParseStackFrame]
    token_stream: list[Grammar.Token]
    finished_parsing: bool
    line_to_move_scrollbar_to: int

    class BaseParseStackFrame:
        def __init__(self, node: Tree) -> None:
            self.node = node

    def input_grammar(self, description: str) -> None:
        self.grammar = Grammar(description)
        self.generate_rules()

    def input_code(self, code: str) -> None:
        self.token_stream = self.grammar.lexer(code)

    def node_on_stack(self, node: Tree) -> bool:
        return any(map(lambda item: node is item.node, self.parse_stack))

    def token_stream_to_str(self) -> str:
        return ' '.join(map(lambda token: token.image, self.token_stream))

    def code_box_text(self) -> str: ...
    def lines_of_code(self) -> int: ...
    def parse_stack_to_str(self) -> str: ...

    def generate_rules(self) -> None: ...
    def step(self) -> None: ...
    def reset(self) -> None: ...


class UsesTable:
    curr_highlighted_row: int
    last_highlighted_row: int
    curr_highlighted_col: int
    last_highlighted_col: int

    def table_height(self) -> int: ...
    def table_width(self) -> int: ...
    def get_table_top_row(self) -> Iterable[str]: ...
    def get_table_left_col(self) -> Iterable[str]: ...
    def get_table_body(self) -> Iterable[Iterable[str]]: ...


class WritesGrammar(UsesGrammar):
    curr_highlighted_line: int

    def grammar_to_numbered_list(self) -> str:
        return HTML.CodeBox.make_html(self.grammar.make_list(), self.curr_highlighted_line)

    def grammar_list_len(self) -> int:
        return len(self.grammar) - 1
