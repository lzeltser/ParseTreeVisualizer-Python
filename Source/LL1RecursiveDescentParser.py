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
from enum import IntEnum, auto

import HTML
import RDCodeRules
from Parser import Parser
from Tree import Tree


class LL1RecursiveDescentParser(Parser):
    start_symbol_name: str
    code: list[str]
    parse_stack: list[ParseStackFrame]
    rules: dict[str, list[Rule]]
    highlighted_rule: Action
    start_rule: Action
    null_rule: Action

    class ParseStackFrame(Parser.BaseParseStackFrame):
        def __init__(self, node: Tree, rule: LL1RecursiveDescentParser.Rule) -> None:
            super().__init__(node)
            self.rule: LL1RecursiveDescentParser.Rule = rule
            self.index: int = 0

        def current_action(self) -> LL1RecursiveDescentParser.Action:
            return self.rule[self.index]

        def should_return(self) -> bool:
            return self.index >= len(self.rule) - 1

    class ActionType(IntEnum):
        Descend = auto()
        Match = auto()
        Nothing = auto()  # for the production at the end of every rule meant to highlight the return line

    class Action:
        def __init__(self, name: str, action: LL1RecursiveDescentParser.ActionType) -> None:
            self.name: str = name
            self.action: LL1RecursiveDescentParser.ActionType = action
            self.code_line: int = -1

    class Rule:
        def __init__(self, tokens: list[str], actions: list[LL1RecursiveDescentParser.Action]) -> None:
            self.tokens: list[str] = tokens
            self.actions: list[LL1RecursiveDescentParser.Action] = actions

        def __contains__(self, item: str) -> bool:
            return item in self.tokens
        
        def __getitem__(self, item: int) -> LL1RecursiveDescentParser.Action:
            return self.actions[item]
        
        def __len__(self) -> int:
            return len(self.actions)

    def __init__(self) -> None:
        self.rules = {}
        self.highlighted_rule = self.null_rule = self.Action('', self.ActionType.Nothing)
        self.start_rule = self.Action('', self.ActionType.Nothing)
        self.languages: list[RDCodeRules.Language] = RDCodeRules.RecursiveDescentCodeLanguages
        self.reset()

    def code_box_text(self) -> str:
        return HTML.CodeBox.make_html(self.code, self.highlighted_rule.code_line)

    def lines_of_code(self) -> int:
        return len(self.code) - 1

    def parse_stack_to_str(self) -> str:
        return ' '.join(map(lambda x: x.node.name, self.parse_stack))

    def generate_rules(self) -> None:
        self.start_symbol_name = 'program'
        self.rules = {
            'program': [], 'stmt_list': [], 'stmt': [], 'cond': [], 'expr': [], 'term_tail': [],
            'term': [], 'factor_tail': [], 'factor': [], 'ro': [], 'ao': [], 'mo': []
        }

        self.rules['program'].append(self.Rule(['<id>', 'read', 'write', '<eof>', 'if', 'while'], [
            self.Action('stmt_list', self.ActionType.Descend), self.Action('<eof>', self.ActionType.Match),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['stmt_list'].append(self.Rule(['<id>', 'read', 'write', 'if', 'while'], [
            self.Action('stmt', self.ActionType.Descend), self.Action('stmt_list', self.ActionType.Descend),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['stmt_list'].append(self.Rule(['end', '<eof>'], [self.Action('', self.ActionType.Nothing)]))
        self.rules['stmt'].append(self.Rule(['<id>'], [
            self.Action('<id>', self.ActionType.Match), self.Action(':=', self.ActionType.Match),
            self.Action('expr', self.ActionType.Descend), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['stmt'].append(self.Rule(['read'], [
            self.Action('read', self.ActionType.Match), self.Action('<id>', self.ActionType.Match),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['stmt'].append(self.Rule(['write'], [
            self.Action('write', self.ActionType.Match), self.Action('expr', self.ActionType.Descend),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['stmt'].append(self.Rule(['if'], [
            self.Action('if', self.ActionType.Match), self.Action('cond', self.ActionType.Descend),
            self.Action('stmt_list', self.ActionType.Descend), self.Action('end', self.ActionType.Match),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['stmt'].append(self.Rule(['while'], [
            self.Action('while', self.ActionType.Match), self.Action('cond', self.ActionType.Descend),
            self.Action('stmt_list', self.ActionType.Descend), self.Action('end', self.ActionType.Match),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['cond'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Action('expr', self.ActionType.Descend), self.Action('ro', self.ActionType.Descend),
            self.Action('expr', self.ActionType.Descend),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['expr'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Action('term', self.ActionType.Descend), self.Action('term_tail', self.ActionType.Descend),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['term_tail'].append(self.Rule(['+', '-'], [
            self.Action('ao', self.ActionType.Descend), self.Action('term', self.ActionType.Descend),
            self.Action('term_tail', self.ActionType.Descend), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['term_tail'].append(self.Rule(['<id>', 'read', 'write', '<eof>', 'if', 'while', 'end', '=', '<>',
                                                  '<', '>', '<=', '>='], [self.Action('', self.ActionType.Nothing)]))
        self.rules['term'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Action('factor', self.ActionType.Descend), self.Action('factor_tail', self.ActionType.Descend),
            self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['factor_tail'].append(self.Rule(['*', '/'], [
            self.Action('mo', self.ActionType.Descend), self.Action('factor', self.ActionType.Descend),
            self.Action('factor_tail', self.ActionType.Descend), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['factor_tail'].append(self.Rule(['+', '-', ')', '<id>', 'read', 'write', '<eof>', 'if',
                                                    'while', 'end', '=', '<>', '<', '>', '<=', '>='],
                                                   [self.Action('', self.ActionType.Nothing)]))
        self.rules['factor'].append(self.Rule(['<i_lit>'], [
            self.Action('<i_lit>', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['factor'].append(self.Rule(['<id>'], [
            self.Action('<id>', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['factor'].append(self.Rule(['('], [
            self.Action('(', self.ActionType.Match), self.Action('<expr>', self.ActionType.Descend),
            self.Action(')', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ro'].append(self.Rule(['='], [
            self.Action('=', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ro'].append(self.Rule(['<>'], [
            self.Action('<>', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ro'].append(self.Rule(['<'], [
            self.Action('<', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ro'].append(self.Rule(['<='], [
            self.Action('<=', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ro'].append(self.Rule(['>'], [
            self.Action('>', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ro'].append(self.Rule(['>='], [
            self.Action('>=', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ao'].append(self.Rule(['+'], [
            self.Action('+', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['ao'].append(self.Rule(['-'], [
            self.Action('-', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['mo'].append(self.Rule(['*'], [
            self.Action('*', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))
        self.rules['mo'].append(self.Rule(['/'], [
            self.Action('/', self.ActionType.Match), self.Action('', self.ActionType.Nothing)
        ]))

        self.make_code()

    def step(self) -> None:
        self.remove_highlight()
        if len(self.parse_stack) < 1:
            self.start_parse() if self.token_stream else self.finish_parse()
        elif self.parse_stack[-1].rule is None:
            self.parse_error()
        elif self.parse_stack[-1].should_return():
            self.return_from_function()
        else:
            match self.parse_stack[-1].current_action().action:
                case self.ActionType.Descend:
                    self.descend_to_function()
                case self.ActionType.Match:
                    self.match_token()
                case _:
                    self.parse_error()

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

    def start_parse(self) -> None:
        self.tree = self.current_node = Tree(self.start_symbol_name)
        self.highlight_line(self.start_rule)
        self.parse_stack.append(self.ParseStackFrame(
            self.tree, self.find_rule(self.start_symbol_name, self.token_stream[0].name)
        ))

    def return_from_function(self) -> None:
        self.current_node = self.parse_stack[-1].node
        self.highlight_line(self.parse_stack[-1].rule.actions[-1])
        self.parse_stack.pop()
        if self.parse_stack:
            self.parse_stack[-1].index += 1

    def descend_to_function(self) -> None:
        self.current_node = self.parse_stack[-1].node.add_child(self.parse_stack[-1].current_action().name)
        self.highlight_line(self.parse_stack[-1].current_action())
        self.parse_stack.append(self.ParseStackFrame(
            self.current_node, self.find_rule(self.parse_stack[-1].current_action().name, self.token_stream[0].name)
        ))

    def match_token(self) -> None:
        if self.parse_stack[-1].current_action().name == self.token_stream[0].name:
            self.current_node = self.parse_stack[-1].node.add_child(self.token_stream[0].image)
            self.highlight_line(self.parse_stack[-1].current_action())
            self.token_stream.pop(0)
            self.parse_stack[-1].index += 1
        else:
            self.parse_error()

    def parse_error(self) -> None:
        self.current_node = self.parse_stack[-1].node.add_child("ERROR")
        self.finished_parsing = True

    def finish_parse(self) -> None:
        self.current_node = self.tree
        self.finished_parsing = True

    def make_code(self, language_index: int = 0) -> None:  # pseudocode is the default option
        # TODO: figure out how to put this in the Language class
        language: RDCodeRules.Language = self.languages[language_index]
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
        self.code[-1] += (self.start_symbol_name + language.end_of_main.split('\n')[0])
        self.start_rule.code_line = len(self.code) - 1
        self.code += language.end_of_main.split('\n')[1:]

        for rule_name, rules in self.rules.items():
            self.code.append(
                language.function_definition_beginning + rule_name + language.function_definition_end +
                (language.start_symbol_comment if self.start_symbol_name == rule_name else ''))
            self.code.append(language.switch_beginning)

            for rule in rules:
                rule_text: list[str] = [production.name for production in rule.actions]
                rule_text = ['epsilon'] if rule_text == [] else rule_text
                self.code += \
                    (language.case_beginning + language.case_separator.join(rule.tokens) + language.case_end +
                     f"{language.comment_begin}P{rule_counter}: {rule_name} -> "
                     f"{' '.join(rule_text)}{language.comment_end}").split('\n')
                rule_counter += 1
                for i, production in enumerate(rule.actions):
                    production.code_line = i + len(self.code)

                steps_text: str = ''
                for production in rule.actions[:-1]:
                    steps_text += ((language.call_function_beginning + production.name + language.call_function_end
                                    if not production.action else
                                    language.call_match_beginning + production.name + language.call_match_end) + '\n')
                steps_text = (language.skip_case + '\n') if steps_text == '' else steps_text

                self.code += steps_text.split('\n')[:-1]
                if language.end_of_case != '':
                    self.code += language.end_of_case.split('\n')

            self.code += language.switch_default.split('\n')
            return_line: int = len(self.code)
            for rule in rules:
                rule.actions[-1].code_line = return_line

            self.code += language.function_last_lines.split('\n')
        self.code.pop()

        if language.program_last_statements != '':
            self.code += language.program_last_statements.split('\n')

    def highlight_line(self, rule: Action) -> None:
        self.highlighted_rule = rule
        self.line_to_move_scrollbar_to = rule.code_line

    def remove_highlight(self) -> None:
        self.highlighted_rule = self.null_rule

    def update_code(self, index: int) -> None:
        self.make_code(index)
        if self.highlighted_rule is not None:
            self.highlight_line(self.highlighted_rule)
