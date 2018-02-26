# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\report_alignment\report_alignment\res_Editor\Editor_Main.ui'
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

class Ui_Editor_Main(object):
    def setupUi(self, Editor_Main):
        Editor_Main.setObjectName(_fromUtf8("Editor_Main"))
        Editor_Main.resize(1416, 847)
        Editor_Main.setMinimumSize(QtCore.QSize(1227, 847))
        Editor_Main.setAcceptDrops(True)
        self.btn_add_sec = QtGui.QPushButton(Editor_Main)
        self.btn_add_sec.setGeometry(QtCore.QRect(270, 10, 75, 31))
        self.btn_add_sec.setObjectName(_fromUtf8("btn_add_sec"))
        self.btn_print_preview = QtGui.QPushButton(Editor_Main)
        self.btn_print_preview.setGeometry(QtCore.QRect(1230, 20, 75, 31))
        self.btn_print_preview.setObjectName(_fromUtf8("btn_print_preview"))
        self.btn_save = QtGui.QPushButton(Editor_Main)
        self.btn_save.setGeometry(QtCore.QRect(90, 10, 75, 31))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.btn_open = QtGui.QPushButton(Editor_Main)
        self.btn_open.setGeometry(QtCore.QRect(170, 10, 75, 31))
        self.btn_open.setObjectName(_fromUtf8("btn_open"))
        self.btn_new = QtGui.QPushButton(Editor_Main)
        self.btn_new.setGeometry(QtCore.QRect(10, 10, 75, 31))
        self.btn_new.setObjectName(_fromUtf8("btn_new"))
        self.btn_add_line = QtGui.QPushButton(Editor_Main)
        self.btn_add_line.setGeometry(QtCore.QRect(350, 10, 75, 31))
        self.btn_add_line.setObjectName(_fromUtf8("btn_add_line"))
        self.btn_add_image = QtGui.QPushButton(Editor_Main)
        self.btn_add_image.setGeometry(QtCore.QRect(430, 10, 75, 31))
        self.btn_add_image.setObjectName(_fromUtf8("btn_add_image"))
        self.line = QtGui.QFrame(Editor_Main)
        self.line.setGeometry(QtCore.QRect(1210, 20, 21, 781))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label = QtGui.QLabel(Editor_Main)
        self.label.setGeometry(QtCore.QRect(1240, 80, 41, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_filename = QtGui.QLabel(Editor_Main)
        self.label_filename.setGeometry(QtCore.QRect(680, 20, 521, 16))
        self.label_filename.setObjectName(_fromUtf8("label_filename"))
        self.btn_add_table = QtGui.QPushButton(Editor_Main)
        self.btn_add_table.setGeometry(QtCore.QRect(510, 10, 75, 31))
        self.btn_add_table.setObjectName(_fromUtf8("btn_add_table"))
        self.btn_add_footer = QtGui.QPushButton(Editor_Main)
        self.btn_add_footer.setGeometry(QtCore.QRect(590, 10, 75, 31))
        self.btn_add_footer.setObjectName(_fromUtf8("btn_add_footer"))
        self.textEdit = QtGui.QTextEdit(Editor_Main)
        self.textEdit.setGeometry(QtCore.QRect(1230, 100, 171, 701))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(Editor_Main)
        QtCore.QMetaObject.connectSlotsByName(Editor_Main)

    def retranslateUi(self, Editor_Main):
        Editor_Main.setWindowTitle(_translate("Editor_Main", "模板编辑器", None))
        self.btn_add_sec.setText(_translate("Editor_Main", "添加文本框", None))
        self.btn_print_preview.setText(_translate("Editor_Main", "打印预览", None))
        self.btn_save.setText(_translate("Editor_Main", "保存", None))
        self.btn_open.setText(_translate("Editor_Main", "打开", None))
        self.btn_new.setText(_translate("Editor_Main", "新建", None))
        self.btn_add_line.setText(_translate("Editor_Main", "添加线条", None))
        self.btn_add_image.setText(_translate("Editor_Main", "添加图片", None))
        self.label.setText(_translate("Editor_Main", "数据：", None))
        self.label_filename.setText(_translate("Editor_Main", "New File", None))
        self.btn_add_table.setText(_translate("Editor_Main", "添加表格", None))
        self.btn_add_footer.setText(_translate("Editor_Main", "添加页脚", None))

