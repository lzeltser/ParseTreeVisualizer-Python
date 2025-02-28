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
from enum import StrEnum

from Parser import Parser, UsesTable, WritesGrammar
from Tree import Tree


class SLRTableParser(Parser, UsesTable, WritesGrammar):
    parse_stack: list[ParseStackFrame]
    table: list[list[TableEntry]]
    production_list: list[Production]
    tree_is_first_in_token_stream: bool

    class ParseStackFrame(Parser.BaseParseStackFrame):
        def __init__(self, node: Tree, symbol: str, state: int) -> None:
            super().__init__(node)
            self.symbol: str = symbol
            self.state: int = state

    class Actions(StrEnum):
        Shift = 's'
        Reduce = 'r'
        ShiftReduce = 'b'
        Nothing = ''

    class TableEntry:
        def __init__(self, action: SLRTableParser.Actions, target: int) -> None:
            self.action: SLRTableParser.Actions = action
            self.target: int = target

        def __str__(self) -> str:
            return self.action + str(self.target)

    class Production:
        def __init__(self, name: str, right_side_len: int) -> None:
            self.name: str = name
            self.right_side_len: int = right_side_len

    def __init__(self) -> None:
        self.reset()

        self.table = []
        self.production_list = []
        self.symbol_list: list[str] = []

    def table_height(self) -> int:
        return len(self.table)

    def table_width(self) -> int:
        return len(self.table[0])

    def get_table_top_row(self) -> Iterable[str]:
        return self.symbol_list

    def get_table_left_col(self) -> Iterable[str]:
        return map(str, range(len(self.table)))

    def get_table_body(self) -> Iterable[Iterable[str]]:
        return [['' if str(i) == '-1' else str(i) for i in row] for row in self.table]

    def code_box_text(self) -> str:
        return self.grammar_to_numbered_list()

    def lines_of_code(self) -> int:
        return self.grammar_list_len()

    def parse_stack_to_str(self) -> str:
        return ' '.join(map(lambda x: f"{x.node.name} {x.state}", self.parse_stack))

    def generate_rules(self) -> None:
        self.symbol_list = ['stmt_list', 'stmt', 'expr', 'term', 'factor', 'ao', 'mo', '<id>',
                               '<i_lit>', 'read', 'write', ':=', '(', ')', '+', '-', '*', '/', '<eof>']
        be = self.TableEntry(self.Actions.Nothing, -1)  # blank entry
        self.table = [
            [self.TableEntry(self.Actions.Shift, 2), self.TableEntry(self.Actions.ShiftReduce, 3), be, be, be, be,
             be, self.TableEntry(self.Actions.Shift, 3), be, self.TableEntry(self.Actions.Shift, 1),
             self.TableEntry(self.Actions.Shift, 4), be, be, be, be, be, be, be, be],
            [be, be, be, be, be, be, be, self.TableEntry(self.Actions.ShiftReduce, 5), be, be, be, be, be, be, be, be,
             be, be, be],
            [be, self.TableEntry(self.Actions.ShiftReduce, 2), be, be, be, be, be,
             self.TableEntry(self.Actions.Shift, 3), be, self.TableEntry(self.Actions.Shift, 1),
             self.TableEntry(self.Actions.Shift, 4), be, be, be, be, be, be, be,
             self.TableEntry(self.Actions.ShiftReduce, 1)],
            [be, be, be, be, be, be, be, be, be, be, be, self.TableEntry(self.Actions.Shift, 5),
             be, be, be, be, be, be, be],
            [be, be, self.TableEntry(self.Actions.Shift, 6), self.TableEntry(self.Actions.Shift, 7),
             self.TableEntry(self.Actions.ShiftReduce, 9), be, be, self.TableEntry(self.Actions.ShiftReduce, 12),
             self.TableEntry(self.Actions.ShiftReduce, 13), be, be, be, self.TableEntry(self.Actions.Shift, 8),
             be, be, be, be, be, be],
            [be, be, self.TableEntry(self.Actions.Shift, 9), self.TableEntry(self.Actions.Shift, 7), self.TableEntry(self.Actions.ShiftReduce, 9), be, be,
             self.TableEntry(self.Actions.ShiftReduce, 12), self.TableEntry(self.Actions.ShiftReduce, 13), be, be, be, self.TableEntry(self.Actions.Shift, 8),
             be, be, be, be, be, be],
            [be, be, be, be, be, self.TableEntry(self.Actions.Shift, 10), be,
             self.TableEntry(self.Actions.Reduce, 6), be, self.TableEntry(self.Actions.Reduce, 6),
             self.TableEntry(self.Actions.Reduce, 6), be, be, be, self.TableEntry(self.Actions.ShiftReduce, 14),
             self.TableEntry(self.Actions.ShiftReduce, 15), be, be, self.TableEntry(self.Actions.Reduce, 6)],
            [be, be, be, be, be, be, self.TableEntry(self.Actions.Shift, 11),
             self.TableEntry(self.Actions.Reduce, 7), be, self.TableEntry(self.Actions.Reduce, 7),
             self.TableEntry(self.Actions.Reduce, 7), be, be, self.TableEntry(self.Actions.Reduce, 7),
             self.TableEntry(self.Actions.Reduce, 7), self.TableEntry(self.Actions.Reduce, 7),
             self.TableEntry(self.Actions.ShiftReduce, 16), self.TableEntry(self.Actions.ShiftReduce, 17),
             self.TableEntry(self.Actions.Reduce, 7)],
            [be, be, self.TableEntry(self.Actions.Shift, 12), self.TableEntry(self.Actions.Shift, 7),
             self.TableEntry(self.Actions.ShiftReduce, 9), be, be, self.TableEntry(self.Actions.ShiftReduce, 12),
             self.TableEntry(self.Actions.ShiftReduce, 13), be, be, be, self.TableEntry(self.Actions.Shift, 8),
             be, be, be, be, be, be],
            [be, be, be, be, be, self.TableEntry(self.Actions.Shift, 10), be,
             self.TableEntry(self.Actions.Reduce, 4), be, self.TableEntry(self.Actions.Reduce, 4),
             self.TableEntry(self.Actions.Reduce, 4), be, be, be, self.TableEntry(self.Actions.ShiftReduce, 14),
             self.TableEntry(self.Actions.ShiftReduce, 15), be, be, self.TableEntry(self.Actions.Reduce, 4)],
            [be, be, be, self.TableEntry(self.Actions.Shift, 13), self.TableEntry(self.Actions.ShiftReduce, 9),
             be, be, self.TableEntry(self.Actions.ShiftReduce, 12), self.TableEntry(self.Actions.ShiftReduce, 13),
             be, be, be, self.TableEntry(self.Actions.Shift, 8), be, be, be, be, be, be],
            [be, be, be, be, self.TableEntry(self.Actions.ShiftReduce, 10), be, be,
             self.TableEntry(self.Actions.ShiftReduce, 12), self.TableEntry(self.Actions.ShiftReduce, 13),
             be, be, be, self.TableEntry(self.Actions.Shift, 8), be, be, be, be, be, be],
            [be, be, be, be, be, self.TableEntry(self.Actions.Shift, 10), be, be, be, be, be, be, be,
             self.TableEntry(self.Actions.ShiftReduce, 11), self.TableEntry(self.Actions.ShiftReduce, 14),
             self.TableEntry(self.Actions.ShiftReduce, 15), be, be, be],
            [be, be, be, be, be, be, self.TableEntry(self.Actions.Shift, 11),
             self.TableEntry(self.Actions.Reduce, 8), be, self.TableEntry(self.Actions.Reduce, 8),
             self.TableEntry(self.Actions.Reduce, 8), be, be, self.TableEntry(self.Actions.Reduce, 8),
             self.TableEntry(self.Actions.Reduce, 8), self.TableEntry(self.Actions.Reduce, 8),
             self.TableEntry(self.Actions.ShiftReduce, 16), self.TableEntry(self.Actions.ShiftReduce, 17),
             self.TableEntry(self.Actions.Reduce, 8)]
        ]
        self.production_list = [
            None, self.Production('program', 2), self.Production('stmt_list', 2),
            self.Production('stmt_list', 1), self.Production('stmt', 3), self.Production('stmt', 2),
            self.Production('stmt', 2), self.Production('expr', 1), self.Production('expr', 3),
            self.Production('term', 1), self.Production('term', 3), self.Production('factor', 3),
            self.Production('factor', 1), self.Production('factor', 1), self.Production('ao', 1),
            self.Production('ao', 1), self.Production('mo', 1), self.Production('mo', 1)
        ]

    def step(self) -> None:
        self.reset_highlighted_line()
        if not self.parse_stack:
            self.start_parse()
        elif self.token_stream[0].name == self.production_list[1].name and self.parse_stack[-1].state == 0:
            self.finish_parse()
        else:
            self.do_action()

    def reset(self) -> None:
        self.reset_parser_attributes()
        self.reset_table_highlights()
        self.reset_highlighted_line()
        self.tree_is_first_in_token_stream = False

    def next_row(self) -> int:
        return self.parse_stack[-1].state

    def next_col(self) -> int:
        return self.symbol_list.index(self.token_stream[0].name)

    def next_rule(self) -> SLRTableParser.TableEntry:
        return self.table[self.next_row()][self.next_col()]

    def start_parse(self) -> None:
        self.tree = self.current_node = Tree('')
        self.parse_stack.append(self.ParseStackFrame(self.tree, '', 0))

    def do_action(self) -> None:
        self.highlight_row(self.next_row())
        self.highlight_col(self.next_col())
        match self.next_rule().action:
            case self.Actions.Shift:
                self.shift(self.next_rule().target)
            case self.Actions.Reduce:
                self.reduce(self.next_rule().target)
            case self.Actions.ShiftReduce:
                self.shift_reduce(self.next_rule().target)
            case _:
                self.finish_parse_with_error()

    def shift(self, rule_target: int) -> None:
        self.current_node = (
            self.tree[-1] if self.tree_is_first_in_token_stream else self.tree.add_child(self.token_stream[0].name))
        self.parse_stack.append(self.ParseStackFrame(self.current_node, self.token_stream[0].name, rule_target))
        self.token_stream.pop(0)
        self.tree_is_first_in_token_stream = False

    def reduce(self, rule_target: int) -> None:
        self.set_scroll_bar_to_line(rule_target)
        self.set_highlighted_line(rule_target)
        production = self.production_list[rule_target]
        self.token_stream.insert(0, self.grammar.Token(production.name))
        self.tree_is_first_in_token_stream = True
        popped_nodes: list[Tree] = []
        for _ in range(production.right_side_len):
            self.parse_stack.pop()
            popped_nodes.insert(0, self.tree.remove_last_child())
        self.current_node = self.tree.add_child(production.name, children_list=popped_nodes)

    def shift_reduce(self, rule_target: int) -> None:
        current_symbol: str = self.token_stream[0].name
        self.set_scroll_bar_to_line(rule_target)
        self.set_highlighted_line(rule_target)
        self.token_stream.pop(0)
        production = self.production_list[rule_target]
        self.token_stream.insert(0, self.grammar.Token(production.name))
        popped_nodes: list[Tree] = []
        for _ in range(production.right_side_len - 1):
            self.parse_stack.pop()
            popped_nodes.insert(0, self.tree.remove_last_child())
        if self.tree_is_first_in_token_stream:
            popped_nodes.insert(0, self.tree.remove_last_child())
            self.current_node = self.tree.add_child(production.name, children_list=popped_nodes)
        else:
            self.current_node = self.tree.add_child(production.name, children_list=popped_nodes)
            self.current_node.add_child(current_symbol)
        self.tree_is_first_in_token_stream = True

    def finish_parse_with_error(self) -> None:
        self.current_node = self.tree.add_child("ERROR")
        self.finished_parsing = True
        self.parse_error = True

    def finish_parse(self):
        self.unhighlight_table()
        self.current_node = self.tree[0]
        self.finished_parsing = True
