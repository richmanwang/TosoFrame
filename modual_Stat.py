# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 13:49:26 2016

@author: 008
"""

import calendar
import datetime
import sqlite3
import os
import win32com.client

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot

from ui_Stat_Main import Ui_Stat_Main
from ui_Stat_AddCost import Ui_Stat_AddCost
from ui_Stat_UnitCost import Ui_Stat_UnitCost
from ui_Stat_UnitCostEditor import Ui_Stat_UnitCostEditor

from core import MysqlHandle
from core import LoadServerDataClass_PYQT_ODBC

import pdb


class Frm_Stat_Main(QtGui.QWidget, Ui_Stat_Main):
     
    def __init__(self, parent=None):
        super(Frm_Stat_Main, self).__init__(parent)
        self.setupUi(self)
        
        # 初始化查询日期
        today = QtCore.QDate().currentDate()
        start_date = QtCore.QDate(today.getDate()[0], today.getDate()[1], 1)
        
        if today.getDate()[2] == 1:     #某月1日
            end_date = start_date
        else:
            end_date = today.addDays(-1)
        
        self.dateEdit_start.setDate(start_date)
        self.dateEdit_end.setDate(end_date)
        
        
    def __create_date_list(self, year, month):
        # 日期格式统一为 2015-01-01
        # 不管现在是几号，直接生成当月全部日期
        weekday_mapping = {1:'一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六', 7:'日'}
        
        result_list = []
        
        # 此句可以返回当月全部日期
        day_list = range(calendar.monthrange(year, month)[1]+1)[1:]
        
        for day in day_list:
            p_date = datetime.date(year, month, day)
            result_tuple = ( p_date.isoformat(), weekday_mapping[p_date.isoweekday()] )
            result_list.append(result_tuple)   # isoweekday 星期一返回1，星期六返回6，星期日返回7
        return result_list
    
    
    def __update_date_list(self):
        date = self.dateEdit_start.date()
        year = date.year()
        month = date.month()
        
        date_list = self.__create_date_list(year, month)
        
        ldh = SqliteStat()
        
        ldh.delete_date_list()
        ldh.insert_date_list(date_list)
    
    # 月中统计还需要使用，暂时不能去除
    @pyqtSlot()
    def on_btn_tongbu_inventory_clicked(self):
        U8 = LoadServerDataClass_PYQT_ODBC()
        ldh = SqliteStat()
        
        #1、删除表内容：inv
        ldh.delete_inv()

        #2、读取服务器 mx_list
        print('load server inventory...', end='')
        U8.add_conn()
        mx_list = U8.Stat_fetch_inventory()
        U8.remove_conn()
        print('Done!')
        
        #3、加入表 inv
        print('insert inventory...', end='')
        ldh.insert_inv(mx_list)
        print('Done!')
        
        QtGui.QMessageBox.information(self, '提示', '同步完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    
    @pyqtSlot()
    def on_btn_tongbu_clicked(self):
        start_date = self.dateEdit_start.text()
        end_date   = self.dateEdit_end.text()
        
        print(start_date, end_date)
        
        U8 = LoadServerDataClass_PYQT_ODBC()
        ldh = SqliteStat()
        
        
        #1、删除表内容：dispatch_mx
        print('delete old dispatch datas...', end='\t')
        ldh.delete_dispatch_mx()
        print('Done!')
        
        #2、删除表内容：inv
        print('delete inv datas...', end='\t')
        ldh.delete_inv()
        print('Done!')
        
        
        U8.add_conn()
        
        #3、读取服务器 inv
        print('load server data: inventory...', end='\t')
        inv_list = U8.Stat_fetch_inventory()
        print('Done!')
        
        #4、读取服务器 mx_list
        print('load server data...', end='\t')
        mx_list = U8.Stat_fetch_dispatch_mx(start_date, end_date)
        print('Done!')
        
        U8.remove_conn()
        
        
        #5、加入表 inv
        print('insert local table inv...', end='\t')
        ldh.insert_inv(inv_list)
        print('Done!')
        
        #6、加入表 dispatch_mx
        print('insert local table dispatch_mx...', end='\t')
        ldh.insert_dispatch_mx(mx_list)
        print('Done!')
        
        #4、刷新日期列表
        print('update local table date_list...', end='\t')
        self.__update_date_list()
        print('Done!')
        
        #5、update成本信息
        print('update cost data...', end='\t')
        ldh.updateCost()
        print('Done!')

        print('Comlelted!')
        
        QtGui.QMessageBox.information(self, '提示', '同步完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    
    
    
    @pyqtSlot()
    def on_btn_tongbu_mysql_clicked(self):
        start_date = self.dateEdit_start.text()
        end_date   = self.dateEdit_end.text()
#        year = self.dateEdit_start.date().year()
#        month = self.dateEdit_start.date().month()
        
        print('同步mx到服务器')
        print(start_date, end_date)
        
        U8 = LoadServerDataClass_PYQT_ODBC()
        mh = MysqlHandle()
        
        
        U8.add_conn()
        
        #1、读取服务器 inv
        print('load server data: inventory...', end='\t')
        invList = U8.Stat_fetch_inventory()
        print('Done!')
        
        #2、读取服务器 dispatches
        print('load server data: dispatches...', end='\t')
        headList, bodyList = U8.Stat_fetch_dispatch(start_date, end_date)
        print('Done!')
        
        U8.remove_conn()
        
        
        mh.connect()
        
        #3、更新表 inventory
        print('update inventory...', end='\t')
        mh.ST_update_inventory(invList)
        print('Done!')
        
        #4、更新表：ST_Cost_dispatchList  ST_Cost_dispatchLists
        print('update dispatch datas...', end='\t')
        mh.ST_update_dispatch(headList, bodyList)
        print('Done!')
        
        #5、update成本信息
        print('update cost data...', end='\t')
        mh.ST_Cost_appendCost()
        print('Done!')
        
        #6、刷新日期列表
        print('update date list...', end='\t')
        mh.ST_update_dateList(start_date, end_date)
        print('Done!')
        
        mh.disconnect()

        print('Comlelted!')
        
        QtGui.QMessageBox.information(self, '提示', '同步完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    
    
    @pyqtSlot()
    def on_btn_addcost_clicked(self):
        a = Frm_Stat_AddCost(self)
        a.exec_()
    
    
    @pyqtSlot()
    def on_btn_unitcost_clicked(self):
        a = Frm_Stat_UnitCost(self)
        a.exec_()
    
    
#    @pyqtSlot()
#    def on_btn_excel_clicked(self):
#        # 不含成本数据的报表
#        ldh = SqliteStat()
#        xlh = ExcelHandle()
#        
#        start_date = self.dateEdit_start.text()
#        end_date   = self.dateEdit_end.text()
#        
#        person_list = ldh.getPersonNameList()
#        
#        # 生成list（公司汇总及按担当）
#        person_data_list = []
#        for person_name in person_list:
#            lst = ldh.select_summary_everyday_by_person(person_name)
#            data_tuple = (person_name, start_date, end_date, lst)
#            person_data_list.append(data_tuple)
#        
#        # 生成list（客户汇总）
#        lst = ldh.select_summary_customer()
#        data_tuple_customer = (start_date, end_date, lst)
#        
#        # 开启Excel
#        xlh.createExcelApp()
#        
#        # 开启工作簿
#        xlh.openExcelBook()
#        
#        # 输出到Excel（公司汇总及按担当）
#        xlh.write_to_excel_everyday(person_data_list)
#        
#        # 输出到Excel（客户汇总）
#        xlh.write_to_excel_customer(data_tuple_customer)
#        
#        # 保存文件
#        xlFileFullName = "\\\\tososh\\公司资料\\营业资料\\月中销售实绩\\月中统计%s.xlsx" % (end_date,)
#        xlh.excelBookSaveAs(xlFileFullName)
#        
#        # 关闭工作簿
#        xlh.closeExcelBook()
#        
#        # 关闭Excel
#        xlh.quitExcelApp()
#        
#        QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


    @pyqtSlot()
    def on_btn_excel_mysql_clicked(self):
        # 不含成本数据的报表，只有客户汇总，没有每日汇总
        mh = MysqlHandle()
        xlh = ExcelHandle()
        
        start_date = self.dateEdit_start.text()
        end_date   = self.dateEdit_end.text()
        
        
        mh.connect()
        
        # 生成list（客户汇总）
        lst = mh.ST_get_customer()
        data_tuple_customer = (start_date, end_date, lst)
        
        mh.disconnect()
        
        
        # 开启Excel
        xlh.createExcelApp()
        
        # 开启工作簿
        xlh.openExcelBook()
        
        # 输出到Excel（公司汇总及按担当）
#        xlh.write_to_excel_everyday(person_data_list)
        
        # 输出到Excel（客户汇总）
        xlh.write_to_excel_customer(data_tuple_customer)
        
        # 保存文件
        xlFileFullName = "\\\\tososh\\公司资料\\营业资料\\月中销售实绩\\无成本_月中统计%s.xlsx" % (end_date,)
        xlh.excelBookSaveAs(xlFileFullName)
        
        # 关闭工作簿
        xlh.closeExcelBook()
        
        # 关闭Excel
        xlh.quitExcelApp()
        
        QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


#    @pyqtSlot()
#    def on_btn_excel_2_clicked(self):
#        # 包含成本数据的报表
#        ldh = SqliteStat()
#        xlh = ExcelHandle()
#        
#        start_date = self.dateEdit_start.text()
#        end_date   = self.dateEdit_end.text()
#        
#        person_list = ldh.getPersonNameList()
#        
#        # 生成list（公司汇总及按担当）
#        person_data_list = []
#        for person in person_list:
#            lst = ldh.select_summary_everyday_by_person_2(person)
#            data_tuple = (person, start_date, end_date, lst)
#            person_data_list.append(data_tuple)
#        
#        
#        # 生成list（客户汇总）
#        lst = ldh.select_summary_customer_2()
#        data_tuple_customer = (start_date, end_date, lst)
#        
#        # 开启Excel
#        xlh.createExcelApp()
#        
#        # 开启工作簿
#        xlh.openExcelBook_2()
#
#        # 输出到Excel（公司汇总及按担当）
#        xlh.write_to_excel_everyday_2(person_data_list)
#        
#        # 输出到Excel（客户汇总）
#        xlh.write_to_excel_customer_2(data_tuple_customer)
#        
#        # 保存文件
#        xlFileFullName = "\\\\tososh\\公司资料\\营业资料\\月中销售实绩\\月中统计%s with cost.xlsx" % (end_date,)
#        xlh.excelBookSaveAs(xlFileFullName)
#        
#        # 关闭工作簿
#        xlh.closeExcelBook()
#        
#        # 关闭Excel
#        xlh.quitExcelApp()
#
#        QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)



    @pyqtSlot()
    def on_btn_excel_2_mysql_clicked(self):
        # 包含成本数据的报表 完全通过mysql
        mh = MysqlHandle()
        xlh = ExcelHandle()
        
        start_date = self.dateEdit_start.text()
        end_date   = self.dateEdit_end.text()
        
        
        mh.connect()
        
        # 生成list（客户汇总）
        lst = mh.ST_get_customerWithCost()
        data_tuple_customer = (start_date, end_date, lst)
        
        # 生成担当者列表（第一个是 公司汇总 ）
        personNameList = mh.ST_get_personNameList()
        
        # 生成list（公司汇总及按担当）
        personDataList = []
        for personName in personNameList:
            lst = mh.ST_get_personByDay(personName)
            data_tuple = (personName, start_date, end_date, lst)
            personDataList.append(data_tuple)
        
        mh.disconnect()
        
        # 开启Excel
        xlh.createExcelApp()
        
        # 开启工作簿
        xlh.openExcelBook_2()

        # 输出到Excel（公司汇总及按担当）
        xlh.write_to_excel_everyday_2(personDataList)
        
        # 输出到Excel（客户汇总）
        xlh.write_to_excel_customer_2(data_tuple_customer)
        
        # 保存文件
        xlFileFullName = "\\\\tososh\\公司资料\\营业资料\\月中销售实绩\\月中统计%s with cost.xlsx" % (end_date,)
        xlh.excelBookSaveAs(xlFileFullName)
        
        # 关闭工作簿
        xlh.closeExcelBook()
        
        # 关闭Excel
        xlh.quitExcelApp()

        QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)






class Frm_Stat_AddCost(QtGui.QDialog, Ui_Stat_AddCost):
     
    def __init__(self, parent=None):
        super(Frm_Stat_AddCost, self).__init__(parent)
        self.setupUi(self)
        
        # create model
        self.tableModel_price = QtGui.QStandardItemModel()
        self.tableModel_rate  = QtGui.QStandardItemModel()
        
        
        # create tablewidget head
        head_str_price = ["存货编码", "存货名称", "单位", "存货大类", "单位成本"]
        head_str_rate  = ["存货编码", "存货名称", "单位", "存货大类", "成本率"]
        head_width = [100, 340, 70, 70, 80]
        
        # set model
        self.tableModel_price.setHorizontalHeaderLabels(head_str_price)
        self.tableModel_rate.setHorizontalHeaderLabels(head_str_rate)
        
        self.tableView_price.setModel(self.tableModel_price)
        self.tableView_rate.setModel(self.tableModel_rate)
        
        # set col width
        for i in range( len(head_width) ):
            self.tableView_price.setColumnWidth(i, head_width[i])
            self.tableView_rate.setColumnWidth(i, head_width[i])
        
        self.__refresh_table()
        
        # 输入框
        self.tableModel_price.dataChanged.connect(self.__item_changed)
    
    
    @pyqtSlot()
    def on_btn_submit_clicked(self):
        # 提交
        lst = self.__collect_table_data()
        
        self.ldh.insert_cost_data(lst)
        
        lst = self.ldh.getCostNullList()
        
        self.__refresh_table(lst)
    
    
    def __refresh_table(self):
        
        ldh = SqliteStat()
        
        lst = ldh.getCostNullList()
        
        data_count = len(lst)
        
        self.tableModel_price.setRowCount(0)
        self.tableModel_price.setRowCount(data_count)
        
        # lst写入grid
        # If you want to set several items of a particular row (say, by calling setItem() in a loop), you may want to turn off sorting before doing so, and turn it back on afterwards; this will allow you to use the same row argument for all items in the same row (i.e. setItem() will not move the row).
#        self.tableWidget_price.setSortingEnabled(False)
#        self.tableWidget_price.itemChanged.disconnect(self.__item_changed)
        for i in range(data_count):
            
            code, name, unit, cata = lst[i]
            amount = None
            
            # 定义item
            itm_0 = QtGui.QStandardItem()
            itm_1 = QtGui.QStandardItem()
            itm_2 = QtGui.QStandardItem()
            itm_3 = QtGui.QStandardItem()
            itm_4 = QtGui.QStandardItem()
            
            # 设置userrole（纯data）
            itm_0.setData(code, QtCore.Qt.UserRole)
            itm_1.setData(name, QtCore.Qt.UserRole)
            itm_2.setData(unit, QtCore.Qt.UserRole)
            itm_3.setData(cata, QtCore.Qt.UserRole)
            itm_4.setData(amount, QtCore.Qt.UserRole)
            
            # 设置 displayrole
            itm_0.setData(code, QtCore.Qt.DisplayRole)
            itm_1.setData(name, QtCore.Qt.DisplayRole)
            itm_2.setData(unit, QtCore.Qt.DisplayRole)
            itm_3.setData(cata, QtCore.Qt.DisplayRole)
            itm_4.setData('', QtCore.Qt.DisplayRole)
            
            # 设置对齐
            itm_4.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            
            # 放入model
            self.tableModel_price.setItem(i, 0, itm_0)
            self.tableModel_price.setItem(i, 1, itm_1)
            self.tableModel_price.setItem(i, 2, itm_2)
            self.tableModel_price.setItem(i, 3, itm_3)
            self.tableModel_price.setItem(i, 4, itm_4)
            
        
#        self.tableWidget_price.itemChanged.connect(self.__item_changed)
#        self.tableWidget_price.setSortingEnabled(True)
        
    
    
    @pyqtSlot(QtCore.QModelIndex)
    def __item_changed(self, idx):
        
        self.tableModel_price.dataChanged.disconnect(self.__item_changed)
        
#        row = idx.row()
        col = idx.column()
        value = self.tableModel_price.data(idx, QtCore.Qt.DisplayRole)
        
#        {0: 'aaa', 32: None, 7: 130}
#        print(self.tableModel_price.itemData(idx))
        
#        print('changed  row:%s  col:%s  value:%s' % (row, col, value))
        
        
        if col == 4:
            # 成本单价
            if value != '':
                try:
                    value = float(value)
                except(ValueError):
                    value = 0.0
                finally:
                    self.tableModel_price.setData(idx, '{:,.2f}'.format(value), QtCore.Qt.DisplayRole)
                    self.tableModel_price.setData(idx, value, QtCore.Qt.UserRole)
                    
#                print('changed  row:%s  col:%s  value:%s' % (row, col, value))
            
        self.tableModel_price.dataChanged.connect(self.__item_changed)
    
    
    
    
    def __collect_table_data(self):
        # 收集已经填写好成本的数据，并返回一个列表（为了更新数据库成本信息）
        # 返回一个列表  [ (u'01101', 0, 12.34, 0.0, 'memo'), (u'01102', 1, 0.00, 0.6, 'memo'), ....]
        # 此处不做数据校验
        
        lst = []
        
        for i in range(self.tableWidget.rowCount()):
            code_itm = self.tableWidget.item(i, 0)
            is_p_itm = self.tableWidget.item(i, 4)
            cost_itm = self.tableWidget.item(i, 5)
            rate_itm = self.tableWidget.item(i, 6)
            
            if is_p_itm.text() != '' and cost_itm.text() != '' and rate_itm.text() != '':
                tp = (
                    code_itm.text(),
                    int(is_p_itm.text()),
                    float(cost_itm.text()),
                    float(rate_itm.text())
                    )
                lst.append(tp)
        
        return lst



class Frm_Stat_UnitCost(QtGui.QDialog, Ui_Stat_UnitCost):
     
    def __init__(self, parent=None):
        super(Frm_Stat_UnitCost, self).__init__(parent)
        self.setupUi(self)
        
        # create tablewidget head
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['存货编码', '存货名称', '存货大类', '平均尺寸', '单位', 'SET原价', '单位原价', '备注'])
        
        col_width = [70, 340, 70, 70, 70, 70, 70, 200]
        
        for i, width in enumerate(col_width):
            self.tableWidget.setColumnWidth(i, width)
        
        self.__refresh_table()
        
    
    @pyqtSlot()
    def on_btn_addnew_clicked(self):
        aa = Frm_Stat_UnitCostEditor(parent=self)
        aa.exec_()
        
        
    @pyqtSlot()
    def on_btn_edit_clicked(self):
        row = self.tableWidget.currentRow()
        
        invCode = self.tableWidget.item(row, 0).text()
        aa = Frm_Stat_UnitCostEditor(parent=self)
        aa.setInvcode(invCode)
        aa.exec_()
    
    
        
    @pyqtSlot() 
    def __refresh_table(self):
        mh = MysqlHandle()
        lst = mh.ST_Cost_getAllList()
        data_count = len(lst)
        
        self.tableWidget.clearContents()
        
        self.tableWidget.setRowCount(data_count)
        
        # lst写入grid
        # If you want to set several items of a particular row (say, by calling setItem() in a loop), you may want to turn off sorting before doing so, and turn it back on afterwards; this will allow you to use the same row argument for all items in the same row (i.e. setItem() will not move the row).
        self.tableWidget.setSortingEnabled(False)
#        self.tableWidget.itemChanged.disconnect(self.__item_changed)
        
        for i in range(data_count):
            code, name, cata, size, unit, cost, unitcost, memo = lst[i]
            
            # code
            item_0 = QtGui.QTableWidgetItem(code)
            item_0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            
            # name
            item_1 = QtGui.QTableWidgetItem(name)
            item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            
            # cata
            item_2 = QtGui.QTableWidgetItem(cata)
            item_2.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            
            # size
            item_3 = QtGui.QTableWidgetItem('{:.2f}'.format(size))
            item_3.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            item_3.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
            
            # unit
            item_4 = QtGui.QTableWidgetItem(unit)
            item_4.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            
            # cost
            item_5 = QtGui.QTableWidgetItem('{:.2f}'.format(cost))
            item_5.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            item_5.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
            
            # unitcost
            item_6 = QtGui.QTableWidgetItem('{:.2f}'.format(unitcost))
            item_6.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            item_6.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
            
            # memo
            item_7 = QtGui.QTableWidgetItem(memo)
            item_7.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
            
            
            self.tableWidget.setItem(i, 0, item_0)
            self.tableWidget.setItem(i, 1, item_1)
            self.tableWidget.setItem(i, 2, item_2)
            self.tableWidget.setItem(i, 3, item_3)
            self.tableWidget.setItem(i, 4, item_4)
            self.tableWidget.setItem(i, 5, item_5)
            self.tableWidget.setItem(i, 6, item_6)
            self.tableWidget.setItem(i, 7, item_7)
        
#        self.tableWidget.itemChanged.connect(self.__item_changed)
        self.tableWidget.setSortingEnabled(True)




class Frm_Stat_UnitCostEditor(QtGui.QDialog, Ui_Stat_UnitCostEditor):
     
    def __init__(self, parent=None):
        super(Frm_Stat_UnitCostEditor, self).__init__(parent)
        self.setupUi(self)
        
        # create tablewidget head
        col_name = ['存货编码', '存货名称', '存货大类', '使用量', '单位', '损耗率', '单位原价', '金额']
        col_width = [70, 130, 70, 70, 70, 70, 70, 70]
        
        self.tableWidget.setColumnCount(len(col_name))
        self.tableWidget.setHorizontalHeaderLabels(col_name)
        
        for col in range( len(col_width) ):
            self.tableWidget.setColumnWidth(col, col_width[col])
        
        # NEW为新增，EDIT为修改
        self.STATE = 'NEW'
        
        self.tableWidget.itemChanged.connect(self.__item_changed)

    
    
    def setInvcode(self, invCode):
        
        self.STATE = 'EDIT'
        
        mh = MysqlHandle()
        rst = mh.ST_Cost_getBom(invCode)
        
        # 填写表头 'head': ('68136', 'FH F-27双轨', 'FH', '米', 3.12, 1.0, 3.12, 143.34, 45.94, 'aaa'),
        head = rst['head']
        self.lineEdit_code.setText(head[0])
        self.lineEdit_name.setText(head[1])
        self.lineEdit_cata.setText(head[2])
        self.lineEdit_unit.setText(head[3])
        self.lineEdit_avgW.setText('{:.2f}'.format(rst['head'][4]))
        self.lineEdit_avgH.setText('{:.2f}'.format(rst['head'][5]))
        self.lineEdit_size.setText('{:.2f}'.format(rst['head'][6]))
        self.lineEdit_cost.setText('{:.2f}'.format(rst['head'][7]))
        self.lineEdit_unitcost.setText('{:.2f}'.format(rst['head'][8]))
        self.lineEdit_memo.setText(rst['head'][9] or '')
        
        # 填写表体
        bodyData = rst['body']
        
        for i in range(len(bodyData)):
            code, name, cata, amount, unitname, loss, invrcost, cost = bodyData[i]
            self.__addrow()
            
            self.tableWidget.itemChanged.disconnect(self.__item_changed)
            
            self.tableWidget.item(i, 0).setText(code)
            self.tableWidget.item(i, 1).setText(name)
            self.tableWidget.item(i, 2).setText(cata)
            self.tableWidget.item(i, 3).setText('{:.2f}'.format(amount))
            self.tableWidget.item(i, 4).setText(unitname)
            self.tableWidget.item(i, 5).setText('{:.2f}'.format(loss))
            self.tableWidget.item(i, 6).setText('{:.2f}'.format(invrcost))
            self.tableWidget.item(i, 7).setText('{:.2f}'.format(cost))
        
            self.tableWidget.itemChanged.connect(self.__item_changed)
        
    
    @pyqtSlot()
    def on_btn_load_clicked(self):
        mh = MysqlHandle()
        rst = mh.ST_Cost_getInvInfo(self.lineEdit_code.text())
        if rst:
            self.lineEdit_name.setText(rst[1])
            self.lineEdit_cata.setText(rst[2])
            self.lineEdit_unit.setText(rst[3])
        else:
            self.lineEdit_name.setText('')
            self.lineEdit_cata.setText('')
            self.lineEdit_unit.setText('')
        
        
    
    @pyqtSlot()
    def __addrow(self):
        rowcount = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowcount+1)
        
        rowIndex = rowcount + 1 - 1
        
        # 存货编码
        item_code = QtGui.QTableWidgetItem('')
        
        # 存货名称
        item_name = QtGui.QTableWidgetItem('')
        item_name.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
        item_name.setBackgroundColor(QtCore.Qt.lightGray)
        
        # 存货大类
        item_cata = QtGui.QTableWidgetItem('')
        item_cata.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
        item_cata.setBackgroundColor(QtCore.Qt.lightGray)
        
        # 使用量
        item_amount = QtGui.QTableWidgetItem('0.00')
        item_amount.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
        
        # 单位
        item_unit = QtGui.QTableWidgetItem('')
        item_unit.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
        item_unit.setBackgroundColor(QtCore.Qt.lightGray)
        
        # 损耗率
        item_loss = QtGui.QTableWidgetItem('0.00')
        item_loss.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
        
        # 单位原价
        item_unitcost = QtGui.QTableWidgetItem('0.00')
        item_unitcost.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
        item_unitcost.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
        item_unitcost.setBackgroundColor(QtCore.Qt.lightGray)
        
        # 金额
        item_cost = QtGui.QTableWidgetItem('0.00')
        item_cost.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  #设置不可编辑
        item_cost.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  #设置右对齐
        item_cost.setBackgroundColor(QtCore.Qt.lightGray)
        
        
        self.tableWidget.itemChanged.disconnect(self.__item_changed)
        
        self.tableWidget.setItem(rowIndex, 0, item_code)
        self.tableWidget.setItem(rowIndex, 1, item_name)
        self.tableWidget.setItem(rowIndex, 2, item_cata)
        self.tableWidget.setItem(rowIndex, 3, item_amount)
        self.tableWidget.setItem(rowIndex, 4, item_unit)
        self.tableWidget.setItem(rowIndex, 5, item_loss)
        self.tableWidget.setItem(rowIndex, 6, item_unitcost)
        self.tableWidget.setItem(rowIndex, 7, item_cost)
        
        self.tableWidget.itemChanged.connect(self.__item_changed)
        
        

    
        
    
    @pyqtSlot()
    def on_btn_addrow_clicked(self):
        self.__addrow()
        
    
    
    @pyqtSlot()
    def on_btn_delrow_clicked(self):
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        self.cacuCost()
    
    
    
    @pyqtSlot(QtGui.QTableWidgetItem)
    def __item_changed(self, itm):
#        print('changed  row:%s  col:%s' % (itm.row(), itm.column()))
        row = itm.row()
        col = itm.column()
        invCode = self.tableWidget.item(row, col).text()
        
        self.tableWidget.itemChanged.disconnect(self.__item_changed)
        
        
        # 存货编码栏
        if col == 0:
            mh = MysqlHandle()
            rst = mh.ST_Cost_getInvInfo(invCode)
#            print(rst)
            if rst:
                self.tableWidget.item(row, 1).setText(rst[1])
                self.tableWidget.item(row, 2).setText(rst[2])
                self.tableWidget.item(row, 4).setText(rst[3])
                self.tableWidget.item(row, 6).setText('{:.2f}'.format(rst[4] or 0.0))
            else:
                #重置
                self.tableWidget.item(row, 0).setText('')
                self.tableWidget.item(row, 1).setText('')
                self.tableWidget.item(row, 2).setText('')
                self.tableWidget.item(row, 4).setText('')
                self.tableWidget.item(row, 6).setText('0.0')
        
        # 使用量栏        
        elif col == 3:
            txt = itm.text()
            if self.isFloat(txt) == True:
                self.tableWidget.item(row, 3).setText('{:.2f}'.format(float(txt)))
            else:
                itm.setText('0.00')
                self.tableWidget.item(row, 7).setText('0.00')
        
        # 损耗率栏        
        elif col == 5:
            txt = itm.text()
            if self.isFloat(txt) == True:
                self.tableWidget.item(row, 5).setText('{:.2f}'.format(float(txt)))
            else:
                itm.setText('0.00')
                self.tableWidget.item(row, 7).setText('0.00')
        
        # 都填妥后，最后计算金额
        amount   = float(self.tableWidget.item(row, 3).text())
        loss     = float(self.tableWidget.item(row, 5).text())
        unitcost = float(self.tableWidget.item(row, 6).text())
        cost     = amount * (1+loss) * unitcost
        self.tableWidget.item(row, 7).setText('{:.2f}'.format(cost))
        
        self.tableWidget.itemChanged.connect(self.__item_changed)
        
        self.cacuCost()
        
        
    def isFloat(self, txt):
        try:
            float(txt)
            return True #能成功转换为浮点型，则是数字
        except:
            return False #不能成功转换为浮点型，则不是数字
        
    
    def cacuCost(self):
        totalcost = 0.0
        
        for i in range(self.tableWidget.rowCount()):
            totalcost += float(self.tableWidget.item(i, 7).text())
        
        self.lineEdit_cost.setText('{:.2f}'.format(totalcost))
        
        size = float(self.lineEdit_size.text())
        unitcost = round(totalcost / size,2)
        
        self.lineEdit_unitcost.setText('{:.2f}'.format(unitcost))
    
        
    @pyqtSlot()
    def on_btn_submit_clicked(self):
        # cacu cost
        self.cacuCost()
        
        # collect data
        data = {}
        data['head'] = (self.lineEdit_code.text(),
                        float(self.lineEdit_avgW.text()),
                        float(self.lineEdit_avgH.text()),
                        float(self.lineEdit_size.text()),
                        float(self.lineEdit_cost.text()),
                        float(self.lineEdit_unitcost.text()),
                        None if self.lineEdit_memo.text()=='' else self.lineEdit_memo.text()
                        )
        
        rowCount = self.tableWidget.rowCount()
        mx = []
        for i in range(rowCount):
            tp = (self.lineEdit_code.text(),                    # invcode
                  i+1,                                          # seqNum
                  self.tableWidget.item(i, 0).text(),           # invcodeMX
                  self.tableWidget.item(i, 1).text(),           # name
                  self.tableWidget.item(i, 2).text(),           # cata
                  float(self.tableWidget.item(i, 3).text()),    # amount
                  self.tableWidget.item(i, 4).text(),           # unit
                  float(self.tableWidget.item(i, 5).text()),           # loss
                  float(self.tableWidget.item(i, 6).text()),           # RCost
                  float(self.tableWidget.item(i, 7).text())            # total
                  )
            mx.append(tp)
            
        data['body'] = mx
        
        # 保存
        mh = MysqlHandle()
        mh.ST_Cost_saveBom(data)
        






class SqliteStat:
    
    def __init__(self):
        self.db = ".\\Stat\\plist.sqlite"
        
    
    def db_connect(self):
        return sqlite3.connect(self.db)
    
    
        
        
    def select_summary_everyday_by_person(self, personName):
        
        if personName == "公司汇总":
            
            sqlstr = """
                SELECT
                    "1_pivot_everyday_all".date,
                    "1_pivot_everyday_all".weekday,
                    "1_pivot_everyday_all".IB,
                    "1_pivot_everyday_all".RB,
                    "1_pivot_everyday_all".CR,
                    "1_pivot_everyday_all".RS,
                    "1_pivot_everyday_all".FH,
                    "1_pivot_everyday_all".DII,
                    "1_pivot_everyday_all".TA
                FROM
                    "1_pivot_everyday_all"
            """
            sqlite_conn = sqlite3.connect(self.db)
            sqlite_cur = sqlite_conn.cursor()
            sqlite_cur.execute(sqlstr)
        
        else:
            sqlstr = """
                    SELECT
                        date_list.date,
                        date_list.weekday,
                        IB,
                        RB,
                        CR,
                        RS,
                        FH,
                        DII,
                        TA
                    FROM
                        date_list
                    LEFT JOIN
                        (SELECT
                        "1_pivot_everyday_person".dDate d,
                        "1_pivot_everyday_person".IB IB,
                        "1_pivot_everyday_person".RB RB,
                        "1_pivot_everyday_person".CR CR,
                        "1_pivot_everyday_person".RS RS,
                        "1_pivot_everyday_person".FH FH,
                        "1_pivot_everyday_person".DII DII,
                        "1_pivot_everyday_person"."其他" TA
                        FROM
                        "1_pivot_everyday_person"
                        WHERE
                        "1_pivot_everyday_person".cPersonName=?)
                    ON
                        date_list.date=d
            """
            sqlite_conn = sqlite3.connect(self.db)
            sqlite_cur = sqlite_conn.cursor()
            sqlite_cur.execute(sqlstr, (personName,))
        
        
        result = sqlite_cur.fetchall()
        
        return result
    


    def select_summary_everyday_by_person_2(self, personName):
        
        if personName == "公司汇总":
            
            sqlstr = """
                    SELECT
                    	"2_pivot_everyday_all".date,
                    	"2_pivot_everyday_all".weekday,
                       "2_pivot_everyday_all".total_amount,
                       "2_pivot_everyday_all".total_cost,
                       "2_pivot_everyday_all".total_profit,
                    	"2_pivot_everyday_all".IB,
                    	"2_pivot_everyday_all".IB_COST,
                    	"2_pivot_everyday_all".IB_PROFIT,
                    	"2_pivot_everyday_all".RB,
                    	"2_pivot_everyday_all".RB_COST,
                    	"2_pivot_everyday_all".RB_PROFIT,
                    	"2_pivot_everyday_all".CR,
                    	"2_pivot_everyday_all".CR_COST,
                    	"2_pivot_everyday_all".CR_PROFIT,
                    	"2_pivot_everyday_all".RS,
                    	"2_pivot_everyday_all".RS_COST,
                    	"2_pivot_everyday_all".RS_PROFIT,
                    	"2_pivot_everyday_all".FH,
                    	"2_pivot_everyday_all".FH_COST,
                    	"2_pivot_everyday_all".FH_PROFIT,
                    	"2_pivot_everyday_all".DII,
                    	"2_pivot_everyday_all".DII_COST,
                    	"2_pivot_everyday_all".DII_PROFIT,
                    	"2_pivot_everyday_all".TA,
                    	"2_pivot_everyday_all".TA_COST,
                    	"2_pivot_everyday_all".TA_PROFIT
                    FROM
                    	"2_pivot_everyday_all"
            """
            sqlite_conn = sqlite3.connect(self.db)
            sqlite_cur = sqlite_conn.cursor()
            sqlite_cur.execute(sqlstr)
        
        else:
            sqlstr = """
                    SELECT
                    	date_list.date,
                    	date_list.weekday,
                       total_amount,
                       total_cost,
                       total_profit,
                    	IB,
                    	IB_COST,
                    	IB_PROFIT,
                    	RB,
                    	RB_COST,
                    	RB_PROFIT,
                    	CR,
                    	CR_COST,
                    	CR_PROFIT,
                    	RS,
                    	RS_COST,
                    	RS_PROFIT,
                    	FH,
                    	FH_COST,
                    	FH_PROFIT,
                    	DII,
                    	DII_COST,
                    	DII_PROFIT,
                    	TA,
                    	TA_COST,
                    	TA_PROFIT
                    FROM
                    	date_list
                    LEFT JOIN (
                    	SELECT
                    		"2_pivot_everyday_person".dDate AS d,
                    		"2_pivot_everyday_person".total_amount,
                    		"2_pivot_everyday_person".total_cost,
                    		"2_pivot_everyday_person".total_profit,
                    		"2_pivot_everyday_person".IB,
                    		"2_pivot_everyday_person".IB_COST,
                    		"2_pivot_everyday_person".IB_PROFIT,
                    		"2_pivot_everyday_person".RB,
                    		"2_pivot_everyday_person".RB_COST,
                    		"2_pivot_everyday_person".RB_PROFIT,
                    		"2_pivot_everyday_person".CR,
                    		"2_pivot_everyday_person".CR_COST,
                    		"2_pivot_everyday_person".CR_PROFIT,
                    		"2_pivot_everyday_person".RS,
                    		"2_pivot_everyday_person".RS_COST,
                    		"2_pivot_everyday_person".RS_PROFIT,
                    		"2_pivot_everyday_person".FH,
                    		"2_pivot_everyday_person".FH_COST,
                    		"2_pivot_everyday_person".FH_PROFIT,
                    		"2_pivot_everyday_person".DII,
                    		"2_pivot_everyday_person".DII_COST,
                    		"2_pivot_everyday_person".DII_PROFIT,
                    		"2_pivot_everyday_person".TA,
                    		"2_pivot_everyday_person".TA_COST,
                    		"2_pivot_everyday_person".TA_PROFIT
                    	FROM
                    		"2_pivot_everyday_person"
                    	WHERE
                    		"2_pivot_everyday_person".p_name=?
                    ) ON date_list.date = d
            """
            sqlite_conn = sqlite3.connect(self.db)
            sqlite_cur = sqlite_conn.cursor()
            sqlite_cur.execute(sqlstr, (personName,))
        
        result = sqlite_cur.fetchall()
        
        return result




    def select_summary_customer(self):
        sqlstr = """
            SELECT
                Code,
                Name,
                Person,
                IB+RB+CR+RS+FH+DII+其他 AS 合计,
                IB,
                RB,
                CR,
                RS,
                FH,
                DII,
                其他
            FROM
                (SELECT
                    dispatch_mx.cCusCode Code,
                    dispatch_mx.cCusAbbName Name,
                    dispatch_mx.cPersonName Person,
                    ifnull(sum(case when dispatch_mx.cInvCName = "IB" then dispatch_mx.iNatMoney end), 0.0) IB,
                    ifnull(sum(case when dispatch_mx.cInvCName = "RB" then dispatch_mx.iNatMoney end), 0.0) RB,
                    ifnull(sum(case when dispatch_mx.cInvCName = "CR" then dispatch_mx.iNatMoney end), 0.0) CR,
                    ifnull(sum(case when dispatch_mx.cInvCName = "RS" then dispatch_mx.iNatMoney end), 0.0) RS,
                    ifnull(sum(case when dispatch_mx.cInvCName = "FH" then dispatch_mx.iNatMoney end), 0.0) FH,
                    ifnull(sum(case when dispatch_mx.cInvCName = "DII" then dispatch_mx.iNatMoney end), 0.0) DII,
                    ifnull(sum(case when dispatch_mx.cInvCName = "其他" then dispatch_mx.iNatMoney end), 0.0) 其他
                FROM
                    dispatch_mx
                GROUP BY dispatch_mx.cCusCode)
            ORDER BY 合计 DESC
        """
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(sqlstr)
        
        result = sqlite_cur.fetchall()
        
        sqlite_cur.close()
        sqlite_conn.close()
        
        return result


    def select_summary_customer_2(self):
        
        sqlstr_sum = """
        SELECT
		cCusCode,
		cCusAbbName,
		cCCName,
		cPersonName,
		IB+RB+CR+RS+FH+DII+TA AS HUIZONG,
		IBC+RBC+CRC+RSC+FHC+DIIC+TAC AS HUIZONG_COST,
		(IB+RB+CR+RS+FH+DII+TA)-(IBC+RBC+CRC+RSC+FHC+DIIC+TAC) AS HUIZONG_PROFIT,
           ((IB+RB+CR+RS+FH+DII+TA)-(IBC+RBC+CRC+RSC+FHC+DIIC+TAC))/(IB+RB+CR+RS+FH+DII+TA) AS PROFIT_RATE,
		IB,
		IBC,
		IB-IBC AS IB_PROFIT,
		RB,
		RBC,
		RB-RBC AS RB_PROFIT,
		CR,
		CRC,
		CR-CRC AS CR_PROFIT,
		RS,
		RSC,
		RS-RSC AS RS_PROFIT,
		FH,
		FHC,
		FH-FHC AS FH_PROFIT,
		DII,
		DIIC,
		DII-DIIC AS DII_PROFIT,
		TA,
		TAC,
		TA-TAC AS TA_PROFIT
        FROM
		(SELECT
			dispatch_mx.cCusCode,
			dispatch_mx.cCusAbbName,
			dispatch_mx.cCCName,
			dispatch_mx.cPersonName,
			ifnull(sum(case when dispatch_mx.cInvCName = "IB" then dispatch_mx.iNatMoney end), 0.0)  AS IB,
			ifnull(sum(case when dispatch_mx.cInvCName = "IB" then dispatch_mx.Cost end), 0.0)   AS IBC,
			ifnull(sum(case when dispatch_mx.cInvCName = "RB" then dispatch_mx.iNatMoney end), 0.0)  AS RB,
			ifnull(sum(case when dispatch_mx.cInvCName = "RB" then dispatch_mx.Cost end), 0.0)   AS RBC,
			ifnull(sum(case when dispatch_mx.cInvCName = "CR" then dispatch_mx.iNatMoney end), 0.0)  AS CR,
			ifnull(sum(case when dispatch_mx.cInvCName = "CR" then dispatch_mx.Cost end), 0.0)   AS CRC,
			ifnull(sum(case when dispatch_mx.cInvCName = "RS" then dispatch_mx.iNatMoney end), 0.0)  AS RS,
			ifnull(sum(case when dispatch_mx.cInvCName = "RS" then dispatch_mx.Cost end), 0.0)   AS RSC,
			ifnull(sum(case when dispatch_mx.cInvCName = "FH" then dispatch_mx.iNatMoney end), 0.0)  AS FH,
			ifnull(sum(case when dispatch_mx.cInvCName = "FH" then dispatch_mx.Cost end), 0.0)   AS FHC,
			ifnull(sum(case when dispatch_mx.cInvCName = "DII" then dispatch_mx.iNatMoney end), 0.0) AS DII,
			ifnull(sum(case when dispatch_mx.cInvCName = "DII" then dispatch_mx.Cost end), 0.0)  AS DIIC,
			ifnull(sum(case when dispatch_mx.cInvCName = "其他" then dispatch_mx.iNatMoney end), 0.0) AS TA,
			ifnull(sum(case when dispatch_mx.cInvCName = "其他" then dispatch_mx.Cost end), 0.0)  AS TAC
		FROM
        		dispatch_mx
		GROUP BY dispatch_mx.cCusCode, dispatch_mx.cPersonName)
      ORDER BY HUIZONG DESC
        """
        
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        
        # 生成统计表
        sqlite_cur.execute(sqlstr_sum)
        
        result = sqlite_cur.fetchall()
        
        sqlite_cur.close()
        sqlite_conn.close()
        
        return result



    def getPersonNameList(self):
    # 取得担当者的列表
    # 第一个总是 “公司汇总”
        lst = ["公司汇总", ]
    
        sqlstr = """
                SELECT DISTINCT
                    dispatch_mx.cPersonName
                FROM
                    dispatch_mx
                """
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(sqlstr)
        
        result = sqlite_cur.fetchall()
        
        for rec in result:
            lst.append(rec[0])
        
        sqlite_cur.close()
        sqlite_conn.close()
        
        return lst

    
#    def updateCost(self):
#        
#        sqlite_conn = sqlite3.connect(self.db)
#        sqlite_cur = sqlite_conn.cursor()
#        
#        # STEP 1   更新CostPrice表单价信息
#        
#        # 从inv中读取资材信息放入(inv中已经包含了组装品信息。见函数insert_inv，补充加入)
#        sqlstr_update_costprice_1 = """
#            INSERT OR REPLACE INTO CostPrice (cInvCode, CostPrice)
#            SELECT inv.cInvCode, inv.iInvRCost FROM inv WHERE inv.iInvRCost NOTNULL
#        """
#        
#        # 从BomList读取商品信息放入
#        sqlstr_update_costprice_2 = """
#            INSERT OR REPLACE INTO CostPrice (cInvCode, CostPrice, memo)
#            SELECT BomList.invCode, BomList.UnitCost, BomList.memo FROM BomList
#        """
#        
#        # update
#        sqlite_cur.execute(sqlstr_update_costprice_1)
#        sqlite_conn.commit()
#        
#        sqlite_cur.execute(sqlstr_update_costprice_2)
#        sqlite_conn.commit()
#        
#        
#        # STEP 2   更新dispatch_mx表的原价信息
#        
#        # 从CostPrice表中读取成本信息并计算
#        sqlstr_update_1 = """
#            UPDATE
#            	dispatch_mx
#            SET
#            	UnitCost=(SELECT CostPrice.CostPrice FROM CostPrice WHERE dispatch_mx.cInvCode=CostPrice.cInvCode),
#            	Cost=ROUND((SELECT CostPrice.CostPrice FROM CostPrice WHERE dispatch_mx.cInvCode=CostPrice.cInvCode)*iQuantity, 2),
#            	CostRateFlag=NULL
#            """
#        
#        # 从CostRate表中读取成本信息并计算
#        sqlstr_update_2 = """
#            UPDATE
#            	dispatch_mx
#            SET
#            	UnitCost=NULL,
#            	Cost=ROUND((SELECT CostRate.CostRate FROM CostRate WHERE dispatch_mx.cInvCode=CostRate.cInvCode)*iNatMoney, 2),
#            	CostRateFlag="Y"
#            WHERE 
#            	dispatch_mx.cInvCode IN (SELECT CostRate.cInvCode FROM CostRate)
#            """
#        
#        # update（有成本单价的存货）
#        sqlite_cur.execute(sqlstr_update_1)
#        sqlite_conn.commit()
#        
#        # update（无成本单价的存货）
#        sqlite_cur.execute(sqlstr_update_2)
#        sqlite_conn.commit()
#        
#        sqlite_conn.close()
        
    
    
    def updateCost(self):
        # 考虑到，如果是资材成本，则在inv表中，如果是商品，局在BomList中，再无，就在CostRate中
        # 所以要更新3次，这样就不用CostPrice表了
        
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        
        # STEP 1   从inv中读取资材信息放入(inv中已经包含了组装品信息。见函数insert_inv，补充加入)
        sqlstr = """
            UPDATE
                dispatch_mx
            SET
                UnitCost=(SELECT iInvRCost FROM inv WHERE dispatch_mx.cInvCode=inv.cInvCode),
                Cost=ROUND((SELECT iInvRCost FROM inv WHERE dispatch_mx.cInvCode=inv.cInvCode)*iQuantity, 2)
        """
        # update
        sqlite_cur.execute(sqlstr)
        sqlite_conn.commit()
        
        # STEP 2   从BomList表中读取成本信息并计算
        sqlstr = """
            UPDATE
                dispatch_mx
            SET
                UnitCost=(SELECT UnitCost FROM BomList WHERE dispatch_mx.cInvCode=BomList.invCode),
                Cost=ROUND((SELECT UnitCost FROM BomList WHERE dispatch_mx.cInvCode=BomList.invCode)*iQuantity, 2)
		WHERE
                dispatch_mx.UnitCost is NULL
        """
        # update
        sqlite_cur.execute(sqlstr)
        sqlite_conn.commit()
        
        
        # STEP 3  从CostRate表中读取成本信息并计算
        sqlstr = """
            UPDATE
                dispatch_mx
            SET
                Cost=ROUND((SELECT CostRate FROM CostRate WHERE dispatch_mx.cInvCode=CostRate.cInvCode)*iNatMoney, 2),
                CostRateFlag="Y"
		WHERE
                dispatch_mx.cInvCode IN (SELECT CostRate.cInvCode FROM CostRate)
            """
        # update（有成本单价的存货）
        sqlite_cur.execute(sqlstr)
        sqlite_conn.commit()
        
        sqlite_conn.close()
    
    
    
    
    
    def getCostNullList(self):
    # 取得未设定成本价格的条目
    # 返回4列。存货编码，存货名称，单位，存货大类
        sqlstr = """
        SELECT DISTINCT
            dispatch_mx.cInvCode,
            dispatch_mx.cInvName,
            dispatch_mx.cComUnitName,
            dispatch_mx.cInvCName
        FROM
            dispatch_mx
        WHERE dispatch_mx.cInvCode NOT IN (SELECT CostPrice.cInvCode FROM CostPrice UNION SELECT CostRate.cInvCode FROM CostRate)
                """
        
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(sqlstr)
        
        result = sqlite_cur.fetchall()
        
        sqlite_cur.close()
        sqlite_conn.close()
        
        return result
    
    
    def delete_dispatch_mx(self):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute("delete from dispatch_mx")
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def delete_inv(self):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute("delete from inv")
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def delete_date_list(self):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute("delete from date_list")
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def insert_dispatch_mx(self, mx_list):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        
        sqlstr = """
        INSERT INTO dispatch_mx (AutoID,
                                DLID,
                                cDLCode,
                                dDate,
                                cCusCode,
                                cCusAbbName,
                                cCCName,
                                cPersonName,
                                cInvCode,
                                cInvName,
                                cDefine22,
                                cDefine23,
                                cDefine25,
                                cDefine26,
                                iQuantity,
                                iNatMoney,
                                iNatTax,
                                iNatSum,
                                cInvCName,
                                cComUnitName,
                                cMemo,
                                cDefine29,
                                cSoCode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # 由于已经在提取数据时，日期使用了convert函数转换，这里直接输入
        sqlite_cur.executemany(sqlstr, mx_list)
        
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def delete_dispatch(self):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute("delete from dispatchList")
        sqlite_cur.execute("delete from dispatchLists")
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def insert_dispatch(self, head_list, body_list):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        
        # 表头
        sqlstr = """
        INSERT INTO dispatchList (DLID,
                                cDLCode,
                                dDate,
                                cCusCode,
                                cCusAbbName,
                                cCCName,
                                cPersonName,
                                cSOCode,
                                cMemo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # 由于已经在提取数据时，日期使用了convert函数转换，这里直接输入
        sqlite_cur.executemany(sqlstr, head_list)
        
        # 表体
        sqlstr = """
        INSERT INTO dispatchLists (AutoID,
                                DLID,
                                cInvCode,
                                cInvName,
                                cDefine22,
                                cDefine23,
                                cDefine25,
                                cDefine26,
                                iQuantity,
                                iNatMoney,
                                iNatTax,
                                iNatSum,
                                cComUnitName,
                                cDefine29,
                                cInvCName)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        sqlite_cur.executemany(sqlstr, body_list)
        
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    
    def insert_inv(self, mx_list):
        
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.executemany("INSERT INTO inv VALUES (?, ?, ?, ?, ?, ?, ?, ?)", mx_list)
        
        # 插入组装数据（用友取得的全部，不含AD和其他）
        bcp = [
            ('87101', 'POWERFUL 3L 电机',    '0301', 'CR', '5', '个', None, 618.92),
            ('87103', 'CM2000 限位开关',     '0301', 'CR', '4', '对', None, 68.41),
            ('87104', 'SP 限位开关',         '0301', 'CR', '4', '对', None, 69.38),
            ('87105', 'POWERFUL 3L-HL 电机', '0301', 'CR', '5', '个', None, 642.6),
            ('87201', 'ND双顶码75-T',        '0301', 'CR', '5', '个', None, 3.0),
        
            ('87220', 'F直轨单顶码', '0306', 'FH', '5', '个', None, 1.62),
            ('87221', 'F直轨双顶码', '0306', 'FH', '5', '个', None, 3.0),
            ('87222', 'W-16端套',    '0306', 'FH', '5', '个', None, 1.09),
            ('87223', 'W-24端套',    '0306', 'FH', '5', '个', None, 1.18),
            ('87243', 'W-24端套FH',  '0306', 'FH', '5', '个', None, 1.18)
        ]
        
        # 手动替换半成品内容
        sqlite_cur.executemany('INSERT OR REPLACE INTO inv (cInvCode, cInvName, cInvCCode, cInvCName, cComUnitCode, cComUnitName, iInvSCost, iInvRCost) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', bcp)
        
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def insert_date_list(self, date_list):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        # 由于已经在提取数据时，日期使用了convert函数转换，这里直接输入
        sqlite_cur.executemany("INSERT INTO date_list VALUES (?, ?)", date_list)
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
    def insert_cost_data(self, cost_data_list):
        sqlite_conn = sqlite3.connect(self.db)
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.executemany("INSERT INTO cost_master (cInvCode, useCostRate, CostPrice, CostRate) VALUES (?, ?, ?, ?)", cost_data_list)
        sqlite_conn.commit()
        sqlite_conn.close()
    
    
#    def uc_getAllList(self):
#    # 取得物料计算的条目
#    # 返回7列。'存货编码', '存货名称', '存货大类', '平均尺寸', '单位', 'SET原价', '单位原价'
#        sqlstr = """
#            SELECT
#                BomList.invCode,
#                inv.cInvName,
#                inv.cInvCName,
#                BomList.avgSize,
#                inv.cComUnitName,
#                BomList.Cost,
#                BomList.UnitCost,
#                BomList.memo
#            FROM
#                BomList
#            INNER JOIN inv ON BomList.invCode = inv.cInvCode
#                """
#        
#        sqlite_conn = sqlite3.connect(self.db)
#        sqlite_cur = sqlite_conn.cursor()
#        sqlite_cur.execute(sqlstr)
#        
#        result = sqlite_cur.fetchall()
#        
#        sqlite_cur.close()
#        sqlite_conn.close()
#        
#        return result
#    
#    
#    def uc_getInvInfo(self, invcode):
#    # 取得inv条目
#    # 返回5列。'存货编码', '存货名称', '存货大类', '单位', 单位原价
#        sqlstr = """
#            SELECT
#                inv.cInvCode,
#                inv.cInvName,
#                inv.cInvCName,
#                inv.cComUnitName,
#                inv.iInvRCost
#            FROM inv
#            WHERE inv.cInvCode=?
#                """
#        
#        sqlite_conn = sqlite3.connect(self.db)
#        sqlite_cur = sqlite_conn.cursor()
#        
#        sqlite_cur.execute(sqlstr, (invcode,))
#        
#        result = sqlite_cur.fetchall()
#        
#        sqlite_cur.close()
#        sqlite_conn.close()
#        
#        if result:
#            return result[0]
#        else:
#            return ()
#    
#    
#    def uc_getBom(self, invcode):
#    # 取得Bom，包括头和体
#    # 返回字典 {'head':(), 'body':[(),(),...]}
#    # head'存货编码', '存货名称', '存货大类', '单位', 单位原价
##        {'head': ('68136', 'FH F-27双轨', 'FH', '米', 3.12, 1.0, 3.12, 143.34, 45.94, 'aaa'),
##        'body': [('93132', 1.04, 0.08), ('93101', 62.0, 0.0), ('93131', 7.0, 0.0), ('92001', 14.0, 0.0), ('92002', 14.0, 0.0), ('83435', 2.0, 0.0), ('83436', 2.0, 0.0), ('93124', 4.0, 0.0), ('93106', 2.0, 0.0), ('89201', 1.04, 0.03)]}
#
#        rst = {'head':None, 'body':None}
#        
#        sqlstr_head = """
#            SELECT
#                BomList.invCode,
#                inv.cInvName,
#                inv.cInvCName,
#                inv.cComUnitName,
#                BomList.avgW,
#                BomList.avgH,
#                BomList.avgSize,
#                BomList.Cost,
#                BomList.UnitCost,
#                BomList.memo
#            FROM
#                BomList
#            INNER JOIN inv ON BomList.invCode = inv.cInvCode
#            WHERE
#                BomList.invCode=?
#                """
#        sqlstr_body = """
#            SELECT
#                BomLists.invCodeMX,
#                BomLists.invName,
#                BomLists.invCata,
#                BomLists.amount,
#                BomLists.unitName,
#                BomLists.lossRate,
#                BomLists.invRCost,
#                BomLists.cost
#            FROM
#                BomLists
#            WHERE
#                BomLists.invCode=?
#            ORDER BY BomLists.seqNum ASC
#                """
#        
#        sqlite_conn = sqlite3.connect(self.db)
#        sqlite_cur = sqlite_conn.cursor()
#        
#        sqlite_cur.execute(sqlstr_head, (invcode,))
#        result = sqlite_cur.fetchall()
#        
#        rst['head'] = result[0]
#        
#        
#        sqlite_cur.execute(sqlstr_body, (invcode,))
#        result = sqlite_cur.fetchall()
#        
#        rst['body'] = result
#        
#        
#        sqlite_cur.close()
#        sqlite_conn.close()
#
#        return rst
#
#
#    def uc_saveBom(self, data):
#        sqlite_conn = sqlite3.connect(self.db)
#        sqlite_cur = sqlite_conn.cursor()
#        
#        invcode = data['head'][0]
#        
#        # 检查invcode是否已经存在
#        sqlite_cur.execute('SELECT count(invCode) AS C FROM BomList WHERE invCode=?', (invcode,))
#        result = sqlite_cur.fetchone()  # (0,)
#        
#        # 表头
#        sqlite_cur.execute('INSERT OR REPLACE INTO BomList (invCode, avgW, avgH, avgSize, Cost, UnitCost, memo) VALUES (?, ?, ?, ?, ?, ?, ?)', data['head'])
#        
#        # 表体删旧
#        if result[0] != 0:
#            sqlite_cur.execute('DELETE FROM BomLists WHERE invCode=?', (invcode,))
#        
#        # 表体新增
#        sqlite_cur.executemany("INSERT INTO BomLists (invCode, seqNum, invCodeMX, invName, invCata, amount, unitName, lossRate, invRCost, cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data['body'])
#        
#        sqlite_conn.commit()
#        sqlite_cur.close()
#        sqlite_conn.close()
        




class ExcelHandle(object):
    
    def createExcelApp(self):
        #创建excel
        self.xlApp = win32com.client.DispatchEx('Excel.Application')
        print('Excel 程序开启')
    
    
    def quitExcelApp(self):
        self.xlApp.Quit()
        print('Excel 程序退出')
    
    
    def openExcelBook(self):
        xfile = os.path.split(os.path.realpath(__file__))[0] + '\\Stat\\mx.xlsx'
        self.xlBook = self.xlApp.Workbooks.Open(xfile)
        print('文件已打开 mx')

    
    def openExcelBook_2(self):
#        self.xlBook = self.xlApp.Workbooks.Open(sys.path[0] + '\\Stat\\mx_with_cost.xlsx')
        xfile = os.path.split(os.path.realpath(__file__))[0] + '\\Stat\\mx_with_cost.xlsx'
        self.xlBook = self.xlApp.Workbooks.Open(xfile)
        print('文件已打开 mx_with_cost')
    
    
    def closeExcelBook(self):
        self.xlBook.Close()
        print('文件已关闭')
        
    
    def excelBookSaveAs(self, fullName):
    #   xlBook.Save()
        self.xlBook.SaveAs(fullName)
        print('文件保存至: %s' % fullName)
    

#    def write_to_excel_everyday(self, all_data_list):
#        # all_data_list = [data_tuple_liuhao, data_tuple_wjj, data_tuple_wl, ....]
#        # data_tuple = (  u'刘浩',  u'2015-11-01', u'2015-11-12', [(u'2015-11-01', u'日', 39.97, 39.97, 39.97, 39.97, 39.97, 39.97, 39.97, 39.97), .... ]    )
#        
#        self.xlApp.Calculation = -4135 #(xlCalculationManual)
#        
#        for data_tuple in all_data_list:
#            # 取值
#            name, start_date, end_date, lst = data_tuple
#            
#            print('process %s by day' % name)
#            
#            # 在p后，复制一张工作表，并重命名
#            self.xlBook.Sheets("p").Copy(None, self.xlBook.Sheets(self.xlBook.Worksheets.Count) )
#            self.xlBook.ActiveSheet.Name = name
#            
#            
#            xlSheet = self.xlBook.Sheets[name]
#            
#            xlSheet.Cells(1, 3).Value = name
#            xlSheet.Cells(3, 4).Value = start_date
#            xlSheet.Cells(4, 4).Value = end_date
#            
#            #初始日期格在(7, 3)
#            self.writeAreaData(xlSheet, lst, start_row=7, start_col=3, text_col=[1,2])
#        
#        # 隐藏p表
#        self.xlBook.Sheets('p').Visible = False
#        
#        self.xlApp.Calculation = -4105 # xlCalculationAutomatic
    
    
    def write_to_excel_everyday_2(self, all_data_list):
        # all_data_list = [data_tuple_liuhao, data_tuple_wjj, data_tuple_wl, ....]
        # data_tuple = (  u'刘浩',  u'2015-11-01', u'2015-11-12', [(u'2015-11-01', u'日', 39.97, 39.97, 39.97, 39.97, 39.97, 39.97, 39.97, 39.97), .... ]    )
        
        for data_tuple in all_data_list:
            # 取值
            name, start_date, end_date, lst = data_tuple
            
            print('process %s by day' % name)
            
            # 在p后，复制一张工作表，并重命名
            self.xlBook.Sheets('p').Copy(None, self.xlBook.Sheets(self.xlBook.Worksheets.Count))
            self.xlBook.ActiveSheet.Name = name
            
            xlSheet = self.xlBook.Sheets[name]
            
            xlSheet.Cells(1, 3).Value = name
            xlSheet.Cells(3, 4).Value = start_date
            xlSheet.Cells(4, 4).Value = end_date
            
            #初始日期格在(18, 3)，从第3列一直写到28列
            self.writeAreaData(xlSheet, lst, start_row=18, start_col=3, text_col=[1,2], float_col=list(range(3,29)))
        
        # 隐藏p表
        self.xlBook.Sheets('p').Visible = False
    
    

    def write_to_excel_customer(self, data_tuple):
#        data_tuple = ('2015-11-01',
#                     '2015-11-12',
#                     [('2015-11-01', '日', 39.97, 39.97, 39.97, 39.97, 39.97, 39.97, 39.97, 39.97), ])
        
        self.xlApp.Calculation = -4135   #(xlCalculationManual)
        
        # 取值
        start_date, end_date, lst = data_tuple
        
        print('process 客户汇总')
        
        xlSheet = self.xlBook.Sheets['客户汇总']
        
        xlSheet.Cells(3, 4).Value = start_date
        xlSheet.Cells(4, 4).Value = end_date
        
        #初始日期格在(16, 3)  C16格
        self.writeAreaData(xlSheet, lst, start_row=16, start_col=3, text_col=[1,2,3], float_col=[4,5,6,7,8,9,10,11])
        
        # 活动工作表定位到 客户汇总
        xlSheet = self.xlBook.Sheets['客户汇总'].Activate()

        self.xlApp.Calculation = -4105   # xlCalculationAutomatic


    def write_to_excel_customer_2(self, data_tuple):
        # 取值
        start_date, end_date, lst = data_tuple
        
        print('process 客户汇总')
        
        xlSheet = self.xlBook.Sheets['客户汇总']
        
        xlSheet.Cells(3, 4).Value = start_date
        xlSheet.Cells(4, 4).Value = end_date
        
        #初始日期格在(12, 3)  C12格
        self.writeAreaData(xlSheet, lst, start_row=16, start_col=3,
                           text_col=[1,2,3,4],
                           float_col=[5,6,7]+list(range(9,30)))
        
        # 活动工作表定位到 客户汇总
        xlSheet = self.xlBook.Sheets['客户汇总'].Activate()
        


    def newWorkBook(self):
        # 文件只有1个工作表 Sheet1
        self.xlBook = self.xlApp.Workbooks.Add()
        self.xlSheet = self.xlBook.Sheets['Sheet1']
    
    

    def writeAreaData(self, xlSheet, data_list, start_row=1, start_col=1, text_col=[], float_col=[], ignore_col=[]):
        """
        把data_list数据一次写入xlSheet
        data_list = [ (a,b,c), (a,b,c), ... ]
        start_row, start_col 是xlSheet的，从1开始
        text_col是列表，指出数据中，这些列要在前标单引号，从1开始。遇到数据Null则替换为空串
        float_col是列表，指出数据中，这些列要为保留2位小数，从1开始。遇到数据Null则替换为0.00
        ignore_col是列表，指出数据中，这些列跳过不处理。（无论数据内容为什么，都不写入xls）
        不指定的话，按照原数据写入
        """
        
        row_count = len(data_list)
        col_count = len(data_list[0])
        
        # 调整3个列表，从1基调整为0基
        text_col   = [t-1 for t in text_col]
        float_col  = [t-1 for t in float_col]
        ignore_col = [t-1 for t in ignore_col]
        
        ##  竖着写入（先写入第一列，然后第二列。。。）
        for i in range(col_count):     # 一共有col_count列数据
            
            if i in text_col:
                for j in range(row_count):     # 一共有data_count行数据
                    # 把一列的数据全部写完（竖着写），写入row, col格
                    cell_data = data_list[j][i]
                    if cell_data is not None:
                        cell_data = "'" + (data_list[j][i] or '')
                        sheet_row = j+start_row
                        sheet_col = i+start_col
                        xlSheet.Cells(sheet_row, sheet_col).Value = cell_data

            elif i in float_col:
                for j in range(row_count):
                    cell_data = data_list[j][i]
                    if cell_data not in [0.0, '', None]:
                        cell_data = "%.2f" % (cell_data)
                        sheet_row = j+start_row
                        sheet_col = i+start_col
                        xlSheet.Cells(sheet_row, sheet_col).Value = cell_data

            elif i in ignore_col:
                pass
            
            else:
                for j in range(row_count):
                    cell_data = data_list[j][i]
                    sheet_row = j+start_row
                    sheet_col = i+start_col
                    xlSheet.Cells(sheet_row, sheet_col).Value = cell_data

