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


class Tree:
    def __init__(self, name: str, parent: Tree = None, children_list: list[Tree] = None) -> None:
        self.name = name
        self.parent: Tree | None = parent
        self.children: list[Tree] = [] if children_list is None else children_list
        for child in self.children:
            child.parent = self

    def __getitem__(self, item: int) -> Tree:
        return self.children[item]

    def __len__(self) -> int:
        return self.number_of_children

    @property
    def number_of_children(self) -> int:
        return len(self.children)

    def add_child(self, name: str, index: int = -1, children_list: list[Tree] = None) -> Tree:
        child = Tree(name, self, children_list)
        if index < 0:
            index = len(self)
        self.children.insert(index, child)
        return child

    def remove_last_child(self) -> Tree:
        return self.children.pop()
