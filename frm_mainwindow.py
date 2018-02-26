# -*- coding:utf-8 -*-


from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot

from ui_mainwindow import Ui_MainWindow

from modual_Editor import Frm_Editor_Main

from modual_Sales import Frm_Sales_SO_Main
from modual_Sales import Frm_Sales_DB_Main

from modual_Nitori import Frm_Nitori_Main
from modual_Nitori import Frm_Nitori_CargoCheck

from modual_Stat import Frm_Stat_Main


from core import LoadServerDataClass_PYQT_ODBC
from core import MysqlHandle

from bom import Bom

import pdb


class Frm_MainWindow(QtGui.QMainWindow, Ui_MainWindow):
     
    def __init__(self, parent=None):
        
        super(Frm_MainWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.tabWidget.tabCloseRequested.connect(self._tab_close_requested)
        
        if self.tabWidget.count() == 0:
            self.on_btn_so_clicked()


    @pyqtSlot(int)
    def _tab_close_requested(self, tabIndex):
        w = self.tabWidget.widget(tabIndex)
        w.close()
        self.tabWidget.removeTab(tabIndex)
    
    
    @pyqtSlot()
    def on_action_editor_triggered(self):
        ed = Frm_Editor_Main(parent=self)
        ed.exec_()
    

    @pyqtSlot()
    def on_action_Quit_triggered(self):
        self.close()
    
    
    @pyqtSlot()
    def on_actionBom_triggered(self):
        bp = Bom()
        
        all_need_list = bp.define_01709()
        
        guige = {'w': 1.02,
                 'h': 2.3,
                 'op': 'r'}
        
        lst = bp.cacu(all_need_list, guige)
        
#        print(lst)
#[('89309', 0.16708333333333333), ('84131', 0.3333333333333333), ('84132', 0.0), ('84135', 0.194), ('85254', 0), ('84110', 4), ('84024', 4), ('84115', 9.799999999999999), ('84121', 4.6), ('84122', 1), ('84111', 0), ('84113', 1), ('84102', 1), ('84112', 1), ('84103', 1), ('84039', 12.87), ('84034', 13.52), ('89301', 1.04), ('84123', 2.3), ('84104', 2)]
        
        
        # 针对以上列表，计算总cost
        mh = MysqlHandle()
        mh.connect()
        
        
        lst2 = []
        for invCode, quantity in lst:
            invCost = mh.BOM_get_invCost(invCode)
            amount = invCost * quantity
            lst2.append((invCode, quantity, invCost, amount))
        
        mh.disconnect()
        
        print(lst2)
        
        total = sum([tp[3] for tp in lst2])
        print(total)
    

    # 需要把tab全部手动关闭，否则资源回收错误，程序崩溃
    def closeEvent(self, event):
        while self.tabWidget.currentIndex() >= 0:
            w = self.tabWidget.widget(self.tabWidget.currentIndex())
            w.close()
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
        event.accept()


    @pyqtSlot()
    def on_btn_so_clicked(self):
        w = Frm_Sales_SO_Main()
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        idx = self.tabWidget.addTab(w, '销售订单列表')
        self.tabWidget.setCurrentIndex(idx)
    
    
    @pyqtSlot()
    def on_btn_db_clicked(self):
        w = Frm_Sales_DB_Main()
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        idx = self.tabWidget.addTab(w, '发货单列表')
        self.tabWidget.setCurrentIndex(idx)
    
    
    @pyqtSlot()
    def on_btn_nm_clicked(self):
        w = Frm_Nitori_Main()
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        idx = self.tabWidget.addTab(w, 'NITORI订单处理')
        self.tabWidget.setCurrentIndex(idx)


    @pyqtSlot()
    def on_btn_nitori_cargocheck_clicked(self):
        w = Frm_Nitori_CargoCheck()
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        idx = self.tabWidget.addTab(w, 'NITORI对账')
        self.tabWidget.setCurrentIndex(idx)



    @pyqtSlot()
    def on_btn_stat_clicked(self):
        w = Frm_Stat_Main()
        w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        idx = self.tabWidget.addTab(w, '销售统计')
        self.tabWidget.setCurrentIndex(idx)





#class printer():
#    
#    #打印机列表
#    @staticmethod
#    def printerList():
#        printer = []
#        printerInfo = QtGui.QPrinterInfo()
#        for item in printerInfo.availablePrinters():
#            printer.append(item.printerName())
#        return printer
#    
#    #打印任务
#    @staticmethod
#    def printing(printer, context, preview=True):
#        
#        printerInfo = QtGui.QPrinterInfo()
#        p = QtGui.QPrinter()
#        for item in printerInfo.availablePrinters():
#            if printer == item.printerName():
#                p = QtGui.QPrinter(item)
#        doc = QtGui.QTextDocument()
#        doc.setHtml(u'%s' % context)
##        print(doc.pageSize())
#        doc.setPageSize(QtCore.QSizeF(793.7, 1122.5))
##        print(doc.pageSize())
#        
#        # 这里要设置纸张横向
#        #QPrinter.Portrait	0	the page's height is greater than its width.
#        #QPrinter.Landscape	1	the page's width is greater than its height.
#
#        p.setOrientation(QtGui.QPrinter.Landscape)
#        
##        doc.setPageSize(QtCore.QSizeF(793.7, 1122.5))
#        
#        doc.setPageSize(QtCore.QSizeF(1122.5, 793.7))
#        
#        
##        doc.setPageSize(QtCore.QSizeF(p.logicalDpiX()*(80/25.4),
##                                      p.logicalDpiY()*(297/25.4)))
##        p.setOutputFormat(QtGui.QPrinter.NativeFormat)
#        
#        
#        
#        if preview == False:
#            doc.print_(p)
#        
#        else:
#            #开启预览窗体，如果关闭则返回0，打印则返回1
#            prt_preview = QtGui.QPrintPreviewDialog(p)
#            # void paintRequested (QPrinter*)
#            prt_preview.paintRequested.connect(doc.print_)
#            
#            if prt_preview.exec_() == 1:
#                pass
        