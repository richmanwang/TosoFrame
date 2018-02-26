# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Stat\Stat_UnitCost.ui'
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

class Ui_Stat_UnitCost(object):
    def setupUi(self, Stat_UnitCost):
        Stat_UnitCost.setObjectName(_fromUtf8("Stat_UnitCost"))
        Stat_UnitCost.resize(1080, 765)
        Stat_UnitCost.setMinimumSize(QtCore.QSize(1080, 765))
        self.tableWidget = QtGui.QTableWidget(Stat_UnitCost)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 1041, 681))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.btn_addnew = QtGui.QPushButton(Stat_UnitCost)
        self.btn_addnew.setEnabled(True)
        self.btn_addnew.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.btn_addnew.setObjectName(_fromUtf8("btn_addnew"))
        self.btn_edit = QtGui.QPushButton(Stat_UnitCost)
        self.btn_edit.setEnabled(True)
        self.btn_edit.setGeometry(QtCore.QRect(140, 10, 121, 41))
        self.btn_edit.setObjectName(_fromUtf8("btn_edit"))
        self.btn_update = QtGui.QPushButton(Stat_UnitCost)
        self.btn_update.setEnabled(True)
        self.btn_update.setGeometry(QtCore.QRect(300, 10, 121, 41))
        self.btn_update.setObjectName(_fromUtf8("btn_update"))

        self.retranslateUi(Stat_UnitCost)
        QtCore.QMetaObject.connectSlotsByName(Stat_UnitCost)

    def retranslateUi(self, Stat_UnitCost):
        Stat_UnitCost.setWindowTitle(_translate("Stat_UnitCost", "Form", None))
        self.tableWidget.setSortingEnabled(True)
        self.btn_addnew.setText(_translate("Stat_UnitCost", "新增", None))
        self.btn_edit.setText(_translate("Stat_UnitCost", "修改", None))
        self.btn_update.setText(_translate("Stat_UnitCost", "数据更新入单价表", None))

