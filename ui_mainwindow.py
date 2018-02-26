# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1518, 922)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(80, 10, 1421, 851))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.btn_so = QtGui.QPushButton(self.centralwidget)
        self.btn_so.setGeometry(QtCore.QRect(10, 10, 61, 51))
        self.btn_so.setObjectName(_fromUtf8("btn_so"))
        self.btn_nm = QtGui.QPushButton(self.centralwidget)
        self.btn_nm.setGeometry(QtCore.QRect(10, 590, 61, 51))
        self.btn_nm.setObjectName(_fromUtf8("btn_nm"))
        self.btn_db = QtGui.QPushButton(self.centralwidget)
        self.btn_db.setGeometry(QtCore.QRect(10, 70, 61, 51))
        self.btn_db.setObjectName(_fromUtf8("btn_db"))
        self.btn_stat = QtGui.QPushButton(self.centralwidget)
        self.btn_stat.setGeometry(QtCore.QRect(10, 810, 61, 51))
        self.btn_stat.setObjectName(_fromUtf8("btn_stat"))
        self.btn_nitori_cargocheck = QtGui.QPushButton(self.centralwidget)
        self.btn_nitori_cargocheck.setGeometry(QtCore.QRect(10, 650, 61, 51))
        self.btn_nitori_cargocheck.setObjectName(_fromUtf8("btn_nitori_cargocheck"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1518, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_editor = QtGui.QAction(MainWindow)
        self.action_editor.setObjectName(_fromUtf8("action_editor"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_tongbu_inventory = QtGui.QAction(MainWindow)
        self.action_tongbu_inventory.setObjectName(_fromUtf8("action_tongbu_inventory"))
        self.actionBom = QtGui.QAction(MainWindow)
        self.actionBom.setObjectName(_fromUtf8("actionBom"))
        self.menu.addAction(self.action_editor)
        self.menu.addSeparator()
        self.menu.addAction(self.action_Quit)
        self.menu.addAction(self.actionBom)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_so.setText(_translate("MainWindow", "销售订单\n"
"列表", None))
        self.btn_nm.setText(_translate("MainWindow", "NITORI\n"
"订单处理", None))
        self.btn_db.setText(_translate("MainWindow", "发货单\n"
"列表", None))
        self.btn_stat.setText(_translate("MainWindow", "销售统计", None))
        self.btn_nitori_cargocheck.setText(_translate("MainWindow", "NITORI\n"
"对账", None))
        self.menu.setTitle(_translate("MainWindow", "编辑", None))
        self.action_editor.setText(_translate("MainWindow", "模板编辑器...", None))
        self.action_Quit.setText(_translate("MainWindow", "退出", None))
        self.action_tongbu_inventory.setText(_translate("MainWindow", "同步存货信息", None))
        self.actionBom.setText(_translate("MainWindow", "Bom测试", None))

