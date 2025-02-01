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
    class Item:
        def __init__(self, name: str, terminal: bool) -> None:
            self.name: str = name
            self.terminal: bool = terminal

        def __str__(self) -> str:
            return f'"{self.name.replace('\n', '\\n')}"' if self.terminal else f'<{self.name}>'

    class Rule:  # special cases: <eof>, "" (epsilon), <i_lit> (integer literal), <id> (variable)
        def __init__(self, name: str, rules: list[Grammar.Item] = None) -> None:
            self.name: str = name
            self.rules: list[Grammar.Item] = [] if rules is None else rules

        def __str__(self) -> str:
            return self.name + ' ::= ' + ' '.join(map(str, self.rules))

    class GrammarParsingError(Exception):
        pass

    def __init__(self, description: str) -> None:
        self.description: str = description
        self.rules: list[Grammar.Rule] = []
        self.tokens_list: list[str] = []

        current_state: int = 0
        current_string: str = ''
        current_rule_name: str = ''

        for char in self.description:
            char.lower()
            match current_state:
                case 0:
                    if char == '<':
                        current_string = ''
                        current_state = 1
                    elif char.isspace():
                        pass
                    else:
                        raise self.GrammarParsingError("All rules must start with '<'.")
                case 1:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 2
                    else:
                        raise self.GrammarParsingError("Symbols can only have letters, numbers, '_', or '-'.")
                case 2:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 2
                    elif char == '>':
                        current_rule_name = current_string
                        self.rules.append(Grammar.Rule(current_rule_name))
                        current_state = 3
                    else:
                        raise self.GrammarParsingError("Symbols can only have letters, numbers, '_', or '-'.")
                case 3:
                    if char == ':':
                        current_state = 4
                    elif char.isspace() and char != '\n':
                        pass
                    else:
                        raise self.GrammarParsingError("First symbol most be followed by '::='")
                case 4:
                    if char == ':':
                        current_state = 5
                    else:
                        raise self.GrammarParsingError("First symbol most be followed by '::='")
                case 5:
                    if char == '=':
                        current_state = 6
                    else:
                        raise self.GrammarParsingError("First symbol most be followed by '::='")
                case 6:
                    if char == '<':
                        current_string = ''
                        current_state = 7
                    elif char == '"':
                        current_string = ''
                        current_state = 10
                    elif char.isspace() and char != '\n':
                        pass
                    else:
                        raise self.GrammarParsingError("Symbol must begin with '<' or '\"'")
                case 7:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 8
                    else:
                        raise self.GrammarParsingError("Symbols can only have letters, numbers, '_', or '-'.")
                case 8:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 8
                    elif char == '>':
                        self.rules[-1].rules.append(Grammar.Item(current_string, False))
                        current_state = 9
                    else:
                        raise self.GrammarParsingError("Symbols can only have letters, numbers, '_', or '-'.")
                case 9:
                    if char == '<':
                        current_string = ''
                        current_state = 7
                    elif char == '"':
                        current_string = ''
                        current_state = 10
                    elif char.isspace() and char != '\n':
                        pass
                    elif char == '|':
                        self.rules.append(Grammar.Rule(current_rule_name))
                        current_state = 6
                    elif char == '\n':
                        current_state = 0
                    elif char == ';':
                        current_state = 12
                    else:
                        raise self.GrammarParsingError("Symbol must begin with '<' or '\"'")
                case 10:
                    if char == '\n':
                        raise self.GrammarParsingError("Symbol definition incomplete")
                    elif char == '\\':
                        current_state = 11
                    elif char == '"':
                        self.rules[-1].rules.append(Grammar.Item(current_string, True))
                        self.tokens_list.append(current_string)
                        current_state = 13
                    else:
                        current_string += char
                case 11:
                    if char == 'n':
                        current_string += '\n'
                        current_state = 10
                    else:
                        current_string += char
                        current_state = 10
                case 12:
                    if char == '\n':
                        current_state = 0
                    else:
                        pass
                case 13:
                    if char == '<':
                        current_string = ''
                        current_state = 7
                    elif char.isspace() and char != '\n':
                        pass
                    elif char == '|':
                        self.rules.append(Grammar.Rule(current_rule_name))
                        current_state = 6
                    elif char == '\n':
                        current_state = 0
                    elif char == ';':
                        current_state = 12
                    else:
                        raise self.GrammarParsingError("Symbol following literal must begin with '<'")
                case _:
                    raise self.GrammarParsingError("Something went wrong.")

        if current_state != 0 and current_state != 9 and current_state != 13:
            raise self.GrammarParsingError("Grammar definition is incomplete")

        self.tokens_list = list(set(self.tokens_list))
        if '' in self.tokens_list:
            self.tokens_list.remove('')
