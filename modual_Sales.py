# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:26:56 2016

@author: 008
"""

import os
import datetime
import xlsxwriter
import win32com.client

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot

from ui_Sales_SelectCus import Ui_Sales_SelectCus
from ui_Sales_SO_Main import Ui_Sales_SO_Main
from ui_Sales_SO_Detail import Ui_Sales_SO_Detail
from ui_Sales_DB_Main import Ui_Sales_DB_Main
from ui_Sales_DB_Detail import Ui_Sales_DB_Detail
from ui_Sales_LabelPrint import Ui_Sales_LabelPrint
from ui_Sales_DB_NitoriDispatch import Ui_Sales_DB_NitoriDispatch

from core import LoadServerDataClass_PYQT_ODBC
from core import MysqlHandle
from core import FETCH_DATA_MERGE

from core import Template
from core import SO_dataColumnArrange
from core import TableModelCreater
from core import SettingReader
#from core import SO


import pdb


class Frm_Sales_SelectCus(QtGui.QDialog, Ui_Sales_SelectCus):
     
    def __init__(self, parent=None):
        super(Frm_Sales_SelectCus, self).__init__(parent)
        self.setupUi(self)
        
        head_str = ['客户编码', '客户简称']
        head_width = [120, 300]
        
        self.tableModel = QtGui.QStandardItemModel()
        
        # 此处设定按照userrole排序（userrole中为数据实际值）
        self.tableModel.setSortRole(QtCore.Qt.UserRole)
        
        self.tableModel.setHorizontalHeaderLabels(head_str)
        
        self.tableView.setModel(self.tableModel)
        
        for i, width in enumerate(head_width):
            self.tableView.setColumnWidth(i, width)
        
        # 设置默认行高
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        
        # 双击事件
        self.tableView.doubleClicked.connect(self.__db_click)
        
        # 放置选择后的cuscode
        self.cusCode = ''
        
        self.lineEdit.setFocus()
    
        
    
    @pyqtSlot(QtCore.QModelIndex)
    def __db_click(self, idx):
        itm = self.tableModel.item(idx.row(), 0)        
        txt = itm.text()
        
        # 设定一个变量，放cuscode        
        self.cusCode = txt
        self.accept()
    
    
    
    def set_filter_keyword(self, filter_keyword):
        self.lineEdit.setText(filter_keyword)
        
        lsdc = LoadServerDataClass_PYQT_ODBC()
        lsdc.add_conn()
        lst = lsdc.fetch_Customer(filter_keyword)
        lsdc.remove_conn()
        
        self.__update_tableModel(lst)
        
    
    
    def __update_tableModel(self, dataList):
        
        self.tableModel.setRowCount(0)
        
        if dataList:
            for i, tp in enumerate(dataList):
                # 先把纯data设置到userrole（目的是以后可以按照userrole排序）
                for j in range(len(tp)):
                    itm = QtGui.QStandardItem()
                    value = tp[j] if tp[j] is not None else ''
                    itm.setData(value, QtCore.Qt.DisplayRole)   # 同样设置displayrole
                    self.tableModel.setItem(i, j, itm)


    @pyqtSlot()
    def on_pushButton_clicked(self):
        txt = self.lineEdit.text().strip()
        
        lsdc = LoadServerDataClass_PYQT_ODBC()
        lsdc.add_conn()
        lst = lsdc.fetch_Customer(filter_keyword=txt)
        lsdc.remove_conn()
        
        self.__update_tableModel(lst)




class Frm_Sales_SO_Main(QtGui.QWidget, Ui_Sales_SO_Main):
     
    def __init__(self, parent=None):
        super(Frm_Sales_SO_Main, self).__init__(parent)
        self.setupUi(self)
        
        # 初始化查询日期
        today = QtCore.QDate().currentDate()
        self.dateEdit_start.setDate(today)
        self.dateEdit_end.setDate(today)
        
        # 设置模板
        templateNameList = ['销售订单（公司留存）.xml', '生产检验单.xml', '外包单.xml', '现场生产单.xml', '现场生产单2.xml']
        for templateName in templateNameList:
            itm = QtGui.QListWidgetItem(templateName)
            itm.setCheckState(QtCore.Qt.Checked)
            self.list_template.addItem(itm)
        
        itm = self.list_template.item(0)
        itm.setCheckState(QtCore.Qt.Unchecked)
        
        # 读取列setting
        sr = SettingReader()
        self.columnRef = sr.load_SO_HEAD()
        
        # (程序内英文名，表头显示名， 列宽， 列格式， 是否合计0否1是)
#        self.columnRef =    [('soCode', '订单号', 80, 'CHECK_STYLE', 0),
#                             ('cusCode', '客户编码', 65, '', 0),
#                             ('cusAbbName', '客户简称', 90, '', 0),
#                             ('po', '对方订单号', 110, '', 0),
#                             ('iMoney', '无税价格', 80, 'MONEY_STYLE', 1),
#                             ('iTax', '税额', 80, 'MONEY_STYLE', 1),
#                             ('iSum', '价税合计', 80, 'MONEY_STYLE', 1),
#                             ('memo', '备注', 230, '', 0),
#                             ('soDate', '订单日期', 80, '', 0),
#                             ('preDate', '预发货日期', 80, '', 0),
#                             ('scName', '发运方式', 100, '', 0),
#                             ('maker', '制单人', 60, '', 0),
#                             ('verifier', '审核人', 60, '', 0),
#                             ('lastPrint', '最后打印', 130, '', 0)]

        # 生成model
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef)
        self.tableView.setModel(self.tableModel)
        
        # 设置列宽
        for i, width in enumerate([tp[2] for tp in self.columnRef]):
            self.tableView.setColumnWidth(i, width)
        
        self.color_0 = QtGui.QColor(255, 255, 255)  #未选
        self.color_1 = QtGui.QColor(0, 255, 255)  #选中
        
        # 设置表头不高亮
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setHighlightSections(False)
        
        # 设置默认行高
        self.tableView.verticalHeader().setDefaultSectionSize(26)
        
        # 设置可点击排序
        self.tableView.setSortingEnabled(True)
        
        # 生成右键菜单
        self.pop_menu = QtGui.QMenu()
        self.action_details = QtGui.QAction(self)
        self.action_find_db = QtGui.QAction(self)
        self.pop_menu.addAction(self.action_details)
        self.pop_menu.addAction(self.action_find_db)
        self.tableView.customContextMenuRequested.connect(self.__contextMenuOpen)
        
        # 第一列勾选事件
        self.tableModel.dataChanged.connect(self.__itemCheckChanged)
        
        # cell双击事件
        self.tableView.doubleClicked.connect(self.__cell_dbclick)
        
        # 全选 全消事件
        self.checkBox.stateChanged.connect(self.__boxCheckChanged)
        
        # 鼠标回车 事件
        self.lineEdit_cusCode.returnPressed.connect(self.on_btn_query_clicked)
        self.lineEdit_socode.returnPressed.connect(self.on_btn_query_clicked)
        
        # 右键菜单 事件
        self.action_details.triggered.connect(self.__action_details_trigger)
        self.action_find_db.triggered.connect(self.__action_find_db_trigger)
    
    
    def update_tableModel(self, dataList):
        self.tableModel.dataChanged.disconnect(self.__itemCheckChanged)
        
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef, dataList)
        
        self.tableModel.dataChanged.connect(self.__itemCheckChanged)
        
        self.tableView.setModel(self.tableModel)
    
    
    @pyqtSlot()
    def __action_details_trigger(self):
        soCode = self.action_details.data()
        if soCode:
            fd = FETCH_DATA_MERGE()
            soList = fd.fetch_SOs(soCode)
            
            so = soList[0]
            
            w = Frm_Sales_SO_Detail()
            w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            w.setSO(so)
            tabWidget = self.parent().parent()
            idx = tabWidget.addTab(w, '销售订单')
            tabWidget.setCurrentIndex(idx)
    
    
    @pyqtSlot()
    def __action_find_db_trigger(self):
        soCode = self.action_details.data()
        if soCode:
            fd = FETCH_DATA_MERGE()
            dataList = fd.fetch_DB_HEAD_BY_SO(soCode)
            
            # 打开 发货单列表 界面
            w = Frm_Sales_DB_Main()
            w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            tabWidget = self.parent().parent()
            idx = tabWidget.addTab(w, '发货单列表')
            tabWidget.setCurrentIndex(idx)
            # 显示
            w.update_tableModel(dataList)
    
    
    @pyqtSlot(QtCore.QPoint)
    def __contextMenuOpen(self, pos):
#        self.pop_menu.clear()
#        self.pop_menu.exec_(pos)
        # 取得当前item（idx总归是一个对象，if idx没什么意义。但是点击表格空白处，idx.row()返回-1）
        idx = self.tableView.indexAt(pos)
        
        # 表示点击的地方有格子。row()能正常返回行号
        if idx.row() != -1:
            # 这里要去除最后合计行（合计行userrole为None）
            row = idx.row()
            col = [tp[0] for tp in self.columnRef].index('soCode')
            
            itm = self.tableModel.item(row, col)
            soCode = itm.data(QtCore.Qt.UserRole)
            if soCode:
#                self.action_details.setText('{} 明细...'.format(soCode))
                self.action_details.setText('查看明细...')
                self.action_details.setData(soCode)
                
                self.action_find_db.setText('{}下查发货单...'.format(soCode))
                self.action_find_db.setData(soCode)
                
                self.pop_menu.exec_(QtGui.QCursor.pos())
    
    
    @pyqtSlot(QtCore.QModelIndex)
    def __itemCheckChanged(self, idx):
        # 只针对第一列，勾选变化
        self.tableModel.dataChanged.disconnect(self.__itemCheckChanged)
        
        if idx.column() == 0:
            row = idx.row()
            columnCount = self.tableModel.columnCount()
            
            # cellwidget的格子，item()会返回None
            if self.tableModel.item(row, 0).data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Unchecked:
                for i in range(columnCount):
                    self.tableModel.item(row, i).setData(QtGui.QBrush(self.color_0), QtCore.Qt.BackgroundRole)
            else:
                for i in range(columnCount):
                    self.tableModel.item(row, i).setData(QtGui.QBrush(self.color_1), QtCore.Qt.BackgroundRole)
        
        self.tableModel.dataChanged.connect(self.__itemCheckChanged)
        
        self.tableView.setModel(self.tableModel)


    @pyqtSlot(int)
    def __boxCheckChanged(self, state):
        # 全选 全消事件
        rowCount = self.tableModel.rowCount() - 1
        if state == QtCore.Qt.Checked:
            for i in range(rowCount):
                self.tableModel.item(i, 0).setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
        else:
            for i in range(rowCount):
                self.tableModel.item(i, 0).setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)


    @pyqtSlot()
    def on_btn_unprinted_clicked(self):
        # 查找 最后打印  是在哪一栏
        lst = [ tp[0] for tp in self.columnRef ]
        if ('lastPrint' in lst) and ('soCode' in lst):
            idx_soCode = lst.index('soCode')
            idx_lastPrint = lst.index('lastPrint')
            
            # 勾选未打印订单
            rowCount = self.tableModel.rowCount() - 1
            for i in range(rowCount):
                itm_soCode = self.tableModel.item(i, idx_soCode)
                itm_lastPrint = self.tableModel.item(i, idx_lastPrint)  # 最后一列打印时间
                if not itm_lastPrint.text():
                    itm_soCode.setCheckState(QtCore.Qt.Checked)


    @pyqtSlot(QtCore.QModelIndex)
    def __cell_dbclick(self, idx):
        # 任何一个双击，显示明细
        row = idx.row()
        col = [tp[0] for tp in self.columnRef].index('soCode')
        
        # 最后一行例外（为合计行）
        if row < self.tableModel.rowCount() - 1:
            
            itm = self.tableModel.item(row, col)
            soCode = itm.text()
            
            if soCode:
                fd = FETCH_DATA_MERGE()
                soList = fd.fetch_SOs(soCode)
                
                so = soList[0]
                
                w = Frm_Sales_SO_Detail()
                w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                w.setSO(so)
                tabWidget = self.parent().parent()
                idx = tabWidget.addTab(w, '销售订单')
                tabWidget.setCurrentIndex(idx)
    
    
    @pyqtSlot()
    def on_btn_query_clicked(self):
        if self.lineEdit_socode.text().strip() == '':
            startDate = self.dateEdit_start.text()
            endDate   = self.dateEdit_end.text()
            cusCode   = self.lineEdit_cusCode.text().strip()
            dataList = self.__query(startDate, endDate, cusCode)
        else:
            dataList = self.__query_socode()
        # 设置model
        self.update_tableModel(dataList)
    
    
    @pyqtSlot()
    def on_btn_query_today_clicked(self):
        now = datetime.datetime.now()
        startDate = now.strftime("%Y-%m-%d")
        endDate   = now.strftime("%Y-%m-%d")
        
        dataList = self.__query(startDate, endDate)
        # 设置model
        self.update_tableModel(dataList)
    
    
    @pyqtSlot()
    def on_btn_SelectCus_clicked(self):
        aa = Frm_Sales_SelectCus(self)
        aa.set_filter_keyword( self.lineEdit_cusCode.text().strip() )
        aa.exec_()
        if aa.cusCode:
            self.lineEdit_cusCode.setText(aa.cusCode)
    
    
    @pyqtSlot()
    def __query(self, startDate, endDate, cusCode=''):
        fd = FETCH_DATA_MERGE()
        dataList = fd.fetch_SO_HEAD(startDate, endDate, cusCode)
        return dataList


    @pyqtSlot()
    def __query_socode(self):
        soCode = self.lineEdit_socode.text().strip()
        fd = FETCH_DATA_MERGE()
        dataList = fd.fetch_SO_HEAD_BY_CODE(soCode)
        return dataList
                
    
    @pyqtSlot()
    def on_btn_print_clicked(self):
        
        model = self.tableView.model()
        rowCount = model.rowCount()
        
        # 生成订单号列表lst
        soList = []
        for i in range(rowCount-1):
            itm = model.item(i, 0)
            if itm.checkState() == QtCore.Qt.Checked:
                soList.append(itm.data(QtCore.Qt.UserRole))
        
        # 读入模板名 templateNameList （只有文件名，不含全地址）
        tptShortNameList = []
        for i in range(self.list_template.count()):
            itm = self.list_template.item(i)
            if itm.checkState() == QtCore.Qt.Checked:
                tptShortNameList.append(itm.text())
        
        # 弹窗提示：已选订单
        if soList == []:
            return
        else:
            result = QtGui.QMessageBox.question(self, '确认', '共选择了 {} 份订单，打印吗？'.format(len(soList)), QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        
        if result != QtGui.QMessageBox.Yes:
            return
        
        # 弹窗提示：未审核订单
        uncheckedSoList = []
        for i in range(rowCount-1):
            itm_soCode = model.item(i, 0)
            itm_verifier = model.item(i, 12)
            
            if itm_soCode.checkState() == QtCore.Qt.Checked:
                if itm_verifier.data(QtCore.Qt.DisplayRole) == '':
                    uncheckedSoList.append(itm_soCode.data(QtCore.Qt.DisplayRole))
        
        if uncheckedSoList != []:
            result = QtGui.QMessageBox.question(self, '确认', '已勾选订单中包含 {} 份未审核订单，打印吗？'.format( len(uncheckedSoList) ), QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        
        if result != QtGui.QMessageBox.Yes:
            return
        
        # 提交打印
        isPrintlog = True
        if self.checkBox_printlog.checkState() == QtCore.Qt.Unchecked:
            isPrintlog = False
        
        isActualPrint = True
        if self.checkBox_actualprint.checkState() == QtCore.Qt.Unchecked:
            isActualPrint = False
        
        psoc = PrintSoClass()
        psoc.printSOs(soList, tptShortNameList, printlog=isPrintlog, actualPrint=isActualPrint)
        
        # 刷新一遍列表，或许有更新打印日期数据
        self.on_btn_query_clicked()
        
        #提示完成
        QtGui.QMessageBox.information(self, '提示', '打印完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    
    @pyqtSlot()
    def on_btn_output_excel_clicked(self):
        fileFullName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + '销售订单列表', 'Excel Files (*.xlsx)')
        if fileFullName:
            ew = ExcelWrite()
            ew.fromTableModel(fileFullName, self.tableModel)
            QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        



class Frm_Sales_SO_Detail(QtGui.QWidget, Ui_Sales_SO_Detail):
     
    def __init__(self, parent=None):
        super(Frm_Sales_SO_Detail, self).__init__(parent)
        self.setupUi(self)
        
        # 读取列setting
        sr = SettingReader()
        self.columnRef = sr.load_SO()
        
        # 生成model
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef)
        self.tableView.setModel(self.tableModel)
        
        # 设置列宽
        for i, width in enumerate( [tp[2] for tp in self.columnRef] ):
            self.tableView.setColumnWidth(i, width)
        
        # 设置表头不高亮
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setHighlightSections(False)
        
        # 设置默认行高
        self.tableView.verticalHeader().setDefaultSectionSize(38)
    
    
    def setSO(self, so):
        # 传入这里的是标准SO （已经增加cutHint，lastprint）
        soData = so.data
#        pdb.set_trace()
        # 表头数据显示
        self.label_socode.setText(soData['soCode'])
        self.label_soabbname.setText(soData['cusAbbName'])
        self.label_date.setText(soData['soDate'])
        self.label_predate.setText(soData['preDate'])
        self.label_cuspo.setText(soData['po'])
        self.label_person.setText(soData['personName'])
        self.label_koulv.setText(soData['hKoulv'])
        self.label_memo.setText(soData['hMemo'])
        self.label_maker.setText(soData['maker'])
        self.label_verifier.setText(soData['verifier'])
        self.label_scname.setText(soData['scName'])
        self.label_cuthint.setText(soData['cutHint'])
        
        # 表体数据显示（显示数据先按照columnRef顺序排列。这样就可以在setting里随意定义列，不导致出错）
        colsName = [ tp[0] for tp in self.columnRef ]
        soData = SO_dataColumnArrange(soData, colsName)
        
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef, soData['table'])
        
        self.tableView.setModel(self.tableModel)


    @pyqtSlot()
    def on_btn_print_clicked(self):
        soList = [self.label_socode.text(), ]
        tptShortNameList = ['生产检验单.xml', '外包单.xml', '现场生产单.xml', '现场生产单2.xml']
        # 提交打印
        psoc = PrintSoClass()
        psoc.printSOs(soList, tptShortNameList)



class Frm_Sales_DB_Main(QtGui.QWidget, Ui_Sales_DB_Main):
     
    def __init__(self, parent=None):
        super(Frm_Sales_DB_Main, self).__init__(parent)
        self.setupUi(self)

        # 初始化查询日期
        today = QtCore.QDate().currentDate()
        self.dateEdit_start.setDate(today)
        self.dateEdit_end.setDate(today)
        
        # 设置模板
#        file_name_list = ['销售订单（公司留存）.xml', '生产检验单.xml', '外包单.xml', '现场生产单.xml', '现场生产单2.xml']
#        
#        for file_name in file_name_list:
#            itm = QtGui.QListWidgetItem(file_name)
#            itm.setCheckState(QtCore.Qt.Checked)
#            self.list_template.addItem(itm)
#        
#        itm = self.list_template.item(0)
#        itm.setCheckState(QtCore.Qt.Unchecked)
        
#        head_str = ['发货单号', '客户编码', '客户简称', '价税合计', '备注', '发货单日期', '订单号', '发运方式', '制单', '审核', '最后标签打印']
#        head_width = [110, 70, 120, 90, 320, 90, 60, 110, 60, 60, 140]
        
        
        # 读取列setting
        sr = SettingReader()
        self.columnRef = sr.load_DB_HEAD()
        
        # 生成model
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef)
        self.tableView.setModel(self.tableModel)
        
        # 设置列宽
        for i, width in enumerate( [tp[2] for tp in self.columnRef] ):
            self.tableView.setColumnWidth(i, width)
        
        
        self.color_0 = QtGui.QColor(255, 255, 255)  #未选
        self.color_1 = QtGui.QColor(0, 255, 255)  #选中
        
        # 设置表头不高亮
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setHighlightSections(False)
        
        # 设置默认行高
        self.tableView.verticalHeader().setDefaultSectionSize(26)
        
        # 设置可点击排序
        self.tableView.setSortingEnabled(True)
        
        # 生成右键菜单
        self.pop_menu = QtGui.QMenu()
        self.action_details = QtGui.QAction(self)
        self.action_find_so = QtGui.QAction(self)
        self.pop_menu.addAction(self.action_details)
        self.pop_menu.addAction(self.action_find_so)
        self.tableView.customContextMenuRequested.connect(self.__contextMenuOpen)
        
        # 第一列勾选事件
        self.tableModel.dataChanged.connect(self.__check_changed)
        
        # cell双击事件
        self.tableView.doubleClicked.connect(self.__cell_dbclick)
        
        # 全选 全消事件
        self.checkBox.stateChanged.connect(self.__checkstate_changed)
        
        # 鼠标回车 事件
        self.lineEdit_cusCode.returnPressed.connect(self.on_btn_query_clicked)
        self.lineEdit_dbcode.returnPressed.connect(self.on_btn_query_clicked)
        
        # 右键菜单 事件
        self.action_details.triggered.connect(self.__action_details_trigger)
        self.action_find_so.triggered.connect(self.__action_find_so_trigger)
    
    
    def update_tableModel(self, dataList):
        self.tableModel.dataChanged.disconnect(self.__check_changed)
        
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef, dataList)
        
        self.tableModel.dataChanged.connect(self.__check_changed)
        # 设置model
        self.tableView.setModel(self.tableModel)
        
        
        
#        lastRow = self.tableModel.rowCount()
#        for row in range(self.tableModel.rowCount()):
##            for col in range(self.tableModel.columnCount()):
#            itm = self.tableModel.item(row, 5)
#            print(itm.data(QtCore.Qt.DisplayRole), itm.data(QtCore.Qt.UserRole))
#        
#        self.tableModel.setSortRole(QtCore.Qt.DisplayRole)
#        
#        self.tableView.sortByColumn(5, QtCore.Qt.DescendingOrder)
        
        
        
    
    
    @pyqtSlot()
    def __action_details_trigger(self):
        dbCode = self.action_details.data()
        # 任何非0数字或非空对象对象都是真
        # 数字0，空对象以及特殊对象None都被认作是假
        if dbCode:
            fd = FETCH_DATA_MERGE()
            dbList = fd.fetch_DBs(dbCode)
            
            db = dbList[0]
            
            w = Frm_Sales_DB_Detail()
            w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            w.setDB(db)
            tabWidget = self.parent().parent()
            idx = tabWidget.addTab(w, '发货单')
            tabWidget.setCurrentIndex(idx)
        
    
    @pyqtSlot()
    def __action_find_so_trigger(self):
        soCode = self.action_find_so.data()
        if soCode:
            fd = FETCH_DATA_MERGE()
            dataList = fd.fetch_SO_HEAD_BY_CODE(soCode)
            
            # 打开 发货单列表 界面
            w = Frm_Sales_SO_Main()
            w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            tabWidget = self.parent().parent()
            idx = tabWidget.addTab(w, '销售订单列表')
            tabWidget.setCurrentIndex(idx)
            # 显示
            w.update_tableModel(dataList)
        
    
    @pyqtSlot(QtCore.QPoint)
    def __contextMenuOpen(self, pos):
        idx = self.tableView.indexAt(pos)
        if idx.row() != -1:
            
            row = idx.row()
            so_col = [tp[0] for tp in self.columnRef].index('soCode')
            db_col = [tp[0] for tp in self.columnRef].index('dbCode')
            
            itm_dbCode = self.tableModel.item(row, db_col)
            dbCode = itm_dbCode.data(QtCore.Qt.UserRole)
            itm_soCode = self.tableModel.item(row, so_col)
            soCode = itm_soCode.data(QtCore.Qt.UserRole)
            if dbCode:
                self.action_details.setText('查看明细...')
                self.action_details.setData(dbCode)
                
                self.action_find_so.setText('上查销售订单...')
                self.action_find_so.setData(soCode)
                
                self.pop_menu.exec_(QtGui.QCursor.pos())
    
    
    @pyqtSlot(QtCore.QModelIndex)
    def __check_changed(self, idx):
        # 只针对第一列，勾选变化
        self.tableModel.dataChanged.disconnect(self.__check_changed)
        
        if idx.column() == 0:
            
            row = idx.row()
            columnCount = self.tableModel.columnCount()
            
            # cellwidget的格子，item()会返回None
            if self.tableModel.item(row, 0).data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Unchecked:
                for i in range(columnCount):
                    self.tableModel.item(row, i).setData(QtGui.QBrush(self.color_0), QtCore.Qt.BackgroundRole)
            else:
                for i in range(columnCount):
                    self.tableModel.item(row, i).setData(QtGui.QBrush(self.color_1), QtCore.Qt.BackgroundRole)
            
        self.tableModel.dataChanged.connect(self.__check_changed)
        
        self.tableView.setModel(self.tableModel)


    @pyqtSlot(QtCore.QModelIndex)
    def __cell_dbclick(self, idx):
        row = idx.row()
        col = [tp[0] for tp in self.columnRef].index('dbCode')
        
        # 最后一行例外（为合计行）
        if row < self.tableModel.rowCount() - 1:
            
            itm = self.tableModel.item(row, col)
            dbCode = itm.text()            
            if dbCode:
                fd = FETCH_DATA_MERGE()
                dbList = fd.fetch_DBs(dbCode)
                
                db = dbList[0]
                
                w = Frm_Sales_DB_Detail()
                w.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                w.setDB(db)
                tabWidget = self.parent().parent()
                idx = tabWidget.addTab(w, '发货单')
                tabWidget.setCurrentIndex(idx)


    @pyqtSlot(int)
    def __checkstate_changed(self, state_int):
        # 全选 全消事件
        rows = self.tableModel.rowCount() - 1
        
        if state_int == QtCore.Qt.Checked:
            for row in range(rows):
                self.tableModel.item(row, 0).setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
        else:
            for row in range(rows):
                self.tableModel.item(row, 0).setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
    
    
    @pyqtSlot()
    def on_btn_query_clicked(self):
        if self.lineEdit_dbcode.text().strip() == '':
            startDate = self.dateEdit_start.text()
            endDate   = self.dateEdit_end.text()
            cusCode   = self.lineEdit_cusCode.text().strip()
            dataList  = self.__query(startDate, endDate, cusCode)
        else:
            dataList = self.__query_dbcode()
        # 显示数据
        self.update_tableModel(dataList)
    
    
    @pyqtSlot()
    def on_btn_query_today_clicked(self):
        now = datetime.datetime.now()
        startDate = now.strftime("%Y-%m-%d")
        endDate   = now.strftime("%Y-%m-%d")
        
        dataList = self.__query(startDate, endDate)
        # 显示数据
        self.update_tableModel(dataList)
    
    
    @pyqtSlot()
    def on_btn_SelectCus_clicked(self):
        aa = Frm_Sales_SelectCus(self)
        aa.set_filter_keyword( self.lineEdit_cusCode.text().strip() )
        aa.exec_()
        if aa.cusCode:
            self.lineEdit_cusCode.setText(aa.cusCode)
    
    
    @pyqtSlot()
    def __query(self, startDate, endDate, cusCode=''):
        fd = FETCH_DATA_MERGE()
        dbList = fd.fetch_DB_HEAD(startDate, endDate, cusCode)
        return dbList
    
    
    @pyqtSlot()
    def __query_dbcode(self):
        dbCode = self.lineEdit_dbcode.text().strip()
        fd = FETCH_DATA_MERGE()
        dbList = fd.fetch_DB_HEAD_BY_CODE(dbCode)
        return dbList

    


    @pyqtSlot()
    def on_btn_print_label_clicked(self):
        
#        cols = ['dbCode', 'soCode', 'cusAbbName', 'hMemo']
        
        # 生成model
        resultModel = QtGui.QStandardItemModel()
        resultModel.setHorizontalHeaderLabels(['发货单号', '订单号', '客户简称', '备注'])
        
        model = self.tableModel
        
        
        colNameList = [tp[0] for tp in self.columnRef]
        
        for i in range(model.rowCount()):
            
            idx_dbCode = colNameList.index('dbCode')
            itm_dbCode = model.item(i, idx_dbCode)
            
            if itm_dbCode.checkState() == QtCore.Qt.Checked:
                # 复制item，给resultModel用
                idx_dbCode = colNameList.index('dbCode')
                idx_soCode = colNameList.index('soCode')
                idx_cusAbbName = colNameList.index('cusAbbName')
                idx_hMemo = colNameList.index('hMemo')
                
                itm_dbCode = model.item(i, idx_dbCode).clone()
                itm_soCode = model.item(i, idx_soCode).clone()
                itm_cusAbbName = model.item(i, idx_cusAbbName).clone()
                itm_hMemo = model.item(i, idx_hMemo).clone()
                
                resultModel.appendRow([itm_dbCode, itm_soCode, itm_cusAbbName, itm_hMemo])
        
        
        aa = Frm_Sales_LabelPrint(self)
        aa.setModelData(resultModel)
        aa.exec_()
        
        # 最后刷新列表，就能显示打印时间戳
        self.on_btn_query_clicked()




    @pyqtSlot()
    def on_btn_fhmxb_clicked(self):
        """
        按所选的发货单，生成Nitori发货明细表
        需要先选择发货单，再按此处
        提取nitori店名，订单号，
        按照店名排序
        再按照店名汇总
        所以最好提取数据重新生成，而不是clone model item
        """
        
        model = self.tableModel
        
        colNameList = [tp[0] for tp in self.columnRef]
        
        # 提取 备注 及 订单号数据
        fetchData = [] #准备放提取的数据
        
        for i in range(model.rowCount()):
            
            idx_dbCode = colNameList.index('dbCode')
            itm_dbCode = model.item(i, idx_dbCode)
            
            if itm_dbCode.checkState() == QtCore.Qt.Checked:
                # 复制item，给resultModel用
                idx_hMemo = colNameList.index('hMemo')
                idx_soCode = colNameList.index('soCode')
                
                lst = [model.item(i, idx_hMemo).text(), model.item(i, idx_soCode).text()]
                
                #取得数据（还未提取店名）
                fetchData.append(lst)
                
        
        aa = Frm_Sales_DB_NitoriDispatch(self)
        aa.setData1(fetchData)
        aa.exec_()
        

        

        
        



            
            
#宁波店 ['115557']
#武汉经开店 ['115546', '115548', '115549', '115550', '115576']
#上海中山公园店 ['115499', '115500', '115501', '115502', '115503', '115504', '115512', '115514', '115515', '115516', '115517', '115518', '115519', '115520', '115513', '115561', '115562']
#武汉群星城店 ['115481', '115482', '115483', '115484', '115485', '115577', '115578', '115579', '115586']
#武汉世纪都会店 ['115477', '115541', '115542']
#            for key in dct:
#                print(key, dct[key])







    
    
    @pyqtSlot()
    def on_btn_output_excel_clicked(self):
        fileFullName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + '发货单列表', 'Excel Files (*.xlsx)')
        if fileFullName:
            ew = ExcelWrite()
            ew.fromTableModel(fileFullName, self.tableModel)
            QtGui.QMessageBox.information(self, '提示', '输出完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    


class Frm_Sales_DB_Detail(QtGui.QWidget, Ui_Sales_DB_Detail):
     
    def __init__(self, parent=None):
        super(Frm_Sales_DB_Detail, self).__init__(parent)
        self.setupUi(self)
        
        # 读取列setting
        sr = SettingReader()
        self.columnRef = sr.load_DB()
        
        # 生成model
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef)
        self.tableView.setModel(self.tableModel)
        
        # 设置列宽
        for i, width in enumerate( [tp[2] for tp in self.columnRef] ):
            self.tableView.setColumnWidth(i, width)
        
        # 设置表头不高亮
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setHighlightSections(False)
        
        # 设置默认行高
        self.tableView.verticalHeader().setDefaultSectionSize(38)
    
    
    def setDB(self, db):
        # 传入这里的是标准db（已添加lastLabelPrint）
        dbData = db.data
        
        # 表头数据显示
        self.label_dbcode.setText(dbData['dbCode'])
        self.label_soabbname.setText(dbData['cusAbbName'])
        self.label_date.setText(dbData['dbDate'])
        self.label_socode.setText(dbData['soCode'])
        self.label_person.setText(dbData['personName'])
        self.label_koulv.setText(dbData['hKoulv'])
        self.label_memo.setText(dbData['hMemo'])
        self.label_maker.setText(dbData['maker'])
        self.label_verifier.setText(dbData['verifier'])
        self.label_scname.setText(dbData['scName'])
        
        # 表体数据显示（显示数据先按照columnRef顺序排列。这样就可以在setting里随意定义列，不导致出错）
        colsName = [ tp[0] for tp in self.columnRef ]
        dbData = SO_dataColumnArrange(dbData, colsName)
        
        tmc = TableModelCreater()
        self.tableModel = tmc.create(self.columnRef, dbData['table'])
        
        self.tableView.setModel(self.tableModel)
        



class Frm_Sales_DB_NitoriDispatch(QtGui.QDialog, Ui_Sales_DB_NitoriDispatch):
    
    def __init__(self, parent=None):
        super(Frm_Sales_DB_NitoriDispatch, self).__init__(parent)
        self.setupUi(self)
        
#        self.color_0 = QtGui.QColor(255, 255, 255)  #未选
#        self.color_1 = QtGui.QColor(0, 255, 255)  #选中
#        
        self.tableModel1 = QtGui.QStandardItemModel()
        self.tableModel1.setHorizontalHeaderLabels( ['备注', '订单号'] )
        
        self.tableModel2 = QtGui.QStandardItemModel()
        self.tableModel2.setHorizontalHeaderLabels( ['店名', '订单号'] )
        
        self.tableModel3 = QtGui.QStandardItemModel()
        self.tableModel3.setHorizontalHeaderLabels( ['店名', '订单号'] )
        
        
        # 设置表头不高亮
        self.tableView1.horizontalHeader().setHighlightSections(False)
        self.tableView1.verticalHeader().setHighlightSections(False)
        self.tableView2.horizontalHeader().setHighlightSections(False)
        self.tableView2.verticalHeader().setHighlightSections(False)
        self.tableView3.horizontalHeader().setHighlightSections(False)
        self.tableView3.verticalHeader().setHighlightSections(False)
        
        # 设置默认行高
        self.tableView1.verticalHeader().setDefaultSectionSize(24)
        self.tableView2.verticalHeader().setDefaultSectionSize(24)
        self.tableView3.verticalHeader().setDefaultSectionSize(24)
        
        # 设置可点击排序
#        self.tableView.setSortingEnabled(True)
        
        
    @pyqtSlot()
    def on_pushButton1_clicked(self):
        """
        收集tableview1的内容，
        提取店名
        整理后传递到setData2
        """
#        pdb.set_trace()
        model = self.tableModel1
        
#        colNameList = [tp[0] for tp in self.columnRef]
        
        # 提取 备注 及 订单号数据
        dataList = [] #准备放提取的数据
        
        for i in range(model.rowCount()):
            
            memo = model.item(i, 0).text()
            soCode = model.item(i, 1).text()
            
            # memo需要整理。1去除“加急单”，2收尾去除空格，3全角空格转半角（好像不需要？），另split()不加参数，会把多个空格都去除
            memo = memo.replace('加急单', '')
            memo = memo.strip()
#            memo = memo.replace(' ', ' ')
            shopName = memo.split()[1]
            
            dataList.append( [shopName, soCode] )
        
#        dataList [['武汉经开店', '115576'], ['武汉群星城店', '115481'], ['武汉群星城店', '115482'], ['武汉群星城店', '115483'], ['武汉群星城店', '115484'], ['武汉群星城店', '115485'], ['武汉群星城店', '115577'], ['武汉群星城店', '115578'], ['武汉群星城店', '115579'], ['武汉群星城店', '115586'], ['武汉金银潭店', '115479'], ['武汉金银潭店', '115480'], ['武汉金银潭店', '115551'], ['武汉金银潭店', '115552'], ['武汉金银潭店', '115580'], ['武汉金银潭店', '115581'], ['武汉金银潭店', '115582'], ['苏州园区店', '115476'], ['苏州园区店', '115553'], ['苏州园区店', '115594'], ['苏州高新店', '115554'], ['苏州高新店', '115555'], ['苏州高新店', '115583']]

       # 设置tableView2
        self.setData2(dataList)
        
        #激活tab2
        self.tabWidget.setCurrentIndex(1)


    @pyqtSlot()
    def on_pushButton2_clicked(self):
        """
        收集tableview2的内容，
        按店名排序
        按店名归类出订单号
        整理后传递到setData3
        """
        model = self.tableModel2
        
        # 提取数据
        dataList = [] #准备放提取的数据
        
        for i in range(model.rowCount()):
            
            shopName = model.item(i, 0).text()
            soCode = model.item(i, 1).text()
            
            dataList.append( [shopName, soCode] )
        
        # 按店名排序
        # sorted(list)返回一个对象，可以用作表达式
        # list.sort() 不会返回对象，改变原有的list
#        fetchData = sorted(fetchData, key=lambda x: x[0])
        dataList.sort(key=lambda x: x[0])
        
        # 按照店名归类
        dataDct = {}
        for li in dataList:
            shopName = li[0]
            if shopName not in dataDct:
                dataDct[shopName] = [li[1], ]
            else:
                dataDct[shopName].append(li[1])
        
        # 转为list
        tmpList = []
        for key in dataDct:
            shopName = key
            soCodes = ' '.join(dataDct[key])
            tmpList.append( [shopName, soCodes] )
        
        # 再按店名排序
        tmpList.sort(key=lambda x: x[0])
        
        
       # 设置tableView3
        self.setData3(tmpList)
        
#        #激活tab3
        self.tabWidget.setCurrentIndex(2)


    @pyqtSlot()
    def on_pushButton3_clicked(self):
        """
        收集tableview3的内容，
        输出到excel
        """
        model = self.tableModel3
        
        # 提取数据
        dataList = []
        for i in range(model.rowCount()):
            shopName = model.item(i, 0).text()
            soCodes = model.item(i, 1).text()
            dataList.append( (shopName, soCodes) )
        
        # 生成xlsx文件
#        sourceFileName = self.lineEdit.text()
#        place = sourceFileName.find('Hard_TOSO_') + 10
#        saveName = sourceFileName[place:place+8]
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save As', '.\\' + '' + 'Nitori发货明细表', 'Excel Files (*.xlsx)')
        
        if fileName != '':
            # 需要替换，否则保存出错
            fileName = fileName.replace('/', '\\') 
            
            xlh = ExcelHandle()
            
            xlh.createExcelApp()
            
            xlh.createNitoriDispatch(dataList)
            
            xlh.excelBookSaveAs(fileName)
            
            xlh.closeExcelBook()
            xlh.quitExcelApp()
            QtGui.QMessageBox.information(self, '提示', '完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        
        
        
        
        
        
        
        


    
    def setData1(self, dataList:list):
        
        model = self.tableModel1
        
        if dataList:
            # 纯data设置到userrole（目的是以后可以按照userrole排序）
            for i, tp in enumerate(dataList):
                for j in range(len(tp)):
                    itm = QtGui.QStandardItem()
                    # 注意：需要把None全部转为空串，否则None是不参与排序的。但是0.0不能变）
                    value =   tp[j] if tp[j] is not None else ''
#                    itm.setData(value, QtCore.Qt.UserRole)
                    itm.setData(value, QtCore.Qt.DisplayRole)   # 同样设置displayrole
                    model.setItem(i, j, itm)
        
        self.tableView1.setModel(self.tableModel1)
        
        head_width = [300, 120]
        for i, width in enumerate(head_width):
            self.tableView1.setColumnWidth(i, width)
    
        # 第一列勾选事件
#        self.tableModel.dataChanged.connect(self.__check_changed)



    def setData2(self, dataList:list):
        
        model = self.tableModel2
        
        if dataList:
            # 纯data设置到userrole（目的是以后可以按照userrole排序）
            for i, tp in enumerate(dataList):
                for j in range(len(tp)):
                    itm = QtGui.QStandardItem()
                    # 注意：需要把None全部转为空串，否则None是不参与排序的。但是0.0不能变）
                    value =   tp[j] if tp[j] is not None else ''
#                    itm.setData(value, QtCore.Qt.UserRole)
                    itm.setData(value, QtCore.Qt.DisplayRole)   # 同样设置displayrole
                    model.setItem(i, j, itm)
        
        self.tableView2.setModel(self.tableModel2)
        
        head_width = [300, 120]
        for i, width in enumerate(head_width):
            self.tableView2.setColumnWidth(i, width)



    def setData3(self, dataList:list):
        
        model = self.tableModel3
        
        if dataList:
            for i, tp in enumerate(dataList):
                for j in range(len(tp)):
                    itm = QtGui.QStandardItem()
                    value = tp[j] if tp[j] is not None else ''
                    itm.setData(value, QtCore.Qt.DisplayRole)
                    model.setItem(i, j, itm)
        
        self.tableView3.setModel(self.tableModel3)
        
        head_width = [200, 700]
        for i, width in enumerate(head_width):
            self.tableView3.setColumnWidth(i, width)













class Frm_Sales_LabelPrint(QtGui.QDialog, Ui_Sales_LabelPrint):
    
    def __init__(self, parent=None):
        super(Frm_Sales_LabelPrint, self).__init__(parent)
        self.setupUi(self)
        
        self.color_0 = QtGui.QColor(255, 255, 255)  #未选
        self.color_1 = QtGui.QColor(0, 255, 255)  #选中
        
        self.tableModel = None
        
        # 设置表头不高亮
        self.tableView.horizontalHeader().setHighlightSections(False)
        self.tableView.verticalHeader().setHighlightSections(False)
        
        # 设置默认行高
        self.tableView.verticalHeader().setDefaultSectionSize(24)
        
        # 设置可点击排序
        self.tableView.setSortingEnabled(True)
        
    
    def setModelData(self, model):
        
        self.tableModel = model
        
        self.tableView.setModel(model)
        
        head_width = [120, 90, 120, 450]
        for i, width in enumerate(head_width):
            self.tableView.setColumnWidth(i, width)
    
        # 第一列勾选事件
        self.tableModel.dataChanged.connect(self.__check_changed)
    
    
    @pyqtSlot(QtCore.QModelIndex)
    def __check_changed(self, idx):
        # 只针对第一列，勾选变化
        self.tableModel.dataChanged.disconnect(self.__check_changed)
        
        if idx.column() == 0:
            row = idx.row()
            columnCount = self.tableModel.columnCount()
            # cellwidget的格子，item()会返回None
            if self.tableModel.item(row, 0).data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Unchecked:
                for i in range(columnCount):
                    self.tableModel.item(row, i).setData(QtGui.QBrush(self.color_0), QtCore.Qt.BackgroundRole)
            else:
                for i in range(columnCount):
                    self.tableModel.item(row, i).setData(QtGui.QBrush(self.color_1), QtCore.Qt.BackgroundRole)
            
        self.tableModel.dataChanged.connect(self.__check_changed)
        
        self.tableView.setModel(self.tableModel)
    
    
    def __getPrintDataList(self):
        # 从表格中取数，构建列表
        lst = []
        rowCount = self.tableModel.rowCount()
        
        for i in range(rowCount):
            printData = {}
            if self.tableModel.item(i, 0).checkState() == QtCore.Qt.Checked:
                printData['soCode'] = self.tableModel.item(i, 1).data(QtCore.Qt.DisplayRole)
                printData['cusAbbName'] = self.tableModel.item(i, 2).data(QtCore.Qt.DisplayRole)
                printData['hMemo'] = self.tableModel.item(i, 3).data(QtCore.Qt.DisplayRole)
                lst.append(printData)
        return lst
    
    
    def __getPrintDBCodeList(self):
        # 从表格中取数，构建列表
        lst = []
        rowCount = self.tableModel.rowCount()
        
        for i in range(rowCount):
            if self.tableModel.item(i, 0).checkState() == QtCore.Qt.Checked:
                DBCode = self.tableModel.item(i, 0).data(QtCore.Qt.DisplayRole)
                lst.append(DBCode)
        return lst
        
    
    @pyqtSlot()
    def on_btn_print_clicked(self):
        
        tptDir = os.path.split(os.path.realpath(__file__))[0] + '\\template\\'
        
        # 读入打印模板 tptList
        fullName = tptDir + 'label.xml'
        tpt = Template()
        tpt.loadTemplate(fullName)
        tptList = [tpt,]
        
        # 取得 printData
        printDataList = self.__getPrintDataList()
        
        # 指定打印机（如果template内有指定，用指定的。无指定就用系统默认的）
        printerName = tpt.template['Canvas'][4]
        # 先把打印机设置为默认打印机
        printer = QtGui.QPrinter(QtGui.QPrinterInfo().defaultPrinter())
        # 如果有指定打印机名称，系统内找找看，找到则切换，找不到跳过呗
        if printerName:
            for prtInfo in QtGui.QPrinterInfo().availablePrinters():
                if printerName == prtInfo.printerName():
                    printer = QtGui.QPrinter(prtInfo)
                    break
        
        # 打印（每条数据套用各个template）
        for printData in printDataList:
            
            for tpt in tptList:
                
                w, h, offsetX, offsetY, printerName, landscape = tpt.template['Canvas']
                
                # 设置纸张。在数据库里总归是按照竖向存放的  纸张设置不能放入goprint，会跳错误
                printer.setPaperSize(QtCore.QSizeF(w, h), printer.DevicePixel)
                # 设置纸张方向
                if landscape == 1:
                    printer.setOrientation(printer.Landscape)
                # 设置纸张边距
#                printer.setPageMargins(0.0, 0.0, 0.0, 0.0, printer.Millimeter)
                printer.setPageMargins(offsetX, offsetY, 0.0, 0.0, printer.DevicePixel)
                # 设置源数据
                tpt.setPrintData(printData)
                # 打印
                print('打印：{0} ({1})'.format(printData['soCode'], tpt.template['ReportName']))
                tpt.render(printer)
        
        # 保存打印记录
        dblist = self.__getPrintDBCodeList()
        
        mh = MysqlHandle()
        mh.connect()
        mh.SO_Printlog_save_label(dblist)
        mh.disconnect()
        
        print('Completed!')
        QtGui.QMessageBox.information(self, '提示', '打印完成', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        
        
        
class PrintSoClass:
    
    def __init__(self):
        self.tptDir = os.path.split(os.path.realpath(__file__))[0] + '\\template\\'
    
        
    def printSOs(self, soCodeList: list, tptShortName: list, printlog=True, actualPrint=True):
        
        tptList = []
        soList = []
        
        # 读入打印模板 tptList
        for tptName in tptShortName:
            fullName = self.tptDir + tptName
            tpt = Template()
            tpt.loadTemplate(fullName)
            tptList.append(tpt)
        
        # 查询取得 printData （已经添加截断信息）
        fd = FETCH_DATA_MERGE()
        soList = fd.fetch_SOs(soCodeList)
        
        # 每条数据打印各个template，此处必须按照这个顺序，整理单子方便
        for so in soList:
            
            soData = so.data
            
            for tpt in tptList:
                w, h, offsetX, offsetY, printerName, landscape = tpt.template['Canvas']
                # 先指定为默认打印机
                prt = QtGui.QPrinter(QtGui.QPrinterInfo().defaultPrinter())
                # 查找是否有指定打印机  如果有指定打印机名称，系统内找找看，找到则切换，找不到跳过
                if printerName:
                    for prtInfo in QtGui.QPrinterInfo().availablePrinters():
                        if printerName == prtInfo.printerName():
                            prt = QtGui.QPrinter(prtInfo)
                            break
                
                # 设置纸张。在数据库里总归是按照竖向存放的
                # 纸张设置不能放入goprint，会跳错误
                prt.setPaperSize(QtCore.QSizeF(w, h), prt.DevicePixel)
                
                # 设置纸张方向
                if landscape == 1:
                    prt.setOrientation(prt.Landscape)
                # 设置纸张边距  QPrinter.setPageMargins (self, float left, float top, float right, float bottom, Unit unit)
                prt.setPageMargins(offsetX, offsetY, 0.0, 0.0, prt.DevicePixel)
                # 设置源数据（setPrintData已包含改变数据形状）
                tpt.setPrintData(soData)
                # 打印（考虑控制参数actualPrint）
                print('打印：{0}\t模板：{1}\tPrinter:{2}'.format(soData['soCode'], tpt.template['ReportName'], prt.printerName()))
                if actualPrint:
                    tpt.render(prt)
        
        # 本地数据库，加上打印时间（考虑控制参数printlog）
        if printlog:
            mh = MysqlHandle()
            mh.connect()
            mh.SO_Printlog_save(soCodeList)
            mh.disconnect()
        
        print('Completed!')
        



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
    
    def excelBookSaveAs(self, fileName):
        self.xlsBook.SaveAs(fileName)
        print("文件另存为: %s" % fileName)
    
    def createNitoriDispatch(self, dataList):
        """
        生成Nitori发货明细表
        按照店名归类，写出此店所有的发货订单号
        """
        # 填充excel
        xlsBook = self.openExcelBook(os.path.split(os.path.realpath(__file__))[0] + "\\Nitori\\nitori_dispatch.xlsx")
        
        for i, tp in enumerate(dataList):
            # (xxxx店,  '111111 222222 333333')
            shopName, soCodes = tp
            
            # 填充数据（start_row=2, start_col=1） A2单元格
            xlsBook.ActiveSheet.Cells(i+2, 1).Value = shopName
            xlsBook.ActiveSheet.Cells(i+2, 2).Value = "'" + soCodes  #如果只有1个单号，会当成数字处理，所以打撇号
            



class ExcelWrite:
    
    def fromTableModel(self, fileFullName, model):
#        直接从tableView导出数据到xlsx   QStandardItemModel
        
        # 取得tableView数据
        tableHead = []
        tableBody = []
        rows = model.rowCount()-1 # 最后有合计行，暂时先不读
        cols = model.columnCount()
        
        # 取得表头
        for i in range(cols):
            headItem = model.horizontalHeaderItem(i)
            tableHead.append(headItem.text())
        
        # 取得表体
        for i in range(rows):
            tp = ()
            for j in range(cols):
                itm = model.item(i, j)
                value = itm.data(QtCore.Qt.UserRole)
                tp += (value,)
            tableBody.append(tp)
        
        # 生成xlsx
        book = xlsxwriter.Workbook(fileFullName) # 建立文件
        sheet = book.add_worksheet('Sheet1') # 建立sheet， 可以work.add_worksheet('employee')来指定sheet名，但中文名会报UnicodeDecodeErro的错误
        
        num_format = book.add_format()
        num_format.set_num_format('_ * #,##0.00_ ;_ * -#,##0.00_ ;_ * "-"??_ ;_ @_ ') 
        
        # 写入表头
        for i, value in enumerate(tableHead):
            sheet.write(0, i, value)
        
        # 写入表体
        for i, tp in enumerate(tableBody):
            for j in range(cols):
                sheet.write(i+1, j, tp[j]) # 首行是标题，从第二行开始
        
        book.close()

    