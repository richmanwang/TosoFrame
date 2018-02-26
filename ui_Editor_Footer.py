# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\report_alignment\report_alignment\res_Editor\Editor_Footer.ui'
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

class Ui_Editor_Footer(object):
    def setupUi(self, Editor_Footer):
        Editor_Footer.setObjectName(_fromUtf8("Editor_Footer"))
        Editor_Footer.resize(377, 442)
        self.tabWidget = QtGui.QTabWidget(Editor_Footer)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 341, 361))
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.lineEdit_text = QtGui.QLineEdit(self.tab)
        self.lineEdit_text.setGeometry(QtCore.QRect(70, 30, 251, 20))
        self.lineEdit_text.setObjectName(_fromUtf8("lineEdit_text"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 54, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_16 = QtGui.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(20, 70, 241, 61))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.box_secFontName = QtGui.QFontComboBox(self.tab_2)
        self.box_secFontName.setGeometry(QtCore.QRect(70, 30, 191, 22))
        self.box_secFontName.setObjectName(_fromUtf8("box_secFontName"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 54, 12))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_fontSize = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_fontSize.setGeometry(QtCore.QRect(70, 80, 191, 20))
        self.lineEdit_fontSize.setObjectName(_fromUtf8("lineEdit_fontSize"))
        self.label_12 = QtGui.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(20, 130, 54, 12))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit_borderWidth = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_borderWidth.setGeometry(QtCore.QRect(70, 130, 191, 20))
        self.lineEdit_borderWidth.setObjectName(_fromUtf8("lineEdit_borderWidth"))
        self.label_13 = QtGui.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(20, 180, 54, 12))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.lineEdit_borderPenStyle = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_borderPenStyle.setGeometry(QtCore.QRect(70, 180, 191, 20))
        self.lineEdit_borderPenStyle.setObjectName(_fromUtf8("lineEdit_borderPenStyle"))
        self.label_14 = QtGui.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(70, 200, 91, 91))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(70, 150, 261, 21))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_height = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_height.setGeometry(QtCore.QRect(70, 160, 113, 20))
        self.lineEdit_height.setObjectName(_fromUtf8("lineEdit_height"))
        self.lineEdit_x = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_x.setGeometry(QtCore.QRect(70, 30, 113, 20))
        self.lineEdit_x.setObjectName(_fromUtf8("lineEdit_x"))
        self.lineEdit_width = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_width.setGeometry(QtCore.QRect(70, 120, 113, 20))
        self.lineEdit_width.setObjectName(_fromUtf8("lineEdit_width"))
        self.lineEdit_y = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_y.setGeometry(QtCore.QRect(70, 70, 113, 20))
        self.lineEdit_y.setObjectName(_fromUtf8("lineEdit_y"))
        self.label_7 = QtGui.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(20, 70, 54, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(20, 160, 54, 12))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(20, 120, 54, 12))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.label_6 = QtGui.QLabel(self.tab_4)
        self.label_6.setGeometry(QtCore.QRect(30, 30, 54, 12))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_10 = QtGui.QLabel(self.tab_4)
        self.label_10.setGeometry(QtCore.QRect(30, 110, 54, 12))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.tab_4)
        self.label_11.setGeometry(QtCore.QRect(30, 200, 54, 12))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.combo_align_h = QtGui.QComboBox(self.tab_4)
        self.combo_align_h.setGeometry(QtCore.QRect(30, 50, 151, 22))
        self.combo_align_h.setObjectName(_fromUtf8("combo_align_h"))
        self.combo_align_v = QtGui.QComboBox(self.tab_4)
        self.combo_align_v.setGeometry(QtCore.QRect(30, 130, 151, 22))
        self.combo_align_v.setObjectName(_fromUtf8("combo_align_v"))
        self.combo_textwrap = QtGui.QComboBox(self.tab_4)
        self.combo_textwrap.setGeometry(QtCore.QRect(30, 220, 151, 22))
        self.combo_textwrap.setObjectName(_fromUtf8("combo_textwrap"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.btn_ok = QtGui.QPushButton(Editor_Footer)
        self.btn_ok.setGeometry(QtCore.QRect(180, 390, 81, 31))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_cancel = QtGui.QPushButton(Editor_Footer)
        self.btn_cancel.setGeometry(QtCore.QRect(264, 390, 81, 31))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))

        self.retranslateUi(Editor_Footer)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Editor_Footer)

    def retranslateUi(self, Editor_Footer):
        Editor_Footer.setWindowTitle(_translate("Editor_Footer", "页脚属性", None))
        self.lineEdit_text.setText(_translate("Editor_Footer", "第{currentPage}页 共{totalPage}页", None))
        self.label_2.setText(_translate("Editor_Footer", "文本", None))
        self.label_16.setText(_translate("Editor_Footer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">用 {&amp;cp} 标记表示当前页</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">用 {&amp;tp} 标记表示总数页</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">xml内为 {&amp;amp;cp} {&amp;amp;tp}</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Editor_Footer", "内容", None))
        self.label_3.setText(_translate("Editor_Footer", "字体", None))
        self.label_4.setText(_translate("Editor_Footer", "字号", None))
        self.lineEdit_fontSize.setText(_translate("Editor_Footer", "9", None))
        self.label_12.setText(_translate("Editor_Footer", "边框宽度", None))
        self.lineEdit_borderWidth.setText(_translate("Editor_Footer", "1", None))
        self.label_13.setText(_translate("Editor_Footer", "边框样式", None))
        self.lineEdit_borderPenStyle.setText(_translate("Editor_Footer", "0", None))
        self.label_14.setText(_translate("Editor_Footer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">边框样式：</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0 无边框</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1 实线</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2 短划线</p>\n"
"<p style=\" margin-top:2px; margin-bottom:2px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3 点线</p></body></html>", None))
        self.label_15.setText(_translate("Editor_Footer", "边框样式非0才有效。这里设置0其实是有最细线", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Editor_Footer", "字体及边框", None))
        self.label_5.setText(_translate("Editor_Footer", "坐标X", None))
        self.label_7.setText(_translate("Editor_Footer", "坐标Y", None))
        self.label_8.setText(_translate("Editor_Footer", "高度", None))
        self.label_9.setText(_translate("Editor_Footer", "宽度", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Editor_Footer", "尺寸", None))
        self.label_6.setText(_translate("Editor_Footer", "水平对齐", None))
        self.label_10.setText(_translate("Editor_Footer", "垂直对齐", None))
        self.label_11.setText(_translate("Editor_Footer", "文本控制", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Editor_Footer", "对齐", None))
        self.btn_ok.setText(_translate("Editor_Footer", "确定", None))
        self.btn_cancel.setText(_translate("Editor_Footer", "取消", None))

