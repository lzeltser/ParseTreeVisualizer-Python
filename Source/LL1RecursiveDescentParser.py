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
    rules: dict[str, list[Rule]]
    highlighted_rule: Production
    start_rule: Production
    null_rule: Production

    class ParseStackFrame(Parser.BaseParseStackFrame):
        def __init__(self, node: Tree, rule: LL1RecursiveDescentParser.Rule) -> None:
            super().__init__(node)
            self.rule: LL1RecursiveDescentParser.Rule = rule
            self.index: int = 0

    class Production:
        def __init__(self, name: str, match: bool) -> None:
            self.name: str = name
            self.match: bool = match
            self.code_line: int = -1

    class Rule:
        def __init__(self, tokens: list[str], productions: list[LL1RecursiveDescentParser.Production]) -> None:
            self.tokens: list[str] = tokens
            self.productions: list[LL1RecursiveDescentParser.Production] = productions

        def __contains__(self, item: str) -> bool:
            return item in self.tokens

    def __init__(self) -> None:
        self.rules = {}
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
        self.start_rule_name = 'program'
        self.rules = {
            'program': [], 'stmt_list': [], 'stmt': [], 'cond': [], 'expr': [], 'term_tail': [],
            'term': [], 'factor_tail': [], 'factor': [], 'ro': [], 'ao': [], 'mo': []
        }
        self.rules['program'].append(self.Rule(['<id>', 'read', 'write', '<eof>', 'if', 'while'], [
            self.Production('stmt_list', False), self.Production('<eof>', True), self.Production('', True)
        ]))
        self.rules['stmt_list'].append(self.Rule(['<id>', 'read', 'write', 'if', 'while'], [
            self.Production('stmt', False), self.Production('stmt_list', False), self.Production('', True)
        ]))
        self.rules['stmt_list'].append(self.Rule(['end', '<eof>'], [self.Production('', True)]))
        self.rules['stmt'].append(self.Rule(['<id>'], [
            self.Production('<id>', True), self.Production(':=', True), self.Production('expr', False),
            self.Production('', True)
        ]))
        self.rules['stmt'].append(self.Rule(['read'], [
            self.Production('read', True), self.Production('<id>', True), self.Production('', True)
        ]))
        self.rules['stmt'].append(self.Rule(['write'], [
            self.Production('write', True), self.Production('expr', False), self.Production('', True)
        ]))
        self.rules['stmt'].append(self.Rule(['if'], [
            self.Production('if', True), self.Production('cond', False), self.Production('stmt_list', False),
            self.Production('end', True), self.Production('', True)
        ]))
        self.rules['stmt'].append(self.Rule(['while'], [
            self.Production('while', True), self.Production('cond', False), self.Production('stmt_list', False),
            self.Production('end', True), self.Production('', True)
        ]))
        self.rules['cond'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Production('expr', False), self.Production('ro', False), self.Production('expr', False),
            self.Production('', True)
        ]))
        self.rules['expr'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Production('term', False), self.Production('term_tail', False), self.Production('', True)
        ]))
        self.rules['term_tail'].append(self.Rule(['+', '-'], [
            self.Production('ao', False), self.Production('term', False), self.Production('term_tail', False),
            self.Production('', True)
        ]))
        self.rules['term_tail'].append(self.Rule(['<id>', 'read', 'write', '<eof>', 'if', 'while', 'end',
                                                  '=', '<>', '<', '>', '<=', '>='], [self.Production('', True)]))
        self.rules['term'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Production('factor', False), self.Production('factor_tail', False), self.Production('', True)
        ]))
        self.rules['factor_tail'].append(self.Rule(['*', '/'], [
            self.Production('mo', False), self.Production('factor', False), self.Production('factor_tail', False),
            self.Production('', True)
        ]))
        self.rules['factor_tail'].append(self.Rule(['+', '-', ')', '<id>', 'read', 'write', '<eof>', 'if', 'while',
                                                    'end', '=', '<>', '<', '>', '<=', '>='], [self.Production('', True)]))
        self.rules['factor'].append(self.Rule(['<i_lit>'], [
            self.Production('<i_lit>', True), self.Production('', True)
        ]))
        self.rules['factor'].append(self.Rule(['<id>'], [
            self.Production('<id>', True), self.Production('', True)
        ]))
        self.rules['factor'].append(self.Rule(['('], [
            self.Production('(', True), self.Production('<expr>', False), self.Production(')', True),
            self.Production('', True)
        ]))
        self.rules['ro'].append(self.Rule(['='], [self.Production('=', True), self.Production('', True)]))
        self.rules['ro'].append(self.Rule(['<>'], [self.Production('<>', True), self.Production('', True)]))
        self.rules['ro'].append(self.Rule(['<'], [self.Production('<', True), self.Production('', True)]))
        self.rules['ro'].append(self.Rule(['<='], [self.Production('<=', True), self.Production('', True)]))
        self.rules['ro'].append(self.Rule(['>'], [self.Production('>', True), self.Production('', True)]))
        self.rules['ro'].append(self.Rule(['>='], [self.Production('>=', True), self.Production('', True)]))
        self.rules['ao'].append(self.Rule(['+'], [self.Production('+', True), self.Production('', True)]))
        self.rules['ao'].append(self.Rule(['-'], [self.Production('-', True), self.Production('', True)]))
        self.rules['mo'].append(self.Rule(['*'], [self.Production('*', True), self.Production('', True)]))
        self.rules['mo'].append(self.Rule(['/'], [self.Production('/', True), self.Production('', True)]))

        self.make_code()

    def step(self) -> None:
        self.remove_highlight()
        if len(self.parse_stack) < 1:
            if len(self.token_stream) > 0:
                # empty stack: start recursive descent
                self.tree = self.current_node = Tree(self.start_rule_name)
                self.highlight_line(self.start_rule)
                self.parse_stack.append(
                    self.ParseStackFrame(self.tree, self.find_rule(self.start_rule_name, self.token_stream[0].name)))
            else:
                # empty stack: finish recursive descent
                self.current_node = self.tree
                self.finished_parsing = True
        else:
            current_rule: LL1RecursiveDescentParser.Rule = self.parse_stack[-1].rule
            if current_rule is None:
                self.current_node = self.parse_stack[-1].node.add_child("ERROR")
                self.finished_parsing = True
            else:
                if self.parse_stack[-1].index >= len(current_rule.productions) - 1:
                    # made it to the end of rules list, exit function
                    self.current_node = self.parse_stack[-1].node
                    self.highlight_line(current_rule.productions[-1])
                    self.parse_stack.pop()
                    if len(self.parse_stack) > 0:
                        self.parse_stack[-1].index += 1
                elif not current_rule.productions[self.parse_stack[-1].index].match:
                    # descend rule
                    self.current_node = self.parse_stack[-1].node.add_child(
                        current_rule.productions[self.parse_stack[-1].index].name)
                    self.highlight_line(current_rule.productions[self.parse_stack[-1].index])
                    self.parse_stack.append(self.ParseStackFrame(
                        self.current_node, self.find_rule(current_rule.productions[self.parse_stack[-1].index].name,
                                                          self.token_stream[0].name)))
                else:
                    # match token rule
                    if current_rule.productions[self.parse_stack[-1].index].name == self.token_stream[0].name:
                        self.current_node = self.parse_stack[-1].node.add_child(self.token_stream[0].image)
                        self.highlight_line(current_rule.productions[self.parse_stack[-1].index])
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

    def find_rule(self, current_function: str, next_token: str) -> Rule:
        for rule in self.rules[current_function]:
            if next_token in rule:
                return rule

    def make_code(self, language_index: int = 0) -> None:  # pseudocode is the default option
        language: RDCodeRules.RDCodeRules = self.languages[language_index]
        rule_counter: int = 1
        self.code = []

        if language.program_first_statements != '':
            self.code += language.program_first_statements.split('\n')
        if language.declare_functions:
            for declaration in self.rules:
                self.code.append(
                    language.function_declaration_beginning + declaration + language.function_declaration_end)
            self.code.append('')
            self.code.append('')
        self.code += language.first_code.split('\n')
        self.code[-1] += (self.start_rule_name + language.end_of_main.split('\n')[0])
        self.start_rule.code_line = len(self.code) - 1
        self.code += language.end_of_main.split('\n')[1:]

        for rule_name, rules in self.rules.items():
            self.code.append(
                language.function_definition_beginning + rule_name + language.function_definition_end +
                (language.start_symbol_comment if self.start_rule_name == rule_name else ''))
            self.code.append(language.switch_beginning)

            for rule in rules:
                rule_text: list[str] = [production.name for production in rule.productions]
                rule_text = ['epsilon'] if rule_text == [] else rule_text
                self.code += \
                    (language.case_beginning + language.case_separator.join(rule.tokens) + language.case_end +
                     f"{language.comment_begin}P{rule_counter}: {rule_name} -> "
                     f"{' '.join(rule_text)}{language.comment_end}").split('\n')
                rule_counter += 1
                for i, production in enumerate(rule.productions):
                    production.code_line = i + len(self.code)

                steps_text: str = ''
                for production in rule.productions[:-1]:
                    steps_text += ((language.call_function_beginning + production.name + language.call_function_end
                                    if not production.match else
                                    language.call_match_beginning + production.name + language.call_match_end) + '\n')
                steps_text = (language.skip_case + '\n') if steps_text == '' else steps_text

                self.code += steps_text.split('\n')[:-1]
                if language.end_of_case != '':
                    self.code += language.end_of_case.split('\n')

            self.code += language.switch_default.split('\n')
            return_line: int = len(self.code)
            for rule in rules:
                rule.productions[-1].code_line = return_line

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
