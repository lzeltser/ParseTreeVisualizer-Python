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

from Parser import Parser, TableParser
from Tree import Tree


class LL1TableParser(TableParser):
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
        self.remove_highlight()
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
                    self.highlight_line(rule_index-1)

    def parse_stack_to_str(self) -> str:
        return ' '.join(map(lambda x: x.node.name, self.parse_stack))
