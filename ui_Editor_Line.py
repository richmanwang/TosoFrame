# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\report_alignment\report_alignment\res_Editor\Editor_Line.ui'
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

class Ui_Editor_Line(object):
    def setupUi(self, Editor_Line):
        Editor_Line.setObjectName(_fromUtf8("Editor_Line"))
        Editor_Line.resize(617, 442)
        self.tabWidget = QtGui.QTabWidget(Editor_Line)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 581, 351))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_x1 = QtGui.QLineEdit(self.tab)
        self.lineEdit_x1.setGeometry(QtCore.QRect(80, 30, 113, 20))
        self.lineEdit_x1.setObjectName(_fromUtf8("lineEdit_x1"))
        self.lineEdit_y1 = QtGui.QLineEdit(self.tab)
        self.lineEdit_y1.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.lineEdit_y1.setObjectName(_fromUtf8("lineEdit_y1"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_x2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_x2.setGeometry(QtCore.QRect(80, 120, 113, 20))
        self.lineEdit_x2.setObjectName(_fromUtf8("lineEdit_x2"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 160, 54, 12))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_y2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_y2.setGeometry(QtCore.QRect(80, 160, 113, 20))
        self.lineEdit_y2.setObjectName(_fromUtf8("lineEdit_y2"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(20, 240, 54, 12))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_width = QtGui.QLineEdit(self.tab)
        self.lineEdit_width.setGeometry(QtCore.QRect(80, 240, 113, 20))
        self.lineEdit_width.setObjectName(_fromUtf8("lineEdit_width"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.btn_ok = QtGui.QPushButton(Editor_Line)
        self.btn_ok.setGeometry(QtCore.QRect(430, 390, 75, 31))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_cancel = QtGui.QPushButton(Editor_Line)
        self.btn_cancel.setGeometry(QtCore.QRect(520, 390, 75, 31))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))

        self.retranslateUi(Editor_Line)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Editor_Line)

    def retranslateUi(self, Editor_Line):
        Editor_Line.setWindowTitle(_translate("Editor_Line", "线条属性", None))
        self.label_2.setText(_translate("Editor_Line", "Y1", None))
        self.label.setText(_translate("Editor_Line", "X1", None))
        self.lineEdit_x1.setText(_translate("Editor_Line", "0.00", None))
        self.lineEdit_y1.setText(_translate("Editor_Line", "0.00", None))
        self.label_3.setText(_translate("Editor_Line", "X2", None))
        self.lineEdit_x2.setText(_translate("Editor_Line", "0.00", None))
        self.label_4.setText(_translate("Editor_Line", "Y2", None))
        self.lineEdit_y2.setText(_translate("Editor_Line", "0.00", None))
        self.label_5.setText(_translate("Editor_Line", "线宽", None))
        self.lineEdit_width.setText(_translate("Editor_Line", "0.00", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Editor_Line", "尺寸", None))
        self.btn_ok.setText(_translate("Editor_Line", "确定", None))
        self.btn_cancel.setText(_translate("Editor_Line", "取消", None))

