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
    parse_error: bool
    scroll_bar_line: int

    class BaseParseStackFrame:
        def __init__(self, node: Tree) -> None:
            self.node = node

    def input_grammar(self, description: str) -> None:
        self.grammar = Grammar(description)
        self.generate_rules()

    def input_code(self, code: str) -> None:
        self.token_stream = self.grammar.lexer(code)

    def node_on_stack(self, node: Tree) -> bool:
        return any(map(lambda frame: node is frame.node, self.parse_stack))

    def node_should_be_highlighted(self, node: Tree) -> bool:
        return node is self.current_node and (not self.finished_parsing or self.parse_error)

    def token_stream_to_str(self) -> str:
        return ' '.join(map(lambda token: token.image, self.token_stream))

    def set_scroll_bar_to_line(self, line: int) -> None:
        self.scroll_bar_line = line - 1

    def set_scroll_bar_to_index(self, index: int) -> None:
        self.scroll_bar_line = index

    def reset_parser_attributes(self) -> None:
        self.tree = None
        self.current_node = None
        self.parse_stack = []
        self.token_stream = []
        self.finished_parsing = False
        self.parse_error = False
        self.scroll_bar_line = -1

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

    def highlight_row(self, row: int) -> None:
        self.curr_highlighted_row = self.last_highlighted_row = row

    def highlight_col(self, col: int) -> None:
        self.curr_highlighted_col = self.last_highlighted_col = col

    def unhighlight_table(self) -> None:
        self.curr_highlighted_row = self.curr_highlighted_col = -1

    def reset_table_highlights(self) -> None:
        self.highlight_row(-1)
        self.highlight_col(-1)

    def table_height(self) -> int: ...
    def table_width(self) -> int: ...
    def get_table_top_row(self) -> Iterable[str]: ...
    def get_table_left_col(self) -> Iterable[str]: ...
    def get_table_body(self) -> Iterable[Iterable[str]]: ...


class WritesGrammar(UsesGrammar):
    current_highlighted_line: int

    def set_highlighted_line(self, line: int) -> None:
        self.current_highlighted_line = line - 1

    def reset_highlighted_line(self) -> None:
        self.current_highlighted_line = -1

    def grammar_to_numbered_list(self) -> str:
        return HTML.CodeBox.make_html(self.grammar.make_list(), self.current_highlighted_line)

    def grammar_list_len(self) -> int:
        return len(self.grammar) - 1


class LL1Parser(UsesGrammar):
    def generate_predict_sets(self) -> list[list[str]]:
        first_sets: dict[str, list[str]] = self.grammar.generate_first_sets()
        follow_sets: dict[str, list[str]] = self.grammar.generate_follow_sets()
        predict_sets: list[list[str]] = []

        for rule in self.grammar.rules:
            new_set: list[str] = [symbol for symbol in first_sets[rule.productions[0].name]]
            if '' in new_set:
                new_set.remove('')
                new_set = list(set(new_set + follow_sets[rule.name]))
            predict_sets.append(new_set)
        if '' in predict_sets[0]:
            predict_sets[0].remove('')
        if 'eof' not in predict_sets[0]:
            predict_sets[0].append('eof')

        return predict_sets
