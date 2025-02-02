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
import RDCodeRules
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

    @staticmethod
    def iterable_attributes_to_str(iterable: Iterable, *args: tuple[str, ...] | str, separator: str = ' ') -> str:
        stream = ''
        for item in iterable:
            for arg in args:
                if type(arg) == str:
                    obj = getattr(item, arg)
                else:
                    obj = item
                    for attr in arg:
                        obj = getattr(obj, attr)
                stream += str(obj)
                stream += separator
        return '' if stream == '' else stream[:-len(separator)]

    def token_stream_to_str(self) -> str:
        return self.iterable_attributes_to_str(self.token_stream, "image")


class TableDrivenParser(Parser):
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
        HTML.Code.highlight_line(self.code[line])
        self.last_highlighted_line = line

    def remove_highlight(self) -> None:
        if 0 <= self.last_highlighted_line < len(self.code):
            HTML.Code.remove_highlight(self.code[self.last_highlighted_line])


class LLRecursiveDescentParser(Parser):
    parse_stack: list[RDStackFrame]
    recursive_descent_rules: dict[str, dict[str, list[RDRule]]]
    highlighted_rule: RDRule | None
    start_rule: RDRule

    class RDStackFrame(Parser.ParseStackFrame):
        def __init__(self, node: Tree, rule: str, first_token: str) -> None:
            super().__init__(node)
            self.rule: str = rule
            self.first_token: str = first_token
            self.index: int = 0

    class RDRule:
        def __init__(self, item: str, descend: bool) -> None:
            self.item: str = item
            self.descend: bool = descend
            # True: item is another rule, descend to it
            # False: item is a token, match it
            self.code_line: int = 0  # line in the rules list that will get highlighted

    def __init__(self) -> None:
        self.starting_rule: str = ''

        self.highlighted_rule = None
        self.recursive_descent_rules = {}
        self.start_rule = self.RDRule('', True)
        self.languages: list[RDCodeRules.RDCodeRules] = RDCodeRules.RecursiveDescentCodeLanguages
        super().__init__()

    def generate_rules(self) -> None:
        new_recursive_descent_rules = {}

        # calculator language rules
        self.starting_rule = 'program'
        empty_list = []
        program_rules = [self.RDRule('stmt_list', True), self.RDRule('<eof>', False)]
        new_recursive_descent_rules['program'] = {'<id>': program_rules, 'read': program_rules, 'write': program_rules,
                                                  '<eof>': program_rules, 'if': program_rules, 'while': program_rules}
        stmt_list_rules = [self.RDRule('stmt', True), self.RDRule('stmt_list', True)]
        new_recursive_descent_rules['stmt_list'] = {
            '<id>': stmt_list_rules, 'read': stmt_list_rules, 'write': stmt_list_rules,
            'if': stmt_list_rules, 'while': stmt_list_rules, 'end': empty_list, '<eof>': empty_list}
        new_recursive_descent_rules['stmt'] = {
            '<id>': [self.RDRule('<id>', False), self.RDRule(':=', False),
                     self.RDRule('expr', True)],
            'read': [self.RDRule('read', False), self.RDRule('<id>', False)],
            'write': [self.RDRule('write', False), self.RDRule('expr', True)],
            'if': [self.RDRule('if', False), self.RDRule('cond', True),
                   self.RDRule('stmt_list', True), self.RDRule('end', False)],
            'while': [self.RDRule('while', False), self.RDRule('cond', True),
                      self.RDRule('stmt_list', True), self.RDRule('end', False)]}
        cond_rules = [self.RDRule('expr', True), self.RDRule('ro', True),
                      self.RDRule('expr', True)]
        new_recursive_descent_rules['cond'] = {'(': cond_rules, '<id>': cond_rules, '<i_lit>': cond_rules}
        expr_rules = [self.RDRule('term', True), self.RDRule('term_tail', True)]
        new_recursive_descent_rules['expr'] = {'(': expr_rules, '<id>': expr_rules, '<i_lit>': expr_rules}
        term_tail_rules = [self.RDRule('ao', True), self.RDRule('term', True),
                           self.RDRule('term_tail', True)]
        new_recursive_descent_rules['term_tail'] = {
            '+': term_tail_rules, '-': term_tail_rules, ')': empty_list, '<id>': empty_list, 'read': empty_list,
            'write': empty_list, '<eof>': empty_list, 'if': empty_list, 'while': empty_list, 'end': empty_list,
            '=': empty_list, '<>': empty_list, '<': empty_list, '>': empty_list, '<=': empty_list, '>=': empty_list}
        term_rules = [self.RDRule('factor', True), self.RDRule('factor_tail', True)]
        new_recursive_descent_rules['term'] = {'(': term_rules, '<id>': term_rules, '<i_lit>': term_rules}
        factor_tail_rules = [self.RDRule('mo', True), self.RDRule('factor', True),
                             self.RDRule('factor_tail', True)]
        new_recursive_descent_rules['factor_tail'] = {
            '*': factor_tail_rules, '/': factor_tail_rules, '+': empty_list, '-': empty_list, ')': empty_list,
            '<id>': empty_list, 'read': empty_list, 'write': empty_list, '<eof>': empty_list, 'if': empty_list,
            'while': empty_list, 'end': empty_list, '=': empty_list, '<>': empty_list, '<': empty_list, '>': empty_list,
            '<=': empty_list, '>=': empty_list}
        new_recursive_descent_rules['factor'] = {
            '<i_lit>': [self.RDRule('<i_lit>', False)],
            '<id>': [self.RDRule('<id>', False)],
            '(': [self.RDRule('(', False), self.RDRule('expr', True),
                  self.RDRule(')', False)]}
        new_recursive_descent_rules['ro'] = {
            '=': [self.RDRule('=', False)], '<>': [self.RDRule('<>', False)],
            '<': [self.RDRule('<', False)], '<=': [self.RDRule('<=', False)],
            '>': [self.RDRule('>', False)], '>=': [self.RDRule('>=', False)]}
        new_recursive_descent_rules['ao'] = {
            '+': [self.RDRule('+', False)], '-': [self.RDRule('-', False)]}
        new_recursive_descent_rules['mo'] = {
            '*': [self.RDRule('*', False)], '/': [self.RDRule('/', False)]}

        self.recursive_descent_rules = new_recursive_descent_rules
        self.make_code()

    def step(self) -> None:
        if len(self.parse_stack) < 1:
            if self.current_node is None:
                # empty stack: start recursive descent
                self.tree = self.current_node = Tree(self.starting_rule)
                self.highlight_line(self.start_rule)
                self.parse_stack.append(
                    self.RDStackFrame(self.tree, self.starting_rule, self.token_stream[0].name))
            else:
                # empty stack: finish recursive descent
                self.current_node = self.tree
                self.finished_parsing = True
        else:
            # lookup which rule to use based on the next token
            try:
                current_rule = \
                    self.recursive_descent_rules[self.parse_stack[-1].rule][self.parse_stack[-1].first_token]
            except KeyError:
                self.current_node = self.parse_stack[-1].node.add_child("ERROR")
                self.finished_parsing = True  # stop the parser
            else:
                if self.parse_stack[-1].index >= len(current_rule):
                    # made it to the end of rules list, exit function
                    self.remove_highlight()
                    self.current_node = self.parse_stack[-1].node
                    self.parse_stack.pop()
                    if len(self.parse_stack) > 0:
                        self.parse_stack[-1].index += 1
                elif current_rule[self.parse_stack[-1].index].descend:
                    # descend rule
                    self.current_node = self.parse_stack[-1].node.add_child(
                        current_rule[self.parse_stack[-1].index].item)
                    self.highlight_line(current_rule[self.parse_stack[-1].index])
                    self.parse_stack.append(self.RDStackFrame(
                        self.current_node, current_rule[self.parse_stack[-1].index].item, self.token_stream[0].name))
                else:
                    # match token rule
                    if current_rule[self.parse_stack[-1].index].item == self.token_stream[0].name:
                        self.current_node = self.parse_stack[-1].node.add_child(self.token_stream[0].image)
                        self.highlight_line(
                            current_rule[self.parse_stack[-1].index])
                        self.token_stream.pop(0)
                        self.parse_stack[-1].index += 1
                    else:
                        self.current_node = self.parse_stack[-1].node.add_child("ERROR")
                        self.finished_parsing = True  # stop the parser

    def parse_stack_to_str(self) -> str:
        return self.iterable_attributes_to_str(self.parse_stack, ("node", "name"))

    def reset(self) -> None:
        super().reset()
        self.remove_highlight()

    def make_code(self, language_index: int = 0) -> None:  # pseudocode is the default option
        language: RDCodeRules.RDCodeRules = self.languages[language_index]
        rule_counter: int = 1
        self.code = []

        if language.program_first_statements != '':
            self.code += language.program_first_statements.split('\n')
        if language.declare_functions:
            for declaration in self.recursive_descent_rules:
                self.code.append(
                    language.function_declaration_beginning + declaration + language.function_declaration_end)
            self.code.append('')
            self.code.append('')
        self.code += language.first_code.split('\n')
        self.code[-1] += (self.starting_rule + language.end_of_main.split('\n')[0])
        self.start_rule.code_line = len(self.code) - 1
        self.code += language.end_of_main.split('\n')[1:]

        for rule_name, tokens in self.recursive_descent_rules.items():
            self.code.append(
                language.function_definition_beginning + rule_name + language.function_definition_end +
                (language.start_symbol_comment if self.starting_rule == rule_name else '')+language.function_last_line)
            self.code.append(language.switch_beginning)
            steps_text_lists: dict[str, list[str]] = {}
            for token, steps_list in tokens.items():
                steps_text: str = ""
                for rule in steps_list:
                    item = rule.item
                    steps_text += ((language.call_function_beginning + item + language.call_function_end if rule.descend
                                    else language.call_match_beginning + item + language.call_match_end) + '\n')
                steps_text = (language.skip_case + '\n') if steps_text == '' else steps_text
                if steps_text in steps_text_lists:
                    steps_text_lists[steps_text].append(token)
                else:
                    steps_text_lists[steps_text] = [token]
            for steps_list_text, token_list in steps_text_lists.items():
                rule_text: list[str] = [token.item for token in tokens[token_list[0]]]
                rule_text = ['epsilon'] if rule_text == [] else rule_text
                self.code += \
                    (language.case_beginning + language.case_separator.join(token_list) + language.case_end +
                        f"{language.comment_begin}P{rule_counter}: {rule_name} -> "
                        f"{' '.join(rule_text)}{language.comment_end}").split('\n')
                rule_counter += 1
                for token in token_list:
                    for i, step in enumerate(tokens[token]):
                        step.code_line = i + len(self.code)
                self.code += steps_list_text.split('\n')[:-1]
                if language.end_of_case != '':
                    self.code += language.end_of_case.split('\n')
            self.code += language.switch_default.split('\n')
            self.code += language.function_last_line.split('\n')
        self.code.pop()

        if language.program_last_statements != '':
            self.code += language.program_last_statements.split('\n')

    def highlight_line(self, rule: RDRule) -> None:
        self.remove_highlight()
        self.code[rule.code_line] = (HTML.Code.highlight_line(self.code[rule.code_line]))
        self.highlighted_rule = rule
        self.last_highlighted_line = rule.code_line

    def remove_highlight(self) -> None:
        if self.highlighted_rule is not None:
            self.code[self.highlighted_rule.code_line] = (
                HTML.Code.remove_highlight(self.code[self.highlighted_rule.code_line]))
            self.highlighted_rule = None

    def update_code(self, index: int) -> None:
        self.make_code(index)
        if self.highlighted_rule is not None:
            self.highlight_line(self.highlighted_rule)


