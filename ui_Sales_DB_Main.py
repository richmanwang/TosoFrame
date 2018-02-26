# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Sales\Sales_DB_Main.ui'
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

class Ui_Sales_DB_Main(object):
    def setupUi(self, Sales_DB_Main):
        Sales_DB_Main.setObjectName(_fromUtf8("Sales_DB_Main"))
        Sales_DB_Main.resize(1419, 822)
        self.groupBox = QtGui.QGroupBox(Sales_DB_Main)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 461, 151))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btn_query = QtGui.QPushButton(self.groupBox)
        self.btn_query.setGeometry(QtCore.QRect(300, 30, 91, 61))
        self.btn_query.setObjectName(_fromUtf8("btn_query"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 120, 52, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_dbcode = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_dbcode.setEnabled(True)
        self.lineEdit_dbcode.setGeometry(QtCore.QRect(70, 120, 101, 20))
        self.lineEdit_dbcode.setObjectName(_fromUtf8("lineEdit_dbcode"))
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(10, 100, 441, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.btn_SelectCus = QtGui.QPushButton(self.groupBox)
        self.btn_SelectCus.setGeometry(QtCore.QRect(260, 70, 31, 20))
        self.btn_SelectCus.setObjectName(_fromUtf8("btn_SelectCus"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(160, 30, 16, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.dateEdit_start = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_start.setGeometry(QtCore.QRect(45, 30, 109, 20))
        self.dateEdit_start.setReadOnly(False)
        self.dateEdit_start.setObjectName(_fromUtf8("dateEdit_start"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(11, 30, 28, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.dateEdit_end = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_end.setGeometry(QtCore.QRect(181, 30, 109, 20))
        self.dateEdit_end.setObjectName(_fromUtf8("dateEdit_end"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 52, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_cusCode = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_cusCode.setEnabled(True)
        self.lineEdit_cusCode.setGeometry(QtCore.QRect(69, 70, 191, 20))
        self.lineEdit_cusCode.setObjectName(_fromUtf8("lineEdit_cusCode"))
        self.btn_query_today = QtGui.QPushButton(self.groupBox)
        self.btn_query_today.setGeometry(QtCore.QRect(400, 30, 51, 61))
        self.btn_query_today.setObjectName(_fromUtf8("btn_query_today"))
        self.checkBox = QtGui.QCheckBox(Sales_DB_Main)
        self.checkBox.setGeometry(QtCore.QRect(40, 180, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.tableView = QtGui.QTableView(Sales_DB_Main)
        self.tableView.setGeometry(QtCore.QRect(20, 210, 1381, 591))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableView.setFont(font)
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.btn_print_label = QtGui.QPushButton(Sales_DB_Main)
        self.btn_print_label.setEnabled(True)
        self.btn_print_label.setGeometry(QtCore.QRect(1240, 160, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_print_label.setFont(font)
        self.btn_print_label.setObjectName(_fromUtf8("btn_print_label"))
        self.btn_output_excel = QtGui.QPushButton(Sales_DB_Main)
        self.btn_output_excel.setGeometry(QtCore.QRect(260, 180, 101, 23))
        self.btn_output_excel.setObjectName(_fromUtf8("btn_output_excel"))
        self.btn_fhmxb = QtGui.QPushButton(Sales_DB_Main)
        self.btn_fhmxb.setEnabled(True)
        self.btn_fhmxb.setGeometry(QtCore.QRect(1080, 160, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_fhmxb.setFont(font)
        self.btn_fhmxb.setObjectName(_fromUtf8("btn_fhmxb"))

        self.retranslateUi(Sales_DB_Main)
        QtCore.QMetaObject.connectSlotsByName(Sales_DB_Main)

    def retranslateUi(self, Sales_DB_Main):
        Sales_DB_Main.setWindowTitle(_translate("Sales_DB_Main", "Form", None))
        self.groupBox.setTitle(_translate("Sales_DB_Main", "提取服务器数据", None))
        self.btn_query.setText(_translate("Sales_DB_Main", "查询", None))
        self.label_6.setText(_translate("Sales_DB_Main", "发货单号", None))
        self.btn_SelectCus.setText(_translate("Sales_DB_Main", "...", None))
        self.label_4.setText(_translate("Sales_DB_Main", "To", None))
        self.label_3.setText(_translate("Sales_DB_Main", "From", None))
        self.label_5.setText(_translate("Sales_DB_Main", "客户编码", None))
        self.btn_query_today.setText(_translate("Sales_DB_Main", "今日\n"
"发货单", None))
        self.checkBox.setText(_translate("Sales_DB_Main", "全选/全消", None))
        self.btn_print_label.setText(_translate("Sales_DB_Main", "标签打印...", None))
        self.btn_output_excel.setText(_translate("Sales_DB_Main", "导出Excel", None))
        self.btn_fhmxb.setText(_translate("Sales_DB_Main", "按所选发货单\n"
"生成Nitori发货明细表", None))

