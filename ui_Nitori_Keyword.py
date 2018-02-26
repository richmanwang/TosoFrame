# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\report_alignment\report_alignment\res_Nitori\Nitori_Keyword.ui'
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

class Ui_Nitori_Keyword(object):
    def setupUi(self, Nitori_Keyword):
        Nitori_Keyword.setObjectName(_fromUtf8("Nitori_Keyword"))
        Nitori_Keyword.setWindowModality(QtCore.Qt.ApplicationModal)
        Nitori_Keyword.resize(849, 625)
        self.btn_ok = QtGui.QPushButton(Nitori_Keyword)
        self.btn_ok.setGeometry(QtCore.QRect(420, 550, 201, 51))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_cancel = QtGui.QPushButton(Nitori_Keyword)
        self.btn_cancel.setGeometry(QtCore.QRect(630, 550, 201, 51))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.btn_refresh = QtGui.QPushButton(Nitori_Keyword)
        self.btn_refresh.setGeometry(QtCore.QRect(20, 550, 151, 51))
        self.btn_refresh.setObjectName(_fromUtf8("btn_refresh"))
        self.tableWidget = QtGui.QTableWidget(Nitori_Keyword)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 811, 511))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Nitori_Keyword)
        QtCore.QMetaObject.connectSlotsByName(Nitori_Keyword)

    def retranslateUi(self, Nitori_Keyword):
        Nitori_Keyword.setWindowTitle(_translate("Nitori_Keyword", "数据处理", None))
        self.btn_ok.setText(_translate("Nitori_Keyword", "确认输入", None))
        self.btn_cancel.setText(_translate("Nitori_Keyword", "返回", None))
        self.btn_refresh.setText(_translate("Nitori_Keyword", "刷新", None))

