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
    table: list[list[LRTableEntry]]
    lr_production_list: list[LRProduction]

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

    class LRTableEntry:
        def __init__(self, action: SLRTableParser.Actions, target: int) -> None:
            self.action: SLRTableParser.Actions = action
            self.target: int = target

        def __str__(self) -> str:
            return self.action + str(self.target)

    class LRProduction:
        def __init__(self, name: str, right_side_len: int) -> None:
            self.name: str = name
            self.right_side_len: int = right_side_len

    def __init__(self) -> None:
        self.reset()

        self.table = []
        self.lr_production_list = []
        self.lr_symbol_list: list[str] = []
        self.tree_is_first_in_token_stream: bool = False

    def table_height(self) -> int:
        return len(self.table)

    def table_width(self) -> int:
        return len(self.table[0])

    def get_table_top_row(self) -> Iterable[str]:
        return self.lr_symbol_list

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
        self.lr_symbol_list = ['stmt_list', 'stmt', 'expr', 'term', 'factor', 'ao', 'mo', '<id>',
                               '<i_lit>', 'read', 'write', ':=', '(', ')', '+', '-', '*', '/', '<eof>']
        be = self.LRTableEntry(self.Actions.Nothing, -1)  # blank entry
        self.table = [
            [self.LRTableEntry(self.Actions.Shift, 2), self.LRTableEntry(self.Actions.ShiftReduce, 3), be, be, be, be,
             be, self.LRTableEntry(self.Actions.Shift, 3), be, self.LRTableEntry(self.Actions.Shift, 1),
             self.LRTableEntry(self.Actions.Shift, 4), be, be, be, be, be, be, be, be],
            [be, be, be, be, be, be, be, self.LRTableEntry(self.Actions.ShiftReduce, 5), be, be, be, be, be, be, be, be,
             be, be, be],
            [be, self.LRTableEntry(self.Actions.ShiftReduce, 2), be, be, be, be, be,
             self.LRTableEntry(self.Actions.Shift, 3), be, self.LRTableEntry(self.Actions.Shift, 1),
             self.LRTableEntry(self.Actions.Shift, 4), be, be, be, be, be, be, be,
             self.LRTableEntry(self.Actions.ShiftReduce, 1)],
            [be, be, be, be, be, be, be, be, be, be, be, self.LRTableEntry(self.Actions.Shift, 5),
             be, be, be, be, be, be, be],
            [be, be, self.LRTableEntry(self.Actions.Shift, 6), self.LRTableEntry(self.Actions.Shift, 7),
             self.LRTableEntry(self.Actions.ShiftReduce, 9), be, be, self.LRTableEntry(self.Actions.ShiftReduce, 12),
             self.LRTableEntry(self.Actions.ShiftReduce, 13), be, be, be, self.LRTableEntry(self.Actions.Shift, 8),
             be, be, be, be, be, be],
            [be, be, self.LRTableEntry(self.Actions.Shift, 9), self.LRTableEntry(self.Actions.Shift, 7), self.LRTableEntry(self.Actions.ShiftReduce, 9), be, be,
             self.LRTableEntry(self.Actions.ShiftReduce, 12), self.LRTableEntry(self.Actions.ShiftReduce, 13), be, be, be, self.LRTableEntry(self.Actions.Shift, 8),
             be, be, be, be, be, be],
            [be, be, be, be, be, self.LRTableEntry(self.Actions.Shift, 10), be,
             self.LRTableEntry(self.Actions.Reduce, 6), be, self.LRTableEntry(self.Actions.Reduce, 6),
             self.LRTableEntry(self.Actions.Reduce, 6), be, be, be, self.LRTableEntry(self.Actions.ShiftReduce, 14),
             self.LRTableEntry(self.Actions.ShiftReduce, 15), be, be, self.LRTableEntry(self.Actions.Reduce, 6)],
            [be, be, be, be, be, be, self.LRTableEntry(self.Actions.Shift, 11),
             self.LRTableEntry(self.Actions.Reduce, 7), be, self.LRTableEntry(self.Actions.Reduce, 7),
             self.LRTableEntry(self.Actions.Reduce, 7), be, be, self.LRTableEntry(self.Actions.Reduce, 7),
             self.LRTableEntry(self.Actions.Reduce, 7), self.LRTableEntry(self.Actions.Reduce, 7),
             self.LRTableEntry(self.Actions.ShiftReduce, 16), self.LRTableEntry(self.Actions.ShiftReduce, 17),
             self.LRTableEntry(self.Actions.Reduce, 7)],
            [be, be, self.LRTableEntry(self.Actions.Shift, 12), self.LRTableEntry(self.Actions.Shift, 7),
             self.LRTableEntry(self.Actions.ShiftReduce, 9), be, be, self.LRTableEntry(self.Actions.ShiftReduce, 12),
             self.LRTableEntry(self.Actions.ShiftReduce, 13), be, be, be, self.LRTableEntry(self.Actions.Shift, 8),
             be, be, be, be, be, be],
            [be, be, be, be, be, self.LRTableEntry(self.Actions.Shift, 10), be,
             self.LRTableEntry(self.Actions.Reduce, 4), be, self.LRTableEntry(self.Actions.Reduce, 4),
             self.LRTableEntry(self.Actions.Reduce, 4), be, be, be, self.LRTableEntry(self.Actions.ShiftReduce, 14),
             self.LRTableEntry(self.Actions.ShiftReduce, 15), be, be, self.LRTableEntry(self.Actions.Reduce, 4)],
            [be, be, be, self.LRTableEntry(self.Actions.Shift, 13), self.LRTableEntry(self.Actions.ShiftReduce, 9),
             be, be, self.LRTableEntry(self.Actions.ShiftReduce, 12), self.LRTableEntry(self.Actions.ShiftReduce, 13),
             be, be, be, self.LRTableEntry(self.Actions.Shift, 8), be, be, be, be, be, be],
            [be, be, be, be, self.LRTableEntry(self.Actions.ShiftReduce, 10), be, be,
             self.LRTableEntry(self.Actions.ShiftReduce, 12), self.LRTableEntry(self.Actions.ShiftReduce, 13),
             be, be, be, self.LRTableEntry(self.Actions.Shift, 8), be, be, be, be, be, be],
            [be, be, be, be, be, self.LRTableEntry(self.Actions.Shift, 10), be, be, be, be, be, be, be,
             self.LRTableEntry(self.Actions.ShiftReduce, 11), self.LRTableEntry(self.Actions.ShiftReduce, 14),
             self.LRTableEntry(self.Actions.ShiftReduce, 15), be, be, be],
            [be, be, be, be, be, be, self.LRTableEntry(self.Actions.Shift, 11),
             self.LRTableEntry(self.Actions.Reduce, 8), be, self.LRTableEntry(self.Actions.Reduce, 8),
             self.LRTableEntry(self.Actions.Reduce, 8), be, be, self.LRTableEntry(self.Actions.Reduce, 8),
             self.LRTableEntry(self.Actions.Reduce, 8), self.LRTableEntry(self.Actions.Reduce, 8),
             self.LRTableEntry(self.Actions.ShiftReduce, 16), self.LRTableEntry(self.Actions.ShiftReduce, 17),
             self.LRTableEntry(self.Actions.Reduce, 8)]
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
        self.curr_highlighted_line = -1
        if len(self.parse_stack) < 1:
            self.tree = self.current_node = Tree('')
            self.parse_stack.append(self.ParseStackFrame(self.tree, '', 0))
        elif self.token_stream[0].name == self.lr_production_list[1].name and self.parse_stack[-1].state == 0:
            self.curr_highlighted_row = self.curr_highlighted_col = -1
            self.current_node = self.tree[0]
            self.finished_parsing = True
        else:
            current_symbol: str = self.token_stream[0].name
            self.curr_highlighted_row = self.last_highlighted_row = self.parse_stack[-1].state
            self.curr_highlighted_col = self.last_highlighted_col = self.lr_symbol_list.index(current_symbol)
            rule = self.table[self.curr_highlighted_row][self.curr_highlighted_col]
            match rule.action:
                case self.Actions.Shift:
                    self.token_stream.pop(0)
                    self.current_node = self.tree[-1] if self.tree_is_first_in_token_stream else self.tree.add_child(current_symbol)
                    self.tree_is_first_in_token_stream = False
                    self.parse_stack.append(self.ParseStackFrame(self.current_node, current_symbol, rule.target))
                case self.Actions.Reduce:
                    self.line_to_move_scrollbar_to = self.curr_highlighted_line = rule.target - 1
                    production = self.lr_production_list[rule.target]
                    self.token_stream.insert(0, self.grammar.Token(production.name))
                    self.tree_is_first_in_token_stream = True
                    popped_nodes: list[Tree] = []
                    for _ in range(production.right_side_len):
                        self.parse_stack.pop()
                        popped_nodes.insert(0, self.tree.remove_last_child())
                    self.current_node = self.tree.add_child(production.name, children_list=popped_nodes)
                case self.Actions.ShiftReduce:
                    self.line_to_move_scrollbar_to = self.curr_highlighted_line = rule.target - 1
                    self.token_stream.pop(0)
                    production = self.lr_production_list[rule.target]
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
                case _:  # parse error
                    self.current_node = self.tree.add_child("ERROR")
                    self.finished_parsing = True

    def reset(self) -> None:
        self.tree = None
        self.current_node = None
        self.parse_stack = []
        self.token_stream = []
        self.finished_parsing = False
        self.curr_highlighted_line = -1
        self.line_to_move_scrollbar_to = -1
        self.curr_highlighted_row = -1
        self.curr_highlighted_col = -1
        self.last_highlighted_row = -1
        self.last_highlighted_col = -1
        self.tree_is_first_in_token_stream = False
