# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Stat\Stat_Main.ui'
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

class Ui_Stat_Main(object):
    def setupUi(self, Stat_Main):
        Stat_Main.setObjectName(_fromUtf8("Stat_Main"))
        Stat_Main.resize(526, 439)
        Stat_Main.setMinimumSize(QtCore.QSize(488, 333))
        self.btn_excel = QtGui.QPushButton(Stat_Main)
        self.btn_excel.setGeometry(QtCore.QRect(30, 250, 181, 41))
        self.btn_excel.setObjectName(_fromUtf8("btn_excel"))
        self.btn_addcost = QtGui.QPushButton(Stat_Main)
        self.btn_addcost.setGeometry(QtCore.QRect(380, 370, 111, 41))
        self.btn_addcost.setObjectName(_fromUtf8("btn_addcost"))
        self.groupBox = QtGui.QGroupBox(Stat_Main)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 481, 111))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 151, 61))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.dateEdit_start = QtGui.QDateEdit(self.layoutWidget)
        self.dateEdit_start.setReadOnly(False)
        self.dateEdit_start.setObjectName(_fromUtf8("dateEdit_start"))
        self.gridLayout.addWidget(self.dateEdit_start, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.dateEdit_end = QtGui.QDateEdit(self.layoutWidget)
        self.dateEdit_end.setObjectName(_fromUtf8("dateEdit_end"))
        self.gridLayout.addWidget(self.dateEdit_end, 1, 1, 1, 1)
        self.btn_tongbu = QtGui.QPushButton(self.groupBox)
        self.btn_tongbu.setGeometry(QtCore.QRect(190, 30, 131, 61))
        self.btn_tongbu.setObjectName(_fromUtf8("btn_tongbu"))
        self.btn_tongbu_mysql = QtGui.QPushButton(self.groupBox)
        self.btn_tongbu_mysql.setGeometry(QtCore.QRect(330, 30, 131, 61))
        self.btn_tongbu_mysql.setObjectName(_fromUtf8("btn_tongbu_mysql"))
        self.btn_excel_2 = QtGui.QPushButton(Stat_Main)
        self.btn_excel_2.setGeometry(QtCore.QRect(30, 150, 181, 41))
        self.btn_excel_2.setObjectName(_fromUtf8("btn_excel_2"))
        self.btn_tongbu_inventory = QtGui.QPushButton(Stat_Main)
        self.btn_tongbu_inventory.setGeometry(QtCore.QRect(30, 370, 101, 41))
        self.btn_tongbu_inventory.setObjectName(_fromUtf8("btn_tongbu_inventory"))
        self.btn_unitcost = QtGui.QPushButton(Stat_Main)
        self.btn_unitcost.setGeometry(QtCore.QRect(150, 370, 101, 41))
        self.btn_unitcost.setObjectName(_fromUtf8("btn_unitcost"))
        self.btn_excel_2_mysql = QtGui.QPushButton(Stat_Main)
        self.btn_excel_2_mysql.setGeometry(QtCore.QRect(350, 150, 141, 61))
        self.btn_excel_2_mysql.setObjectName(_fromUtf8("btn_excel_2_mysql"))
        self.btn_excel_mysql = QtGui.QPushButton(Stat_Main)
        self.btn_excel_mysql.setGeometry(QtCore.QRect(350, 250, 141, 61))
        self.btn_excel_mysql.setObjectName(_fromUtf8("btn_excel_mysql"))

        self.retranslateUi(Stat_Main)
        QtCore.QMetaObject.connectSlotsByName(Stat_Main)

    def retranslateUi(self, Stat_Main):
        Stat_Main.setWindowTitle(_translate("Stat_Main", "销售统计", None))
        self.btn_excel.setText(_translate("Stat_Main", "输出excel（财务用不含成本）", None))
        self.btn_addcost.setText(_translate("Stat_Main", "单位成本输入...", None))
        self.groupBox.setTitle(_translate("Stat_Main", "提取服务器数据", None))
        self.label_2.setText(_translate("Stat_Main", "From", None))
        self.label_3.setText(_translate("Stat_Main", "To", None))
        self.btn_tongbu.setText(_translate("Stat_Main", "同步信息\n"
"（至本地）", None))
        self.btn_tongbu_mysql.setText(_translate("Stat_Main", "同步信息\n"
"（至Mysql）", None))
        self.btn_excel_2.setText(_translate("Stat_Main", "输出excel（含成本）", None))
        self.btn_tongbu_inventory.setText(_translate("Stat_Main", "同步存货", None))
        self.btn_unitcost.setText(_translate("Stat_Main", "成本单价...", None))
        self.btn_excel_2_mysql.setText(_translate("Stat_Main", "输出excel（含成本）\n"
"mysql", None))
        self.btn_excel_mysql.setText(_translate("Stat_Main", "输出excel（不含成本）\n"
"mysql", None))

