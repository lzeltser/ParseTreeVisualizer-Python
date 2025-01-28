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


class Grammar:
    grammar_rules: dict[str, list[list[GrammarRule]]]

    class GrammarRule:  # special cases: <eof>, "" (epsilon), <i_lit> (integer literal), <id> (variable)
        def __init__(self, text: str, terminal: bool) -> None:
            self.text = text
            self.terminal = terminal

    class GrammarProcessingException(Exception):
        pass

    def __init__(self, description: str) -> None:
        self.description: str = description

        # TODO: make tokens and rules from grammar
        self.tokens_list: list[str] = [
            'read', 'write', 'while', 'if', 'end', ':=', '(', ')', '+', '-', '*', '/', '=', '<>', '<', '<=', '>', '>=']
