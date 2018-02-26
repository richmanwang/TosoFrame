# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Editor\Editor_Table.ui'
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

class Ui_Editor_Table(object):
    def setupUi(self, Editor_Table):
        Editor_Table.setObjectName(_fromUtf8("Editor_Table"))
        Editor_Table.resize(1095, 564)
        self.tabWidget = QtGui.QTabWidget(Editor_Table)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 1051, 471))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.layoutWidget = QtGui.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 231, 271))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_x = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_x.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_x.setObjectName(_fromUtf8("lineEdit_x"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_x)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_y = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_y.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_y.setObjectName(_fromUtf8("lineEdit_y"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_y)
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_9)
        self.lineEdit_width = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_width.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_width.setObjectName(_fromUtf8("lineEdit_width"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_width)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lineEdit_height = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_height.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_height.setObjectName(_fromUtf8("lineEdit_height"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_height)
        self.label_12 = QtGui.QLabel(self.layoutWidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_12)
        self.lineEdit_borderWidth = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_borderWidth.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_borderWidth.setObjectName(_fromUtf8("lineEdit_borderWidth"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_borderWidth)
        self.label_13 = QtGui.QLabel(self.layoutWidget)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_13)
        self.lineEdit_borderPenStyle = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_borderPenStyle.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_borderPenStyle.setObjectName(_fromUtf8("lineEdit_borderPenStyle"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_borderPenStyle)
        self.label_15 = QtGui.QLabel(self.layoutWidget)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_15)
        self.lineEdit_Head_h = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Head_h.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_Head_h.setObjectName(_fromUtf8("lineEdit_Head_h"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_Head_h)
        self.label_16 = QtGui.QLabel(self.layoutWidget)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_16)
        self.lineEdit_Body_h = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Body_h.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_Body_h.setObjectName(_fromUtf8("lineEdit_Body_h"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.lineEdit_Body_h)
        self.label_17 = QtGui.QLabel(self.layoutWidget)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_17)
        self.lineEdit_Subtotal_h = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Subtotal_h.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_Subtotal_h.setObjectName(_fromUtf8("lineEdit_Subtotal_h"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.lineEdit_Subtotal_h)
        self.label_18 = QtGui.QLabel(self.layoutWidget)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_18)
        self.lineEdit_Total_h = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_Total_h.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_Total_h.setObjectName(_fromUtf8("lineEdit_Total_h"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.lineEdit_Total_h)
        self.label_19 = QtGui.QLabel(self.tab)
        self.label_19.setGeometry(QtCore.QRect(290, 130, 261, 21))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_20 = QtGui.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(290, 150, 91, 91))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tableWidgetColumn = QtGui.QTableWidget(self.tab_2)
        self.tableWidgetColumn.setGeometry(QtCore.QRect(20, 50, 1001, 381))
        self.tableWidgetColumn.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidgetColumn.setObjectName(_fromUtf8("tableWidgetColumn"))
        self.tableWidgetColumn.setColumnCount(0)
        self.tableWidgetColumn.setRowCount(0)
        self.tableWidgetColumn.verticalHeader().setVisible(False)
        self.btn_addRow = QtGui.QPushButton(self.tab_2)
        self.btn_addRow.setGeometry(QtCore.QRect(20, 10, 71, 31))
        self.btn_addRow.setObjectName(_fromUtf8("btn_addRow"))
        self.btn_removeRow = QtGui.QPushButton(self.tab_2)
        self.btn_removeRow.setGeometry(QtCore.QRect(100, 10, 71, 31))
        self.btn_removeRow.setObjectName(_fromUtf8("btn_removeRow"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.btn_ok = QtGui.QPushButton(Editor_Table)
        self.btn_ok.setGeometry(QtCore.QRect(870, 500, 81, 31))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_cancel = QtGui.QPushButton(Editor_Table)
        self.btn_cancel.setGeometry(QtCore.QRect(960, 500, 81, 31))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))

        self.retranslateUi(Editor_Table)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Editor_Table)

    def retranslateUi(self, Editor_Table):
        Editor_Table.setWindowTitle(_translate("Editor_Table", "表格属性", None))
        self.label_5.setText(_translate("Editor_Table", "坐标X", None))
        self.label_7.setText(_translate("Editor_Table", "坐标Y", None))
        self.label_9.setText(_translate("Editor_Table", "表格宽度", None))
        self.label_8.setText(_translate("Editor_Table", "表格高度", None))
        self.label_12.setText(_translate("Editor_Table", "边框宽度", None))
        self.lineEdit_borderWidth.setText(_translate("Editor_Table", "1", None))
        self.label_13.setText(_translate("Editor_Table", "边框样式", None))
        self.lineEdit_borderPenStyle.setText(_translate("Editor_Table", "0", None))
        self.label_15.setText(_translate("Editor_Table", "表头行高", None))
        self.lineEdit_Head_h.setText(_translate("Editor_Table", "25", None))
        self.label_16.setText(_translate("Editor_Table", "表体行高", None))
        self.lineEdit_Body_h.setText(_translate("Editor_Table", "35", None))
        self.label_17.setText(_translate("Editor_Table", "小计行高", None))
        self.lineEdit_Subtotal_h.setText(_translate("Editor_Table", "20", None))
        self.label_18.setText(_translate("Editor_Table", "合计行高", None))
        self.lineEdit_Total_h.setText(_translate("Editor_Table", "20", None))
        self.label_19.setText(_translate("Editor_Table", "边框样式非0时有效。这里设置0其实是有最细线", None))
        self.label_20.setText(_translate("Editor_Table", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">边框样式：</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0 无边框</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1 实线</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2 短划线</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3 点线</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Editor_Table", "尺寸", None))
        self.btn_addRow.setText(_translate("Editor_Table", "增行", None))
        self.btn_removeRow.setText(_translate("Editor_Table", "删行", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Editor_Table", "栏目", None))
        self.btn_ok.setText(_translate("Editor_Table", "确定", None))
        self.btn_cancel.setText(_translate("Editor_Table", "取消", None))

