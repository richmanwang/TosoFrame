# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:25:48 2017

@author: 008
"""

from PyQt4 import QtGui
from PyQt4 import QtCore


class MyFileView(QtGui.QTableView):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        head_str = ['文件名', '状态', '行数', '单据总金额', '明细总金额']
        head_width = [600, 50, 50, 90, 90]
        
        self.tableModel = QtGui.QStandardItemModel()
        
        self.tableModel.setHorizontalHeaderLabels(head_str)
        self.setModel(self.tableModel)
        
        for i, width in enumerate(head_width):
            self.setColumnWidth(i, width)
        
        # 设置默认行高
        self.verticalHeader().setDefaultSectionSize(26)
    
    
    def dragEnterEvent(self, event):
        # Sets the drop action to be the proposed action.  QDropEvent  dragMoveEvent inherited by QDropEvent
        event.acceptProposedAction()      
    
    
    def dragMoveEvent(self, event):
        event.acceptProposedAction()
    
    
    def dropEvent(self, event):
        
        mimeData = event.mimeData()
        
        lst = []
        
        if mimeData.hasUrls():
            for url in mimeData.urls():
                fileName = url.toLocalFile()
                lst.append(fileName)
        
        # 显示全部文件
        self.tableModel.setRowCount(0)
        
        for i, fileName in enumerate(lst):
            # 先把纯data设置到displayrole
            itm = QtGui.QStandardItem()
            itm.setData(fileName, QtCore.Qt.DisplayRole)
            self.tableModel.setItem(i, 0, itm)
            
            itm = QtGui.QStandardItem()
            itm.setData('未处理', QtCore.Qt.DisplayRole)
            self.tableModel.setItem(i, 1, itm)
            
            itm = QtGui.QStandardItem()
            itm.setData('?', QtCore.Qt.DisplayRole)
            self.tableModel.setItem(i, 2, itm)
            
            itm = QtGui.QStandardItem()
            itm.setData('?', QtCore.Qt.DisplayRole)
            self.tableModel.setItem(i, 3, itm)
            
            itm = QtGui.QStandardItem()
            itm.setData('?', QtCore.Qt.DisplayRole)
            self.tableModel.setItem(i, 4, itm)
