# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\TosoProgram\TosoFrame\TosoFrame\res_Sales\Sales_SO_Detail.ui'
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

class Ui_Sales_SO_Detail(object):
    def setupUi(self, Sales_SO_Detail):
        Sales_SO_Detail.setObjectName(_fromUtf8("Sales_SO_Detail"))
        Sales_SO_Detail.resize(1408, 836)
        self.btn_print = QtGui.QPushButton(Sales_SO_Detail)
        self.btn_print.setGeometry(QtCore.QRect(20, 10, 101, 31))
        self.btn_print.setObjectName(_fromUtf8("btn_print"))
        self.layoutWidget = QtGui.QWidget(Sales_SO_Detail)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 50, 1232, 131))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_socode = QtGui.QLabel(self.layoutWidget)
        self.label_socode.setMinimumSize(QtCore.QSize(320, 0))
        self.label_socode.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.label_socode.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_socode.setFont(font)
        self.label_socode.setObjectName(_fromUtf8("label_socode"))
        self.gridLayout.addWidget(self.label_socode, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_soabbname = QtGui.QLabel(self.layoutWidget)
        self.label_soabbname.setMinimumSize(QtCore.QSize(320, 0))
        self.label_soabbname.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_soabbname.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_soabbname.setFont(font)
        self.label_soabbname.setObjectName(_fromUtf8("label_soabbname"))
        self.gridLayout.addWidget(self.label_soabbname, 0, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 4, 1, 1)
        self.label_date = QtGui.QLabel(self.layoutWidget)
        self.label_date.setMinimumSize(QtCore.QSize(320, 0))
        self.label_date.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_date.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_date.setFont(font)
        self.label_date.setObjectName(_fromUtf8("label_date"))
        self.gridLayout.addWidget(self.label_date, 0, 5, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(80, 0))
        self.label_3.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_cuspo = QtGui.QLabel(self.layoutWidget)
        self.label_cuspo.setMinimumSize(QtCore.QSize(320, 0))
        self.label_cuspo.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_cuspo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_cuspo.setFont(font)
        self.label_cuspo.setObjectName(_fromUtf8("label_cuspo"))
        self.gridLayout.addWidget(self.label_cuspo, 1, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.layoutWidget)
        self.label_11.setMinimumSize(QtCore.QSize(80, 0))
        self.label_11.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 1, 2, 1, 1)
        self.label_person = QtGui.QLabel(self.layoutWidget)
        self.label_person.setMinimumSize(QtCore.QSize(320, 0))
        self.label_person.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_person.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_person.setFont(font)
        self.label_person.setObjectName(_fromUtf8("label_person"))
        self.gridLayout.addWidget(self.label_person, 1, 3, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(80, 0))
        self.label_5.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 4, 1, 1)
        self.label_predate = QtGui.QLabel(self.layoutWidget)
        self.label_predate.setMinimumSize(QtCore.QSize(320, 0))
        self.label_predate.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_predate.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_predate.setFont(font)
        self.label_predate.setObjectName(_fromUtf8("label_predate"))
        self.gridLayout.addWidget(self.label_predate, 1, 5, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(80, 0))
        self.label_8.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.label_memo = QtGui.QLabel(self.layoutWidget)
        self.label_memo.setMinimumSize(QtCore.QSize(320, 0))
        self.label_memo.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_memo.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_memo.setFont(font)
        self.label_memo.setObjectName(_fromUtf8("label_memo"))
        self.gridLayout.addWidget(self.label_memo, 2, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.layoutWidget)
        self.label_10.setMinimumSize(QtCore.QSize(80, 0))
        self.label_10.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 2, 1, 1)
        self.label_koulv = QtGui.QLabel(self.layoutWidget)
        self.label_koulv.setMinimumSize(QtCore.QSize(320, 0))
        self.label_koulv.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_koulv.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_koulv.setFont(font)
        self.label_koulv.setObjectName(_fromUtf8("label_koulv"))
        self.gridLayout.addWidget(self.label_koulv, 2, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(80, 0))
        self.label_6.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 4, 1, 1)
        self.label_scname = QtGui.QLabel(self.layoutWidget)
        self.label_scname.setMinimumSize(QtCore.QSize(320, 0))
        self.label_scname.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_scname.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_scname.setFont(font)
        self.label_scname.setObjectName(_fromUtf8("label_scname"))
        self.gridLayout.addWidget(self.label_scname, 2, 5, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setMinimumSize(QtCore.QSize(80, 0))
        self.label_9.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_maker = QtGui.QLabel(self.layoutWidget)
        self.label_maker.setMinimumSize(QtCore.QSize(320, 0))
        self.label_maker.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_maker.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_maker.setFont(font)
        self.label_maker.setObjectName(_fromUtf8("label_maker"))
        self.gridLayout.addWidget(self.label_maker, 3, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setMinimumSize(QtCore.QSize(80, 0))
        self.label_7.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 3, 2, 1, 1)
        self.label_verifier = QtGui.QLabel(self.layoutWidget)
        self.label_verifier.setMinimumSize(QtCore.QSize(320, 0))
        self.label_verifier.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_verifier.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_verifier.setFont(font)
        self.label_verifier.setObjectName(_fromUtf8("label_verifier"))
        self.gridLayout.addWidget(self.label_verifier, 3, 3, 1, 1)
        self.label_12 = QtGui.QLabel(self.layoutWidget)
        self.label_12.setMinimumSize(QtCore.QSize(80, 0))
        self.label_12.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 3, 4, 1, 1)
        self.label_cuthint = QtGui.QLabel(self.layoutWidget)
        self.label_cuthint.setMinimumSize(QtCore.QSize(320, 0))
        self.label_cuthint.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_cuthint.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_cuthint.setFont(font)
        self.label_cuthint.setObjectName(_fromUtf8("label_cuthint"))
        self.gridLayout.addWidget(self.label_cuthint, 3, 5, 1, 1)
        self.label_14 = QtGui.QLabel(self.layoutWidget)
        self.label_14.setMinimumSize(QtCore.QSize(80, 0))
        self.label_14.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout.addWidget(self.label_14, 4, 0, 1, 1)
        self.label_income = QtGui.QLabel(self.layoutWidget)
        self.label_income.setMinimumSize(QtCore.QSize(320, 0))
        self.label_income.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_income.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_income.setFont(font)
        self.label_income.setObjectName(_fromUtf8("label_income"))
        self.gridLayout.addWidget(self.label_income, 4, 1, 1, 1)
        self.label_13 = QtGui.QLabel(self.layoutWidget)
        self.label_13.setMinimumSize(QtCore.QSize(80, 0))
        self.label_13.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 4, 2, 1, 1)
        self.label_cost = QtGui.QLabel(self.layoutWidget)
        self.label_cost.setMinimumSize(QtCore.QSize(320, 0))
        self.label_cost.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_cost.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_cost.setFont(font)
        self.label_cost.setObjectName(_fromUtf8("label_cost"))
        self.gridLayout.addWidget(self.label_cost, 4, 3, 1, 1)
        self.label_15 = QtGui.QLabel(self.layoutWidget)
        self.label_15.setMinimumSize(QtCore.QSize(80, 0))
        self.label_15.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 4, 4, 1, 1)
        self.label_costrate = QtGui.QLabel(self.layoutWidget)
        self.label_costrate.setMinimumSize(QtCore.QSize(320, 0))
        self.label_costrate.setMaximumSize(QtCore.QSize(320, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_costrate.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_costrate.setFont(font)
        self.label_costrate.setObjectName(_fromUtf8("label_costrate"))
        self.gridLayout.addWidget(self.label_costrate, 4, 5, 1, 1)
        self.tableView = QtGui.QTableView(Sales_SO_Detail)
        self.tableView.setGeometry(QtCore.QRect(20, 190, 1371, 621))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableView.setFont(font)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.verticalHeader().setVisible(False)

        self.retranslateUi(Sales_SO_Detail)
        QtCore.QMetaObject.connectSlotsByName(Sales_SO_Detail)

    def retranslateUi(self, Sales_SO_Detail):
        Sales_SO_Detail.setWindowTitle(_translate("Sales_SO_Detail", "Form", None))
        self.btn_print.setText(_translate("Sales_SO_Detail", "套打四联单", None))
        self.label.setText(_translate("Sales_SO_Detail", "订单号", None))
        self.label_socode.setText(_translate("Sales_SO_Detail", "socode", None))
        self.label_2.setText(_translate("Sales_SO_Detail", "客户简称", None))
        self.label_soabbname.setText(_translate("Sales_SO_Detail", "soabbname", None))
        self.label_4.setText(_translate("Sales_SO_Detail", "订单日期", None))
        self.label_date.setText(_translate("Sales_SO_Detail", "date", None))
        self.label_3.setText(_translate("Sales_SO_Detail", "对方订单号", None))
        self.label_cuspo.setText(_translate("Sales_SO_Detail", "cuspo", None))
        self.label_11.setText(_translate("Sales_SO_Detail", "业务员", None))
        self.label_person.setText(_translate("Sales_SO_Detail", "person", None))
        self.label_5.setText(_translate("Sales_SO_Detail", "预发货日期", None))
        self.label_predate.setText(_translate("Sales_SO_Detail", "predate", None))
        self.label_8.setText(_translate("Sales_SO_Detail", "备注", None))
        self.label_memo.setText(_translate("Sales_SO_Detail", "memo", None))
        self.label_10.setText(_translate("Sales_SO_Detail", "扣率%", None))
        self.label_koulv.setText(_translate("Sales_SO_Detail", "koulv", None))
        self.label_6.setText(_translate("Sales_SO_Detail", "发运方式", None))
        self.label_scname.setText(_translate("Sales_SO_Detail", "scname", None))
        self.label_9.setText(_translate("Sales_SO_Detail", "制单人", None))
        self.label_maker.setText(_translate("Sales_SO_Detail", "maker", None))
        self.label_7.setText(_translate("Sales_SO_Detail", "审核人", None))
        self.label_verifier.setText(_translate("Sales_SO_Detail", "verifier", None))
        self.label_12.setText(_translate("Sales_SO_Detail", "截断方式", None))
        self.label_cuthint.setText(_translate("Sales_SO_Detail", "cuthint", None))
        self.label_14.setText(_translate("Sales_SO_Detail", "销售收入", None))
        self.label_income.setText(_translate("Sales_SO_Detail", "income", None))
        self.label_13.setText(_translate("Sales_SO_Detail", "销售成本", None))
        self.label_cost.setText(_translate("Sales_SO_Detail", "cost", None))
        self.label_15.setText(_translate("Sales_SO_Detail", "成本率", None))
        self.label_costrate.setText(_translate("Sales_SO_Detail", "costrate", None))

