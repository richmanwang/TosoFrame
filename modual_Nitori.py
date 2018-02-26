# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 13:49:26 2016

@author: 008
"""

import sqlite3
import os
import win32com.client
import xlrd
import xlsxwriter
from collections import defaultdict

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot

from ui_Nitori_Main import Ui_Nitori_Main
from ui_Nitori_Keyword import Ui_Nitori_Keyword
from ui_Nitori_CargoCheck import Ui_Nitori_CargoCheck

from core import MysqlHandle

import pdb


class Frm_Nitori_CargoCheck(QtGui.QWidget, Ui_Nitori_CargoCheck):
     
#    Nitori发来的货物入仓清单 CARGO RECEIPT 里面只有1个表，表名 001796700002-1
#    cargo_receipt_no	K4
#    cargo_receipt_date	K5
#    date	B12
#    place_name	B14
#    file_name	读取文件名称
#    数据区域  B16~L 行数不定
     
    def __init__(self, parent=None):
        super(Frm_Nitori_CargoCheck, self).__init__(parent)
        self.setupUi(self)
    
    
    @pyqtSlot()
    def on_btn_process_2_clicked(self):
        count = self.tableView.tableModel.rowCount()
        if count > 0:
            lst = []
            for i in range(count):
                itm = self.tableView.tableModel.item(i, 0)
                fileFullName = itm.text()
                lst.append(fileFullName)
            
            # 以下读取文件
            xrd = ExcelRead()
            sn = SqliteNitori()
            
            for i, fileFullName in enumerate(lst):
                
                h_list, b_list = xrd.CC_get_CargoReceipt(fileFullName)
#                pdb.set_trace()
                sn.CC_insert_CargoReceipt(h_list, b_list)
                
                # 设置 "已读入" 字样
                itm = self.tableView.tableModel.item(i, 1)
                itm.setData('已读入', QtCore.Qt.DisplayRole)
                self.tableView.tableModel.setItem(i, 1, itm)
                
                # 设置总行数
                itm = self.tableView.tableModel.item(i, 2)
                itm.setData(len(b_list), QtCore.Qt.DisplayRole)
                self.tableView.tableModel.setItem(i, 2, itm)
                
                # 设置 单据总金额
                itm = self.tableView.tableModel.item(i, 3)
                itm.setData(h_list[-1], QtCore.Qt.DisplayRole)
                self.tableView.tableModel.setItem(i, 3, itm)
                
                # 设置 明细总金额
                mx_total_amoount = sum( [tp[8] for tp in b_list] )
                itm = self.tableView.tableModel.item(i, 4)
                itm.setData(mx_total_amoount, QtCore.Qt.DisplayRole)
                self.tableView.tableModel.setItem(i, 4, itm)
                
                self.tableView.repaint()
            
            QtGui.QMessageBox.information(self, '提示', '读取完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    
    
    @pyqtSlot()
    def on_btn_delete_all_data_clicked(self):
        result = QtGui.QMessageBox.warning(self, '警告', '将会删除所有旧数据，确定吗？', QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes:
            sn = SqliteNitori()
            sn.CC_delete_data()
            QtGui.QMessageBox.information(self, '提示', '旧数据已全部删除', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


    @pyqtSlot()
    def on_btn_output_clicked(self):
#        QString getSaveFileName (QWidget parent = None, QString caption = '', QString directory = '', QString filter = '', Options options = 0)
        fileFullName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + 'Summary', 'Excel Files (*.xlsx)')
        
        if fileFullName:
            ew = ExcelWrite()
            sn = SqliteNitori()
            
#            [('2017/03/13-2017/03/19', '000000510005 宁波银泰城店', '2000000038660', 440.6, 5, '2017/03/18', 'DONG BO20170313-20170319.xls'), .... ]
            dataList200 = sn.CC_get_200_summary()
            
#            [('DONG BAO20170327-20170331.xls', 4, 550.9), .... ]
            dataListCargo = sn.CC_get_cargo_summary()
            
            ew.CC_output_summary(fileFullName, dataList200, dataListCargo)
            
            QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)




class Frm_Nitori_Main(QtGui.QWidget, Ui_Nitori_Main):
     
    def __init__(self, parent=None):
        super(Frm_Nitori_Main, self).__init__(parent)
        self.setupUi(self)
        
        self.database_columns = ['采购单号', 
                                '行号', 
                                '单据号', 
                                '订单行', 
                                '顾客名', 
                                '销售日', 
                                '收货日', 
                                '商品CD', 
                                '商品名', 
                                '原价', 
                                '成品宽', 
                                '成品高', 
                                '安装高度', 
                                '安装方法', 
                                '系列', 
                                '式样', 
                                '操作方法', 
                                '操作位置', 
                                '号码', 
                                '数量', 
                                '进货方CD', 
                                '进货方名称', 
                                '单位原价', 
                                '备注']
        # create tableView head
        headStr = ['采购单号', '单据号', '顾客名', '进货方名称', '源文件名', '总行数', 'Nitori总原价', 'Toso总金额', '差额', '差额率%', '匹配失败']
        headWidth = [130, 130, 80, 110, 170, 60, 90, 90, 90, 90, 90]
        
        # 设置model
        self.tableModel = QtGui.QStandardItemModel()
        self.tableModel.setSortRole(QtCore.Qt.UserRole)
        self.tableModel.setHorizontalHeaderLabels(headStr)
        
        self.tableView.setModel(self.tableModel)
        
        # 设置可点击排序
#        self.tableView.setSortingEnabled(True)
        
        for i, width in enumerate(headWidth):
            self.tableView.setColumnWidth(i, width)


    @pyqtSlot()
    def on_btn_open_clicked(self):
        fileFullName = QtGui.QFileDialog.getOpenFileName(self, 'Choose a file', '.', 'Excel Files (*.xls *.xlsx)')
        
        if fileFullName:
            # 设置lineEdit
            self.lineEdit.setText(fileFullName)
            self.lineEdit.repaint()
            
            # 取得文件名
            fi = QtCore.QFileInfo(fileFullName)
            fileName = fi.fileName()
            
            xrd = ExcelRead()
            
            mxList = xrd.getHardMX(fileFullName)
            
            # 每行末尾追加文件名
            for mx in mxList:
                mx.append(fileName)
            
#            # 加入判断 （暂时不用判断）
#            chk = xrd.checkHardData(mxList)
#            if True not in chk:
#                # 插入原始数据
#                mh = MysqlHandle()
#                mh.NT_Match_insert_mx(mxList)
#                
#                print('数据已读入')
#                
#                # 追加update
#                mh.NT_Match_update_mx()
#                print('数据已update处理')
#                
#                # 刷新table
#                self.__update_tableModel()
#            
#            else:
#                QtGui.QMessageBox.information(self,
#                                              '提示',
#                                              '源文件含有非标准行，已停止处理。\n请检查以下列：\n\n  A列（采购单号未填）\n  J列（原价未填或为零）\n  O列（系列未填）',
#                                              QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            
            # 插入原始数据（mxList每行末尾包含文件名）
            mh = MysqlHandle()
            mh.NT_Match_insert_mx(mxList)
            
            print('数据已读入')
            
            # 追加update
            mh.NT_Match_update_mx()
            print('数据已update处理')
            
            # 刷新table
            self.__update_tableModel()
            
            

    
    def __update_tableModel(self):
        
        mh = MysqlHandle()
        dataList = mh.NT_Match_fetch_distinct_orders()
        
        rowCount = len(dataList)
        
        self.tableModel.setRowCount(0)
        
        if dataList:
            # ('2000000040065', '1000001505848', '周 小姐', '上海七宝店', 3, 2100.30, 2167.43, -67.13, 0)
            for i, tp in enumerate(dataList):
                # 先把纯data设置到userrole（目的是以后可以按照userrole排序）
                for j in range(len(tp)):
                    itm = QtGui.QStandardItem()
                    value = tp[j]
                    itm.setData(value, QtCore.Qt.UserRole)
                    itm.setData(value, QtCore.Qt.DisplayRole)   # 同样设置displayrole
                    self.tableModel.setItem(i, j, itm)
            
            # 第六列（总行数）整形设置，对齐设置（这里要把金额改回来。如果总金额是0，会设置成空串，造成格式化出错）
            for i in range(rowCount):
                itm = self.tableModel.item(i, 5)
                amount = itm.data(QtCore.Qt.UserRole)
                itm.setTextAlignment(QtCore.Qt.AlignCenter)
            
            # 第七列（Nitori总原价）金额设置，对齐设置（这里要把金额改回来。如果总金额是0，会设置成空串，造成格式化出错）
            for i in range(rowCount):
                itm = self.tableModel.item(i, 6)
                amount = itm.data(QtCore.Qt.UserRole)
                if amount == '':
                    amount = 0.0
                itm.setData('{:,.2f}'.format(amount), QtCore.Qt.DisplayRole)
                itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
            # 第八列（Toso总金额）金额设置，对齐设置（这里要把金额改回来。如果总金额是0，会设置成空串，造成格式化出错）
            for i in range(rowCount):
                itm = self.tableModel.item(i, 7)
                amount = itm.data(QtCore.Qt.UserRole)
                if amount == '':
                    amount = 0.0
                itm.setData('{:,.2f}'.format(amount), QtCore.Qt.DisplayRole)
                itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            
            # 第九列（差额）金额设置，对齐设置（这里要把金额改回来。如果总金额是0，会设置成空串，造成格式化出错）
            for i in range(rowCount):
                itm = self.tableModel.item(i, 8)
                amount = itm.data(QtCore.Qt.UserRole)
                if amount == '':
                    amount = 0.0
                itm.setData('{:,.2f}'.format(amount), QtCore.Qt.DisplayRole)
                itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            
            # 第十列（差额率）设置
            for i in range(rowCount):
                itm = self.tableModel.item(i, 9)
                amount = itm.data(QtCore.Qt.UserRole)
                if amount == '':
                    amount = 0.0
                itm.setData('{:,.2f}'.format(amount), QtCore.Qt.DisplayRole)
                itm.setTextAlignment(QtCore.Qt.AlignCenter)
            
            # 第十一列（匹配失败）整形设置，对齐设置
            for i in range(rowCount):
                itm = self.tableModel.item(i, 10)
                amount = itm.data(QtCore.Qt.UserRole)
                itm.setTextAlignment(QtCore.Qt.AlignCenter)
            
            # 最后一行添加合计信息（设置所有userrole为None，就可以不参与排序，一直再最后一行）
            for i in range(self.tableModel.columnCount()):
                itm = QtGui.QStandardItem()
                itm.setData(None, QtCore.Qt.UserRole)
                itm.setData(QtGui.QBrush(QtGui.QColor(253, 236, 212)), QtCore.Qt.BackgroundRole)
                self.tableModel.setItem(rowCount, i, itm)
            
            #追加check double
            self.__check_double()
            
            #追加check rate
            self.__check_rate()
            
            #追加匹配失败
            self.__check_match_fail()
            
        # 设置合计值
        if dataList:
            rows = sum([tp[5] for tp in dataList])
            nt_price = sum([tp[6] for tp in dataList])
            toso_price = sum([tp[7] for tp in dataList])
            price_diff = sum([tp[8] for tp in dataList])
            match_fail = sum([tp[10] for tp in dataList])
        else:
            rows = 0
            nt_price = 0.0
            toso_price = 0.0
            price_diff = 0.0
            match_fail = 0
        
        # 设置合计行
        itm = self.tableModel.item(rowCount, 5)
        itm.setData(rows, QtCore.Qt.DisplayRole)
        itm.setTextAlignment(QtCore.Qt.AlignCenter)
        
        itm = self.tableModel.item(rowCount, 6)
        itm.setData('{:,.2f}'.format(nt_price), QtCore.Qt.DisplayRole)
        itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            
        itm = self.tableModel.item(rowCount, 7)
        itm.setData('{:,.2f}'.format(toso_price), QtCore.Qt.DisplayRole)
        itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        itm = self.tableModel.item(rowCount, 8)
        itm.setData('{:,.2f}'.format(price_diff), QtCore.Qt.DisplayRole)
        itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        itm = self.tableModel.item(rowCount, 10)
        itm.setData(match_fail, QtCore.Qt.DisplayRole)
        itm.setTextAlignment(QtCore.Qt.AlignCenter)
    
    
    def __check_match_fail(self):
        # 检查 差额率
        # 行数-1 扣除合计栏
        for i in range(self.tableModel.rowCount()-1):
            itm = self.tableModel.item(i, 9)
            value = itm.data(QtCore.Qt.UserRole)
            if value < -0.1 or value > 0.1:
                itm.setData(QtGui.QBrush(QtCore.Qt.red), QtCore.Qt.BackgroundColorRole)
    
            
    def __check_rate(self):
        # 检查 差额
        # 行数-1 扣除合计栏
        for i in range(self.tableModel.rowCount()-1):
            itm = self.tableModel.item(i, 8)
            value = itm.data(QtCore.Qt.UserRole)
            if value < -3.0 or value > 3.0:
                itm.setData(QtGui.QBrush(QtCore.Qt.red), QtCore.Qt.BackgroundColorRole)
        
        
    
    def __check_double(self):
        # 检查model，返回可疑列表
        # 以下检查重复数据（2,3列）  '1000001505848', '周 小姐'        第4列为店名，是有重复的
        # 行数-1 扣除合计栏
        # 第二列
        lst = []
        for i in range(self.tableModel.rowCount()-1):
            lst.append( self.tableModel.item(i, 1).data(QtCore.Qt.UserRole) )
        rst = self.__check_double_data(lst)
        self.__mark_double(1, rst)
        
        # 第三列
        lst = []
        for i in range(self.tableModel.rowCount()-1):
            lst.append( self.tableModel.item(i, 2).data(QtCore.Qt.UserRole) )
        rst = self.__check_double_data(lst)
        self.__mark_double(2, rst)


    def __check_double_data(self, lst):
        # 检查一个列表中是否出现重复值，以及值在列表中的位置
        # s=[11,22,11,44,22,33]
        s = lst
        d = defaultdict(list)
        for k, va in [(v, i) for i, v in enumerate(s)]:
            d[k].append(va)
        return d.items()
    
    
    def __mark_double(self, col, check_result):
        # (33, [5])
        # 标记
        for value, addressList in check_result:
            if len(addressList) > 1:   #出现重复值
                for address in addressList:
                    itm = self.tableModel.item(address, col)
                    itm.setData(QtGui.QBrush(QtCore.Qt.yellow), QtCore.Qt.BackgroundColorRole)
    
    
    @pyqtSlot()
    def on_btn_refresh_table_clicked(self):
        self.__update_tableModel()
        

#    @pyqtSlot()
#    def on_btn_create_order_clicked(self):
#        # 如果存在匹配失败的订单，弹出警告
#        for i in range(self.tableModel.rowCount()-1):
#            itm = self.tableModel.item(i, 9)
#            if itm.data(QtCore.Qt.UserRole) != 0:
#                QtGui.QMessageBox.warning(self, '确认', '请注意，存在未能匹配商品编码的数据！')
#        
#        sourceFileName = self.lineEdit.text()
#        place = sourceFileName.find('Hard_TOSO_') + 10
#        saveName = sourceFileName[place:place+8]
#        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + saveName + ' 东装订单', 'Excel Files (*.xlsx)')
#        
#        if fileName != '':
#            # 需要替换，否则保存出错
#            fileName = fileName.replace('/', '\\') 
#            
#            # 取得文件名称
#            fi = QtCore.QFileInfo(sourceFileName)
#            sourceShortFileName = fi.fileName()
#            
#            mh = MysqlHandle()
#            dataList = mh.NT_Match_organize_order_data()
#            
#            xlh = ExcelHandle()
#            
#            xlh.createExcelApp()
#            
#            xlh.createFinalOrders(sourceShortFileName, dataList)
#            
#            xlh.excelBookSaveAs(fileName)
#            
#            xlh.closeExcelBook()
#            xlh.quitExcelApp()
#            QtGui.QMessageBox.information(self, '提示', '完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            
    
    @pyqtSlot()
    def on_btn_create_order_clicked(self):
        # 如果存在匹配失败的订单，弹出警告
        match_fail = False
        for i in range(self.tableModel.rowCount()-1):
            itm = self.tableModel.item(i, 10) #检查第11列匹配失败数
            if itm.data(QtCore.Qt.UserRole) != 0:
                match_fail = True
        
        if match_fail == True:
            QtGui.QMessageBox.warning(self, '确认', '请注意，存在未能匹配商品编码的数据！')
        
        
        sourceFileName = self.lineEdit.text()
        place = sourceFileName.find('Hard_TOSO_') + 10
        saveName = sourceFileName[place:place+8]
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + saveName + ' 东装订单', 'Excel Files (*.xlsx)')
        
        if fileName:
            # 需要替换，否则保存出错
            fileName = fileName.replace('/', '\\') 
            
            mh = MysqlHandle()
            #dataList里含有源文件名
            dataList = mh.NT_Match_organize_order_data()
            
            xlh = ExcelHandle()
            
            xlh.createExcelApp()
            
            xlh.createFinalOrders(dataList)
            
            xlh.excelBookSaveAs(fileName)
            
            xlh.closeExcelBook()
            xlh.quitExcelApp()
            QtGui.QMessageBox.information(self, '提示', '完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    
    
    
    
    
    
    
    @pyqtSlot()
    def on_btn_create_dispatch_clicked(self):
        sourceFileName = self.lineEdit.text()
        place = sourceFileName.find('Hard_TOSO_') + 10
        saveName = sourceFileName[place:place+8]
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + saveName + ' 发货单', 'Excel Files (*.xlsx)')
        
        if fileName:
            ##### 需要替换，否则保存出错 #####
            fileName = fileName.replace('/', '\\') 
            
            mh = MysqlHandle()
            dataList = mh.NT_Match_organize_dispatch_data()
            
            xlh = ExcelHandle()
            
            xlh.createExcelApp()
            
            xlh.createFinalDispatches(dataList)
            
            xlh.excelBookSaveAs(fileName)
            
            xlh.closeExcelBook()
            xlh.quitExcelApp()
            QtGui.QMessageBox.information(self, '提示', '完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


    @pyqtSlot()
    def on_btn_input_keyword_clicked(self):
        a = Frm_Nitori_Keyword(self)
        a.exec_()




class Frm_Nitori_Keyword(QtGui.QDialog, Ui_Nitori_Keyword):
     
    def __init__(self, parent=None):
        super(Frm_Nitori_Keyword, self).__init__(parent)
        self.setupUi(self)
        
        # create tablewidget head
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["关键字", "商品编码", "价格表定价", "扣率"])
        
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 80)
        
#        self.ldh = SqliteNitori()
        
        self.tableWidget.itemChanged.connect(self.__item_changed)
        
        self.__refresh_table()


    def __refresh_table(self):
        mh = MysqlHandle()
        lst = mh.NT_Match_fetch_keyword_match_fail()
        # [('F-15单轨FH基本',), ('F-23单轨FH基本',), ('F-23双轨FH基本',), ('F-27单轨FH基本',)]
        lst = [tp[0] for tp in lst]
        
        self.tableWidget.clearContents()

        rowCount = len(lst)
        self.tableWidget.setRowCount(rowCount)
        
        self.tableWidget.itemChanged.disconnect(self.__item_changed)
        
        # keyword 编码 定价 折扣   共4列
        for i, keyword in enumerate(lst):
            
            itm_0 = QtGui.QTableWidgetItem( keyword )
            itm_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            
            itm_1 = QtGui.QTableWidgetItem("")
            
            itm_2 = QtGui.QTableWidgetItem("")
            itm_2.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置对齐
            
            itm_3 = QtGui.QTableWidgetItem("")
            itm_3.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置对齐
        
            self.tableWidget.setItem(i, 0, itm_0)
            self.tableWidget.setItem(i, 1, itm_1)
            self.tableWidget.setItem(i, 2, itm_2)
            self.tableWidget.setItem(i, 3, itm_3)

        self.tableWidget.itemChanged.connect(self.__item_changed)
    
    

    @pyqtSlot()
    def on_btn_refresh_clicked(self):
        self.__refresh_table()
    
    
    
    @pyqtSlot()
    def on_btn_ok_clicked(self):
        
        lst = self.__collect_table_data()
        
        self.ldh.NM_insert_keyword(lst)
        
        #再次update
        self.ldh.NM_update_mx()
        
        self.__refresh_table()



    def __collect_table_data(self):
        # 收集已经填写好的数据，并返回一个列表（为了更新数据库成本信息）
        # 返回一个元组列表  [ (), (), ....]
        # 此处不做数据校验
        # keyword 编码 定价 折扣   共4列
        
        result_list = []
        
        for i in range(self.tableWidget.rowCount()):
            
            itm_0 = self.tableWidget.item(i, 0)
            itm_1 = self.tableWidget.item(i, 1)
            itm_2 = self.tableWidget.item(i, 2)
            itm_3 = self.tableWidget.item(i, 3)

            if (itm_1.text() != "") and (itm_2.text() != "") and (itm_3.text() != ""):
                tp = (itm_0.text(),
                      itm_1.text(),
                      float(itm_2.text()),
                      float(itm_3.text()),
                      None)     # 备注行空
                result_list.append(tp)
            
            else:
                print("忽略：未填写的完整的行", i)
        
        return result_list



    def __item_changed(self, itm):
        
        if itm.column() in [2, 3]:
            
            txt = itm.text()
            
            if itm.text() == "":
                pass
            
            else:
                try:
                    txt = float(txt)
                    txt = "%.2f" % (txt)
                except(ValueError):
                    txt = ""
                finally:
                    self.tableWidget.itemChanged.disconnect(self.__item_changed)
                    itm.setText(txt)
                    self.tableWidget.itemChanged.connect(self.__item_changed)


    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        self.close()



class SqliteNitori:
    
    def __init__(self):
        self.db = ".\\Nitori\\nitori.sqlite"
    
    
    def CC_delete_data(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM CC_CargoReceipt_HEAD")
        cursor.execute("DELETE FROM CC_CargoReceipt_BODY")
        conn.commit()
        
        cursor.close()
        conn.close()
    
        
    def CC_insert_CargoReceipt(self, headList, bodyList):
        
        # 最后加入文件名
#        headList.append(fileName)
        
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        # TODO: 查找是否编号重复
#        cargo_receipt_id = headList[0]
#        
#        sql = "SELECT cargo_receipt_no FROM CC_CargoReceipt_HEAD WHERE cargo_receipt_id=?"
#        cursor.execute(sql, (cargo_receipt_id,))
#        result = cursor.fetchone()
#        
#        if result:
#            print('发现重复，删除原有内容')
#            cursor.execute("DELETE FROM CC_CargoReceipt_HEAD WHERE cargo_receipt_id=?", (cargo_receipt_id,))
#            cursor.execute("DELETE FROM CC_CargoReceipt_BODY WHERE cargo_receipt_id=?", (cargo_receipt_id,))
        
        # 插入head
        head_sql = """
                    INSERT INTO
                    CC_CargoReceipt_HEAD (cargo_receipt_id, cargo_receipt_no, cargo_receipt_date, date, place_name, file_name, total_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
        cursor.executemany(head_sql, headList)
        
        body_sql = """
                    INSERT INTO
                    CC_CargoReceipt_BODY (cargo_receipt_id, NO, PO, nitori_code, description, price, PO_QTY, QTY, amount, arrival_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
        cursor.executemany(body_sql, bodyList)
        
        # 提交前，以上所有的都不会被写入
        conn.commit()
        
        cursor.close()
        conn.close()
    
    
        
    def CC_get_200_summary(self):
        
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        sql = """
                SELECT
                    CC_CargoReceipt_BODY.PO AS PO_No,
                    CC_CargoReceipt_HEAD.date,
                    CC_CargoReceipt_HEAD.place_name,
                    CC_CargoReceipt_BODY.arrival_date,
                    CC_CargoReceipt_HEAD.file_name,
                    Sum(CC_CargoReceipt_BODY.PO_QTY) AS COUNT,
                    Sum(CC_CargoReceipt_BODY.amount) AS TOTAL
                FROM
                    CC_CargoReceipt_BODY
                INNER JOIN CC_CargoReceipt_HEAD ON CC_CargoReceipt_BODY.cargo_receipt_id = CC_CargoReceipt_HEAD.cargo_receipt_id
                GROUP BY
                    CC_CargoReceipt_BODY.PO
                ORDER BY
                    CC_CargoReceipt_BODY.PO ASC
        """
        
        cursor.execute(sql)
        
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return result
    
    
    def CC_get_cargo_summary(self):
        
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        sql = """
            SELECT
                CC_CargoReceipt_HEAD.file_name,
                count(CC_CargoReceipt_BODY.PO) as rows,
                Sum(CC_CargoReceipt_BODY.amount) as amount
            FROM
                CC_CargoReceipt_BODY
            INNER JOIN CC_CargoReceipt_HEAD ON CC_CargoReceipt_HEAD.cargo_receipt_id = CC_CargoReceipt_BODY.cargo_receipt_id
            GROUP BY
                CC_CargoReceipt_HEAD.file_name
        """
        
        cursor.execute(sql)
        
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return result



class ExcelHandle(object):
    
    def createExcelApp(self):
        #创建excel
        self.xlsApp = win32com.client.DispatchEx("Excel.Application")
        print("Excel 程序开启")
    
    
    def quitExcelApp(self):
        self.xlsApp.Quit()
        print("Excel 程序退出")
    
    
    def openExcelBook(self, full_filename):
        self.xlsBook = self.xlsApp.Workbooks.Open(full_filename)
        print("文件已打开：%s" % full_filename)
        return self.xlsBook
    
    
    def closeExcelBook(self, save=False):
        self.xlsBook.Close(save)
        print("文件已关闭")
        
    
#    def getSheetNameList(self):
#        # 取得当前工作簿的所有表名
#        sheet_name_list = []
#        sheets_count = self.xlsBook.Worksheets.Count
#        for i in range(sheets_count):
#            name = self.xlsBook.Sheets(i+1).Name
#            sheet_name_list.append(name)
#        
#        return sheet_name_list
    
    
#    def getSheetColumnNameList(self, xlsSheetName):
#        # 只读取24列的列名
#        limit = 24
#        lst = []
#        sheet = self.xlsBook.Sheets(xlsSheetName)
#        
#        for i in range(limit):
#            lst.append( sheet.Cells(1, i+1).Text )  # 不用value
#        
#        return lst
    
    
#    def getRowCount(self, xlsSheetName):
#        # 取得数据行数，如果返回-1表示总行数验证出错（表内有空白）
#        # 最多读取1000行数据（从第2行到1001行）
#        rowLimit = 1000
#        sheet = self.xlsBook.Sheets(xlsSheetName)
#        
#        startRow = 2
#        maxRow = startRow + rowLimit
#        
#        lastRow_1 = 2
#        lastRow_2 = 2
#        lastRow_3 = 2
#        
#        # 第1列200号
#        currentRow = startRow
#        while currentRow < maxRow:
#            # 第一列200号，第二列单据号，第十列原价 是否有数据？都有才通过
#            if sheet.Cells(currentRow, 1).Text != "":
#                lastRow_1 += 1
#                currentRow += 1
#            else:
#                break
#        
#        # 第10列原价
#        currentRow = startRow
#        while currentRow < maxRow:
#            # 第一列200号，第二列单据号，第十列原价 是否有数据？都有才通过
#            if sheet.Cells(currentRow, 10).Text != "":
#                lastRow_2 += 1
#                currentRow += 1
#            else:
#                break
#        
#        # 第15列系列
#        currentRow = startRow
#        while currentRow < maxRow:
#            # 第一列200号，第二列单据号，第十列原价 是否有数据？都有才通过
#            if sheet.Cells(currentRow, 15).Text != "":
#                lastRow_3 += 1
#                currentRow += 1
#            else:
#                break
#        
#        
#        if lastRow_1 == lastRow_2 == lastRow_3:
#            return lastRow_1 - 2
#        else:
#            return -1
    
    
#    def getSheetMx(self, xlsSheetName, readRows):
#        
#        # 只读取24列的列名
##        col_limit = 24
#        
#        # 最多读取1000行数据（从第2行到1001行）
##        row_limit = 1000
#        
#        result_list = []
#        
#        sheet = self.xlsBook.Sheets(xlsSheetName)
#        
##        row = 2
##        max_row = row + row_limit
#        
##        while row < max_row:
#        for row in range(readRows):
#            # 调整
#            row += 2
#            tp = (
#                sheet.Cells(row, 1).Text,
#                sheet.Cells(row, 2).Value,  #行号
#                sheet.Cells(row, 3).Text,
#                sheet.Cells(row, 4).Value,  #订单行
#                sheet.Cells(row, 5).Text,
#                sheet.Cells(row, 6).Text,
#                sheet.Cells(row, 7).Text,
#                sheet.Cells(row, 8).Text,
#                sheet.Cells(row, 9).Text,
#                sheet.Cells(row, 10).Value,  #原价
#                sheet.Cells(row, 11).Text,
#                sheet.Cells(row, 12).Text,
#                sheet.Cells(row, 13).Text,
#                sheet.Cells(row, 14).Text,
#                sheet.Cells(row, 15).Text,
#                sheet.Cells(row, 16).Text,
#                sheet.Cells(row, 17).Text,
#                sheet.Cells(row, 18).Text,
#                sheet.Cells(row, 19).Text,
#                sheet.Cells(row, 20).Value,  #数量
#                sheet.Cells(row, 21).Text,
#                sheet.Cells(row, 22).Text,
#                sheet.Cells(row, 23).Value,  #单位原价
#                sheet.Cells(row, 24).Text
#            )
#            result_list.append(tp)
#            
#        return result_list
        
    
    def createSheetWithName(self, sheet_name):
        self.xlsBook.Sheets("s").Copy(None ,self.xlsBook.Sheets("s"))
        
    
    def createFinalOrders(self, organized_order_list):
        # 取得整理后的数据
        data_list = organized_order_list
        
        # 填充excel
#        xlsApp = self.createExcelApp()
#        xlsBook = self.openExcelBook(sys.path[0] + "\\order.xlsx")
#        xlsBook = self.openExcelBook("D:\\order.xlsx")
        xlsBook = self.openExcelBook(os.path.split(os.path.realpath(__file__))[0] + "\\Nitori\\order.xlsx")
        
        # 循环填充
        # [ ( ["采购单号", "单据号", "顾客名", "进货方名称", file_name],  [(row1), (row2), ...] ),
        #    .....]
        
        start = 1
        count = len(data_list)
        
        for data in data_list:
            # (order_number,  (dataes) )
            dataHead, dataMX = data
            
            PO, order_num, c_name, shop_name, file_name, order_rows, arrival_date = dataHead
            
            print("process {} ({}/{})".format(PO, start, count))
            
            # Copy([Before], [After])
            xlsBook.Sheets("s").Copy(None, self.xlsBook.Sheets(self.xlsBook.Worksheets.Count) )
            xlsBook.ActiveSheet.Name = PO
            
            # 填充数据（start_row=9, start_col=1） A9单元格
            self.__writeOrderMX(xlsBook.ActiveSheet,
                                dataHead,
                                dataMX,
                                startRow=9,
                                startCol=1,
                                textForce=[1,])
            start += 1
        # 隐藏s表
        xlsBook.Sheets("s").Visible = False


    def createFinalDispatches(self, organized_dispatch_list):
        # 取得整理后的数据
        dataList = organized_dispatch_list
        
        # 填充excel
#        xlsApp = self.createExcelApp()
        xlsBook = self.openExcelBook(os.path.split(os.path.realpath(__file__))[0]  + "\\Nitori\\dispatch.xlsx")
        # 循环填充
        # [ (shop_name,  (dataes) ),
        #   (shop_name,  (dataes) ),
        #   (shop_name,  (dataes) ).....]
        
        start = 1
        count = len(dataList)
        
        for data in dataList:
            # (shop_name,  [(row1), (row2), ...] )
            shop_name, data_mx_list = data
            
            print("process {} ({}/{})".format(shop_name, start, count))
            
            # Copy([Before], [After])
            xlsBook.Sheets("d").Copy(None ,self.xlsBook.Sheets(self.xlsBook.Worksheets.Count) )
            xlsBook.ActiveSheet.Name = shop_name
            
            # 填充数据（start_row=6, start_col=2）
            self.__writeDispatchMX(xlsBook.ActiveSheet,
                                   data_mx_list,
                                   startRow=6,
                                   startCol=2)
            # 以下可以添加画线
            
            start += 1
        
        # 隐藏s表
        xlsBook.Sheets("d").Visible = False
        

    def excelBookSaveAs(self, fileName):
        self.xlsBook.SaveAs(fileName)
        print("文件另存为: %s" % fileName)
    
    
    def __writeOrderMX(self, xlsSheet, head_data_list, dataMX, startRow, startCol, textForce=[]):
        # write data_list to excel
        # 最后加一个列表，列表中的列，强制加单引号（第一列为1）
        
        # 写入表头数据
        po_num, order_num, c_name, shop_name, file_name, order_rows, arrival_date = head_data_list
        
        xlsSheet.Cells(1, 3).Value = "'" + po_num
        xlsSheet.Cells(2, 3).Value = "'" + order_num
        xlsSheet.Cells(3, 3).Value = "'" + c_name
        xlsSheet.Cells(4, 3).Value = "'" + shop_name
        xlsSheet.Cells(5, 3).Value = "'" + str(order_rows)
        xlsSheet.Cells(6, 3).Value = "'" + arrival_date
        xlsSheet.Cells(1, 10).Value = "'" + file_name  # 写入源文件名称  J1单元格
        
        
        # 写入明细数据
        currentRow = startRow
        for i, tp in enumerate(dataMX):
            # 共colCount列，从第col列开始填写
            for j, value in enumerate(tp):
                if j+1 in textForce:
                    value = "'" + str(value)
                xlsSheet.Cells(currentRow, j+startCol).Value = value
            currentRow += 1
        
        # 最后写入一行end字样
        xlsSheet.Cells(currentRow, 2).Value = "'-- End --"
        
        # 加框线
        currentRow = startRow
        for i, tp in enumerate(dataMX):
            # 共colCount列，从第col列开始填写
            if tp[5] in ('墙装', '伸缩式'):
                xlsSheet.Cells(currentRow, 6).Borders.LineStyle = 1 #xlContinuous
                xlsSheet.Cells(currentRow, 6).Borders.Weight = 4  #xlThin=2 xlThick=4
            if tp[9] == '左':
                xlsSheet.Cells(currentRow, 10).Borders.LineStyle = 1 #xlContinuous
                xlsSheet.Cells(currentRow, 10).Borders.Weight = 4  #xlThin=2 xlThick=4
            if tp[10] != 1:
                xlsSheet.Cells(currentRow, 11).Borders.LineStyle = 1 #xlContinuous
                xlsSheet.Cells(currentRow, 11).Borders.Weight = 4  #xlThin=2 xlThick=4
            currentRow += 1
    

    def __writeDispatchMX(self, xlsSheet, dataMX, startRow, startCol, textForce=[]):
        # write data_list to excel
        # 最后加一个列表，列表中有的列，不在前标单引号（第一列为1）
#        [('1000001505848', 1, '周 小姐', '2017-3-25', '2017-4-14', '261010994400', 'FH窗帘轨道 F-27双轨FH 261010994400  W366', 326.4, '366', '', '', '天花板', 1, '000000510010', '上海七宝店'), ...]
        currentRow = startRow
        for i, tp in enumerate(dataMX):
            # 共colCount列，从第col列开始填写
            for j, value in enumerate(tp):
                xlsSheet.Cells(currentRow, j+startCol).Value = "'" + str(value)
            currentRow += 1
    
    
#    def CC_get_CargoReceipt(self):
#        
#        headList = []
#        bodyList = []
#        
#        sheet = self.xlsBook.Sheets('001796700002-1')
#        
#        cargo_receipt_no = sheet.Cells(4, 11).Text   # K4
#        cargo_receipt_date = sheet.Cells(5, 11).Text  # K5
#        date = sheet.Cells(12, 2).Text  # B12
#        place_name = sheet.Cells(14, 2).Text  # B14
#        
#        # 追加：以编号+交货地点作为id（唯一）
#        cargo_receipt_id = cargo_receipt_no + ' ' + place_name
#        
#        headList.append(cargo_receipt_id)
#        headList.append(cargo_receipt_no)
#        headList.append(cargo_receipt_date)
#        headList.append(date)
#        headList.append(place_name)
#        
#        # 以下读取明细  B16~L??，行数不定，需要if判断
#        # 判断空行方法：用H列判断，要么是空行，要么读取到最后一行，会有“RMB”字样
#        row = 16
#        rowLimit = 1000
#        
#        while row < rowLimit:
#            # 测试是否有数据 用PO号这一栏检测  H列
#            if sheet.Cells(row, 8).Text not in ("", "RMB"):
#                tp = (
#                        cargo_receipt_id,   #key value
#                        int(sheet.Cells(row, 2).Value),    #序号 BCD列合并的
#                        sheet.Cells(row, 5).Text,     #PO
#                        sheet.Cells(row, 6).Text,     #nitori_code
#                        sheet.Cells(row, 7).Text,     #商品名称
#                        sheet.Cells(row, 8).Value,     #单价
#                        sheet.Cells(row, 9).Value,     #po_qty订单数量
#                        sheet.Cells(row, 10).Value,     #交货数量
#                        sheet.Cells(row, 11).Value,     #小计amount
#                        sheet.Cells(row, 12).Text     #交货日
#                    )
#                bodyList.append(tp)
#                row += 1
#            else:
#                print("total rows:", row-16)
#                break
#        
#        return headList, bodyList
    
    
#    def CC_output_summary(self, fileFullName, dataList200, dataListCargo):
##        [('2017/03/13-2017/03/19', '000000510005 宁波银泰城店', '2000000038660', 440.6, 5, '2017/03/18', 'DONG BO20170313-20170319.xls'), ... ]
#        
#        xlsBook = self.xlsApp.Workbooks.Add()
#        
#        xlsSheet = xlsBook.Sheets('Sheet1')
#        
#        # 写表头
#        xlsSheet.Cells(1, 1).Value = 'PO_No'
#        xlsSheet.Cells(1, 2).Value = 'date'
#        xlsSheet.Cells(1, 3).Value = 'place_name'
#        xlsSheet.Cells(1, 4).Value = 'arrival_date'
#        xlsSheet.Cells(1, 5).Value = 'file_name'
#        xlsSheet.Cells(1, 6).Value = 'COUNT'
#        xlsSheet.Cells(1, 7).Value = 'TOTAL'
#        
#        # 写入明细数据（按列写入）
#        dataCount = len(dataList200)
#        colCount = len(dataList200[0])
#        
#        for i in range(colCount):
#            for j in range(dataCount):
#                cell_data = dataList200[j][i]
#                if type(cell_data) == str:
#                    cell_data = "'" + cell_data
#                xlsSheet.Cells(j+2, i+1).Value = cell_data
#        
#        # 格式设置
#        xlsSheet.Columns("G:G").Style = "Comma"
#        xlsSheet.Columns("A:G").EntireColumn.AutoFit()
#        
#        
#        # 新增sheet
#        xlsSheet = xlsBook.Sheets.Add()
#        
#        # 写表头
#        xlsSheet.Cells(1, 1).Value = 'file_name'
#        xlsSheet.Cells(1, 2).Value = 'ROWS'
#        xlsSheet.Cells(1, 3).Value = 'TOTAL'
#        
#        # 写入明细数据（按列写入）
#        dataCount = len(dataListCargo)
#        colCount = len(dataListCargo[0])
#        
#        for i in range(colCount):
#            for j in range(dataCount):
#                cell_data = dataListCargo[j][i]
#                if type(cell_data) == str:
#                    cell_data = "'" + cell_data
#                xlsSheet.Cells(j+2, i+1).Value = cell_data
#        
#        # 格式设置
#        xlsSheet.Columns("C:C").Style = "Comma"
#        xlsSheet.Columns("A:C").EntireColumn.AutoFit()
#        
#        ##### 需要替换，否则保存出错 #####
#        fileFullName = fileFullName.replace('/', '\\') 
#        xlsBook.SaveAs(fileFullName)



class ExcelRead:
    
    def getHardMX(self, fileName):
        
        book = xlrd.open_workbook(fileName)
        sheet = book.sheet_by_name('Hard')
        
#        ['2000000042703', 1.0, '1000001676184', 1.0, '侯 燕华', 42853.0, 42867.0, '261010993800', 'TOSO铝合金百叶帘 单色系列 TB904 W120H129', 465.7, 120.0, 129.0, 229.0, '伸缩式', '单色系列', '基本+伸缩', '单棒', '左', 'TB904', 1.0, '000000510003', '上海中山公园店', 300.9, '厨房']
        mxList = []
        
        for i in range(1, sheet.nrows):
            lst = sheet.row_values(i)
            # 修改2列为日期型字符串 5 6
            lst[5] = self.float2date(lst[5], book.datemode)
            lst[6] = self.float2date(lst[6], book.datemode)
            # 修改 成品宽，成品高，安装高度 列为字符串 10 11 12   有可能为空，需要判断
            lst[10] = '' if lst[10] == '' else str(int(lst[10]))
            lst[11] = '' if lst[11] == '' else str(int(lst[11]))
            lst[12] = '' if lst[12] == '' else str(int(lst[12]))
            # 修改 单位原价 有可能为空，这时替换为0
            lst[22] = 0.0 if lst[22] == '' else lst[22]
            
            mxList.append(lst)
            
        return mxList


    def float2date(self, ms_date_number, date_mode):
        # return a string '2017-03-25'
#        ms_date_number = sheet.cell(5, 19).value # Correct option 2
        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number, date_mode)
#        py_date = datetime.datetime(year, month, day, hour, minute, second)
        return '{}-{}-{}'.format(year, month, day)
        
    
    def checkHardData(self, mxList):
        # 采购单号 列表
        lst1 = [row[0] for row in mxList]
        # 原价 列表
        lst2 = [row[9] for row in mxList]
        # 系列 列表
        lst3 = [row[14] for row in mxList]
        
        check1 = '' in lst1
        check2 = ('' in lst2) or (0.0 in lst2)
        check3 = '' in lst3
        
        return (check1, check2, check3)
        

    def CC_get_CargoReceipt(self, fileName):
        
        # 一个文件中，有许多张表，需要全部读取
        # 把所有head内容加入headList中，每条都是1个tuple
        # 把所有body内容加入bodyList中，每条都是1个tuple
        # 以编号+交货地点作为id（唯一） cargo_receipt_id
        
        rowLimit = 500
        headList = []
        bodyList = []
        
        
        book = xlrd.open_workbook(fileName)
#        sheet = book.sheet_by_name('001796700002-1')
        sheetList = book.sheet_names()
        
        
        # 取得文件名
        fi = QtCore.QFileInfo(fileName)
        fileShortName = fi.fileName()
        
        
        for sheetName in sheetList:
            
            sheet = book.sheet_by_name(sheetName)
        
            # 以下读取表头
            cargo_receipt_no = sheet.cell(3, 10).value   # K4
            cargo_receipt_date = self.float2date(sheet.cell(4, 10).value, book.datemode)  # K5
            date = sheet.cell(11, 1).value  # B12 交货日期，这个不是标准日期型，没关系
            place_name = sheet.cell(13, 1).value  # B14
            
            
            # 追加：以编号+交货地点作为id（唯一）
            cargo_receipt_id = cargo_receipt_no + ' ' + place_name
            
            # 查找单据总计栏，取得总计
            currentRow = 15  # 第16行开始查找
            
            while currentRow < rowLimit:
                # 测试是否有 RMB 字样  H列
                cell_value = sheet.cell(currentRow, 7).value
                if cell_value == 'RMB':
                    # J列，单据总计金额
                    total_amount = sheet.cell(currentRow, 9).value
                    break
                currentRow += 1
            
            head_tp = (
                        cargo_receipt_id,
                        cargo_receipt_no,
                        cargo_receipt_date,
                        date,
                        place_name,
                        fileShortName,
                        total_amount
                    )
            
            headList.append(head_tp)

            
            # 以下读取明细  B16~L??，行数不定，需要if判断
            # 判断空行方法：用H列判断，要么是空行，要么读取到最后一行，会有“RMB”字样
            row = 15
            
            while row < rowLimit:
                # 测试是否有数据 用单价这一栏检测  H列
                if sheet.cell(row, 7).value not in ('', 'RMB'):
                    body_tp = (
                            cargo_receipt_id,   #key value
                            int(sheet.cell(row, 1).value),    #序号 BCD列合并的
                            sheet.cell(row, 4).value,     #PO
                            sheet.cell(row, 5).value,     #nitori_code
                            sheet.cell(row, 6).value,     #商品名称
                            sheet.cell(row, 7).value,     #单价
                            int(sheet.cell(row, 8).value),     #po_qty订单数量
                            int(sheet.cell(row, 9).value),     #交货数量
                            sheet.cell(row, 10).value,     #小计amount
                            sheet.cell(row, 11).value     #交货日
                        )
                    bodyList.append(body_tp)
                    row += 1
                else:
                    break
        
        return headList, bodyList



class ExcelWrite:
    
    def CC_output_summary(self, fileFullName, dataList200, dataListCargo):
#        [('2017/03/13-2017/03/19', '000000510005 宁波银泰城店', '2000000038660', 440.6, 5, '2017/03/18', 'DONG BO20170313-20170319.xls'), ... ]
        
        book = xlsxwriter.Workbook(fileFullName) # 建立文件
        
        num_format = book.add_format()
        num_format.set_num_format('_ * #,##0.00_ ;_ * -#,##0.00_ ;_ * "-"??_ ;_ @_ ') 
        
        sheet = book.add_worksheet('By PO') # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
        
        # 写表头
        sheet.write(0, 0, 'PO_No')
        sheet.write(0, 1, 'date')
        sheet.write(0, 2, 'place_name')
        sheet.write(0, 3, 'arrival_date')
        sheet.write(0, 4, 'file_name')
        sheet.write(0, 5, 'COUNT')
        sheet.write(0, 6, 'TOTAL')
        
        # 写明细（按列写入）
        dataCount = len(dataList200)
        colCount  = len(dataList200[0])
        
        for i in range(colCount):
            for j in range(dataCount):
                cell_data = dataList200[j][i]
                sheet.write(j+1, i, cell_data)
        
        # 格式设置
        sheet.set_column('G:G', 12, num_format)
        
        
        sheet2 = book.add_worksheet('By File') # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
        
        # 写表头
        sheet2.write(0, 0, 'Filename')
        sheet2.write(0, 1, 'Rows')
        sheet2.write(0, 2, 'Total')
        
        # 写明细（按列写入）
        dataCount = len(dataListCargo)
        colCount = len(dataListCargo[0])
        
        for i in range(colCount):
            for j in range(dataCount):
                cell_data = dataListCargo[j][i]
                sheet2.write(j+1, i, cell_data)
        
        # 格式设置
        sheet2.set_column('C:C', 12, num_format)
        
        book.close()
        