class LLTableDrivenParser(TableDrivenParser):
    parse_stack: list[LLStackFrame]
    ll_table_rules: list[list[LLTableRule]]

    class LLStackFrame(Parser.ParseStackFrame):
        def __init__(self, node: Tree, terminal: bool, rule: str) -> None:
            super().__init__(node)
            self.terminal: bool = terminal
            self.rule: str = rule

    class LLTableRule:
        def __init__(self, terminal: bool, item: str) -> None:
            self.terminal: bool = terminal
            self.item: str = item

    def __init__(self) -> None:
        super().__init__()
        self.ll_rule_list: list[str] = []
        self.ll_token_list: list[str] = []
        self.table: list[list[int]] = []

    def table_height(self) -> int:
        return len(self.table)

    def table_width(self) -> int:
        return len(self.table[0])

    def table_top_row(self) -> Iterable[str]:
        return self.ll_token_list

    def table_left_col(self) -> Iterable[str]:
        return self.ll_rule_list

    def get_table(self) -> Iterable[Iterable[str]]:
        return [['' if i < 0 else str(i) for i in row] for row in self.table]

    def push_rules_to_stack(self, rules: list[LLTableRule]) -> None:
        for rule in reversed(rules):
            self.parse_stack.append(self.LLStackFrame(
                self.current_node.add_child(rule.item, 0), rule.terminal, rule.item))

    def generate_rules(self) -> None:
        self.ll_rule_list = ['program', 'stmt_list', 'stmt', 'cond', 'expr', 'term_tail',
                             'term', 'factor_tail', 'factor', 'ro', 'ao', 'mo']
        self.ll_token_list = ['<id>', '<i_lit>', 'read', 'write', 'if', 'while', 'end', ':=', '(',
                              ')', '+', '-', '*', '/', '=', '<>', '<', '<=', '>', '>=', '<eof>']
        self.table = [
            [+1, -1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 , 1],
            [+2, -1,  2,  2,  2,  2,  3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  3],
            [+4, -1,  5,  6,  7,  8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [+9,  9, -1, -1, -1, -1, -1, -1,  9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [10, 10, -1, -1, -1, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [12, -1, 12, 12, 12, 12, 12, -1, -1, 12, 11, 11, -1, -1, 12, 12, 12, 12, 12, 12, 12],
            [13, 13, -1, -1, -1, -1, -1, -1, 13, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [15, -1, 15, 15, 15, 15, 15, -1, -1, 15, 15, 15, 14, 14, 15, 15, 15, 15, 15, 15, 15],
            [17, 16, -1, -1, -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 19, 20, 21, 22, 23, 24, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 25, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 27, 28, -1, -1, -1, -1, -1, -1, -1]
        ]
        self.ll_table_rules = [
            [self.LLTableRule(False, 'program')],
            [self.LLTableRule(False, 'stmt_list'), self.LLTableRule(True, '<eof>')],
            [self.LLTableRule(False, 'stmt'), self.LLTableRule(False, 'stmt_list')],
            [],
            [self.LLTableRule(True, '<id>'), self.LLTableRule(True, ':='), self.LLTableRule(False, 'expr')],
            [self.LLTableRule(True, 'read'), self.LLTableRule(True, '<id>')],
            [self.LLTableRule(True, 'write'), self.LLTableRule(False, 'expr')],
            [self.LLTableRule(True, 'if'), self.LLTableRule(False, 'cond'),
             self.LLTableRule(False, 'stmt_list'), self.LLTableRule(True, 'end')],
            [self.LLTableRule(True, 'while'), self.LLTableRule(False, 'cond'),
             self.LLTableRule(False, 'stmt_list'), self.LLTableRule(True, 'end')],
            [self.LLTableRule(False, 'expr'), self.LLTableRule(False, 'ro'), self.LLTableRule(False, 'expr')],
            [self.LLTableRule(False, 'term'), self.LLTableRule(False, 'term_tail')],
            [self.LLTableRule(False, 'ao'), self.LLTableRule(False, 'term'), self.LLTableRule(False, 'term_tail')],
            [],
            [self.LLTableRule(False, 'factor'), self.LLTableRule(False, 'factor_tail')],
            [self.LLTableRule(False, 'mo'), self.LLTableRule(False, 'factor'), self.LLTableRule(False, 'factor_tail')],
            [],
            [self.LLTableRule(True, '<i_lit>')], [self.LLTableRule(True, '<id>')],
            [self.LLTableRule(True, '('), self.LLTableRule(False, 'expr'), self.LLTableRule(True, ')')],
            [self.LLTableRule(True, '=')], [self.LLTableRule(True, '<>')], [self.LLTableRule(True, '<')],
            [self.LLTableRule(True, '<=')], [self.LLTableRule(True, '>')], [self.LLTableRule(True, '>=')],
            [self.LLTableRule(True, '+')], [self.LLTableRule(True, '-')],
            [self.LLTableRule(True, '*')], [self.LLTableRule(True, '/')]
        ]

    def step(self) -> None:
        if len(self.parse_stack) < 1:
            if self.current_node is None:  # empty stack: push start symbol
                self.tree = self.current_node = Tree(self.ll_table_rules[0][0].item)
                self.parse_stack.append(
                    self.LLStackFrame(self.tree, self.ll_table_rules[0][0].terminal, self.current_node.name))
            else:  # empty stack: finish parse
                self.curr_highlighted_row = self.curr_highlighted_col = self.last_highlighted_row = self.last_highlighted_col = -1
                self.current_node = self.tree
                self.finished_parsing = True
        else:
            frame = self.parse_stack.pop()
            self.current_node = frame.node
            if frame.terminal:  # terminal, match token
                self.curr_highlighted_row = self.curr_highlighted_col = -1
                if frame.rule == self.token_stream[0].name:
                    self.current_node.name = self.token_stream.pop(0).image
                else:
                    self.current_node.name = "ERROR"
                    self.finished_parsing = True
            else:  # non-terminal, push to stack
                self.curr_highlighted_row = self.last_highlighted_row = self.ll_rule_list.index(frame.rule)
                self.curr_highlighted_col = self.last_highlighted_col = self.ll_token_list.index(self.token_stream[0].name)
                rule_index: int = self.table[self.curr_highlighted_row][self.curr_highlighted_col]
                if rule_index < 0:
                    self.current_node = self.current_node.add_child("ERROR")
                    self.finished_parsing = True
                else:  # rule exists
                    self.push_rules_to_stack(self.ll_table_rules[rule_index])

    def parse_stack_to_str(self) -> str:
        return self.iterable_attributes_to_str(self.parse_stack, ("node", "name"))


class LRTableDrivenParser(TableDrivenParser):
    parse_stack: list[LRStackFrame]
    table: list[list[LRTableEntry]]
    lr_production_list: list[LRProduction]

    class LRStackFrame(Parser.ParseStackFrame):
        def __init__(self, node: Tree, symbol: str, state: int) -> None:
            super().__init__(node)
            self.symbol: str = symbol
            self.state: int = state

    class LRTableEntry:
        def __init__(self, action: str, target: int) -> None:
            self.action: str = action
            # s: shift
            # r: reduce
            # b: shift and reduce
            # blank: parse error
            self.target: int = target

        def __str__(self) -> str:
            return self.action + str(self.target)

    class LRProduction:
        def __init__(self, left_side: str, right_side_len: int) -> None:
            self.left_side: str = left_side
            self.right_side_len: int = right_side_len

    def __init__(self) -> None:
        super().__init__()

        self.table = []
        self.lr_production_list = []
        self.lr_symbol_list: list[str] = []
        self.tree_is_first_in_token_stream: bool = False

    def table_height(self) -> int:
        return len(self.table)

    def table_width(self) -> int:
        return len(self.table[0])

    def table_top_row(self) -> Iterable[str]:
        return self.lr_symbol_list

    def table_left_col(self) -> Iterable[str]:
        return map(str, range(len(self.table)))

    def get_table(self) -> Iterable[Iterable[str]]:
        return [['' if str(i) == '-1' else str(i) for i in row] for row in self.table]

    def generate_rules(self) -> None:
        self.lr_symbol_list = ['stmt_list', 'stmt', 'expr', 'term', 'factor', 'ao', 'mo', '<id>',
                               '<i_lit>', 'read', 'write', ':=', '(', ')', '+', '-', '*', '/', '<eof>']
        be = self.LRTableEntry('', -1)  # blank entry
        self.table = [
            [self.LRTableEntry('s', 2), self.LRTableEntry('b', 3), be, be, be, be, be, self.LRTableEntry('s', 3),
             be, self.LRTableEntry('s', 1), self.LRTableEntry('s', 4), be, be, be, be, be, be, be, be],
            [be, be, be, be, be, be, be, self.LRTableEntry('b', 5), be, be, be, be, be, be, be, be, be, be, be],
            [be, self.LRTableEntry('b', 2), be, be, be, be, be, self.LRTableEntry('s', 3), be,
             self.LRTableEntry('s', 1), self.LRTableEntry('s', 4), be, be, be, be, be, be, be,
             self.LRTableEntry('b', 1)],
            [be, be, be, be, be, be, be, be, be, be, be, self.LRTableEntry('s', 5), be, be, be, be, be, be, be],
            [be, be, self.LRTableEntry('s', 6), self.LRTableEntry('s', 7), self.LRTableEntry('b', 9), be, be,
             self.LRTableEntry('b', 12), self.LRTableEntry('b', 13), be, be, be, self.LRTableEntry('s', 8),
             be, be, be, be, be, be],
            [be, be, self.LRTableEntry('s', 9), self.LRTableEntry('s', 7), self.LRTableEntry('b', 9), be, be,
             self.LRTableEntry('b', 12), self.LRTableEntry('b', 13), be, be, be, self.LRTableEntry('s', 8),
             be, be, be, be, be, be],
            [be, be, be, be, be, self.LRTableEntry('s', 10), be, self.LRTableEntry('r', 6), be,
             self.LRTableEntry('r', 6), self.LRTableEntry('r', 6), be, be, be, self.LRTableEntry('b', 14),
             self.LRTableEntry('b', 15), be, be, self.LRTableEntry('r', 6)],
            [be, be, be, be, be, be, self.LRTableEntry('s', 11), self.LRTableEntry('r', 7), be,
             self.LRTableEntry('r', 7), self.LRTableEntry('r', 7), be, be, self.LRTableEntry('r', 7),
             self.LRTableEntry('r', 7), self.LRTableEntry('r', 7), self.LRTableEntry('b', 16),
             self.LRTableEntry('b', 17), self.LRTableEntry('r', 7)],
            [be, be, self.LRTableEntry('s', 12), self.LRTableEntry('s', 7), self.LRTableEntry('b', 9), be, be,
             self.LRTableEntry('b', 12), self.LRTableEntry('b', 13), be, be, be, self.LRTableEntry('s', 8),
             be, be, be, be, be, be],
            [be, be, be, be, be, self.LRTableEntry('s', 10), be, self.LRTableEntry('r', 4), be,
             self.LRTableEntry('r', 4), self.LRTableEntry('r', 4), be, be, be, self.LRTableEntry('b', 14),
             self.LRTableEntry('b', 15), be, be, self.LRTableEntry('r', 4)],
            [be, be, be, self.LRTableEntry('s', 13), self.LRTableEntry('b', 9), be, be, self.LRTableEntry('b', 12),
             self.LRTableEntry('b', 13), be, be, be, self.LRTableEntry('s', 8), be, be, be, be, be, be],
            [be, be, be, be, self.LRTableEntry('b', 10), be, be, self.LRTableEntry('b', 12), self.LRTableEntry('b', 13),
             be, be, be, self.LRTableEntry('s', 8), be, be, be, be, be, be],
            [be, be, be, be, be, self.LRTableEntry('s', 10), be, be, be, be, be, be, be, self.LRTableEntry('b', 11),
             self.LRTableEntry('b', 14), self.LRTableEntry('b', 15), be, be, be],
            [be, be, be, be, be, be, self.LRTableEntry('s', 11), self.LRTableEntry('r', 8), be,
             self.LRTableEntry('r', 8), self.LRTableEntry('r', 8), be, be, self.LRTableEntry('r', 8),
             self.LRTableEntry('r', 8), self.LRTableEntry('r', 8), self.LRTableEntry('b', 16),
             self.LRTableEntry('b', 17), self.LRTableEntry('r', 8)]
        ]
        self.lr_production_list = [
            None, self.LRProduction('program', 2), self.LRProduction('stmt_list', 2),
            self.LRProduction('stmt_list', 1), self.LRProduction('stmt', 3), self.LRProduction('stmt', 2),
            self.LRProduction('stmt', 2), self.LRProduction('expr', 1), self.LRProduction('expr', 3),
            self.LRProduction('term', 1), self.LRProduction('term', 3), self.LRProduction('factor', 3),
            self.LRProduction('factor', 1), self.LRProduction('factor', 1), self.LRProduction('ao', 1),
            self.LRProduction('ao', 1), self.LRProduction('mo', 1), self.LRProduction('mo', 1)
        ]

    def step(self) -> None:
        if len(self.parse_stack) < 1:
            self.tree = self.current_node = Tree("")
            self.parse_stack.append(self.LRStackFrame(self.tree, "", 0))
        elif self.token_stream[0].name == self.lr_production_list[1].left_side and self.parse_stack[-1].state == 0:
            self.curr_highlighted_row = self.curr_highlighted_col = -1
            self.current_node = self.tree[0]
            self.finished_parsing = True
        else:
            current_symbol: str = self.token_stream[0].name
            self.curr_highlighted_row = self.parse_stack[-1].state
            self.curr_highlighted_col = self.lr_symbol_list.index(current_symbol)
            rule = self.table[self.curr_highlighted_row][self.curr_highlighted_col]
            match rule.action:
                case 's':  # shift
                    self.token_stream.pop(0)
                    self.current_node = self.tree[-1] if self.tree_is_first_in_token_stream else self.tree.add_child(current_symbol)
                    self.tree_is_first_in_token_stream = False
                    self.parse_stack.append(self.LRStackFrame(self.current_node, current_symbol, rule.target))
                case 'r':  # reduce
                    production = self.lr_production_list[rule.target]
                    self.token_stream.insert(0, self.Token(production.left_side))
                    self.tree_is_first_in_token_stream = True
                    popped_nodes: list[Tree] = []
                    for _ in range(production.right_side_len):
                        self.parse_stack.pop()
                        popped_nodes.insert(0, self.tree.remove_last_child())
                    self.current_node = self.tree.add_child(production.left_side, children_list=popped_nodes)
                case 'b':  # shift then reduce
                    self.token_stream.pop(0)
                    production = self.lr_production_list[rule.target]
                    self.token_stream.insert(0, self.Token(production.left_side))
                    popped_nodes: list[Tree] = []
                    for _ in range(production.right_side_len - 1):
                        self.parse_stack.pop()
                        popped_nodes.insert(0, self.tree.remove_last_child())
                    if self.tree_is_first_in_token_stream:
                        popped_nodes.insert(0, self.tree.remove_last_child())
                        self.current_node = self.tree.add_child(production.left_side, children_list=popped_nodes)
                    else:
                        self.current_node = self.tree.add_child(production.left_side, children_list=popped_nodes)
                        self.current_node.add_child(current_symbol)
                    self.tree_is_first_in_token_stream = True
                case _:  # parse error
                    self.current_node = self.tree.add_child("ERROR")
                    self.finished_parsing = True

    def parse_stack_to_str(self) -> str:
        return self.iterable_attributes_to_str(self.parse_stack, ("node", "name"), "state")

    def reset(self) -> None:
        super().reset()
        self.tree_is_first_in_token_stream = False
