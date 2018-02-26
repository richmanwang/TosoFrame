# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Sales\Sales_SelectCus.ui'
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

class Ui_Sales_SelectCus(object):
    def setupUi(self, Sales_SelectCus):
        Sales_SelectCus.setObjectName(_fromUtf8("Sales_SelectCus"))
        Sales_SelectCus.resize(554, 679)
        self.tableView = QtGui.QTableView(Sales_SelectCus)
        self.tableView.setGeometry(QtCore.QRect(20, 40, 511, 621))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableView.setFont(font)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.lineEdit = QtGui.QLineEdit(Sales_SelectCus)
        self.lineEdit.setGeometry(QtCore.QRect(20, 10, 221, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton = QtGui.QPushButton(Sales_SelectCus)
        self.pushButton.setGeometry(QtCore.QRect(240, 10, 75, 21))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Sales_SelectCus)
        QtCore.QMetaObject.connectSlotsByName(Sales_SelectCus)

    def retranslateUi(self, Sales_SelectCus):
        Sales_SelectCus.setWindowTitle(_translate("Sales_SelectCus", "选择", None))
        self.pushButton.setText(_translate("Sales_SelectCus", "筛选", None))

