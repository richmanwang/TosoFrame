# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Nitori\Nitori_Main.ui'
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

class Ui_Nitori_Main(object):
    def setupUi(self, Nitori_Main):
        Nitori_Main.setObjectName(_fromUtf8("Nitori_Main"))
        Nitori_Main.resize(1386, 822)
        self.btn_create_order = QtGui.QPushButton(Nitori_Main)
        self.btn_create_order.setGeometry(QtCore.QRect(830, 750, 201, 51))
        self.btn_create_order.setObjectName(_fromUtf8("btn_create_order"))
        self.btn_refresh_table = QtGui.QPushButton(Nitori_Main)
        self.btn_refresh_table.setGeometry(QtCore.QRect(20, 750, 111, 51))
        self.btn_refresh_table.setObjectName(_fromUtf8("btn_refresh_table"))
        self.btn_open = QtGui.QPushButton(Nitori_Main)
        self.btn_open.setGeometry(QtCore.QRect(1250, 20, 121, 31))
        self.btn_open.setObjectName(_fromUtf8("btn_open"))
        self.btn_input_keyword = QtGui.QPushButton(Nitori_Main)
        self.btn_input_keyword.setGeometry(QtCore.QRect(140, 750, 111, 51))
        self.btn_input_keyword.setObjectName(_fromUtf8("btn_input_keyword"))
        self.label = QtGui.QLabel(Nitori_Main)
        self.label.setGeometry(QtCore.QRect(20, 20, 42, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(Nitori_Main)
        self.lineEdit.setGeometry(QtCore.QRect(70, 20, 1161, 31))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.btn_create_dispatch = QtGui.QPushButton(Nitori_Main)
        self.btn_create_dispatch.setGeometry(QtCore.QRect(1040, 750, 201, 51))
        self.btn_create_dispatch.setObjectName(_fromUtf8("btn_create_dispatch"))
        self.tableView = QtGui.QTableView(Nitori_Main)
        self.tableView.setGeometry(QtCore.QRect(20, 60, 1351, 681))
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setObjectName(_fromUtf8("tableView"))

        self.retranslateUi(Nitori_Main)
        QtCore.QMetaObject.connectSlotsByName(Nitori_Main)

    def retranslateUi(self, Nitori_Main):
        Nitori_Main.setWindowTitle(_translate("Nitori_Main", "Nitori Matching", None))
        self.btn_create_order.setText(_translate("Nitori_Main", "生成订单", None))
        self.btn_refresh_table.setText(_translate("Nitori_Main", "刷新表格", None))
        self.btn_open.setText(_translate("Nitori_Main", "选择文件...", None))
        self.btn_input_keyword.setText(_translate("Nitori_Main", "输入关键字", None))
        self.label.setText(_translate("Nitori_Main", "源文件 ", None))
        self.btn_create_dispatch.setText(_translate("Nitori_Main", "生成发货单", None))

