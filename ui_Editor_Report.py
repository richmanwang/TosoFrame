# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\report_alignment\report_alignment\res_Editor\Editor_Report.ui'
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

class Ui_Editor_Report(object):
    def setupUi(self, Editor_Report):
        Editor_Report.setObjectName(_fromUtf8("Editor_Report"))
        Editor_Report.resize(617, 442)
        self.tabWidget = QtGui.QTabWidget(Editor_Report)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 601, 361))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 40, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_width = QtGui.QLineEdit(self.tab)
        self.lineEdit_width.setGeometry(QtCore.QRect(90, 40, 113, 20))
        self.lineEdit_width.setObjectName(_fromUtf8("lineEdit_width"))
        self.lineEdit_height = QtGui.QLineEdit(self.tab)
        self.lineEdit_height.setGeometry(QtCore.QRect(90, 80, 113, 20))
        self.lineEdit_height.setObjectName(_fromUtf8("lineEdit_height"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(30, 230, 61, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_offset_x = QtGui.QLineEdit(self.tab)
        self.lineEdit_offset_x.setGeometry(QtCore.QRect(90, 130, 113, 20))
        self.lineEdit_offset_x.setObjectName(_fromUtf8("lineEdit_offset_x"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(30, 170, 54, 12))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_offset_y = QtGui.QLineEdit(self.tab)
        self.lineEdit_offset_y.setGeometry(QtCore.QRect(90, 170, 113, 20))
        self.lineEdit_offset_y.setObjectName(_fromUtf8("lineEdit_offset_y"))
        self.label_unit = QtGui.QLabel(self.tab)
        self.label_unit.setGeometry(QtCore.QRect(90, 230, 81, 16))
        self.label_unit.setObjectName(_fromUtf8("label_unit"))
        self.btn_unit_change = QtGui.QPushButton(self.tab)
        self.btn_unit_change.setGeometry(QtCore.QRect(170, 230, 51, 23))
        self.btn_unit_change.setObjectName(_fromUtf8("btn_unit_change"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(30, 40, 61, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.list_printer = QtGui.QComboBox(self.tab_2)
        self.list_printer.setGeometry(QtCore.QRect(30, 60, 411, 22))
        self.list_printer.setEditable(True)
        self.list_printer.setObjectName(_fromUtf8("list_printer"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.btn_ok = QtGui.QPushButton(Editor_Report)
        self.btn_ok.setGeometry(QtCore.QRect(430, 390, 75, 31))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_cancel = QtGui.QPushButton(Editor_Report)
        self.btn_cancel.setGeometry(QtCore.QRect(520, 390, 75, 31))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))

        self.retranslateUi(Editor_Report)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Editor_Report)

    def retranslateUi(self, Editor_Report):
        Editor_Report.setWindowTitle(_translate("Editor_Report", "报表属性", None))
        self.label_2.setText(_translate("Editor_Report", "标签高度", None))
        self.label.setText(_translate("Editor_Report", "标签宽度", None))
        self.lineEdit_width.setText(_translate("Editor_Report", "0.00", None))
        self.lineEdit_height.setText(_translate("Editor_Report", "0.00", None))
        self.label_5.setText(_translate("Editor_Report", "当前单位：", None))
        self.label_3.setText(_translate("Editor_Report", "水平偏移", None))
        self.lineEdit_offset_x.setText(_translate("Editor_Report", "0.00", None))
        self.label_4.setText(_translate("Editor_Report", "垂直偏移", None))
        self.lineEdit_offset_y.setText(_translate("Editor_Report", "0.00", None))
        self.label_unit.setText(_translate("Editor_Report", "Point", None))
        self.btn_unit_change.setText(_translate("Editor_Report", "转换", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Editor_Report", "尺寸", None))
        self.label_6.setText(_translate("Editor_Report", "指定打印机", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Editor_Report", "打印机", None))
        self.btn_ok.setText(_translate("Editor_Report", "确定", None))
        self.btn_cancel.setText(_translate("Editor_Report", "取消", None))

