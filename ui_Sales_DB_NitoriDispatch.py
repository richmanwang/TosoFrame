# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Sales\Sales_DB_NitoriDispatch.ui'
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

class Ui_Sales_DB_NitoriDispatch(object):
    def setupUi(self, Sales_DB_NitoriDispatch):
        Sales_DB_NitoriDispatch.setObjectName(_fromUtf8("Sales_DB_NitoriDispatch"))
        Sales_DB_NitoriDispatch.resize(995, 710)
        self.tabWidget = QtGui.QTabWidget(Sales_DB_NitoriDispatch)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 951, 661))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tableView1 = QtGui.QTableView(self.tab)
        self.tableView1.setGeometry(QtCore.QRect(20, 50, 901, 561))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView1.setFont(font)
        self.tableView1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView1.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tableView1.setObjectName(_fromUtf8("tableView1"))
        self.pushButton1 = QtGui.QPushButton(self.tab)
        self.pushButton1.setGeometry(QtCore.QRect(20, 10, 91, 31))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tableView2 = QtGui.QTableView(self.tab_2)
        self.tableView2.setGeometry(QtCore.QRect(20, 50, 901, 561))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView2.setFont(font)
        self.tableView2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView2.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tableView2.setObjectName(_fromUtf8("tableView2"))
        self.pushButton2 = QtGui.QPushButton(self.tab_2)
        self.pushButton2.setGeometry(QtCore.QRect(20, 10, 91, 31))
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tableView3 = QtGui.QTableView(self.tab_3)
        self.tableView3.setGeometry(QtCore.QRect(20, 50, 901, 561))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView3.setFont(font)
        self.tableView3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView3.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tableView3.setObjectName(_fromUtf8("tableView3"))
        self.pushButton3 = QtGui.QPushButton(self.tab_3)
        self.pushButton3.setGeometry(QtCore.QRect(20, 10, 91, 31))
        self.pushButton3.setObjectName(_fromUtf8("pushButton3"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))

        self.retranslateUi(Sales_DB_NitoriDispatch)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Sales_DB_NitoriDispatch)

    def retranslateUi(self, Sales_DB_NitoriDispatch):
        Sales_DB_NitoriDispatch.setWindowTitle(_translate("Sales_DB_NitoriDispatch", "Nitori发货明细表", None))
        self.pushButton1.setText(_translate("Sales_DB_NitoriDispatch", "下一步", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Sales_DB_NitoriDispatch", "第一步 原始数据", None))
        self.pushButton2.setText(_translate("Sales_DB_NitoriDispatch", "下一步", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Sales_DB_NitoriDispatch", "第二步 提取店名", None))
        self.pushButton3.setText(_translate("Sales_DB_NitoriDispatch", "生成表格", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Sales_DB_NitoriDispatch", "第三步 店名归类", None))

