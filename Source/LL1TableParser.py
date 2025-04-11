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
import itertools

from Parser import Parser, UsesTable, WritesGrammar, LL1Parser
from Tree import Tree


class LL1TableParser(Parser, UsesTable, WritesGrammar, LL1Parser):
    parse_stack: list[ParseStackFrame]
    productions_list: list[list[Rule]]

    class ParseStackFrame(Parser.BaseParseStackFrame):
        def __init__(self, node: Tree, rule: LL1TableParser.Rule) -> None:
            super().__init__(node)
            self.terminal: bool = rule.terminal
            self.rule: str = rule.name

    class Rule:
        def __init__(self, terminal: bool, name: str) -> None:
            self.terminal: bool = terminal
            self.name: str = name

    def __init__(self) -> None:
        self.reset()
        self.rule_list: list[str] = []
        self.token_list: list[str] = []
        self.table: list[list[int]] = []

    def table_height(self) -> int:
        return len(self.table)

    def table_width(self) -> int:
        return len(self.table[0])

    def get_table_top_row(self) -> Iterable[str]:
        return self.token_list

    def get_table_left_col(self) -> Iterable[str]:
        return self.rule_list

    def get_table_body(self) -> Iterable[Iterable[str]]:
        return [['' if i < 0 else str(i) for i in row] for row in self.table]

    def code_box_text(self) -> str:
        return self.grammar_to_numbered_list()

    def lines_of_code(self) -> int:
        return self.grammar_list_len()

    def parse_stack_to_str(self) -> str:
        return ' '.join(map(lambda x: x.node.name, self.parse_stack))

    def generate_rules(self) -> None:
        self.rule_list = self.grammar.rule_names_list
        self.token_list = self.grammar.tokens_list
        self.table = []
        for _ in self.rule_list:
            self.table.append([-1] * len(self.token_list))
        self.productions_list = [[self.Rule(False, self.rule_list[0])]]
        for i, rule, predict_set in zip(itertools.count(1), self.grammar.rules, self.make_predict_sets()):
            for token in predict_set:
                self.table[self.rule_list.index(rule.name)][self.token_list.index(token)] = i
            self.productions_list.append(
                [] if rule.productions[0].name == '' else
                [self.Rule(production.terminal, production.name) for production in rule.productions]
            )

    def step(self) -> None:
        self.reset_highlighted_line()
        if not self.parse_stack:
            self.start_parse() if self.should_start_or_finish() else self.finish_parse()
        else:
            current_frame: LL1TableParser.ParseStackFrame = self.parse_stack.pop()
            self.current_node = current_frame.node
            self.match_token(current_frame.rule) if current_frame.terminal else self.non_terminal(current_frame.rule)

    def reset(self) -> None:
        self.reset_parser_attributes()
        self.reset_table_highlights()
        self.reset_highlighted_line()

    def should_start_or_finish(self) -> bool:
        # if token stream is empty finish since there is nothing left to parse, if not start
        return bool(self.token_stream)

    def next_row(self, rule: str) -> int:
        return self.rule_list.index(rule)

    def next_col(self) -> int:
        return self.token_list.index(self.token_stream[0].name)

    def next_rule_index(self, rule: str) -> int:
        return self.table[self.next_row(rule)][self.next_col()]

    def start_parse(self) -> None:
        self.tree = self.current_node = Tree(self.productions_list[0][0].name)
        self.parse_stack.append(self.ParseStackFrame(self.tree, self.productions_list[0][0]))

    def match_token(self, rule: str) -> None:
        self.unhighlight_table()
        if rule == self.token_stream[0].name:
            self.current_node.name = self.token_stream.pop(0).image
        else:
            self.finish_parse_with_error(self.current_node)

    def non_terminal(self, rule: str) -> None:
        self.highlight_row(self.next_row(rule))
        self.highlight_col(self.next_col())
        if self.next_rule_index(rule) >= 0:
            self.push_rules_to_stack(self.productions_list[self.next_rule_index(rule)])
            self.set_scroll_bar_to_line(self.next_rule_index(rule))
            self.set_highlighted_line(self.next_rule_index(rule))
        else:
            self.finish_parse_with_error(self.current_node.add_child(''))

    def push_rules_to_stack(self, rules: list[Rule]) -> None:
        for rule in reversed(rules):
            self.parse_stack.append(self.ParseStackFrame(self.current_node.add_child(rule.name, 0), rule))

    def finish_parse_with_error(self, error_node: Tree) -> None:
        error_node.name = "ERROR"
        self.current_node = error_node
        self.finished_parsing = True
        self.parse_error = True

    def finish_parse(self) -> None:
        self.reset_table_highlights()
        self.current_node = self.tree
        self.finished_parsing = True
