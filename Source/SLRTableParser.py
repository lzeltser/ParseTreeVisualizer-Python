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
        self.symbol_list = self.grammar.rule_names_list + self.grammar.tokens_list

        class LRProduction:
            def __init__(self, name: str, terminal: bool) -> None:
                self.name: str = name
                self.terminal: bool = terminal

            def __eq__(self, other: LRProduction) -> bool:
                return self.name == other.name and self.terminal == other.terminal

            def __str__(self) -> str:
                return f'"{self.name.replace('\n', '\\n')}"' if self.terminal else f'<{self.name}>'

        class LRItem:
            def __init__(self, name: str, productions: list[LRProduction], dot_position: int) -> None:
                self.name: str = name
                self.productions: list[LRProduction] = productions
                self.dot_position: int = dot_position

            def __eq__(self, other: LRItem) -> bool:
                return self.name == other.name and self.productions == other.productions and self.dot_position == other.dot_position

            def make_formatted_str(self) -> str:
                prods = list(map(str, self.productions))
                prods.insert(self.dot_position, '•') if self.dot_position < len(prods) else prods.append('•')
                return '<' + self.name + '> ::= ' + ' '.join(prods)

        def closure(items_list: list[LRItem], all_lr_items: list[LRItem]) -> list[LRItem]:
            list_length: int = 0
            while len(items_list) != list_length:
                list_length = len(items_list)
                for item_ in items_list:
                    if item_.dot_position < len(item_.productions):
                        for lr_item in all_lr_items:
                            if lr_item.name == item_.productions[item_.dot_position].name and lr_item.dot_position == 0 and lr_item not in items_list:
                                items_list.append(lr_item)
            return items_list

        def goto(items: list[LRItem], symbol_: str, all_lr_items: list[LRItem]) -> list[LRItem]:
            new_items: list[LRItem] = []
            for item_ in items:
                if item_.dot_position < len(item_.productions) and item_.productions[item_.dot_position].name == symbol_:
                    new_items.append(LRItem(item_.name, item_.productions, item_.dot_position+1))
            return closure(new_items, all_lr_items)

        def find_rule_index(lr_item_: LRItem) -> int:
            for ri, rule_ in enumerate(self.grammar.rules):
                if [p.name for p in rule_.productions] == [lri.name for lri in lr_item_.productions]:
                    return ri

        lr_items: list[LRItem] = []
        for rule in self.grammar.rules:
            for i in range(len(rule.productions) + 1):
                lr_items.append(LRItem(rule.name, [LRProduction(p.name, p.terminal) for p in rule.productions], i))

        closures: list[list[LRItem]] = [closure([lr_items[0]], lr_items)]
        current_states: int = 0
        while len(closures) != current_states:
            current_states = len(closures)
            for state in closures:
                for symbol in self.symbol_list:
                    new_set: list[LRItem] = goto(state, symbol, lr_items)
                    if len(new_set) > 0 and new_set not in closures:
                        closures.append(new_set)

        singleton_indices: list[int] = []
        for i, state in enumerate(closures):
            if len(state) == 1 and state[0].dot_position >= len(state[0].productions):
                singleton_indices.append(i)
        singleton_states: list[LRItem] = []
        for i in singleton_indices[::-1]:
            singleton_states.append(closures.pop(i).pop())

        follow_sets: dict[str, list[str]] = self.grammar.generate_follow_sets()
        if '' in follow_sets[self.grammar.start_symbol]:
            follow_sets[self.grammar.start_symbol].remove('')
        if 'eof' not in follow_sets[self.grammar.start_symbol]:
            follow_sets[self.grammar.start_symbol].append('eof')

        self.symbol_list.remove(self.grammar.start_symbol)
        blank_entry = self.TableEntry(self.Actions.Nothing, -1)
        self.table = []
        for state in closures:
            self.table.append([blank_entry] * len(self.symbol_list))
            for item in state:
                if item.dot_position < len(item.productions):
                    goto_ = goto(state, item.productions[item.dot_position].name, lr_items)
                    if goto_ in closures:
                        self.table[-1][self.symbol_list.index(item.productions[item.dot_position].name)] =\
                            self.TableEntry(self.Actions.Shift, closures.index(goto_))
                    else:
                        self.table[-1][self.symbol_list.index(item.productions[item.dot_position].name)] = \
                            self.TableEntry(self.Actions.ShiftReduce, find_rule_index(goto_[0]) + 1)

            for item in state:
                if item.dot_position >= len(item.productions):
                    for symbol in follow_sets[item.name]:
                        if self.table[-1][self.symbol_list.index(symbol)] is not blank_entry:
                            print("shift reduce conflict in state:")
                            print('\n'.join(map(lambda j: j.make_formatted_str(), state)))
                        self.table[-1][self.symbol_list.index(symbol)] = self.TableEntry(
                            self.Actions.Reduce, find_rule_index(item) + 1
                        )

        self.production_list = []
        for rule in self.grammar.rules:
            self.production_list.append(self.Production(rule.name, len(rule.productions)))

    def step(self) -> None:
        self.reset_highlighted_line()
        if not self.parse_stack:
            self.start_parse()
        elif (not self.token_stream or self.token_stream[0].name == self.production_list[0].name) and self.parse_stack[-1].state == 0:
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
        return self.symbol_list.index(self.token_stream[0].name if self.token_stream else self.parse_stack[-1].symbol)

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
        production = self.production_list[rule_target-1]
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
        production = self.production_list[rule_target-1]
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
