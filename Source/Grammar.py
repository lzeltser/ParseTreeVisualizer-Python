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
    class Production:
        def __init__(self, name: str, terminal: bool) -> None:
            self.name: str = name
            self.terminal: bool = terminal

        def __str__(self) -> str:
            return f'"{self.name.replace('\n', '\\n')}"' if self.terminal else f'<{self.name}>'

    class Rule:  # special cases: <eof>, "" (epsilon), <i_lit> (integer literal), <id> (variable)
        def __init__(self, name: str, rules: list[Grammar.Production] = None) -> None:
            self.name: str = name
            self.productions: list[Grammar.Production] = [] if rules is None else rules

        def is_epsilon(self) -> bool:
            return len(self.productions) == 1 and self.productions[0].name == ''

        def make_formatted_str(self, longest_rule_len: int) -> str:
            return '<' + self.name + '>' + ' ' * (longest_rule_len - len(self.name)) + ' ::= ' + ' '.join(map(str, self.productions))

    class Token:
        def __init__(self, name: str, image: str = None) -> None:
            self.name = name
            self.image = name if image is None else image

        def __str__(self) -> str:
            return self.image

    class GrammarParsingException(Exception):
        pass

    class LexingException(Exception):
        pass

    def __init__(self, description: str) -> None:
        self.description: str = description.strip()
        self.rules: list[Grammar.Rule] = []
        self.tokens_list: list[str] = []

        current_state: int = 0
        current_string: str = ''
        current_rule_name: str = ''

        for char in self.description:
            match current_state:
                case 0:
                    if char == '<':
                        current_string = ''
                        current_state = 1
                    elif char.isspace():
                        pass
                    else:
                        raise self.GrammarParsingException("All rules must start with '<'.")
                case 1:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 2
                    else:
                        raise self.GrammarParsingException("Symbols can only have letters, numbers, '_', or '-'.")
                case 2:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 2
                    elif char == '>':
                        current_rule_name = current_string
                        self.rules.append(Grammar.Rule(current_rule_name))
                        current_state = 3
                    else:
                        raise self.GrammarParsingException("Symbols can only have letters, numbers, '_', or '-'.")
                case 3:
                    if char == ':':
                        current_state = 4
                    elif char.isspace() and char != '\n':
                        pass
                    else:
                        raise self.GrammarParsingException("First symbol most be followed by '::='")
                case 4:
                    if char == ':':
                        current_state = 5
                    else:
                        raise self.GrammarParsingException("First symbol most be followed by '::='")
                case 5:
                    if char == '=':
                        current_state = 6
                    else:
                        raise self.GrammarParsingException("First symbol most be followed by '::='")
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
                        raise self.GrammarParsingException("Symbol must begin with '<' or '\"'")
                case 7:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 8
                    else:
                        raise self.GrammarParsingException("Symbols can only have letters, numbers, '_', or '-'.")
                case 8:
                    if char.isalpha() or char.isdigit() or char == '-' or char == '_':
                        current_string += char
                        current_state = 8
                    elif char == '>':
                        self.rules[-1].productions.append(Grammar.Production(current_string, False))
                        current_state = 9
                    else:
                        raise self.GrammarParsingException("Symbols can only have letters, numbers, '_', or '-'.")
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
                        raise self.GrammarParsingException("Symbol must begin with '<' or '\"'")
                case 10:
                    if char == '\n':
                        raise self.GrammarParsingException("Symbol definition incomplete")
                    elif char == '\\':
                        current_state = 11
                    elif char == '"':
                        self.rules[-1].productions.append(Grammar.Production(current_string, True))
                        self.tokens_list.append(current_string)
                        current_state = 9
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
                case _:
                    raise self.GrammarParsingException("Something went wrong.")

        if current_state != 0 and current_state != 9 and current_state != 13:
            raise self.GrammarParsingException("Grammar definition is incomplete")

        self.tokens_list = list(dict.fromkeys(self.tokens_list))
        if '' in self.tokens_list:
            self.tokens_list.remove('')
        if 'eof' in self.tokens_list:
            self.tokens_list.remove('eof')
            self.tokens_list.append('eof')

        self.start_symbol: str = self.rule_names_list[0]

    def __len__(self):
        return len(self.rules)

    def longest_rule_len(self) -> int:
        return max(map(lambda x: len(x.name), self.rules))

    def make_list(self) -> list[str]:
        def make_str(n: int, rule: Grammar.Rule) -> str:
            return str(n).rjust(len(str(len(self.rules)))) + '. ' + rule.make_formatted_str(self.longest_rule_len())
        return [make_str(i, r) for i, r, in enumerate(self.rules, start=1)]

    @property
    def rule_names_list(self) -> list[str]:
        return list(dict.fromkeys([rule.name for rule in self.rules]))

    def generate_first_sets(self) -> dict[str, list[str]]:
        def remove_epsilon(l: list) -> list:
            new_l: list = [i for i in l]
            if '' in new_l:
                new_l.remove('')
            return new_l

        first_sets: dict[str, list[str]] = {'': ['']}
        for rule_name in self.rule_names_list:
            first_sets[rule_name] = []
        for token in self.tokens_list:
            first_sets[token] = [token]
        for rule in self.rules:
            if rule.is_epsilon() and len(first_sets[rule.name]) < 1:
                first_sets[rule.name].append('')

        made_progress: bool = True
        while made_progress:
            made_progress = False
            for rule in self.rules:
                first_len = len(first_sets[rule.name])
                for production in rule.productions:
                    first_sets[rule.name] = list(set(first_sets[rule.name] + remove_epsilon(first_sets[production.name])))
                    if '' not in first_sets[production.name]:
                        break

                e_in_all_productions: bool = True
                for production in rule.productions:
                    if '' not in first_sets[production.name]:
                        e_in_all_productions = False
                        break
                if e_in_all_productions and '' not in first_sets[rule.name]:
                    first_sets[rule.name].append('')

                made_progress = made_progress or len(first_sets[rule.name]) > first_len

        if '' in first_sets[self.start_symbol]:
            first_sets[self.start_symbol].remove('')
        if 'eof' not in first_sets[self.start_symbol]:
            first_sets[self.start_symbol].append('eof')

        return first_sets

    def generate_follow_sets(self, first_sets: dict[str, list[str]] = None) -> dict[str, list[str]]:
        def remove_epsilon(l: list) -> list:
            new_l: list = [i for i in l]
            if '' in new_l:
                new_l.remove('')
            return new_l

        first_sets: dict[str, list[str]] = self.generate_first_sets() if first_sets is None else first_sets
        follow_sets: dict[str, list[str]] = {}
        for key in first_sets:
            follow_sets[key] = []
        follow_sets[self.start_symbol].append('')
        made_progress: bool = True
        while made_progress:
            made_progress = False
            for rule in self.rules:
                for i, production in enumerate(rule.productions):
                    first_len = len(follow_sets[production.name])
                    if i + 1 < len(rule.productions):
                        follow_sets[production.name] = list(set(follow_sets[production.name] + remove_epsilon(first_sets[rule.productions[i+1].name])))
                    made_progress = made_progress or len(follow_sets[production.name]) > first_len

                for i, production in enumerate(rule.productions):
                    first_len = len(follow_sets[production.name])
                    if i == len(rule.productions)-1 or '' in first_sets[rule.productions[i+1].name]:
                        follow_sets[production.name] = list(set(follow_sets[production.name] + follow_sets[rule.name]))
                    made_progress = made_progress or len(follow_sets[production.name]) > first_len

        return follow_sets

    def lexer(self, code: str) -> list[Token]:
        # TODO: make state machine

        def get_potential_tokens(list_: list[str], current_token_: str) -> list[str]:
            return [item for item in list_ if item.startswith(current_token_)]

        token_stream: list[Grammar.Token] = []
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
                token_stream.append(self.Token(current_token) if current_token in self.tokens_list
                                    else self.Token('identifier', current_token))
                current_token = ''
            elif code[counter].isdigit():
                while counter < code_length and code[counter].isdigit():
                    current_token += code[counter]
                    counter += 1
                if counter < code_length and code[counter].isalpha():
                    raise self.LexingException(f"Invalid token: '{current_token + code[counter]}'.")
                token_stream.append(self.Token('number_lit', current_token))
                current_token = ''
            elif code[counter] == '"':
                current_token += code[counter]
                counter += 1
                while counter < code_length:
                    if code[counter] == '\\' and counter < len(code)-1:
                        current_token += code[counter]
                        counter += 1
                        current_token += code[counter]
                        counter += 1
                    elif code[counter] == '"':
                        current_token += code[counter]
                        counter += 1
                        token_stream.append(self.Token('string_lit', current_token))
                        current_token = ''
                        break
                    else:
                        current_token += code[counter]
                        counter += 1
            elif code[counter] == "'":
                current_token += code[counter]
                counter += 1
                if code[counter] == '\\':
                    current_token += code[counter]
                    counter += 1
                current_token += code[counter]
                counter += 1
                if code[counter] != "'":
                    raise self.LexingException(f"Chars in single quotes can only have one character.")
                current_token += code[counter]
                counter += 1
                token_stream.append(self.Token('char_lit', current_token))
                current_token = ''
            else:
                potential_tokens = get_potential_tokens(self.tokens_list, current_token)
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
        if current_token != '':
            token_stream.append(self.Token(current_token))
        token_stream.append(self.Token('eof'))
        return token_stream
