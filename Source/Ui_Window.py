# Form implementation generated from reading ui file '../Window.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.SplitterCenter = QtWidgets.QSplitter(parent=self.centralwidget)
        self.SplitterCenter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.SplitterCenter.setObjectName("SplitterCenter")
        self.TreeView = QtWidgets.QGraphicsView(parent=self.SplitterCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.TreeView.sizePolicy().hasHeightForWidth())
        self.TreeView.setSizePolicy(sizePolicy)
        self.TreeView.setObjectName("TreeView")
        self.SplitterBottom = QtWidgets.QSplitter(parent=self.SplitterCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.SplitterBottom.sizePolicy().hasHeightForWidth())
        self.SplitterBottom.setSizePolicy(sizePolicy)
        self.SplitterBottom.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.SplitterBottom.setObjectName("SplitterBottom")
        self.LeftScreen = QtWidgets.QTabWidget(parent=self.SplitterBottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LeftScreen.sizePolicy().hasHeightForWidth())
        self.LeftScreen.setSizePolicy(sizePolicy)
        self.LeftScreen.setObjectName("LeftScreen")
        self.TableTab = QtWidgets.QWidget()
        self.TableTab.setObjectName("TableTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.TableTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.TableBox = QtWidgets.QTextBrowser(parent=self.TableTab)
        self.TableBox.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.TableBox.setObjectName("TableBox")
        self.verticalLayout_5.addWidget(self.TableBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RDCodeLabel = QtWidgets.QLabel(parent=self.TableTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RDCodeLabel.sizePolicy().hasHeightForWidth())
        self.RDCodeLabel.setSizePolicy(sizePolicy)
        self.RDCodeLabel.setObjectName("RDCodeLabel")
        self.horizontalLayout_2.addWidget(self.RDCodeLabel)
        self.RDCodeSelectBox = QtWidgets.QComboBox(parent=self.TableTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RDCodeSelectBox.sizePolicy().hasHeightForWidth())
        self.RDCodeSelectBox.setSizePolicy(sizePolicy)
        self.RDCodeSelectBox.setObjectName("RDCodeSelectBox")
        self.RDCodeSelectBox.addItem("")
        self.RDCodeSelectBox.addItem("")
        self.RDCodeSelectBox.addItem("")
        self.horizontalLayout_2.addWidget(self.RDCodeSelectBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.LeftScreen.addTab(self.TableTab, "")
        self.GrammarTab = QtWidgets.QWidget()
        self.GrammarTab.setObjectName("GrammarTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.GrammarTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.GrammarEditBox = QtWidgets.QPlainTextEdit(parent=self.GrammarTab)
        self.GrammarEditBox.setObjectName("GrammarEditBox")
        self.verticalLayout_6.addWidget(self.GrammarEditBox)
        self.GrammarTabBottom = QtWidgets.QHBoxLayout()
        self.GrammarTabBottom.setObjectName("GrammarTabBottom")
        self.GrammerUpdateButton = QtWidgets.QPushButton(parent=self.GrammarTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GrammerUpdateButton.sizePolicy().hasHeightForWidth())
        self.GrammerUpdateButton.setSizePolicy(sizePolicy)
        self.GrammerUpdateButton.setObjectName("GrammerUpdateButton")
        self.GrammarTabBottom.addWidget(self.GrammerUpdateButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.GrammarTabBottom.addItem(spacerItem1)
        self.GrammarImportButton = QtWidgets.QPushButton(parent=self.GrammarTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GrammarImportButton.sizePolicy().hasHeightForWidth())
        self.GrammarImportButton.setSizePolicy(sizePolicy)
        self.GrammarImportButton.setObjectName("GrammarImportButton")
        self.GrammarTabBottom.addWidget(self.GrammarImportButton)
        self.GrammarExportButton = QtWidgets.QPushButton(parent=self.GrammarTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GrammarExportButton.sizePolicy().hasHeightForWidth())
        self.GrammarExportButton.setSizePolicy(sizePolicy)
        self.GrammarExportButton.setObjectName("GrammarExportButton")
        self.GrammarTabBottom.addWidget(self.GrammarExportButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.GrammarTabBottom.addItem(spacerItem2)
        self.verticalLayout_6.addLayout(self.GrammarTabBottom)
        self.LeftScreen.addTab(self.GrammarTab, "")
        self.GrammarInstructionsTab = QtWidgets.QWidget()
        self.GrammarInstructionsTab.setObjectName("GrammarInstructionsTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.GrammarInstructionsTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GrammarInstructions = QtWidgets.QTextBrowser(parent=self.GrammarInstructionsTab)
        self.GrammarInstructions.setObjectName("GrammarInstructions")
        self.verticalLayout_2.addWidget(self.GrammarInstructions)
        self.LeftScreen.addTab(self.GrammarInstructionsTab, "")
        self.RightScreen = QtWidgets.QTabWidget(parent=self.SplitterBottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RightScreen.sizePolicy().hasHeightForWidth())
        self.RightScreen.setSizePolicy(sizePolicy)
        self.RightScreen.setObjectName("RightScreen")
        self.StackTab = QtWidgets.QWidget()
        self.StackTab.setObjectName("StackTab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.StackTab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.StackDisplay = QtWidgets.QTextBrowser(parent=self.StackTab)
        self.StackDisplay.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.StackDisplay.setLineWrapMode(QtWidgets.QTextEdit.LineWrapMode.NoWrap)
        self.StackDisplay.setObjectName("StackDisplay")
        self.verticalLayout_8.addWidget(self.StackDisplay)
        self.StackTabBottom = QtWidgets.QHBoxLayout()
        self.StackTabBottom.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.StackTabBottom.setObjectName("StackTabBottom")
        self.RunStopButton = QtWidgets.QPushButton(parent=self.StackTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.RunStopButton.sizePolicy().hasHeightForWidth())
        self.RunStopButton.setSizePolicy(sizePolicy)
        self.RunStopButton.setObjectName("RunStopButton")
        self.StackTabBottom.addWidget(self.RunStopButton)
        self.StepButton = QtWidgets.QPushButton(parent=self.StackTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StepButton.sizePolicy().hasHeightForWidth())
        self.StepButton.setSizePolicy(sizePolicy)
        self.StepButton.setObjectName("StepButton")
        self.StackTabBottom.addWidget(self.StepButton)
        self.ResetButton = QtWidgets.QPushButton(parent=self.StackTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResetButton.sizePolicy().hasHeightForWidth())
        self.ResetButton.setSizePolicy(sizePolicy)
        self.ResetButton.setObjectName("ResetButton")
        self.StackTabBottom.addWidget(self.ResetButton)
        self.AlgorithmLabel = QtWidgets.QLabel(parent=self.StackTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlgorithmLabel.sizePolicy().hasHeightForWidth())
        self.AlgorithmLabel.setSizePolicy(sizePolicy)
        self.AlgorithmLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.AlgorithmLabel.setObjectName("AlgorithmLabel")
        self.StackTabBottom.addWidget(self.AlgorithmLabel)
        self.AlgorithmBox = QtWidgets.QComboBox(parent=self.StackTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlgorithmBox.sizePolicy().hasHeightForWidth())
        self.AlgorithmBox.setSizePolicy(sizePolicy)
        self.AlgorithmBox.setObjectName("AlgorithmBox")
        self.AlgorithmBox.addItem("")
        self.AlgorithmBox.addItem("")
        self.AlgorithmBox.addItem("")
        self.StackTabBottom.addWidget(self.AlgorithmBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.StackTabBottom.addItem(spacerItem3)
        self.verticalLayout_8.addLayout(self.StackTabBottom)
        self.RightScreen.addTab(self.StackTab, "")
        self.CodeTab = QtWidgets.QWidget()
        self.CodeTab.setObjectName("CodeTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.CodeTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.CodeTabLayout = QtWidgets.QVBoxLayout()
        self.CodeTabLayout.setObjectName("CodeTabLayout")
        self.CodeEditBox = QtWidgets.QPlainTextEdit(parent=self.CodeTab)
        self.CodeEditBox.setObjectName("CodeEditBox")
        self.CodeTabLayout.addWidget(self.CodeEditBox)
        self.CodeTabBottom = QtWidgets.QHBoxLayout()
        self.CodeTabBottom.setObjectName("CodeTabBottom")
        self.CodeUpdateButton = QtWidgets.QPushButton(parent=self.CodeTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CodeUpdateButton.sizePolicy().hasHeightForWidth())
        self.CodeUpdateButton.setSizePolicy(sizePolicy)
        self.CodeUpdateButton.setObjectName("CodeUpdateButton")
        self.CodeTabBottom.addWidget(self.CodeUpdateButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.CodeTabBottom.addItem(spacerItem4)
        self.CodeImportButton = QtWidgets.QPushButton(parent=self.CodeTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CodeImportButton.sizePolicy().hasHeightForWidth())
        self.CodeImportButton.setSizePolicy(sizePolicy)
        self.CodeImportButton.setObjectName("CodeImportButton")
        self.CodeTabBottom.addWidget(self.CodeImportButton)
        self.CodeExportButton = QtWidgets.QPushButton(parent=self.CodeTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CodeExportButton.sizePolicy().hasHeightForWidth())
        self.CodeExportButton.setSizePolicy(sizePolicy)
        self.CodeExportButton.setObjectName("CodeExportButton")
        self.CodeTabBottom.addWidget(self.CodeExportButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.CodeTabBottom.addItem(spacerItem5)
        self.CodeTabLayout.addLayout(self.CodeTabBottom)
        self.verticalLayout_3.addLayout(self.CodeTabLayout)
        self.RightScreen.addTab(self.CodeTab, "")
        self.verticalLayout.addWidget(self.SplitterCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        self.FileMenu = QtWidgets.QMenu(parent=self.menubar)
        self.FileMenu.setObjectName("FileMenu")
        self.RunMenu = QtWidgets.QMenu(parent=self.menubar)
        self.RunMenu.setObjectName("RunMenu")
        self.HelpMenu = QtWidgets.QMenu(parent=self.menubar)
        self.HelpMenu.setObjectName("HelpMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.MenuImportGrammar = QtGui.QAction(parent=MainWindow)
        self.MenuImportGrammar.setObjectName("MenuImportGrammar")
        self.MenuExportGrammar = QtGui.QAction(parent=MainWindow)
        self.MenuExportGrammar.setObjectName("MenuExportGrammar")
        self.MenuImportCode = QtGui.QAction(parent=MainWindow)
        self.MenuImportCode.setObjectName("MenuImportCode")
        self.MenuExportCode = QtGui.QAction(parent=MainWindow)
        self.MenuExportCode.setObjectName("MenuExportCode")
        self.MenuExportTree = QtGui.QAction(parent=MainWindow)
        self.MenuExportTree.setObjectName("MenuExportTree")
        self.MenuExit = QtGui.QAction(parent=MainWindow)
        self.MenuExit.setObjectName("MenuExit")
        self.MenuAbout = QtGui.QAction(parent=MainWindow)
        self.MenuAbout.setObjectName("MenuAbout")
        self.MenuStep = QtGui.QAction(parent=MainWindow)
        self.MenuStep.setObjectName("MenuStep")
        self.MenuRun = QtGui.QAction(parent=MainWindow)
        self.MenuRun.setObjectName("MenuRun")
        self.MenuStop = QtGui.QAction(parent=MainWindow)
        self.MenuStop.setObjectName("MenuStop")
        self.MenuHelp = QtGui.QAction(parent=MainWindow)
        self.MenuHelp.setObjectName("MenuHelp")
        self.MenuUpdateGrammar = QtGui.QAction(parent=MainWindow)
        self.MenuUpdateGrammar.setObjectName("MenuUpdateGrammar")
        self.MenuUpdateCode = QtGui.QAction(parent=MainWindow)
        self.MenuUpdateCode.setObjectName("MenuUpdateCode")
        self.MenuReset = QtGui.QAction(parent=MainWindow)
        self.MenuReset.setObjectName("MenuReset")
        self.FileMenu.addAction(self.MenuImportGrammar)
        self.FileMenu.addAction(self.MenuExportGrammar)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.MenuImportCode)
        self.FileMenu.addAction(self.MenuExportCode)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.MenuExportTree)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.MenuExit)
        self.RunMenu.addAction(self.MenuUpdateGrammar)
        self.RunMenu.addAction(self.MenuUpdateCode)
        self.RunMenu.addSeparator()
        self.RunMenu.addAction(self.MenuStep)
        self.RunMenu.addAction(self.MenuRun)
        self.RunMenu.addAction(self.MenuStop)
        self.RunMenu.addAction(self.MenuReset)
        self.HelpMenu.addAction(self.MenuHelp)
        self.HelpMenu.addAction(self.MenuAbout)
        self.menubar.addAction(self.FileMenu.menuAction())
        self.menubar.addAction(self.RunMenu.menuAction())
        self.menubar.addAction(self.HelpMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.LeftScreen.setCurrentIndex(0)
        self.RightScreen.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Parse Tree Visualizer"))
        self.RDCodeLabel.setText(_translate("MainWindow", "Code Language (recursive descent only):"))
        self.RDCodeSelectBox.setItemText(0, _translate("MainWindow", "Pseudocode"))
        self.RDCodeSelectBox.setItemText(1, _translate("MainWindow", "C"))
        self.RDCodeSelectBox.setItemText(2, _translate("MainWindow", "Python"))
        self.LeftScreen.setTabText(self.LeftScreen.indexOf(self.TableTab), _translate("MainWindow", "Table/Code"))
        self.GrammerUpdateButton.setText(_translate("MainWindow", "Update"))
        self.GrammarImportButton.setText(_translate("MainWindow", "Import..."))
        self.GrammarExportButton.setText(_translate("MainWindow", "Export..."))
        self.LeftScreen.setTabText(self.LeftScreen.indexOf(self.GrammarTab), _translate("MainWindow", "Grammar"))
        self.GrammarInstructions.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; text-decoration: underline;\">Writing a grammar for Parse Tree Visualizer</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Grammar can be written in Backus-Naur form using the following format:<br />&lt;symbol&gt; ::= expression1 | expression 2</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Expressions are made up of any number of other rules (enclosed in triangle brackets) or other symbols (enclosed in double quotes). Each symbol can have multiple rules, each one seperated by a |. Anything following a semicolon up to the end of the line is a comment. For example, in the following rule:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;ex&gt; ::= &quot;(&quot; &lt;r1&gt; &quot;)&quot; | &lt;r2&gt; &quot;+&quot; &lt;r3&gt; | &lt;r4&gt; ;comment</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The rule ex mean could mean &lt;r1&gt; inside parentheses, &lt;r2&gt; followed by a + followed by &lt;r3&gt;, or &lt;r4&gt; alone. The word &quot;comment&quot; will not be parsed.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Special rules and symbols:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&quot;&quot; - empty string/epsilon</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;eof&gt; - end of file</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;id&gt; - identifier/variable (can start with any letter or underscore, can have any amount of letters, underscores, and numbers)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&lt;i_lit&gt; - integer literal</p></body></html>"))
        self.LeftScreen.setTabText(self.LeftScreen.indexOf(self.GrammarInstructionsTab), _translate("MainWindow", "Writing Grammar Instructions"))
        self.StackDisplay.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.RunStopButton.setText(_translate("MainWindow", "Run"))
        self.StepButton.setText(_translate("MainWindow", "Step"))
        self.ResetButton.setText(_translate("MainWindow", "Reset"))
        self.AlgorithmLabel.setText(_translate("MainWindow", "Algorithm:"))
        self.AlgorithmBox.setItemText(0, _translate("MainWindow", "LL (Recursive Descent)"))
        self.AlgorithmBox.setItemText(1, _translate("MainWindow", "LL (Table)"))
        self.AlgorithmBox.setItemText(2, _translate("MainWindow", "SLR (Table)"))
        self.RightScreen.setTabText(self.RightScreen.indexOf(self.StackTab), _translate("MainWindow", "Stack"))
        self.CodeUpdateButton.setText(_translate("MainWindow", "Update"))
        self.CodeImportButton.setText(_translate("MainWindow", "Import..."))
        self.CodeExportButton.setText(_translate("MainWindow", "Export..."))
        self.RightScreen.setTabText(self.RightScreen.indexOf(self.CodeTab), _translate("MainWindow", "Code"))
        self.FileMenu.setTitle(_translate("MainWindow", "File"))
        self.RunMenu.setTitle(_translate("MainWindow", "Run"))
        self.HelpMenu.setTitle(_translate("MainWindow", "Help"))
        self.MenuImportGrammar.setText(_translate("MainWindow", "Import grammar..."))
        self.MenuExportGrammar.setText(_translate("MainWindow", "Export grammar..."))
        self.MenuImportCode.setText(_translate("MainWindow", "Import code.."))
        self.MenuExportCode.setText(_translate("MainWindow", "Export code..."))
        self.MenuExportTree.setText(_translate("MainWindow", "Export tree..."))
        self.MenuExit.setText(_translate("MainWindow", "Exit"))
        self.MenuAbout.setText(_translate("MainWindow", "About"))
        self.MenuStep.setText(_translate("MainWindow", "Step"))
        self.MenuRun.setText(_translate("MainWindow", "Run"))
        self.MenuStop.setText(_translate("MainWindow", "Stop"))
        self.MenuHelp.setText(_translate("MainWindow", "Help"))
        self.MenuUpdateGrammar.setText(_translate("MainWindow", "Update grammar"))
        self.MenuUpdateCode.setText(_translate("MainWindow", "Update code"))
        self.MenuReset.setText(_translate("MainWindow", "Reset"))
