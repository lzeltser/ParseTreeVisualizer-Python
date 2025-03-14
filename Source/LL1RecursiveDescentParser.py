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
from Parser import Parser, LL1Parser
from Tree import Tree


class LL1RecursiveDescentParser(Parser, LL1Parser):
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
            self._rule: LL1RecursiveDescentParser.Rule = rule
            self._index: int = 0

        def current_action(self) -> LL1RecursiveDescentParser.Action:
            return self._rule[self._index]

        def should_descend(self) -> bool:
            return self.current_action().action == LL1RecursiveDescentParser.ActionType.Descend

        def should_match(self) -> bool:
            return self.current_action().action == LL1RecursiveDescentParser.ActionType.Match

        def should_return(self) -> bool:
            return self.current_action().action == LL1RecursiveDescentParser.ActionType.Return

        def rule_not_found(self) -> bool:
            return self._rule is None

        def return_action(self) -> LL1RecursiveDescentParser.Action:
            return self._rule[-1]

        def increment_index(self) -> None:
            self._index += 1

    class ActionType(IntEnum):
        Descend = auto()
        Match = auto()
        Return = auto()

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

    class Language:
        def __init__(self, file_name: str) -> None:
            self.name: str = file_name.removesuffix('.la')

            self.declare_functions: bool = False

            self.program_first_statements: str = ''  # things like include statements in C go here

            self.function_declaration_beginning: str = ''
            self.function_declaration_end: str = ''

            self.first_code: str = ''  # match, error, and main functions go here
            self.end_of_main: str = ''

            self.function_definition_beginning: str = ''
            self.function_definition_end: str = ''
            self.start_symbol_comment: str = ''

            self.switch_beginning: str = ''
            self.case_beginning: str = ''
            self.case_separator: str = ''
            self.case_end: str = ''
            self.comment_begin: str = ''
            self.comment_end: str = ''

            self.call_function_beginning: str = ''
            self.call_function_end: str = ''
            self.call_match_beginning: str = ''
            self.call_match_end: str = ''

            self.end_of_case: str = ''
            self.skip_case: str = ''
            self.switch_default: str = ''  # this will call the parse error and end of statement

            self.function_last_lines: str = ''

            self.program_last_statements: str = ''

            self.get_attributes_from_file('../RDCodeLanguages/' + file_name)

        def get_attributes_from_file(self, file_name: str) -> None:
            with open(file_name, 'r') as f:
                lines: list[str] = f.read().split('\n')
            self.declare_functions = True if lines.pop(0).split(':')[1].strip().lower()[0] == 't' else False
            attr_lines: list[int] = []
            for i, line in enumerate(lines):
                if hasattr(self, line.removesuffix(':')):
                    attr_lines.append(i)
            attr_lines.append(len(attr_lines) - 1)
            for i, line in enumerate(attr_lines[:-1]):
                setattr(self, lines[line].split(':')[0], '\n'.join(lines[line + 1:attr_lines[i + 1]]))

    def __init__(self) -> None:
        self.rules = {}
        self.highlighted_rule = self.null_rule = self.Action('', self.ActionType.Return)
        self.start_rule = self.Action('', self.ActionType.Return)
        self.languages: list[LL1RecursiveDescentParser.Language] = [
            self.Language('Pseudocode.la'),
            self.Language('C.la'),
            self.Language('Python.la')
        ]  # TODO: look at all files in directory
        self.reset()

    def code_box_text(self) -> str:
        return HTML.CodeBox.make_html(self.code, self.highlighted_rule.code_line)

    def lines_of_code(self) -> int:
        return len(self.code) - 1

    def parse_stack_to_str(self) -> str:
        return ' '.join(map(lambda x: x.node.name, self.parse_stack))

    def generate_rules(self) -> None:
        self.start_symbol_name = 'program'
        self.rules = dict.fromkeys(self.grammar.rule_names_list)
        for entry in self.rules:
            self.rules[entry] = []

        self.rules['program'].append(self.Rule(['<id>', 'read', 'write', '<eof>', 'if', 'while'], [
            self.Action('stmt_list', self.ActionType.Descend), self.Action('<eof>', self.ActionType.Match),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['stmt_list'].append(self.Rule(['<id>', 'read', 'write', 'if', 'while'], [
            self.Action('stmt', self.ActionType.Descend), self.Action('stmt_list', self.ActionType.Descend),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['stmt_list'].append(self.Rule(['end', '<eof>'], [self.Action('', self.ActionType.Return)]))
        self.rules['stmt'].append(self.Rule(['<id>'], [
            self.Action('<id>', self.ActionType.Match), self.Action(':=', self.ActionType.Match),
            self.Action('expr', self.ActionType.Descend), self.Action('', self.ActionType.Return)
        ]))
        self.rules['stmt'].append(self.Rule(['read'], [
            self.Action('read', self.ActionType.Match), self.Action('<id>', self.ActionType.Match),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['stmt'].append(self.Rule(['write'], [
            self.Action('write', self.ActionType.Match), self.Action('expr', self.ActionType.Descend),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['stmt'].append(self.Rule(['if'], [
            self.Action('if', self.ActionType.Match), self.Action('cond', self.ActionType.Descend),
            self.Action('stmt_list', self.ActionType.Descend), self.Action('end', self.ActionType.Match),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['stmt'].append(self.Rule(['while'], [
            self.Action('while', self.ActionType.Match), self.Action('cond', self.ActionType.Descend),
            self.Action('stmt_list', self.ActionType.Descend), self.Action('end', self.ActionType.Match),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['cond'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Action('expr', self.ActionType.Descend), self.Action('ro', self.ActionType.Descend),
            self.Action('expr', self.ActionType.Descend),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['expr'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Action('term', self.ActionType.Descend), self.Action('term_tail', self.ActionType.Descend),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['term_tail'].append(self.Rule(['+', '-'], [
            self.Action('ao', self.ActionType.Descend), self.Action('term', self.ActionType.Descend),
            self.Action('term_tail', self.ActionType.Descend), self.Action('', self.ActionType.Return)
        ]))
        self.rules['term_tail'].append(self.Rule([')', '<id>', 'read', 'write', '<eof>', 'if', 'while', 'end', '=', '<>',
                                                  '<', '>', '<=', '>='], [self.Action('', self.ActionType.Return)]))
        self.rules['term'].append(self.Rule(['(', '<id>', '<i_lit>'], [
            self.Action('factor', self.ActionType.Descend), self.Action('factor_tail', self.ActionType.Descend),
            self.Action('', self.ActionType.Return)
        ]))
        self.rules['factor_tail'].append(self.Rule(['*', '/'], [
            self.Action('mo', self.ActionType.Descend), self.Action('factor', self.ActionType.Descend),
            self.Action('factor_tail', self.ActionType.Descend), self.Action('', self.ActionType.Return)
        ]))
        self.rules['factor_tail'].append(self.Rule(['+', '-', ')', '<id>', 'read', 'write', '<eof>', 'if',
                                                    'while', 'end', '=', '<>', '<', '>', '<=', '>='],
                                                   [self.Action('', self.ActionType.Return)]))
        self.rules['factor'].append(self.Rule(['<i_lit>'], [
            self.Action('<i_lit>', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['factor'].append(self.Rule(['<id>'], [
            self.Action('<id>', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['factor'].append(self.Rule(['('], [
            self.Action('(', self.ActionType.Match), self.Action('expr', self.ActionType.Descend),
            self.Action(')', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ro'].append(self.Rule(['='], [
            self.Action('=', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ro'].append(self.Rule(['<>'], [
            self.Action('<>', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ro'].append(self.Rule(['<'], [
            self.Action('<', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ro'].append(self.Rule(['<='], [
            self.Action('<=', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ro'].append(self.Rule(['>'], [
            self.Action('>', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ro'].append(self.Rule(['>='], [
            self.Action('>=', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ao'].append(self.Rule(['+'], [
            self.Action('+', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['ao'].append(self.Rule(['-'], [
            self.Action('-', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['mo'].append(self.Rule(['*'], [
            self.Action('*', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))
        self.rules['mo'].append(self.Rule(['/'], [
            self.Action('/', self.ActionType.Match), self.Action('', self.ActionType.Return)
        ]))

        self.make_code()

    def step(self) -> None:
        self.remove_highlight()
        if not self.parse_stack:
            self.start_parse() if self.should_start_or_finish() else self.finish_parse()
        elif self.parse_stack[-1].rule_not_found():
            self.finish_parse_with_error()
        elif self.parse_stack[-1].should_descend():
            self.descend_to_function()
        elif self.parse_stack[-1].should_match():
            self.match_token()
        elif self.parse_stack[-1].should_return():
            self.return_from_function()
        else:
            self.finish_parse_with_error()

    def reset(self) -> None:
        self.reset_parser_attributes()
        self.remove_highlight()

    def should_start_or_finish(self) -> bool:
        # if token stream is empty finish since there is nothing left to parse, if not start
        return bool(self.token_stream)

    def next_rule(self) -> Rule:
        return next(filter(
            lambda rule: self.token_stream[0].name in rule,
            self.rules[self.parse_stack[-1].current_action().name if self.parse_stack else self.start_symbol_name]
        ), None)

    def start_parse(self) -> None:
        self.tree = self.current_node = Tree(self.start_symbol_name)
        self.highlight_line(self.start_rule)
        self.parse_stack.append(self.ParseStackFrame(self.tree, self.next_rule()))

    def descend_to_function(self) -> None:
        self.current_node = self.parse_stack[-1].node.add_child(self.parse_stack[-1].current_action().name)
        self.highlight_line(self.parse_stack[-1].current_action())
        self.parse_stack.append(self.ParseStackFrame(self.current_node, self.next_rule()))

    def match_token(self) -> None:
        if self.token_stream[0].name == self.parse_stack[-1].current_action().name:
            self.current_node = self.parse_stack[-1].node.add_child(self.token_stream.pop(0).image)
            self.highlight_line(self.parse_stack[-1].current_action())
            self.parse_stack[-1].increment_index()
        else:
            self.finish_parse_with_error()

    def return_from_function(self) -> None:
        self.current_node = self.parse_stack[-1].node
        self.highlight_line(self.parse_stack[-1].return_action())
        self.parse_stack.pop()
        if self.parse_stack:
            self.parse_stack[-1].increment_index()

    def finish_parse_with_error(self) -> None:
        self.current_node = self.parse_stack[-1].node.add_child("ERROR")
        self.finished_parsing = True
        self.parse_error = True

    def finish_parse(self) -> None:
        self.current_node = self.tree
        self.finished_parsing = True

    def make_code(self, language_index: int = 0) -> None:  # pseudocode is the default option
        # TODO: figure out how to put this in the Language class
        language: LL1RecursiveDescentParser.Language = self.languages[language_index]
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

    def highlight_line(self, action: Action) -> None:
        self.highlighted_rule = action
        self.set_scroll_bar_to_index(action.code_line)

    def remove_highlight(self) -> None:
        self.highlighted_rule = self.null_rule

    def update_code(self, index: int) -> None:
        self.make_code(index)
        if self.highlighted_rule is not None:
            self.highlight_line(self.highlighted_rule)
