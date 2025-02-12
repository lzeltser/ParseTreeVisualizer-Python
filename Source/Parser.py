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
    grammar: Grammar | None
    tree: Tree | None
    current_node: Tree | None
    parse_stack: list[ParseStackFrame]
    token_stream: list[Token]
    finished_parsing: bool
    code: list[str]
    last_highlighted_line: int

    class Token:
        def __init__(self, name: str, image: str = None) -> None:
            self.name = name
            self.image = name if image is None else image

        def __str__(self) -> str:
            return self.image

    class ParseStackFrame:
        def __init__(self, node: Tree) -> None:
            self.node = node

    def __init__(self) -> None:
        self.grammar = None
        self.code = []
        self.reset()

    def input_grammar(self, description: str) -> None:
        self.grammar = Grammar(description)
        self.generate_rules()

    class LexingException(Exception):
        pass

    def lexer(self, code: str) -> None:
        # TODO: replace this with a state machine

        def get_potential_tokens(list_: list[str], current_token_: str) -> list[str]:
            return [item for item in list_ if item.startswith(current_token_)]

        token_stream: list[Parser.Token] = []
        counter: int = 0
        current_token: str = ''
        code_length: int = len(code)

        while counter < code_length:
            if code[counter].isspace():
                counter += 1
            elif code[counter].isidentifier():
                while counter < code_length and (code[counter].isidentifier() or code[counter].isdigit()):
                    current_token += code[counter]
                    counter += 1
                token_stream.append(self.Token(current_token) if current_token in self.grammar.tokens_list
                                    else self.Token('<id>', current_token))
                current_token = ''
            elif code[counter].isdigit():
                while counter < code_length and code[counter].isdigit():
                    current_token += code[counter]
                    counter += 1
                if counter < code_length and code[counter].isalpha():
                    raise self.LexingException(f"Invalid token: '{current_token + code[counter]}'.")
                token_stream.append(self.Token('<i_lit>', current_token))
                current_token = ''
            else:
                potential_tokens = get_potential_tokens(self.grammar.tokens_list, current_token)
                while counter < code_length and \
                        not (code[counter].isidentifier() or code[counter].isdigit() or code[counter].isspace()):
                    current_token += code[counter]
                    counter += 1
                    potential_tokens = get_potential_tokens(potential_tokens, current_token)
                    if len(potential_tokens) < 1:
                        raise self.LexingException(f"Invalid token: '{current_token}'.")
                    if current_token in potential_tokens and \
                            (counter >= code_length or current_token + code[counter] not in
                             get_potential_tokens(potential_tokens, current_token + code[counter])):
                        token_stream.append(self.Token(current_token))
                        current_token = ''
                        break

        token_stream.append(self.Token('<eof>'))
        self.token_stream = token_stream

    def reset(self) -> None:
        self.tree = None
        self.current_node = None
        self.parse_stack = []
        self.token_stream = []
        self.finished_parsing = False
        self.last_highlighted_line = -1

    def node_on_stack(self, node: Tree) -> bool:
        for item in self.parse_stack:
            if node is item.node:
                return True
        return False

    def make_html(self) -> str:
        return HTML.Code.make_html(self.code)

    def generate_rules(self) -> None: ...
    def step(self) -> None: ...
    def parse_stack_to_str(self) -> str: ...

    def token_stream_to_str(self) -> str:
        return ' '.join(map(lambda x: x.image, self.token_stream))


class TableParser(Parser):
    def __init__(self) -> None:
        super().__init__()
        self.curr_highlighted_row: int = -1
        self.curr_highlighted_col: int = -1
        self.last_highlighted_row: int = -1
        self.last_highlighted_col: int = -1

    def table_height(self) -> int: ...
    def table_width(self) -> int: ...
    def table_top_row(self) -> Iterable[str]: ...
    def table_left_col(self) -> Iterable[str]: ...
    def get_table(self) -> Iterable[Iterable[str]]: ...

    def reset(self) -> None:
        super().reset()
        self.curr_highlighted_row = -1
        self.curr_highlighted_col = -1
        self.last_highlighted_row = -1
        self.last_highlighted_col = -1

    def input_grammar(self, description: str) -> None:
        super().input_grammar(description)
        self.code = self.grammar.make_list()

    def highlight_line(self, line: int) -> None:
        self.remove_highlight()
        self.code[line] = HTML.Code.highlight_line(self.code[line])
        self.last_highlighted_line = line

    def remove_highlight(self) -> None:
        if 0 <= self.last_highlighted_line < len(self.code):
            self.code[self.last_highlighted_line] = HTML.Code.remove_highlight(self.code[self.last_highlighted_line])
