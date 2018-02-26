# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Stat\Stat_AddCost.ui'
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

class Ui_Stat_AddCost(object):
    def setupUi(self, Stat_AddCost):
        Stat_AddCost.setObjectName(_fromUtf8("Stat_AddCost"))
        Stat_AddCost.setWindowModality(QtCore.Qt.NonModal)
        Stat_AddCost.resize(764, 799)
        self.btn_submit = QtGui.QPushButton(Stat_AddCost)
        self.btn_submit.setEnabled(True)
        self.btn_submit.setGeometry(QtCore.QRect(580, 330, 151, 41))
        self.btn_submit.setObjectName(_fromUtf8("btn_submit"))
        self.label = QtGui.QLabel(Stat_AddCost)
        self.label.setGeometry(QtCore.QRect(20, 20, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Stat_AddCost)
        self.label_2.setGeometry(QtCore.QRect(20, 410, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btn_submit_rate = QtGui.QPushButton(Stat_AddCost)
        self.btn_submit_rate.setEnabled(True)
        self.btn_submit_rate.setGeometry(QtCore.QRect(580, 720, 151, 41))
        self.btn_submit_rate.setObjectName(_fromUtf8("btn_submit_rate"))
        self.tableView_price = QtGui.QTableView(Stat_AddCost)
        self.tableView_price.setGeometry(QtCore.QRect(20, 40, 721, 271))
        self.tableView_price.setObjectName(_fromUtf8("tableView_price"))
        self.tableView_rate = QtGui.QTableView(Stat_AddCost)
        self.tableView_rate.setGeometry(QtCore.QRect(20, 440, 721, 271))
        self.tableView_rate.setObjectName(_fromUtf8("tableView_rate"))

        self.retranslateUi(Stat_AddCost)
        QtCore.QMetaObject.connectSlotsByName(Stat_AddCost)

    def retranslateUi(self, Stat_AddCost):
        Stat_AddCost.setWindowTitle(_translate("Stat_AddCost", "成本数据补全", None))
        self.btn_submit.setText(_translate("Stat_AddCost", "提交", None))
        self.label.setText(_translate("Stat_AddCost", "按单价", None))
        self.label_2.setText(_translate("Stat_AddCost", "按比率", None))
        self.btn_submit_rate.setText(_translate("Stat_AddCost", "提交", None))

