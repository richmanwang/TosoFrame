# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\report_alignment\report_alignment\res_Sales\Sales_LabelPrint.ui'
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

class Ui_Sales_LabelPrint(object):
    def setupUi(self, Sales_LabelPrint):
        Sales_LabelPrint.setObjectName(_fromUtf8("Sales_LabelPrint"))
        Sales_LabelPrint.resize(934, 631)
        self.tableView = QtGui.QTableView(Sales_LabelPrint)
        self.tableView.setGeometry(QtCore.QRect(20, 20, 901, 531))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableView.setFont(font)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.AnyKeyPressed|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.btn_print = QtGui.QPushButton(Sales_LabelPrint)
        self.btn_print.setGeometry(QtCore.QRect(740, 570, 141, 41))
        self.btn_print.setObjectName(_fromUtf8("btn_print"))

        self.retranslateUi(Sales_LabelPrint)
        QtCore.QMetaObject.connectSlotsByName(Sales_LabelPrint)

    def retranslateUi(self, Sales_LabelPrint):
        Sales_LabelPrint.setWindowTitle(_translate("Sales_LabelPrint", "标签打印", None))
        self.btn_print.setText(_translate("Sales_LabelPrint", "打印", None))

