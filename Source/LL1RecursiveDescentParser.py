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

import HTML
import RDCodeRules
from Parser import Parser
from Tree import Tree


class LL1RecursiveDescentParser(Parser):
    start_rule_name: str
    code: list[str]
    parse_stack: list[ParseStackFrame]
    recursive_descent_rules: dict[str, dict[str, list[Production]]]
    highlighted_rule: Production
    start_rule: Production
    null_rule: Production

    class ParseStackFrame(Parser.BaseParseStackFrame):
        def __init__(self, node: Tree, rule: str, first_token: str) -> None:
            super().__init__(node)
            self.rule: str = rule
            self.first_token: str = first_token
            self.index: int = 0

    class Production:
        def __init__(self, name: str, terminal: bool) -> None:
            self.name: str = name
            self.terminal: bool = terminal
            self.code_line: int = -1

    class Rule:
        def __init__(self, name: str) -> None:
            self.name = name
            self.tokens: list[str] = []
            self.productions: list[LL1RecursiveDescentParser.Production] = []

    def __init__(self) -> None:
        self.recursive_descent_rules = {}
        self.highlighted_rule = self.null_rule = self.Production('', False)
        self.start_rule = self.Production('', False)
        self.languages: list[RDCodeRules.RDCodeRules] = RDCodeRules.RecursiveDescentCodeLanguages
        self.reset()

    def code_box_text(self) -> str:
        return HTML.CodeBox.make_html(self.code, self.highlighted_rule.code_line)

    def lines_of_code(self) -> int:
        return len(self.code) - 1

    def parse_stack_to_str(self) -> str:
        return ' '.join(map(lambda x: x.node.name, self.parse_stack))

    def generate_rules(self) -> None:
        new_recursive_descent_rules = {}

        # calculator language rules
        self.start_rule_name = 'program'
        program_rules = [self.Production('stmt_list', False), self.Production('<eof>', True), self.Production('', False)]
        new_recursive_descent_rules['program'] = {'<id>': program_rules, 'read': program_rules, 'write': program_rules,
                                                  '<eof>': program_rules, 'if': program_rules, 'while': program_rules}
        stmt_list_rules = [self.Production('stmt', False), self.Production('stmt_list', False), self.Production('', False)]
        new_recursive_descent_rules['stmt_list'] = {
            '<id>': stmt_list_rules, 'read': stmt_list_rules, 'write': stmt_list_rules,
            'if': stmt_list_rules, 'while': stmt_list_rules, 'end': [self.Production('', False)], '<eof>': [self.Production('', False)]}
        new_recursive_descent_rules['stmt'] = {
            '<id>': [self.Production('<id>', True), self.Production(':=', True),
                     self.Production('expr', False), self.Production('', False)],
            'read': [self.Production('read', True), self.Production('<id>', True), self.Production('', False)],
            'write': [self.Production('write', True), self.Production('expr', False), self.Production('', False)],
            'if': [self.Production('if', True), self.Production('cond', False),
                   self.Production('stmt_list', False), self.Production('end', True), self.Production('', False)],
            'while': [self.Production('while', True), self.Production('cond', False),
                      self.Production('stmt_list', False), self.Production('end', True), self.Production('', False)]}
        cond_rules = [self.Production('expr', False), self.Production('ro', False),
                      self.Production('expr', False), self.Production('', False)]
        new_recursive_descent_rules['cond'] = {'(': cond_rules, '<id>': cond_rules, '<i_lit>': cond_rules}
        expr_rules = [self.Production('term', False), self.Production('term_tail', False), self.Production('', False)]
        new_recursive_descent_rules['expr'] = {'(': expr_rules, '<id>': expr_rules, '<i_lit>': expr_rules}
        term_tail_rules = [self.Production('ao', False), self.Production('term', False),
                           self.Production('term_tail', False), self.Production('', False)]
        new_recursive_descent_rules['term_tail'] = {
            '+': term_tail_rules, '-': term_tail_rules, ')': [self.Production('', False)], '<id>': [self.Production('', False)],
            'read': [self.Production('', False)], 'write': [self.Production('', False)], '<eof>': [self.Production('', False)],
            'if': [self.Production('', False)], 'while': [self.Production('', False)], 'end': [self.Production('', False)],
            '=': [self.Production('', False)], '<>': [self.Production('', False)], '<': [self.Production('', False)],
            '>': [self.Production('', False)], '<=': [self.Production('', False)], '>=': [self.Production('', False)]}
        term_rules = [self.Production('factor', False), self.Production('factor_tail', False), self.Production('', False)]
        new_recursive_descent_rules['term'] = {'(': term_rules, '<id>': term_rules, '<i_lit>': term_rules}
        factor_tail_rules = [self.Production('mo', False), self.Production('factor', False),
                             self.Production('factor_tail', False), self.Production('', False)]
        new_recursive_descent_rules['factor_tail'] = {
            '*': factor_tail_rules, '/': factor_tail_rules, '+': [self.Production('', False)],
            '-': [self.Production('', False)], ')': [self.Production('', False)], '<id>': [self.Production('', False)],
            'read': [self.Production('', False)], 'write': [self.Production('', False)], '<eof>': [self.Production('', False)],
            'if': [self.Production('', False)], 'while': [self.Production('', False)], 'end': [self.Production('', False)],
            '=': [self.Production('', False)], '<>': [self.Production('', False)], '<': [self.Production('', False)],
            '>': [self.Production('', False)], '<=': [self.Production('', False)], '>=': [self.Production('', False)]}
        new_recursive_descent_rules['factor'] = {
            '<i_lit>': [self.Production('<i_lit>', True), self.Production('', False)],
            '<id>': [self.Production('<id>', True), self.Production('', False)],
            '(': [self.Production('(', True), self.Production('expr', False),
                  self.Production(')', True), self.Production('', False)]}
        new_recursive_descent_rules['ro'] = {
            '=': [self.Production('=', True), self.Production('', False)], '<>': [self.Production('<>', True), self.Production('', False)],
            '<': [self.Production('<', True), self.Production('', False)], '<=': [self.Production('<=', True), self.Production('', False)],
            '>': [self.Production('>', True), self.Production('', False)], '>=': [self.Production('>=', True), self.Production('', False)]}
        new_recursive_descent_rules['ao'] = {
            '+': [self.Production('+', True), self.Production('', False)], '-': [self.Production('-', True), self.Production('', False)]}
        new_recursive_descent_rules['mo'] = {
            '*': [self.Production('*', True), self.Production('', False)], '/': [self.Production('/', True), self.Production('', False)]}

        self.recursive_descent_rules = new_recursive_descent_rules
        self.make_code()

    def step(self) -> None:
        self.remove_highlight()
        if len(self.parse_stack) < 1:
            if self.current_node is None:
                # empty stack: start recursive descent
                self.tree = self.current_node = Tree(self.start_rule_name)
                self.highlight_line(self.start_rule)
                self.parse_stack.append(
                    self.ParseStackFrame(self.tree, self.start_rule_name, self.token_stream[0].name))
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
                if self.parse_stack[-1].index >= len(current_rule) - 1:
                    # made it to the end of rules list, exit function
                    self.current_node = self.parse_stack[-1].node
                    self.highlight_line(current_rule[-1])
                    self.parse_stack.pop()
                    if len(self.parse_stack) > 0:
                        self.parse_stack[-1].index += 1
                elif not current_rule[self.parse_stack[-1].index].terminal:
                    # descend rule
                    self.current_node = self.parse_stack[-1].node.add_child(
                        current_rule[self.parse_stack[-1].index].name)
                    self.highlight_line(current_rule[self.parse_stack[-1].index])
                    self.parse_stack.append(self.ParseStackFrame(
                        self.current_node, current_rule[self.parse_stack[-1].index].name, self.token_stream[0].name))
                else:
                    # match token rule
                    if current_rule[self.parse_stack[-1].index].name == self.token_stream[0].name:
                        self.current_node = self.parse_stack[-1].node.add_child(self.token_stream[0].image)
                        self.highlight_line(current_rule[self.parse_stack[-1].index])
                        self.token_stream.pop(0)
                        self.parse_stack[-1].index += 1
                    else:
                        self.current_node = self.parse_stack[-1].node.add_child("ERROR")
                        self.finished_parsing = True  # stop the parser

    def reset(self) -> None:
        self.tree = None
        self.current_node = None
        self.parse_stack = []
        self.token_stream = []
        self.finished_parsing = False
        self.line_to_move_scrollbar_to = -1
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
        self.code[-1] += (self.start_rule_name + language.end_of_main.split('\n')[0])
        self.start_rule.code_line = len(self.code) - 1
        self.code += language.end_of_main.split('\n')[1:]

        for rule_name, tokens in self.recursive_descent_rules.items():
            self.code.append(
                language.function_definition_beginning + rule_name + language.function_definition_end +
                (language.start_symbol_comment if self.start_rule_name == rule_name else ''))
            self.code.append(language.switch_beginning)
            steps_text_lists: dict[str, list[str]] = {}
            for token, steps_list in tokens.items():
                steps_text: str = ""
                for rule in steps_list[:-1]:
                    item = rule.name
                    steps_text += ((language.call_function_beginning + item + language.call_function_end if not rule.terminal
                                    else language.call_match_beginning + item + language.call_match_end) + '\n')
                steps_text = (language.skip_case + '\n') if steps_text == '' else steps_text
                if steps_text in steps_text_lists:
                    steps_text_lists[steps_text].append(token)
                else:
                    steps_text_lists[steps_text] = [token]
            for steps_list_text, token_list in steps_text_lists.items():
                rule_text: list[str] = [token.name for token in tokens[token_list[0]]]
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
            return_line: int = len(self.code)
            for _, list_ in tokens.items():
                list_[-1].code_line = return_line
            self.code += language.function_last_lines.split('\n')
        self.code.pop()

        if language.program_last_statements != '':
            self.code += language.program_last_statements.split('\n')

    def highlight_line(self, rule: Production) -> None:
        self.highlighted_rule = rule
        self.line_to_move_scrollbar_to = rule.code_line

    def remove_highlight(self) -> None:
        self.highlighted_rule = self.null_rule

    def update_code(self, index: int) -> None:
        self.make_code(index)
        if self.highlighted_rule is not None:
            self.highlight_line(self.highlighted_rule)
