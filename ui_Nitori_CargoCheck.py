# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Nitori\Nitori_CargoCheck.ui'
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

class Ui_Nitori_CargoCheck(object):
    def setupUi(self, Nitori_CargoCheck):
        Nitori_CargoCheck.setObjectName(_fromUtf8("Nitori_CargoCheck"))
        Nitori_CargoCheck.resize(1386, 822)
        self.btn_delete_all_data = QtGui.QPushButton(Nitori_CargoCheck)
        self.btn_delete_all_data.setGeometry(QtCore.QRect(160, 40, 121, 41))
        self.btn_delete_all_data.setObjectName(_fromUtf8("btn_delete_all_data"))
        self.label = QtGui.QLabel(Nitori_CargoCheck)
        self.label.setGeometry(QtCore.QRect(160, 110, 151, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.btn_output = QtGui.QPushButton(Nitori_CargoCheck)
        self.btn_output.setGeometry(QtCore.QRect(160, 710, 121, 41))
        self.btn_output.setObjectName(_fromUtf8("btn_output"))
        self.label_2 = QtGui.QLabel(Nitori_CargoCheck)
        self.label_2.setGeometry(QtCore.QRect(60, 40, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Nitori_CargoCheck)
        self.label_3.setGeometry(QtCore.QRect(60, 110, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Nitori_CargoCheck)
        self.label_4.setGeometry(QtCore.QRect(60, 715, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.tableView = MyFileView(Nitori_CargoCheck)
        self.tableView.setGeometry(QtCore.QRect(160, 140, 971, 551))
        self.tableView.setAcceptDrops(True)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.btn_process_2 = QtGui.QPushButton(Nitori_CargoCheck)
        self.btn_process_2.setGeometry(QtCore.QRect(1140, 650, 121, 41))
        self.btn_process_2.setObjectName(_fromUtf8("btn_process_2"))

        self.retranslateUi(Nitori_CargoCheck)
        QtCore.QMetaObject.connectSlotsByName(Nitori_CargoCheck)

    def retranslateUi(self, Nitori_CargoCheck):
        Nitori_CargoCheck.setWindowTitle(_translate("Nitori_CargoCheck", "Nitori_CargoCheck", None))
        self.btn_delete_all_data.setText(_translate("Nitori_CargoCheck", "清空所有旧数据", None))
        self.label.setText(_translate("Nitori_CargoCheck", "源文件（单次成批拖入）", None))
        self.btn_output.setText(_translate("Nitori_CargoCheck", "输出汇总数据...", None))
        self.label_2.setText(_translate("Nitori_CargoCheck", "Step 1", None))
        self.label_3.setText(_translate("Nitori_CargoCheck", "Step 2", None))
        self.label_4.setText(_translate("Nitori_CargoCheck", "Step 3", None))
        self.btn_process_2.setText(_translate("Nitori_CargoCheck", "读入处理", None))

from myfileview import MyFileView
