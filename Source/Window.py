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
import time

from PyQt6 import QtCore, QtGui, QtWidgets

from GraphicsSettings import GraphicsSettings
from Grid import Grid
from LL1RecursiveDescentParser import LL1RecursiveDescentParser
from LL1TableParser import LL1TableParser
from Parser import Parser, UsesTable
import HTML
from SLRTableParser import SLRTableParser
from Tree import Tree
from Ui_Window import Ui_MainWindow


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    class WorkerSignals(QtCore.QObject):
        draw = QtCore.pyqtSignal()

    class Worker(QtCore.QRunnable):
        def __init__(self, fn, *args, **kwargs) -> None:
            super(Window.Worker, self).__init__()
            self.fn = fn
            self.args = args
            self.kwargs = kwargs
            self.signals = Window.WorkerSignals()
            self.kwargs['draw_callback'] = self.signals.draw

        @QtCore.pyqtSlot()
        def run(self) -> None:
            self.fn(*self.args, **self.kwargs)

    def __init__(self) -> None:
        super(Window, self).__init__()
        self.setupUi(self)

        self.stack_trace_stack_text: list[str] = []
        self.stack_trace_token_list: list[str] = []
        self.stack_trace_max_stack_text_len: int = 0
        self.stack_trace_max_token_text_len: int = 0

        self.currently_running: bool = False
        self.thread_pool: QtCore.QThreadPool = QtCore.QThreadPool()

        self.parsers: list[Parser] = [LL1RecursiveDescentParser(), LL1TableParser(), SLRTableParser()]
        # noinspection PyUnresolvedReferences
        for language in self.parsers[0].languages:
            self.RDCodeSelectBox.addItem(language.name)
        with open("../Grammars/ExtendedCalculator-LL.gr", 'r') as f:
            self.parsers[0].input_grammar(f.read())
        with open("../Grammars/ExtendedCalculator-LL.gr", 'r') as f:
            self.parsers[1].input_grammar(f.read())
        with open("../Grammars/ExtendedCalculator-LR.gr", 'r') as f:
            self.parsers[2].input_grammar(f.read())

        # Initialize grammar, code, and other class variables
        with open("../ExampleCode/SumAverage.cl", "r") as f:
            self.code: str = f.read()
        self.current_parser: Parser = self.parsers[self.AlgorithmBox.currentIndex()]
        self.current_parser.input_code(self.code)

        # Set up GUI stuff
        self.GrammarEditBox.setPlainText(self.current_parser.grammar.description)
        self.CodeBox.setHtml(self.current_parser.code_box_text())
        self.CodeEditBox.setPlainText(self.code)
        self.TableBox.setShowGrid(True)  # TODO: add this to settings, make new graphics settings class for Table maybe
        self.TableBox.hide()

        # Connect buttons to methods
        self.RDCodeSelectBox.activated.connect(self.recursive_descent_code_changed)
        self.GrammerUpdateButton.clicked.connect(self.grammar_update_button_pressed)
        self.GrammarImportButton.clicked.connect(self.grammar_import_button_pressed)
        self.GrammarExportButton.clicked.connect(self.grammar_export_button_pressed)
        self.RunStopButton.clicked.connect(self.run_stop_button_pressed)
        self.StepButton.clicked.connect(self.step_button_pressed)
        self.ResetButton.clicked.connect(self.reset)
        self.ResetButton.setEnabled(False)
        self.AlgorithmBox.activated.connect(self.algorithm_change)
        self.CodeUpdateButton.clicked.connect(self.code_update_button_pressed)
        self.CodeImportButton.clicked.connect(self.code_import_button_pressed)
        self.CodeExportButton.clicked.connect(self.code_export_button_pressed)

        # Connect menu buttons to methods
        # TODO: ^that

        # Initialize graphics stuff
        self.graphics_settings: GraphicsSettings = GraphicsSettings()
        self.TreeScene: QtWidgets.QGraphicsScene = QtWidgets.QGraphicsScene(0, 0,
            self.graphics_settings.first_canvas_width, self.graphics_settings.first_canvas_height)
        self.TreeView.setScene(self.TreeScene)
        self.TreeView.horizontalScrollBar().setValue(1)
        self.TreeView.verticalScrollBar().setValue(1)

        self.line_shadow_pen = QtGui.QPen(QtCore.Qt.GlobalColor.lightGray)
        self.line_shadow_pen.setWidth(self.graphics_settings.line_width)
        self.stacked_line_pen = QtGui.QPen(QtCore.Qt.GlobalColor.green)
        self.stacked_line_pen.setWidth(self.graphics_settings.line_width)
        self.unstacked_line_pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
        self.unstacked_line_pen.setWidth(self.graphics_settings.line_width)

        self.outline_pen = QtGui.QPen(QtCore.Qt.GlobalColor.yellow)
        self.outline_pen.setWidth(self.graphics_settings.outline_width)

        self.shadow_border_pen = QtGui.QPen(QtCore.Qt.GlobalColor.lightGray)
        self.shadow_border_pen.setWidth(0)
        self.stacked_border_pen = QtGui.QPen(QtCore.Qt.GlobalColor.green)
        self.stacked_border_pen.setWidth(0)
        self.unstacked_border_pen = QtGui.QPen(QtCore.Qt.GlobalColor.red)
        self.unstacked_border_pen.setWidth(0)

        self.shadow_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.lightGray)
        self.stacked_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.green)
        self.unstacked_brush = self.text_header_brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)

        self.header_brush = QtGui.QBrush(QtGui.QColor(0xDC, 0xDC, 0xDC))
        self.hl_header_brush = QtGui.QBrush(QtGui.QColor(0xB4, 0xB4, 0xB4))
        self.hl_cell_brush = QtGui.QBrush(QtGui.QColor(0xE6, 0xE6, 0xE6))
        self.double_hl_cell_brush = QtGui.QBrush(QtGui.QColor(0xAA, 0xAA, 0xAA))

    def recursive_descent_code_changed(self) -> None:
        if isinstance(self.current_parser, LL1RecursiveDescentParser):
            self.current_parser.update_code(self.RDCodeSelectBox.currentIndex())
            self.update_code_display()

    def grammar_update_button_pressed(self) -> None:
        try:
            self.current_parser.input_grammar(self.GrammarEditBox.toPlainText())
        except Exception as e:
            # TODO: raise a dialogue box
            raise e
        else:
            self.reset()

    def grammar_import_button_pressed(self) -> None:
        # TODO: import grammar from a file
        pass

    def grammar_export_button_pressed(self) -> None:
        # TODO: export grammar to a file
        pass

    def run_stop_button_pressed(self) -> None:
        if self.currently_running:
            self.currently_running = False
            self.enable_all_buttons()
            self.RunStopButton.setText("Run")
        else:
            self.currently_running = True
            self.disable_all_buttons()
            self.RunStopButton.setText("Stop")
            worker = self.Worker(self.run_parser)
            worker.signals.draw.connect(self.update_display)
            self.thread_pool.start(worker)

    def step_button_pressed(self) -> None:
        if not self.currently_running and not self.current_parser.finished_parsing:
            if not self.ResetButton.isEnabled():
                self.ResetButton.setEnabled(True)
            self.current_parser.step()
            self.update_display()
        if self.current_parser.finished_parsing:
            self.run_stop_button_pressed()  # enable all the disabled buttons again
            self.disable_run_buttons()

    def algorithm_change(self) -> None:
        self.current_parser = self.parsers[self.AlgorithmBox.currentIndex()]
        self.GrammarEditBox.setPlainText(self.current_parser.grammar.description)
        self.RDCodeSelectBox.setEnabled(not self.using_table_driven_parser())
        self.TableBox.setHidden(not self.using_table_driven_parser())
        self.reset()

    def code_update_button_pressed(self) -> None:
        try:
            self.current_parser.input_code(self.CodeEditBox.toPlainText())
        except Exception as e:
            # TODO: raise a dialogue box
            raise e
        else:
            self.code = self.CodeEditBox.toPlainText()
            self.reset()

    def code_import_button_pressed(self) -> None:
        # TODO update code from file
        pass

    def code_export_button_pressed(self) -> None:
        # TODO put code in file
        pass

    def using_table_driven_parser(self) -> bool:
        return isinstance(self.current_parser, UsesTable)

    def reset(self) -> None:
        self.current_parser.reset()
        # TODO: add this method to __init__(), remove redundant lines, replace with type hints
        self.stack_trace_stack_text = []
        self.stack_trace_token_list = []
        self.stack_trace_max_stack_text_len = 0
        self.stack_trace_max_token_text_len = 0
        self.TreeScene.setSceneRect(
            0, 0, self.graphics_settings.first_canvas_width, self.graphics_settings.first_canvas_height)
        self.TreeView.horizontalScrollBar().setValue(1)
        self.TreeView.verticalScrollBar().setValue(1)
        self.update_display()
        self.StackDisplay.setHtml('')
        self.enable_run_buttons()
        self.current_parser.input_code(self.code)
        self.stack_trace_stack_text = []
        self.stack_trace_token_list = []

    def disable_run_buttons(self) -> None:
        self.RunStopButton.setEnabled(False)
        self.StepButton.setEnabled(False)

    def enable_run_buttons(self) -> None:
        self.RunStopButton.setEnabled(True)
        self.StepButton.setEnabled(True)

    def disable_all_buttons(self) -> None:
        self.RDCodeSelectBox.setEnabled(False)
        self.GrammerUpdateButton.setEnabled(False)
        self.GrammarImportButton.setEnabled(False)
        self.StepButton.setEnabled(False)
        self.ResetButton.setEnabled(False)
        self.AlgorithmBox.setEnabled(False)
        self.CodeUpdateButton.setEnabled(False)
        self.CodeImportButton.setEnabled(False)

    def enable_all_buttons(self) -> None:
        self.RDCodeSelectBox.setEnabled(not self.using_table_driven_parser())
        self.GrammerUpdateButton.setEnabled(True)
        self.GrammarImportButton.setEnabled(True)
        self.StepButton.setEnabled(True)
        self.ResetButton.setEnabled(True)
        self.AlgorithmBox.setEnabled(True)
        self.CodeUpdateButton.setEnabled(True)
        self.CodeImportButton.setEnabled(True)

    def run_parser(self, draw_callback) -> None:
        while self.currently_running and not self.current_parser.finished_parsing:
            self.current_parser.step()
            draw_callback.emit()
            time.sleep(1.5)  # TODO: put that in the settings
        if self.current_parser.finished_parsing:
            self.run_stop_button_pressed()  # enable all the disabled buttons again
            self.disable_run_buttons()

    def update_display(self) -> None:
        self.update_code_display()
        if self.using_table_driven_parser():
            self.update_table_display()

        parse_stack_line: str = self.current_parser.parse_stack_to_str()
        self.stack_trace_max_stack_text_len = max(len(parse_stack_line), self.stack_trace_max_stack_text_len)
        self.stack_trace_stack_text.append(parse_stack_line)

        token_stream_line: str = self.current_parser.token_stream_to_str()
        self.stack_trace_max_token_text_len = max(len(token_stream_line), self.stack_trace_max_token_text_len)
        self.stack_trace_token_list.append(token_stream_line)

        self.StackDisplay.setHtml(HTML.StackTrace.make_html(self.stack_trace_stack_text, self.stack_trace_token_list))
        self.StackDisplay.verticalScrollBar().setValue(self.StackDisplay.verticalScrollBar().maximum())

        self.move_scroll_bar(
            self.StackDisplay.horizontalScrollBar(), self.stack_trace_max_stack_text_len,
            self.stack_trace_max_stack_text_len + 3 + self.stack_trace_max_token_text_len
        )

        self.TreeScene.clear()
        if self.current_parser.tree is not None:
            self.draw_tree(Grid(self.current_parser.tree, self.graphics_settings.compact_tree))
        self.TreeScene.update()
        self.TreeView.update()

    def update_code_display(self) -> None:
        self.CodeBox.setHtml(self.current_parser.code_box_text())
        self.move_scroll_bar(
            self.CodeBox.verticalScrollBar(),
            self.current_parser.scroll_bar_line,
            self.current_parser.lines_of_code()
        )

    def update_table_display(self) -> None:
        assert isinstance(self.current_parser, UsesTable)
        self.TableBox.clear()
        self.TableBox.setRowCount(self.current_parser.table_height())
        self.TableBox.setColumnCount(self.current_parser.table_width())

        for i, item in enumerate(self.current_parser.get_table_top_row()):
            self.TableBox.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            cell: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem(item)
            cell.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            cell.setBackground(self.hl_header_brush if i == self.current_parser.curr_highlighted_col else self.header_brush)
            cell.setForeground(self.text_header_brush)
            self.TableBox.setHorizontalHeaderItem(i, cell)

        for i, item in enumerate(self.current_parser.get_table_left_col()):
            cell: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem(item)
            cell.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            cell.setBackground(self.hl_header_brush if i == self.current_parser.curr_highlighted_row else self.header_brush)
            cell.setForeground(self.text_header_brush)
            self.TableBox.setVerticalHeaderItem(i, cell)

        for r, row in enumerate(self.current_parser.get_table_body()):
            for c, item in enumerate(row):
                cell: QtWidgets.QTableWidgetItem = QtWidgets.QTableWidgetItem(item)
                cell.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                if r == self.current_parser.curr_highlighted_row and c == self.current_parser.curr_highlighted_col:
                    cell.setBackground(self.double_hl_cell_brush)
                elif r == self.current_parser.curr_highlighted_row or c == self.current_parser.curr_highlighted_col:
                    cell.setBackground(self.hl_cell_brush)
                self.TableBox.setItem(r, c, cell)

        self.move_scroll_bar(
            self.TableBox.horizontalScrollBar(),
            self.current_parser.last_highlighted_col,
            self.current_parser.table_width()
        )
        self.move_scroll_bar(
            self.TableBox.verticalScrollBar(),
            self.current_parser.last_highlighted_row,
            self.current_parser.table_height()
        )

    def draw_tree(self, grid: Grid) -> None:
        self.TreeScene.setSceneRect(
            0, 0,
            max(self.TreeScene.width(), self.graphics_settings.canvas_width(grid.width)),
            max(self.TreeScene.height(), self.graphics_settings.canvas_height(grid.height))
        )

        for x in range(grid.width):
            for y in range(grid.height):
                node: Tree = grid.get_node((x, y))
                if node is None:
                    continue

                text_width: float = self.make_text_graphic(x, y, node.name).boundingRect().width()
                self.make_box_graphic(
                    x, y, text_width, self.current_parser.node_on_stack(node),
                    self.current_parser.node_should_be_highlighted(node)
                )
                if self.graphics_settings.shadow_enabled:
                    self.make_box_shadow_graphic(x, y, text_width)

                for child in node:
                    self.make_line_graphic(
                        (x, y), grid.get_coords(child), self.current_parser.node_on_stack(child)
                    )
                    if self.graphics_settings.shadow_enabled:
                        self.make_line_shadow_graphic((x, y), grid.get_coords(child))

                if node is self.current_parser.current_node:
                    self.move_scroll_bar_if_off_screen(
                        self.TreeView.horizontalScrollBar(),
                        self.graphics_settings.horizontal_scroll_bar_pos(x, text_width),
                        int(self.TreeScene.width())
                    )
                    self.move_scroll_bar_if_off_screen(
                        self.TreeView.verticalScrollBar(),
                        self.graphics_settings.vertical_scroll_bar_pos(y),
                        int(self.TreeScene.height())
                    )

    def make_text_graphic(self, x_pos: int, y_pos: int, text: str) -> QtWidgets.QGraphicsTextItem:
        text_graphic: QtWidgets.QGraphicsTextItem = QtWidgets.QGraphicsTextItem(text)
        text_graphic.setPos(
            self.graphics_settings.text_x_coord(x_pos, text_graphic.boundingRect().width()),
            self.graphics_settings.text_y_coord(y_pos, text_graphic.boundingRect().height())
        )
        text_graphic.setZValue(3)
        self.TreeScene.addItem(text_graphic)
        return text_graphic

    def make_box_graphic(self, x_pos: int, y_pos: int, text_width: float, on_stack: bool, highlight: bool) -> None:
        box: QtWidgets.QGraphicsRectItem = QtWidgets.QGraphicsRectItem(0, 0,
            self.graphics_settings.box_width(text_width), self.graphics_settings.box_height()
        )
        box.setPos(
            self.graphics_settings.box_x_coord(x_pos, text_width),
            self.graphics_settings.box_y_coord(y_pos)
        )
        box.setBrush(self.stacked_brush if on_stack else self.unstacked_brush)
        box.setPen(
            self.outline_pen if highlight else (self.stacked_border_pen if on_stack else self.unstacked_border_pen)
        )
        box.setZValue(2)
        self.TreeScene.addItem(box)

    def make_line_graphic(self, parent_coords: tuple[int, int],
                          child_coords: tuple[int, int], child_on_stack: bool) -> None:
        line = QtWidgets.QGraphicsLineItem(
            self.graphics_settings.line_start_x_coord(parent_coords[0]),
            self.graphics_settings.line_start_y_coord(parent_coords[1]),
            self.graphics_settings.line_end_x_coord(child_coords[0]),
            self.graphics_settings.line_end_y_coord(child_coords[1])
        )
        line.setPen(self.stacked_line_pen if child_on_stack else self.unstacked_line_pen)
        line.setZValue(1)
        self.TreeScene.addItem(line)

    def make_box_shadow_graphic(self, x_pos: int, y_pos: int, text_width: float) -> None:
        box_shadow = QtWidgets.QGraphicsRectItem(0, 0,
            self.graphics_settings.box_width(text_width),
            self.graphics_settings.box_height()
        )
        box_shadow.setPos(
            self.graphics_settings.box_shadow_x_coord(x_pos, text_width),
            self.graphics_settings.box_shadow_y_coord(y_pos)
        )
        box_shadow.setBrush(self.shadow_brush)
        box_shadow.setPen(self.shadow_border_pen)
        self.TreeScene.addItem(box_shadow)

    def make_line_shadow_graphic(self, parent_coords: tuple[int, int], child_coords: tuple[int, int]) -> None:
        line_shadow = QtWidgets.QGraphicsLineItem(
            self.graphics_settings.line_shadow_start_x_coord(parent_coords[0]),
            self.graphics_settings.line_shadow_start_y_coord(parent_coords[1]),
            self.graphics_settings.line_shadow_end_x_coord(child_coords[0]),
            self.graphics_settings.line_shadow_end_y_coord(child_coords[1])
        )
        line_shadow.setPen(self.line_shadow_pen)
        self.TreeScene.addItem(line_shadow)

    @staticmethod
    def move_scroll_bar(scroll_bar: QtWidgets.QScrollBar, position_to_set: int, max_position: int) -> None:
        scroll_bar.setValue(Window.find_scroll_bar_location(scroll_bar, position_to_set, max_position))

    @staticmethod
    def move_scroll_bar_if_off_screen(scroll_bar: QtWidgets.QScrollBar, position_to_set: int, max_position: int) -> None:
        new_location: int = Window.find_scroll_bar_location(scroll_bar, position_to_set, max_position)
        if not new_location - scroll_bar.pageStep()/2 < scroll_bar.value() < new_location + scroll_bar.pageStep()/2:
            scroll_bar.setValue(new_location)

    @staticmethod
    def find_scroll_bar_location(scroll_bar: QtWidgets.QScrollBar, position_to_set: int, max_position: int) -> int:
        return int((scroll_bar.maximum() - scroll_bar.minimum() + scroll_bar.pageStep())
                   / max_position * position_to_set - scroll_bar.pageStep()/2) if max_position > 0 else 0

    @staticmethod
    def run(argv: list[str]) -> None:
        app: QtWidgets.QApplication = QtWidgets.QApplication(argv)
        app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
        window: Window = Window()
        window.show()
        app.exec()
