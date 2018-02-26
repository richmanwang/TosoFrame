# -*- coding: utf-8 -*-

import calendar
import datetime
import os
import copy
import math
import xml.etree.cElementTree as ET
#import mysql.connector
import pymysql

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtSql
from PyQt4.QtCore import pyqtSlot

import pdb


class LoadServerDataClass_PYQT_ODBC:
    
    def __init__(self):
        self.dsn = "DRIVER={SQL SERVER}; SERVER=tososh; DATABASE=UFDATA_001_2014"
        self.username = 'sa'
        self.password = '1qaz@WSX'
        
        
        
    def add_conn(self):
        # The QSqlDatabase class represents a connection to a database
        U8_db = QtSql.QSqlDatabase.addDatabase("QODBC", "MY_DB")

        # 要注意的就是连接数据库时使用的数据库名，和sqlite等是不同的，并不是直接写入数据库名称，而是DSN名。
        # 如果已设置好了DSN，可以直接输入DSN名。 如果没有，可以采用DSN连接字符串直接连接ODBC数据库。
        # add过后，不需要self保留，其他函数中用 QtSql.QSqlDatabase.database("MY_DB") 取回后打开，就可使用

        # QSqlDatabase QSqlDatabase.database (QString connectionName = '', bool open = True)
        # If open is true (the default) and the database connection is not already open it is opened now.


        U8_db.setDatabaseName(self.dsn)
        U8_db.setUserName(self.username)
        U8_db.setPassword(self.password)
        
    
    def remove_conn(self):
        QtSql.QSqlDatabase.removeDatabase('MY_DB')
    
    
    
    def fetch_Customer(self, filter_keyword=''):
        # 取得客户列表
        # [('1001', '杭州大洋'), ... ]
        # 可以用filter_keyword筛选出包含的客户简称
        
        sqlstr = """
                SELECT
                    cCusCode,
                    cCusAbbName
                FROM
                    Customer
                ORDER BY
                    cCusCode ASC
                """
        
        # 默认同时开启
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.exec_()
        
        result_list = []
        while query.next():
            # tuple重置
            tp = ()
            record = query.record()
            for i in range( record.count() ):
                value = record.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
                
            result_list.append(tp)
        # 关闭连接
        U8_db.close()
        
#         从列表中筛选出指定客户
        if filter_keyword != '':
            result_list = [ tp for tp in result_list if filter_keyword in tp[1] ]
        return result_list
    
    
    def fetch_SO_HEAD_PURE(self, dateStrStart, dateStrEnd, cusCode):
        # connectionName: MY_DB
        # The database connection is referred to by connectionName (MY_DB).
        # The newly added database connection is returned.
#        sqlstr = """
#                SELECT
#                    SO_SOMain.cSOCode,
#                    SO_SOMain.cCusCode,
#                    Customer.cCusAbbName,
#                    SO_SOMain.cDefine1,
#                    Sum(SO_SODetails.iMoney),
#                    Sum(SO_SODetails.iTax),
#                    Sum(SO_SODetails.iSum),
#                    SO_SOMain.cMemo,
#                    CONVERT(varchar(10), SO_SOMain.dDate, 23),
#                    CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
#                    ShippingChoice.cSCName,
#                    SO_SOMain.cMaker,
#                    SO_SOMain.cVerifier
#                FROM
#                    SO_SODetails
#                INNER JOIN SO_SOMain ON SO_SODetails.cSOCode = SO_SOMain.cSOCode
#                INNER JOIN Customer ON SO_SOMain.cCusCode = Customer.cCusCode
#                LEFT JOIN ShippingChoice ON SO_SOMain.cSCCode = ShippingChoice.cSCCode
#                WHERE
#                    SO_SOMain.dDate BETWEEN ? AND ?
#                GROUP BY
#                    SO_SOMain.cSOCode,
#                    SO_SOMain.cCusCode,
#                    Customer.cCusAbbName,
#                    SO_SOMain.cDefine1,
#                    SO_SOMain.cMemo,
#                    CONVERT(varchar(10), SO_SOMain.dDate, 23),
#                    CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
#                    ShippingChoice.cSCName,
#                    SO_SOMain.cMaker,
#                    SO_SOMain.cVerifier
#                """
        
        # 生成sql语句
        
        # 基础语句
        sqlstr_base = """
                SELECT
                    SO_SOMain.cSOCode,
                    SO_SOMain.cCusCode,
                    Customer.cCusAbbName,
                    SO_SOMain.cDefine1,
                    Sum(SO_SODetails.iMoney),
                    Sum(SO_SODetails.iTax),
                    Sum(SO_SODetails.iSum),
                    SO_SOMain.cMemo,
                    CONVERT(varchar(10), SO_SOMain.dDate, 23),
                    CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
                    ShippingChoice.cSCName,
                    SO_SOMain.cMaker,
                    SO_SOMain.cVerifier
                FROM
                    SO_SODetails
                INNER JOIN SO_SOMain ON SO_SODetails.cSOCode = SO_SOMain.cSOCode
                INNER JOIN Customer ON SO_SOMain.cCusCode = Customer.cCusCode
                LEFT JOIN ShippingChoice ON SO_SOMain.cSCCode = ShippingChoice.cSCCode"""
        
        # where语句，需要判断cusCode是否加入
        sqlstr_where = """
                WHERE
                    (SO_SOMain.dDate BETWEEN ? AND ?)"""
        if cusCode:
            sqlstr_where += " AND SO_SOMain.cCusCode = '{}'".format(cusCode)
        
        # group语句
        sqlstr_group="""
                GROUP BY
                    SO_SOMain.cSOCode,
                    SO_SOMain.cCusCode,
                    Customer.cCusAbbName,
                    SO_SOMain.cDefine1,
                    SO_SOMain.cMemo,
                    CONVERT(varchar(10), SO_SOMain.dDate, 23),
                    CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
                    ShippingChoice.cSCName,
                    SO_SOMain.cMaker,
                    SO_SOMain.cVerifier
        """
        
        # 拼接
        sqlstr = sqlstr_base + sqlstr_where + sqlstr_group
        
#        print(sqlstr)
        
        
        # 这样就默认打开连接了
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, dateStrStart)
        query.bindValue(1, dateStrEnd)
        query.exec_()
        
        # 转换，tuple组成的list
        result_list = []
        
        # 这里取得所有日期内的订单头（不指定客户）
        while query.next():
            # tuple重置
            tp = ()
            record = query.record()
            for i in range( record.count() ):
                value = record.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            result_list.append(tp)
        
        # 关闭连接
        U8_db.close()
        
        return result_list
    
    
    def fetch_SO_HEAD_BY_CODE_PURE(self, soCode):
        sqlstr = """
                SELECT
                    SO_SOMain.cSOCode,
                    SO_SOMain.cCusCode,
                    Customer.cCusAbbName,
                    SO_SOMain.cDefine1,
                    Sum(SO_SODetails.iMoney),
                    Sum(SO_SODetails.iTax),
                    Sum(SO_SODetails.iSum),
                    SO_SOMain.cMemo,
                    CONVERT(varchar(10), SO_SOMain.dDate, 23),
                    CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
                    ShippingChoice.cSCName,
                    SO_SOMain.cMaker,
                    SO_SOMain.cVerifier
                FROM
                    SO_SODetails
                INNER JOIN SO_SOMain ON SO_SODetails.cSOCode = SO_SOMain.cSOCode
                INNER JOIN Customer ON SO_SOMain.cCusCode = Customer.cCusCode
                LEFT JOIN ShippingChoice ON SO_SOMain.cSCCode = ShippingChoice.cSCCode
                WHERE
                    SO_SOMain.cSOCode=?
                GROUP BY
                    SO_SOMain.cSOCode,
                    SO_SOMain.cCusCode,
                    Customer.cCusAbbName,
                    SO_SOMain.cDefine1,
                    SO_SOMain.cMemo,
                    CONVERT(varchar(10), SO_SOMain.dDate, 23),
                    CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
                    ShippingChoice.cSCName,
                    SO_SOMain.cMaker,
                    SO_SOMain.cVerifier
                """
        
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, soCode)
        query.exec_()
        
        # 转换，tuple组成的list
        result_list = []
        while query.next():
            # tuple重置
            tp = ()
            record = query.record()
            for i in range(record.count()):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            
            result_list.append(tp)
        
        U8_db.close()
        return result_list


    def fetch_SOs_PURE(self, soCodeList):
        # 如果输入不是一个列表（比如是单个code），则转为列表
        if type(soCodeList) is not list:
            soCodeList = [soCodeList, ]
        
        # 返回一个列表，里面都是字典
        resultList = []
        
        # 表头读取sql（最多返回1行）
        head_sqlstr = """
            SELECT
                SO_SOMain.cSOCode,
                SO_SOMain.cCusCode,
                Customer.cCusAbbName,
                CONVERT(varchar(10), SO_SOMain.dDate, 23),
                SO_SOMain.cDefine1,
                Person.cPersonName,
                CONVERT(varchar(10), SO_SOMain.dPreDateBT, 23),
                SO_SOMain.cDefine2,
                SO_SOMain.cMemo,
                SO_SOMain.cSCCode,
                ShippingChoice.cSCName,
                SO_SOMain.cMaker,
                SO_SOMain.cVerifier
            FROM
                SO_SOMain
            INNER JOIN Customer ON SO_SOMain.cCusCode = Customer.cCusCode
            INNER JOIN Person ON SO_SOMain.cPersonCode = Person.cPersonCode
            LEFT JOIN ShippingChoice ON SO_SOMain.cSCCode = ShippingChoice.cSCCode
            WHERE
                SO_SOMain.cSOCode=?
        """
        
        # 表体读取sql（会返回若干行，cInvName一定要从Inventory表取得，否则订单生成后如果改名，将不显示变化）
        table_sqlstr = """
            SELECT
                SO_SODetails.cDefine34 AS "行号",
                SO_SODetails.cInvCode,
                Inventory.cInvName,
                InventoryClass.cInvCName,
                SO_SODetails.cDefine25 AS "颜色规格型号",
                SO_SODetails.cDefine22 AS "宽",
                SO_SODetails.cDefine23 AS "高",
                SO_SODetails.cDefine24 AS "定价",
                SO_SODetails.cDefine28 AS "扣率",
                SO_SODetails.iTaxUnitPrice AS "含税单价",
                SO_SODetails.iQuantity,
                ComputationUnit.cComUnitName,
                SO_SODetails.iMoney,
                SO_SODetails.iTax,
                SO_SODetails.iSum,
                SO_SODetails.cDefine29 AS "生产要求",
                SO_SODetails.cDefine30
            FROM
                SO_SODetails
            INNER JOIN SO_SOMain ON SO_SOMain.cSOCode = SO_SODetails.cSOCode
            INNER JOIN Inventory ON SO_SODetails.cInvCode = Inventory.cInvCode
            INNER JOIN InventoryClass ON Inventory.cInvCCode = InventoryClass.cInvCCode
            INNER JOIN ComputationUnit ON Inventory.cComUnitCode = ComputationUnit.cComUnitCode
            WHERE
                SO_SODetails.cSOCode=?
            ORDER BY
                SO_SODetails.cDefine34 ASC
        """
        # 数据库连接
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        # 循环开始
        for soCode in soCodeList:
            so = SO()
            
            # 读取表头
            query = QtSql.QSqlQuery(U8_db)
            query.setForwardOnly(True)
            query.prepare(head_sqlstr)
            query.bindValue(0, soCode)
            query.exec_()
            
            if query.next():
                # 生成dict
                so.data['soCode'] = query.value(0)
                so.data['cusCode'] = query.value(1)
                so.data['cusAbbName'] = query.value(2)
                so.data['soDate'] = query.value(3)
                so.data['po'] = query.value(4)
                so.data['personName'] = query.value(5)
                so.data['preDate'] = query.value(6)
                so.data['hKoulv'] = query.value(7)
                so.data['hMemo'] = query.value(8)
                so.data['scCode'] = query.value(9)
                so.data['scName'] = query.value(10)
                so.data['maker'] = query.value(11)
                so.data['verifier'] = query.value(12)
                
            # 替换掉QPyNullVariant
            for key in so.data:
                if isinstance(so.data[key], QtCore.QPyNullVariant):
                    so.data[key] = None
            # 以上表头完成
            
            # 读取表体
            query = QtSql.QSqlQuery(U8_db)
            query.setForwardOnly(True)
            query.prepare(table_sqlstr)
            query.bindValue(0, soCode)
            query.exec_()
            
            # 转换，tuple组成的list
            table = []
            
            while query.next():
                record = query.record()
                # list重置
                lst = []
                
                for i in range(record.count()):
                    lst.append(record.value(i))
                
                # 替换掉QPyNullVariant
                lst = [None if isinstance(itm, QtCore.QPyNullVariant)==True else itm for itm in lst]
                # 转回tuple
                tp = tuple(lst)
                # 添加进list
                table.append(tp)
            # table完成
            so.data['table'] = table
            so.data['tableColumn'] = ['rowNO', 'invCode', 'invName', 'cata', 'ggxh', 'kuan', 'gao', 'dingjia', 'koulv', 'hsdj', 'quantity', 'unitName', 'iMoney', 'iTax', 'iSum', 'scyq', 'memo']
            # 加入列表
            resultList.append(so)
        # 数据库关闭
        U8_db.close()
        
        return resultList


    def fetch_DB_HEAD_PURE(self, dateStrStart, dateStrEnd, cusCode):
        # connectionName: MY_DB
        # The database connection is referred to by connectionName (MY_DB).
        # The newly added database connection is returned.
        sqlstr = """
                SELECT
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    Sum(DispatchLists.iMoney),
                    Sum(DispatchLists.iTax),
                    Sum(DispatchLists.iSum),
                    DispatchList.cMemo,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                FROM
                    DispatchLists
                INNER JOIN DispatchList ON DispatchList.DLID = DispatchLists.DLID
                INNER JOIN Customer ON DispatchList.cCusCode = Customer.cCusCode
                LEFT JOIN ShippingChoice ON DispatchList.cSCCode = ShippingChoice.cSCCode
                WHERE
                    DispatchList.dDate BETWEEN ? AND ?
                GROUP BY
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    DispatchList.cMemo,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                """
        
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, dateStrStart)
        query.bindValue(1, dateStrEnd)
        query.exec_()
        
        # 转换，tuple组成的list
        lst = []
        
        # 生成列表（所有客户）
        while query.next():
            # tuple重置
            tp = ()
            record = query.record()
            for i in range( record.count() ):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            
            lst.append(tp)
            
        # 关闭连接
        U8_db.close()
        
        # 从列表中筛选出指定客户
        if cusCode:
            lst = [tp for tp in lst if tp[1] == cusCode]
        return lst
    
    
    def fetch_DB_HEAD_BY_CODE_PURE(self, dbCode):
        sqlstr = """
                SELECT
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    Sum(DispatchLists.iMoney),
                    Sum(DispatchLists.iTax),
                    Sum(DispatchLists.iSum),
                    DispatchList.cMemo,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                FROM
                    DispatchLists
                INNER JOIN DispatchList ON DispatchList.DLID = DispatchLists.DLID
                INNER JOIN Customer ON DispatchList.cCusCode = Customer.cCusCode
                LEFT JOIN ShippingChoice ON DispatchList.cSCCode = ShippingChoice.cSCCode
                WHERE
                    DispatchList.cDLCode=?
                GROUP BY
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    DispatchList.cMemo,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                """
    
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, dbCode)
        query.exec_()
        
        # 转换，tuple组成的list
        result_list = []
        
        while query.next():
            # tuple重置
            tp = ()
            record = query.record()
            for i in range(record.count()):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            
            result_list.append(tp)
        
        U8_db.close()
        
        return result_list


    def fetch_DB_HEAD_BY_SO_PURE(self, soCode):
        # 销售订单下查发货单使用
        sqlstr = """
                SELECT
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    Sum(DispatchLists.iMoney),
                    Sum(DispatchLists.iTax),
                    Sum(DispatchLists.iSum),
                    DispatchList.cMemo,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                FROM
                    DispatchLists
                INNER JOIN DispatchList ON DispatchList.DLID = DispatchLists.DLID
                INNER JOIN Customer ON DispatchList.cCusCode = Customer.cCusCode
                LEFT JOIN ShippingChoice ON DispatchList.cSCCode = ShippingChoice.cSCCode
                WHERE
                    DispatchList.cSOCode=?
                GROUP BY
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    DispatchList.cMemo,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                """
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, soCode)
        query.exec_()
        
        # 转换，tuple组成的list
        result_list = []
        
        while query.next():
            tp = ()  # tuple重置
            record = query.record()
            for i in range(record.count()):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            
            result_list.append(tp)
        
        U8_db.close()
        return result_list



    def fetch_DBs_PURE(self, dbCodeList):
        # 如果输入不是一个列表（比如是单个code），则转为列表
        if type(dbCodeList) is not list:
            dbCodeList = [dbCodeList, ]
        
        # 返回一个列表
        resultList = []
        
        # 表头读取sql（最多返回1行）
        # cDefine2  扣率
        head_sqlstr = """
                SELECT
                    DispatchList.cDLCode,
                    DispatchList.cCusCode,
                    Customer.cCusAbbName,
                    CONVERT(varchar(10), DispatchList.dDate, 23),
                    DispatchList.cSOCode,
                    Person.cPersonName,
                    DispatchList.cDefine2,
                    DispatchList.cMemo,
                    DispatchList.cSCCode,
                    ShippingChoice.cSCName,
                    DispatchList.cMaker,
                    DispatchList.cVerifier
                FROM
                    DispatchList
                INNER JOIN Customer ON DispatchList.cCusCode = Customer.cCusCode
                INNER JOIN Person ON DispatchList.cPersonCode = Person.cPersonCode
                LEFT JOIN ShippingChoice ON DispatchList.cSCCode = ShippingChoice.cSCCode
                WHERE
                    DispatchList.cDLCode=?
        """
        # 表体
        table_sqlstr = """
            SELECT
                DispatchLists.cDefine34 AS "行号",
                DispatchLists.cInvCode,
                Inventory.cInvName,
                InventoryClass.cInvCName,
                DispatchLists.cDefine25 AS "颜色规格型号",
                DispatchLists.cDefine22 AS "宽",
                DispatchLists.cDefine23 AS "高",
                DispatchLists.cDefine24 AS "定价",
                DispatchLists.cDefine28 AS "扣率",
                DispatchLists.iTaxUnitPrice AS "含税单价",
                DispatchLists.iQuantity,
                ComputationUnit.cComUnitName,
                DispatchLists.iMoney,
                DispatchLists.iTax,
                DispatchLists.iSum,
                DispatchLists.cDefine29 AS "生产要求",
                DispatchLists.cDefine30
            FROM
                DispatchLists
            INNER JOIN DispatchList ON DispatchList.DLID = DispatchLists.DLID
            INNER JOIN Inventory ON DispatchLists.cInvCode = Inventory.cInvCode
            INNER JOIN InventoryClass ON Inventory.cInvCCode = InventoryClass.cInvCCode
            INNER JOIN ComputationUnit ON Inventory.cComUnitCode = ComputationUnit.cComUnitCode
            WHERE
                DispatchList.cDLCode=?
            ORDER BY
                DispatchLists.cDefine34 ASC
        """
        # 数据库连接
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
#        U8_db.open()
        
        # 循环开始
        for dbCode in dbCodeList:
            db = DB()
            
            # 读取表头
            query = QtSql.QSqlQuery(U8_db)
            query.setForwardOnly(True)
            query.prepare(head_sqlstr)
            query.bindValue(0, dbCode)
            query.exec_()
            
            if query.next():
                #取一条记录  QVariant QSqlRecord.value (self, int i)
                record = query.record()
                # 生成dict
                db.data['dbCode'] = record.value(0)
                db.data['cusCode'] = record.value(1)
                db.data['cusAbbName'] = record.value(2)
                db.data['dbDate'] = record.value(3)
                db.data['soCode'] = record.value(4)
                db.data['personName'] = record.value(5)
                db.data['hKoulv'] = record.value(6)
                db.data['hMemo'] = record.value(7)
                db.data['scCode'] = record.value(8)
                db.data['scName'] = record.value(9)
                db.data['maker'] = record.value(10)
                db.data['verifier'] = record.value(11)
            
            # 替换掉QPyNullVariant
            for key in db.data:
                if isinstance(db.data[key], QtCore.QPyNullVariant):
                    db.data[key] = None
            # 以上表头完成
            
            # 读取表体
            query = QtSql.QSqlQuery(U8_db)
            query.setForwardOnly(True)
            query.prepare(table_sqlstr)
            query.bindValue(0, dbCode)
            query.exec_()
            
            # 转换，tuple组成的list
            table = []
            while query.next():
                # list重置（最先会包含发货单号和客户简称）
                lst = []
                record = query.record()
                for i in range(record.count()):
                    lst.append(record.value(i))
                # 替换掉QPyNullVariant
                lst = [None if isinstance(itm, QtCore.QPyNullVariant)==True else itm for itm in lst]
                # 转回tuple
                tp = tuple(lst)
                # 添加进list
                table.append(tp)
            
            # table完成
            db.data['table'] = table
            db.data['tableColumn'] = ['rowNO', 'invCode', 'invName', 'cata', 'ggxh', 'kuan', 'gao', 'dingjia', 'koulv', 'hsdj', 'quantity', 'unitName', 'iMoney', 'iTax', 'iSum', 'scyq', 'memo']
            
            # 加入列表
            resultList.append(db)
        
        # 数据库关闭
        U8_db.close()
        return resultList
    
    
    def Stat_fetch_dispatch_mx(self, dateStrStart, dateStrEnd):
        
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
        
        #  客户简称，从Customer.cCusAbbName取得
        #  已经按照客户登录处理（非发货单的担当）
        
        # cDefine22 宽
        # cDefine23 高
        # cDefine25 颜色规格型号
        # cDefine26 实量
        # cDefine29 生产要求
        
        cols = 23
        
        sqlstr = """
            SELECT
                DispatchLists.AutoID,
                dispatchList.DLID,
                dispatchList.cDLCode,
                CONVERT(varchar(10), DispatchList.dDate, 23),
                DispatchList.cCusCode,
                Customer.cCusAbbName,
                CustomerClass.cCCName,
                Person.cPersonName,
                DispatchLists.cInvCode,
                DispatchLists.cInvName,
                DispatchLists.cDefine22,
                DispatchLists.cDefine23,
                DispatchLists.cDefine25,
                DispatchLists.cDefine26,
                DispatchLists.iQuantity,
                DispatchLists.iNatMoney,
                DispatchLists.iNatTax,
                DispatchLists.iNatSum,
                InventoryClass.cInvCName,
                ComputationUnit.cComUnitName,
                dispatchList.cMemo,
                DispatchLists.cDefine29,
                DispatchLists.cSoCode
            FROM
                DispatchLists
            INNER JOIN DispatchList ON DispatchList.DLID = DispatchLists.DLID
            INNER JOIN Person ON DispatchList.cPersonCode = Person.cPersonCode
            INNER JOIN Customer ON DispatchList.cCusCode = Customer.cCusCode
            INNER JOIN CustomerClass ON Customer.cCCCode = CustomerClass.cCCCode
            INNER JOIN Inventory ON Inventory.cInvCode = DispatchLists.cInvCode
            INNER JOIN InventoryClass ON Inventory.cInvCCode = InventoryClass.cInvCCode
            INNER JOIN ComputationUnit ON Inventory.cComUnitCode = ComputationUnit.cComunitCode
            WHERE
                DispatchList.dDate BETWEEN ? AND ?
                """
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, dateStrStart)
        query.bindValue(1, dateStrEnd)
        query.exec_()
        
        # 转换，tuple组成的list
        result_list = []
        
        while query.next() == True:
            # tuple重置
            tp = ()
            # 用此生成tuple，过滤掉QPyNullVariant
            for i in range(cols):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            
#            (120811, 1000043195, '0000040288', '2016-12-01', '1032', '剪刀石头布', '刘浩', '01101', '新德拉克 单轨', '2.14', '1', '顶装', 2.14, 2.14, 87.79, 14.93, 102.72, 'CR', '米', <PyQt4.QtCore.QPyNullVariant object at 0x06A83870>, None, '109092', 1000224567)
            # 添加进list
            result_list.append(tp)
        
        U8_db.close()
        
        return result_list
    
    
    
    
    
    def Stat_fetch_dispatch(self, dateStrStart, dateStrEnd):
        # 此句自动打开连接
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
        
        # 取得表头 head_list
        head_list = []
        
        sqlstr = """
            SELECT
                dispatchList.DLID,
                dispatchList.cDLCode,
                CONVERT(varchar(10), DispatchList.dDate, 23),
                DispatchList.cCusCode,
                Customer.cCusAbbName,
                CustomerClass.cCCName,
                Person.cPersonName,
                DispatchList.cSOCode,
                dispatchList.cMemo
            FROM
                DispatchList
            INNER JOIN Person ON DispatchList.cPersonCode = Person.cPersonCode
            INNER JOIN Customer ON DispatchList.cCusCode = Customer.cCusCode
            INNER JOIN CustomerClass ON Customer.cCCCode = CustomerClass.cCCCode
            WHERE
                DispatchList.dDate BETWEEN ? AND ?        
        """
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, dateStrStart)
        query.bindValue(1, dateStrEnd)
        query.exec_()
        
        while query.next():
            # tuple重置
            tp = ()
            # 用此生成tuple，过滤掉QPyNullVariant
            for i in range(9):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            head_list.append(tp)
        
        
        
        # 取得表体body_list
        body_list = []
        
        sqlstr = """
            SELECT
                dispatchLists.AutoID,
                dispatchLists.DLID,
                DispatchLists.cInvCode,
                DispatchLists.cInvName,
                DispatchLists.cDefine22,
                DispatchLists.cDefine23,
                DispatchLists.cDefine25,
                DispatchLists.cDefine26,
                DispatchLists.iQuantity,
                DispatchLists.iNatMoney,
                DispatchLists.iNatTax,
                DispatchLists.iNatSum,
                ComputationUnit.cComUnitName,
                DispatchLists.cDefine29,
                InventoryClass.cInvCName
            FROM
                DispatchLists
            INNER JOIN DispatchList ON DispatchList.DLID = DispatchLists.DLID
            INNER JOIN Inventory ON Inventory.cInvCode = DispatchLists.cInvCode
            INNER JOIN InventoryClass ON Inventory.cInvCCode = InventoryClass.cInvCCode
            INNER JOIN ComputationUnit ON Inventory.cComUnitCode = ComputationUnit.cComunitCode
            WHERE
                DispatchList.dDate BETWEEN ? AND ?
                """
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.bindValue(0, dateStrStart)
        query.bindValue(1, dateStrEnd)
        query.exec_()
        
        while query.next():
            # tuple重置
            tp = ()
            # 用此生成tuple，过滤掉QPyNullVariant
            for i in range(15):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            body_list.append(tp)
        
        U8_db.close()
        
        return head_list, body_list


    def Stat_fetch_inventory(self):
        U8_db = QtSql.QSqlDatabase.database("MY_DB")
        
        cols = 8
        
        # iInvRCost 计划价售价
        sqlstr = """
                SELECT
                    Inventory.cInvCode,
                    Inventory.cInvName,
                    Inventory.cInvCCode,
                    InventoryClass.cInvCName,
                    Inventory.cComUnitCode,
                    ComputationUnit.cComUnitName,
                    Inventory.iInvSCost,
                    Inventory.iInvRCost
                FROM
                    Inventory
                INNER JOIN InventoryClass ON Inventory.cInvCCode = InventoryClass.cInvCCode
                INNER JOIN ComputationUnit ON Inventory.cComUnitCode = ComputationUnit.cComunitCode
                    WHERE (InventoryClass.cInvCName <> 'AD') AND (InventoryClass.cInvCName <> '其他')
                """
        
        query = QtSql.QSqlQuery(U8_db)
        query.setForwardOnly(True)
        query.prepare(sqlstr)
        query.exec_()
        
        # 转换，tuple组成的list
        result_list = []
        
        # 取得所有记录
        while query.next():
            # tuple重置
            tp = ()
            for i in range(cols):
                value = query.value(i)
                if isinstance(value, QtCore.QPyNullVariant):
                    value = None
                tp += (value,)
            # 添加进list
            result_list.append(tp)
        
        U8_db.close()
        return result_list


class FETCH_DATA_MERGE:
    """
    此类下，是LoadServerDataClass_PYQT_ODBC的再包装
    主要是取得Mysql下的一点打印资料什么的
    
    """
    
    def fetch_SO_HEAD(self, dateStrStart, dateStrEnd, cusCode):
        #读取U8服务器
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn() 
        dataList = U8.fetch_SO_HEAD_PURE(dateStrStart, dateStrEnd, cusCode)
        U8.remove_conn()
#        data_list = [('108486', '1042', '营业', None, 2800.0, '朱秀军（上海半岛酒店）发上海市普陀区中江路388号国盛中心1号楼907室 13361866767', '2016-11-11', '2016-11-11', '快递（顺丰）', '王成'),
#                     ('108488', '1409', '北京贝特美', None, 568.32, None, '2016-11-11', '2016-11-18', '汽运（德邦包装好不超3.1米）', None), ... ]
        
        # 以下：读取打印记录并合并  [('106544', '2016-08-22 11:24:00'), ('106545', '2016-08-22 11:24:00'), ('106546', '2016-08-22 11:24:00')]
        # 生成订单号list   ['106544', '106545', '106546', ......]
        soList = [tp[0] for tp in dataList]
        if soList:
            mh = MysqlHandle()
            mh.connect()
            printLogDict = mh.SO_Printlog_get(soList)
            mh.disconnect()
            # 与服务器数据合并（服务器数据后面追加一列，写上打印时间信息）
            for i, tp in enumerate(dataList):
                socode = tp[0]
                if socode in printLogDict:
                    dataList[i] += (printLogDict[socode],)
                else:
                    dataList[i] += (None,)
        return dataList
    
    
    def fetch_SO_HEAD_BY_CODE(self, soCode):
        #读取U8服务器
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn()
        dataList = U8.fetch_SO_HEAD_BY_CODE_PURE(soCode)
        U8.remove_conn()
        
        # 以下读取本地打印记录并合并
        # 生成订单号list   ['106544', '106545', '106546', ......]
        soList = [tp[0] for tp in dataList]
        if soList:
            mh = MysqlHandle()
            mh.connect()
            printLogDict = mh.SO_Printlog_get(soList)
            mh.disconnect()
            
            # 与服务器数据合并（服务器数据后面追加一列，写上打印时间信息）
            for i, tp in enumerate(dataList):
                socode = tp[0]
                if socode in printLogDict:
                    dataList[i] += (printLogDict[socode],)
                else:
                    dataList[i] += (None,)
        return dataList
    
    

    def fetch_DB_HEAD(self, dateStrStart, dateStrEnd, cusCode):
        #读取U8服务器
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn()
        dataList = U8.fetch_DB_HEAD_PURE(dateStrStart, dateStrEnd, cusCode)
        U8.remove_conn()
        
#        data_list = [(1000044579, '1400', 'NITORI', 484.0, '1000001152544 杭州滨江宝龙店 戴晓娜', '2017-01-13', '110360', '快递（顺丰）', None),
#        (1000044580, '1400', 'NITORI', 945.72, '1000001150304 杭州滨江宝龙店 张亮', '2017-01-13', '110361', '快递（顺丰）', None),
#        (1000044581, '1400', 'NITORI', 496.19, '1000001151305 上海中山公园店 薛雯珺', '2017-01-13', '110363', '快递（顺丰）', None),
#        (1000044582, '1400', 'NITORI', 316.8, '1000001148944 武汉经开店 汤晶', '2017-01-13', '110364', '快递（顺丰）', None),
#        (1000044583, '1400', 'NITORI', 639.94, '1000001152064 武汉群星城店 王先生', '2017-01-13', '110365', '快递（顺丰）', None)]
        
        # 以下：读取本地打印记录并合并
        # 生成发货单号list   ['0000011111', '0000011112', '0000011113', ......]
        dbList = [tp[0] for tp in dataList]
        if dbList:
            mh = MysqlHandle()
            mh.connect()
            printLogDict = mh.SO_Printlog_get_label(dbList)
            mh.disconnect()
            
            # 与服务器数据合并（服务器数据后面追加一列，写上打印时间信息）
            for i, tp in enumerate(dataList):
                dbcode = tp[0]
                if dbcode in printLogDict:
                    dataList[i] += (printLogDict[dbcode],)
                else:
                    dataList[i] += (None,)
        return dataList
    
    
    def fetch_DB_HEAD_BY_CODE(self, dbCode):
        #读取U8服务器
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn()
        dataList = U8.fetch_DB_HEAD_BY_CODE_PURE(dbCode)
        U8.remove_conn()
        
        # 以下读取本地打印记录并合并
        # 生成发货单号list   ['0000011111', '0000011112', '0000011113', ......]
        dbList = [tp[0] for tp in dataList]
        if dbList:
            mh = MysqlHandle()
            mh.connect()
            printLogDict = mh.SO_Printlog_get_label(dbList)
            mh.disconnect()
            
            # 与服务器数据合并（服务器数据后面追加一列，写上打印时间信息）
            for i, tp in enumerate(dataList):
                dbCode = tp[0]
                if dbCode in printLogDict:
                    dataList[i] += (printLogDict[dbCode],)
                else:
                    dataList[i] += (None,)
        return dataList


    def fetch_DB_HEAD_BY_SO(self, soCode):
        # 用订单号查询，取得发货单 可能有多张
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn()
        dataList = U8.fetch_DB_HEAD_BY_SO_PURE(soCode)
        U8.remove_conn()
        
        # 以下：读取本地打印记录并合并
        # 生成发货单号list   ['0000011111', '0000011112', '0000011113', ......]
        dbList = [tp[0] for tp in dataList]
        if dbList:
            mh = MysqlHandle()
            mh.connect()
            printLogDict = mh.SO_Printlog_get_label(dbList)
            mh.disconnect()
            
            # 与服务器数据合并（服务器数据后面追加一列，写上打印时间信息）
            for i, tp in enumerate(dataList):
                dbcode = tp[0]
                if dbcode in printLogDict:
                    dataList[i] += (printLogDict[dbcode],)
                else:
                    dataList[i] += (None,)
        return dataList
    

    def fetch_SOs(self, soCodeList):
        # 用so_lst查询，取得原始soDataList
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn()
        soList = U8.fetch_SOs_PURE(soCodeList)
        U8.remove_conn()
        
        # 开启mysql
        mh = MysqlHandle()
        mh.connect()
        
        # 1、添加截断信息
        soList = mh.SO_Railcut_appendCutHint(soList)
        
        # 2、添加 lastPrint 信息     return {'111111': '2016-01-01 10:20:30', '222222': '2016-01-01 10:20:33'}
        printlogDict = mh.SO_Printlog_get([so.data['soCode'] for so in soList])
        for i, so in enumerate(soList):
            soCode = so.data['soCode']
            if soCode in printlogDict:
                so.data['lastPrint'] = printlogDict[soCode]
        
        # 关闭mysql
        mh.disconnect()
        return soList
    
    
    def fetch_DBs(self, dbCodeList):
        # 用db_lst查询，取得打印数据
        U8 = LoadServerDataClass_PYQT_ODBC()
        U8.add_conn()
        dbList = U8.fetch_DBs_PURE(dbCodeList)
        U8.remove_conn()
        
        # 开启mysql
        mh = MysqlHandle()
        mh.connect()

        # 添加 lastLabelPrint 信息     return {'0000011111': '2016-01-01 10:20:30', '0000022222': '2016-01-01 10:20:33'}
        printlogDict = mh.SO_Printlog_get_label([db.data['dbCode'] for db in dbList])
        for i, db in enumerate(dbList):
            dbCode = db.data['dbCode']
            if dbCode in printlogDict:
                db.data['lastLabelPrint'] = printlogDict[dbCode]
        
        # 关闭mysql
        mh.disconnect()
        return dbList
    
    


class SO:
    
    def __init__(self):
        
        # 为什么用一个字典维护所有信息？而不是直接用属性？
        # 是为了打印时自动绑定用，方便
        
        self.data = {'soCode': None,
                     'cusCode': None,
                     'cusAbbName': None,
                     'po': None,
                     'soDate': None,
                     'preDate': None,
                     'maker': None,
                     'verifier': None,
                     'hKoulv': None,
                     'scCode': None,
                     'scName': None,
                     'personName': None,
                     'hMemo': None,
                     'cutHint': None,
                     'lastPrint': None,
                     
                     'tableColumn': ['rowNO', 'invCode', 'invName', 'cata', 'ggxh', 'kuan', 'gao', 'dingjia', 'koulv', 'hsdj', 'quantity', 'unitName', 'iMoney', 'iTax', 'iSum', 'scyq', 'memo'],
                     'table': []}
    
    
    def __str__(self):
        value = ''
        lst = ['soCode', 'cusCode', 'cusAbbName', 'po', 'soDate', 'preDate', 'maker', 'verifier', 'hKoulv', 'scCode', 'scName', 'personName', 'hMemo', 'cutHint', 'lastPrint']
        for key in lst:
            value += key
            value += ':\t'
            value += str(self.data[key])
            value += '\n'
        return value
    
    
    def sumMoney(self):
        """取得本SO的销售收入"""
        idx = self.data['tableColumn'].index('iMoney')
        total = sum([row[idx] for row in self.data['table']])
        return round(total, 2)
    
    def sumTax(self):
        """取得本SO的税额"""
        idx = self.data['tableColumn'].index('iTax')
        total = sum([row[idx] for row in self.data['table']])
        return round(total, 2)
    
    def sumSum(self):
        """取得本SO的价税合计"""
        idx = self.data['tableColumn'].index('iSum')
        total = sum([row[idx] for row in self.data['table']])
        return round(total, 2)
    
    def pivot(self):
        """返回销售收入透视表（暂为一个dict）"""
        dct = {}
        
        idx_cata  = self.data['tableColumn'].index('cata')
        idx_money = self.data['tableColumn'].index('iMoney')
        
        # 整理数据
        for row in self.data['table']:
            cata  = row[idx_cata]
            money = row[idx_money]
            if cata in dct:
                dct[cata] += money
            else:
                dct[cata] = money
        
        # 保留2位小数
        for key in dct:
            dct[key] = round(dct[key], 2)
        
        return dct
    
    
    
    
    
    
    
    
    
    
    
class DB:
    
    def __init__(self):
        self.data = {'dbCode': None,
                     'cusCode': None,
                     'cusAbbName': None,
                     'dbDate': None,
                     'soCode': None,
                     'personName': None,
                     'hKoulv': None,
                     'hMemo': None,
                     'scCode': None,
                     'scName': None,
                     'maker': None,
                     'verifier': None,
                     'lastLabelPrint': None,
                     
                     'tableColumn': ['rowNO', 'invCode', 'invName', 'cata', 'ggxh', 'kuan', 'gao', 'dingjia', 'koulv', 'hsdj', 'quantity', 'unitName', 'iMoney', 'iTax', 'iSum', 'scyq', 'memo'],
                     'table': []}
    
    
    def __str__(self):
        value = ''
        lst = ['dbCode', 'cusCode', 'cusAbbName', 'dbDate', 'soCode', 'personName', 'hKoulv', 'hMemo', 'scCode', 'scName', 'maker', 'lastLabelPrint']
        for key in lst:
            value += key
            value += ':\t'
            value += str(self.data[key])
            value += '\n'
        return value
    
    


class MysqlHandle:
    
    def __init__(self):
        self.config = {'host': '192.168.1.13',
                       'user': 'wang',
                       'password': 'shtoso64795156',
                       'port': 3306,
                       'database': 'TOSOINFO',
                       'charset': 'utf8'}
        self.conn = None
    
    
    def connect(self):
        try:
#            self.conn = mysql.connector.connect(**self.config)
            self.conn = pymysql.connect(**self.config)
#            print('Mysql opened')
            return True
        except pymysql.OperationalError as e:
#            print('connect fails!{}'.format(e))
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return False
    
    
    def disconnect(self):
        try:
            self.conn.close()
            self.conn = None
#            print('Mysql closed')
            return True
        except pymysql.OperationalError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))
            return False
    
        
    def SO_Printlog_get(self, soCodeList):
        '''
        读取订单的打印时间
        接收一个codelist，['111111', '222222']形式，也有可能是空列表 []
        返回一个字典 {'111111': '2016-01-01 10:20:30', '222222': '2016-01-01 10:20:33'}
        无法找到打印时间的，不出现在最终字典中
        '''
        resultList = []
        resultDict = {}
        
        if soCodeList:
            
            if len(soCodeList) > 1:
                soCodeStr = tuple(soCodeList)
            else:
                soCodeStr = "('{}')".format(soCodeList[0])
            
            sqlstr = """
                SELECT
                    SOCode,
                    LastPrint
                FROM
                    SO_PrintLog
                WHERE
                    SOCode IN {}
                """
            
            sqlstr = sqlstr.format(soCodeStr)
            
            cursor = self.conn.cursor()
            
            cursor.execute(sqlstr)
            
#        resultList形式  对于没有打印记录的，不返回值了    [('111431', '2017-03-16 09:33:10'), ('111432', '2017-03-16 09:33:10'), ...]
            resultList = cursor.fetchall()
            
            cursor.close()
            
            # 打印记录转为dict    {'111432': '2017-03-16 09:33:10', '111553': '2017-03-16 11:23:00', .... }
            for k, v in resultList:
                resultDict[k] = v
        
        return resultDict
    
    
    def SO_Printlog_save(self, soList):
        # 对soList，保存打印时间记录
        # 没有就新增，有的就更新
        sqlstr = """
                REPLACE INTO SO_PrintLog (SOCode, LastPrint)
                VALUES (%s, current_timestamp())
                """
        
        cursor = self.conn.cursor()
        
        # soList里不是元组形式，修改
        soList = [(socode,) for socode in soList]
        
        cursor.executemany(sqlstr, soList)
        self.conn.commit()
        cursor.close()

    
    
    def SO_Printlog_get_label(self, dbCodeList):
        '''
        读取订单的打印时间
        接收一个codelist，['0000042555', '0000042556']形式，也有可能是空的 []
        返回一个字典 {'0000042555': '2016-01-01 10:20:30', '0000042556': '2016-01-01 10:20:33'}
        无法找到打印时间的，不出现在最终字典中
        '''
        resultList = []
        resultDict = {}
        
        if dbCodeList:
            
            if len(dbCodeList) > 1:
                dbCodeStr = tuple(dbCodeList)
            else:
                dbCodeStr = "('{}')".format(dbCodeList[0])
            
            sqlstr = """
                SELECT
                    DBCode,
                    LastPrint
                FROM
                    SO_LabelPrintLog
                WHERE
                    DBCode IN {}
                """
            sqlstr = sqlstr.format(dbCodeStr)
            
            cursor = self.conn.cursor()
            cursor.execute(sqlstr)
            
#        resultList形式  对于没有打印记录的，不返回值了    [('0000042555', '2017-03-16 09:33:10'), ('0000042556', '2017-03-16 09:33:10'), ...]
            resultList = cursor.fetchall()
            
            cursor.close()
            
            # 打印记录转为dict    {'0000042555': '2017-03-16 09:33:10', '0000042556': '2017-03-16 11:23:00', .... }
            for k, v in resultList:
                resultDict[k] = v
        
        return resultDict


    def SO_Printlog_save_label(self, dbList):
        # 对dbList，保存打印时间记录
        # 没有就新增，有的就更新
        sqlstr = """
                REPLACE INTO SO_LabelPrintLog (DBCode, LastPrint)
                VALUES (%s, current_timestamp())
                """
        cursor = self.conn.cursor()
        
        # dbList里不是元组形式，修改
        dbList = [(dbcode,) for dbcode in dbList]
        
        cursor.executemany(sqlstr, dbList)
        
        self.conn.commit()
        
        cursor.close()


    def SO_Railcut_get_CutDefault(self, scCode):
        '''
        输入scCode，返回一个tuple，分别是直轨和弯轨默认截断上限
        (3.0, 3.0)
        找不到返回None
        '''
        result = None
        
        sqlstr = """
            SELECT
                SO_Railcut_CutDefault.Zcut,
                SO_Railcut_CutDefault.Wcut
            FROM
                SO_Railcut_CutDefault
            WHERE
                SO_Railcut_CutDefault.scCode=%s
            """
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr, (scCode,))
        
        result = cursor.fetchone()
        
        cursor.close()
        
        return result
    
    
    def SO_Railcut_get_CutException(self, cusCode, scCode):
        '''
        输入参数，返回一个tuple，分别是直轨和弯轨默认截断上限
        (3.0, 3.0)
        找不到返回None
        '''
        result = None
        
        sqlstr = """
            SELECT
                SO_Railcut_CutException.Zcut,
                SO_Railcut_CutException.Wcut
            FROM
                SO_Railcut_CutException
            WHERE
                SO_Railcut_CutException.cusCode=%s AND SO_Railcut_CutException.scCode=%s
            """
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr, (cusCode, scCode))
        
        result = cursor.fetchone()
        
        cursor.close()
        
        return result


    def SO_Railcut_get_RailMapping(self):
        # 返回一个列表，里面有5个列表
#        [轨道tp，单轨tp，双轨tp，直轨tp，弯轨tp]
        resultList = []
        
        sql_rail   = 'SELECT SO_Railcut_RailMapping.invCode FROM SO_Railcut_RailMapping ORDER BY SO_Railcut_RailMapping.invCode ASC'
        sql_single = 'SELECT SO_Railcut_RailMapping.invCode FROM SO_Railcut_RailMapping WHERE SO_Railcut_RailMapping.single=1 ORDER BY SO_Railcut_RailMapping.invCode ASC'
        sql_double = 'SELECT SO_Railcut_RailMapping.invCode FROM SO_Railcut_RailMapping WHERE SO_Railcut_RailMapping.double=1 ORDER BY SO_Railcut_RailMapping.invCode ASC'
        sql_zhigui = 'SELECT SO_Railcut_RailMapping.invCode FROM SO_Railcut_RailMapping WHERE SO_Railcut_RailMapping.zhigui=1 ORDER BY SO_Railcut_RailMapping.invCode ASC'
        sql_wangui = 'SELECT SO_Railcut_RailMapping.invCode FROM SO_Railcut_RailMapping WHERE SO_Railcut_RailMapping.wangui=1 ORDER BY SO_Railcut_RailMapping.invCode ASC'
        
        cursor = self.conn.cursor()
        
        cursor.execute(sql_rail)
        lst = cursor.fetchall()      # [('01112',), ('01114',), ('01111',), ('01113',)]
        lst = [i[0] for i in lst]
        resultList.append(lst)
        
        cursor.execute(sql_single)
        lst = cursor.fetchall()
        lst = [i[0] for i in lst]
        resultList.append(lst)
        
        cursor.execute(sql_double)
        lst = cursor.fetchall()
        lst = [i[0] for i in lst]
        resultList.append(lst)
        
        cursor.execute(sql_zhigui)
        lst = cursor.fetchall()
        lst = [i[0] for i in lst]
        resultList.append(lst)
        
        cursor.execute(sql_wangui)
        lst = cursor.fetchall()
        lst = [i[0] for i in lst]
        resultList.append(lst)
        
        cursor.close()
        
        return resultList


    def SO_Railcut_appendCutHint(self, soList):
        '''
        对一个soList里，每个so添加截断信息
        对so.data（为一个dict）：
        1、表头填写截断方式(cutHint)：“默认裁断。。。。。”
        2、table追加实裁尺寸列（sccc）
        返回填写后的soList
        '''
        # 标记定义
        IGNORE_MARK = 'IG'
        NO_MARK = '-'
        
        # 取得mysql固定参数
        CR_LIST, SINGLE_LIST, DOUBLE_LIST, ZHIGUI_LIST, WANGUI_LIST = self.SO_Railcut_get_RailMapping()
        
        
        for so in soList:
            
            cusCode = so.data['cusCode']
            scCode  = so.data['scCode']
            tableColumn = so.data['tableColumn']
            
            idx_invCode = tableColumn.index('invCode')
            idx_kuan    = tableColumn.index('kuan')
            idx_scyq    = tableColumn.index('scyq')
            
            #                     0     1            2             3       4     5       6     7     8     9     10    11     12    13     14      15       16
            # 默认table明细格式  ( 2, '01103', '静音新德拉克 单轨', 'CR', '顶装', '1.85', '1', '148', '40', 59.2, 1.85, '米', 93.61, 15.91, 109.52, None, '01SCJ71296 书房')
    
            # 最终目的是确定 zhigui_limit 和 wangui_limit  先读入默认，再查找例外
            # 取得默认截断值 快递都为2米，其他都为3米
            ZHIGUI_LIMIT, WANGUI_LIMIT = self.SO_Railcut_get_CutDefault(scCode)
            # 查找例外截断值，如果查到，则修改limit值     cut_size  (2.0, 2.0)
            cut_size = self.SO_Railcut_get_CutException(cusCode, scCode)

            # 如果找到，说明有特殊分段方法，找不到就跳过（追加key值）
            if cut_size is not None:
                ZHIGUI_LIMIT = cut_size[0]
                WANGUI_LIMIT = cut_size[1]
                so.data['cutHint'] = '特殊截断 直轨上限{}，弯轨上限{}'.format(ZHIGUI_LIMIT, WANGUI_LIMIT)
            else:
                so.data['cutHint'] = '默认截断 直轨上限{}，弯轨上限{}'.format(ZHIGUI_LIMIT, WANGUI_LIMIT)
            
            # tableColumn扩展
            so.data['tableColumn'].append('sccc')
            
            # table每行扩展sccc信息
            for i, tp in enumerate(so.data['table']):
                markText = ''

                invCode = tp[idx_invCode]
                crWidth = float(tp[idx_kuan])
                scyq    = tp[idx_scyq] or ''
                
                # 初始化参数。cuts是截断信息。cutCount是根数，cutSize是每段长度
                # 目标也就是求这4个值
                IG   = False
                isCR = False
                cuts = 0
                cutCount = 0
                cutSize = 0.0
                
                if invCode in CR_LIST:    #非CR跳过
                    isCR = True     #并维持其他值不变                
                    #  先确定cuts    # 分段，1是整根，2是分二，3是分3, 4是分四
                    if '整根' in scyq:
                        cuts = 1
                    elif '分二' in scyq:
                        cuts = 2
                    elif '分三' in scyq:
                        cuts = 3
                    elif '分四' in scyq:
                        cuts = 4
                    elif '分五' in scyq:
                        cuts = 5
                    elif '分六' in scyq:
                        cuts = 6
                    elif scyq == '':
                        if invCode in ZHIGUI_LIST:
                            cuts = math.ceil( crWidth / ZHIGUI_LIMIT )
                        elif invCode in WANGUI_LIST:
                            cuts = math.ceil( crWidth / WANGUI_LIMIT )
                    else:    # 都不符合，就是说明生产备注里写了各种其他文字，结果就是跳IG
                        IG = True
                    
                    if IG == False:
                        # 计算cutCount和cutSize
                        if invCode in SINGLE_LIST:
                            cutCount = cuts
                            cutSize = crWidth / cutCount
                        elif invCode in DOUBLE_LIST:
                            cutCount = cuts * 2
                            cutSize = crWidth / cutCount * 2
                
                # 此处加上生成markText判断
                if isCR == False:
                    markText = NO_MARK
                elif IG == True:
                    markText = IGNORE_MARK
                else:
                    markText = '{} × {}'.format(int(round(cutSize*1000, 0)), cutCount)    #以千位数表示，一定要这么写，否则小数会舍弃
                
                # 在原始数据上追加实裁尺寸列
                tp += (markText,)
                so.data['table'][i] = tp
        
        return soList


        
    def NT_Match_insert_mx(self, mxList):
        # mxList   [ (), (), ()          ]
        # 每个元组有24个数据
        self.connect()
        cursor = self.conn.cursor()
        
        # 绕过mysql安全机制，如果不加where运行，需要设置参数
        cursor.execute("DELETE FROM NT_Match_Hard WHERE 采购单号 <> ''")
        
        sql = """INSERT INTO NT_Match_Hard (采购单号,行号,单据号,订单行,顾客名,销售日,收货日,商品CD,商品名,原价,成品宽,成品高,安装高度,安装方法,系列,式样,操作方法,操作位置,号码,数量,进货方CD,进货方名称,单位原价,备注,TFileName)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(sql, mxList)
        
        # 提交前，以上所有的都不会被写入
        self.conn.commit()
        
        cursor.close()
        self.disconnect()
    
    
    def NT_Match_update_mx(self):
        '''
        对Hard表更新，追加8项：T总原价，T尺寸，T安装方法，TKeyWord，TInvCode，TDingJia，TZheKou，T总金额
        '''
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE 
                NT_Match_Hard
            SET
                T总原价 = 原价 * 数量,
                T尺寸 = IF(成品高="", IF(ROUND(CAST(成品宽 AS SIGNED)/100.0, 2)<1.0, 1.0, ROUND(CAST(成品宽 AS SIGNED)/100.0, 2)), IF(ROUND(CAST(成品宽 AS SIGNED)*CAST(成品高 AS SIGNED)/10000.0, 2)<1.0, 1.0, ROUND(CAST(成品宽 AS SIGNED)*CAST(成品高 AS SIGNED)/10000.0, 2))),
                TKeyWord = CONCAT(安装方法, 系列, 式样, 操作方法)
                """)
        
        cursor.execute("""
            UPDATE
                NT_Match_Hard INNER JOIN NT_Match_Keyword ON NT_Match_Hard.TKeyWord = NT_Match_Keyword.KeyWord
            SET
                NT_Match_Hard.TInvCode = NT_Match_Keyword.InvCode,
                NT_Match_Hard.TDingJia = NT_Match_Keyword.DingJia,
                NT_Match_Hard.TZheKou = NT_Match_Keyword.ZheKou
                """)
        
        cursor.execute("""
            UPDATE
                NT_Match_Hard
            SET
                T总金额 =  round( (T尺寸 * ROUND(TDingJia * TZheKou / 100.0, 2) * 数量), 2 )
                """)
        
        # 这里追加：把无法匹配的，总金额设置为0，这样刷新tableview不会出错（format时）
        cursor.execute("""
            UPDATE
                NT_Match_Hard
            SET
                T总金额 = 0.0
            WHERE
                T总金额 is null
                """)
        
        cursor.execute("""
            UPDATE
                NT_Match_Hard
            SET
                T安装方法=(CASE WHEN 安装方法="天花板" THEN "顶装" WHEN 安装方法="墙壁" THEN "墙装" END)
                """)
        
        self.conn.commit()
        
        cursor.close()
        self.disconnect()



    def NT_Match_fetch_distinct_orders(self):
#        The SUM() and AVG() functions return a DECIMAL value
#        只有int会变成decimal，float无影响
        # need cast to float
        sqlstr = """
                SELECT
                    采购单号,
                    单据号,
                    顾客名,
                    进货方名称,
                    TFileName,
                    cast(sum(数量) as SIGNED) AS RowCount,
                    round(sum(T总原价), 2) AS T总原价,
                    round(sum(T总金额), 2) AS T总金额,
                    round(sum(T总原价)-sum(T总金额), 2) AS 差额,
                    round((sum(T总原价)-sum(T总金额))/sum(T总原价)*100, 1) AS 差额率,
                    cast(sum( if(isnull(TInvCode), 1, 0) ) as SIGNED) AS CodeEmptyCount
                FROM
                    NT_Match_Hard
                GROUP BY
                    采购单号,
                    单据号,
                    顾客名,
                    进货方名称,
                    TFileName
                ORDER BY
                    进货方名称
                    """
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        
        cursor.close()
        self.disconnect()
        
        return result


    def NT_Match_organize_order_data(self):
        # 组织数据
        # [ ( ["采购单号", "单据号", "顾客名", "进货方名称", file_name],  [(row1), (row2), ...] ),
        #   ( ["采购单号", "单据号", "顾客名", "进货方名称", file_name],  [(row1), (row2), ...] ),
        #   ( ["采购单号", "单据号", "顾客名", "进货方名称", file_name],  [(row1), (row2), ...] ), .....]
        order_sql = """
                SELECT
                    采购单号,
                    单据号,
                    顾客名,
                    进货方名称,
                    TFileName,
                    cast(sum(数量) as SIGNED) AS RowCount,
                    收货日
                FROM
                    NT_Match_Hard
                GROUP BY
                    采购单号,
                    单据号,
                    顾客名,
                    进货方名称,
                    TFileName,
                    收货日
                ORDER BY
                    进货方名称
        """
        
        lst = []
        sqlstr = """
                SELECT
                    TInvCode,
                    商品名,
                    成品宽,
                    成品高,
                    安装高度,
                    T安装方法,
                    系列,
                    式样,
                    操作方法,
                    操作位置,
                    数量,
                    T总金额,
                    备注
                FROM
                    NT_Match_Hard
                WHERE
                    采购单号=%s
        """
        self.connect()
        cursor = self.conn.cursor()
        
        # get distinct order info
        cursor.execute(order_sql)
        orderList = cursor.fetchall()
        
        for order in orderList:
            PO, order_num, c_name, shop_name, file_name, order_rows, arrival_date = order
            
            cursor.execute(sqlstr, (PO,))
            result = cursor.fetchall()
            
            tp = ([PO, order_num, c_name, shop_name, file_name, order_rows, arrival_date], result)
            
            lst.append(tp)
        
        cursor.close()
        self.disconnect()
        
        return lst


    def NT_Match_organize_dispatch_data(self):
        # 组织数据
        # [ ( [u"采购单号", u"单据号", u"顾客名", u"进货方名称"],  [(row1), (row2), ...] ),
        #   ( [u"采购单号", u"单据号", u"顾客名", u"进货方名称"],  [(row1), (row2), ...] ),
        #   ( [u"采购单号", u"单据号", u"顾客名", u"进货方名称"],  [(row1), (row2), ...] ), .....]
        order_sql = """
                SELECT
                    采购单号,
                    单据号,
                    顾客名,
                    进货方名称,
                    cast(sum(数量) as SIGNED) AS RowCount
                FROM
                    NT_Match_Hard
                GROUP BY
                    采购单号,
                    单据号,
                    顾客名,
                    进货方名称
                ORDER BY
                    进货方名称
        """
        
        lst = []
        sqlstr = """
                SELECT
                    单据号,
                    订单行,
                    顾客名,
                    销售日,
                    收货日,
                    商品CD,
                    商品名,
                    原价,
                    成品宽,
                    成品高,
                    "" AS 置空,
                    安装方法,
                    数量,
                    进货方CD,
                    进货方名称
                FROM
                    NT_Match_Hard
                WHERE
                    单据号=%s
                 """
        self.connect()
        cursor = self.conn.cursor()
        
        # get distinct order info
        cursor.execute(order_sql)
        orderList = cursor.fetchall()
        
        for order in orderList:
            PO, order_num, c_name, shop_name, order_rows = order
            cursor.execute(sqlstr, (order_num,))
            result = cursor.fetchall()
            
            tp = (order_num, result)
            lst.append(tp)
        
        cursor.close()
        self.disconnect()

        return lst
    
    
    def NT_Match_fetch_keyword_match_fail(self):
        # 找出未能匹配到的 关键字串
        sqlstr = """
                SELECT
                    TKeyWord
                FROM
                    NT_Match_Hard
                WHERE
                    TInvCode IS NULL
                GROUP BY
                    TKeyWord
                """
        self.connect()
        cursor = self.conn.cursor()
        
        # get distinct order info
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        
        cursor.close()
        self.disconnect()
        
        return result


    def NT_Match_insert_keyword(self, dataList):
        # [('F-15单轨FH基本', '68193', 67.19, 41.67), ...]
        sqlstr = "INSERT INTO NM_KeyWordMapping VALUES (%s, %s, %s, %s, %s)"

        self.connect()
        cursor = self.conn.cursor()
        
        cursor.executemany(sqlstr, dataList)
        self.conn.commit()
        
        cursor.close()
        self.disconnect()
    
    
#    def ST_Stat_delete_dispatchAll(self):
#        # 删除所有dispatch    有2个表：ST_Cost_dispatchList  ST_Cost_dispatchLists
#        # 不需要delete后面必须更where了？？？？
#        sqlhead = "DELETE FROM ST_Cost_dispatchList"
#        sqlbody = "DELETE FROM ST_Cost_dispatchLists"
#        
#        cursor = self.conn.cursor()
#        
#        cursor.execute(sqlhead)
#        cursor.execute(sqlbody)
#        
#        cursor.close()
#        
#    
#    def ST_Stat_insert_dispatchAll(self, headList, bodyList):
#        # 删除所有dispatch    有2个表：ST_Cost_dispatchList  ST_Cost_dispatchLists
#        # 不需要delete后面必须更where了？？？？
#        # 然后写入新数据
#        sqlhead = "INSERT INTO ST_Cost_dispatchList VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#        sqlbody = """INSERT INTO ST_Cost_dispatchLists (AutoID,DLID,cInvCode,cInvName,cDefine22,cDefine23,cDefine25,cDefine26,iQuantity,iMoney,iTax,iSum,cComUnitName,cDefine29,cInvCName)
#        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
##        (140536, 1000047688, '01507', 'TOSO百叶帘 无需安装 单色', '0.49', '1.43', 'TB-601 右拉 1280', 0.7, 1.0, 319.66, 54.34, 374.0, '平方米', None, 'IB')
#        
#        cursor = self.conn.cursor()
#        
#        cursor.executemany(sqlhead, headList)
#        cursor.executemany(sqlbody, bodyList)
#        
#        self.conn.commit()
#        
#        cursor.close()
#        
#        
#    def ST_Stat_delete_invAll(self):
#        # 清空存货表
#        sql = "DELETE FROM inventory"
#        
#        cursor = self.conn.cursor()
#        
#        cursor.executemany(sql)
#        
#        self.conn.commit()
#        
#        cursor.close()
    
    
    def ST_update_inventory(self, invList):
        # 清空inventory表，并重新加入数据
        cursor = self.conn.cursor()
        
        # 绕过mysql安全机制，如果不加where运行，需要设置参数
        # 清空所有内容
        cursor.execute("DELETE FROM inventory WHERE invCode <> ''")
        
        # 插入服务器数据
        sql = "INSERT INTO inventory (invCode, invName, invCCode, invCName, comUnitCode, comUnitName, invSCost, invRCost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, invList)
        
        # 插入组装品数据
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
            ('87243', 'W-24端套FH',  '0306', 'FH', '5', '个', None, 1.18)]
        
        sql = "REPLACE INTO inventory (invCode, invName, invCCode, invCName, comUnitCode, comUnitName, invSCost, invRCost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, bcp)
        
        # 提交前，以上所有的都不会被写入
        self.conn.commit()
        
        cursor.close()
    
    
#    def ST_update_dateList(self, year, month):
#        # 日期格式统一为 2015-01-01
#        # 不管现在是几号，直接生成当月全部日期
#        weekday_mapping = {1:'一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六', 7:'日'}
#        dateList = []
#        
#        # 此句可以返回当月全部日期
#        dayList = range(calendar.monthrange(year, month)[1]+1)[1:]
#        
#        for day in dayList:
#            p_date = datetime.date(year, month, day)
#            dateList.append( (p_date.isoformat(), weekday_mapping[p_date.isoweekday()]) )   # isoweekday 星期一返回1，星期六返回6，星期日返回7
#        
#        # 以下mysql操作
#        deleteSql = "DELETE FROM ST_dateList"
#        insertSql = "INSERT INTO ST_dateList VALUES (%s, %s)"
#        
#        cursor = self.conn.cursor()
#        
#        # 删除
#        cursor.execute(deleteSql)
#        
#        # 添加
#        cursor.executemany(insertSql, dateList)
#        
#        self.conn.commit()
#        
#        cursor.close()
        
    
    def ST_update_dateList(self, start, end, format='%Y-%m-%d'):
        # 日期格式统一为 '2015-01-01'
        # start和end指开始和结束日期（包含）
        
        # 以下返回全部日期
        strptime = datetime.datetime.strptime
        strftime = datetime.datetime.strftime
        days = (strptime(end, format) - strptime(start, format)).days
        days += 1
        dateList = [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, 1)]
        
        # 以下添加星期
        weekday_mapping = {1:'一', 2:'二', 3:'三', 4:'四', 5:'五', 6:'六', 7:'日'}
        dateListFinal = []
        for date in dateList:
            dateListFinal.append( (date, weekday_mapping[strptime(date, format).isoweekday()]) )    # isoweekday 星期一返回1，星期六返回6，星期日返回7
        
        # 以下mysql操作
        deleteSql = "DELETE FROM ST_dateList"
        insertSql = "INSERT INTO ST_dateList VALUES (%s, %s)"
        
        cursor = self.conn.cursor()
        
        # 删除
        cursor.execute(deleteSql)
        
        # 添加
        cursor.executemany(insertSql, dateListFinal)
        
        self.conn.commit()
        
        cursor.close()
    
    
    
    
    
    
    def ST_update_dispatch(self, headList, bodyList):
        # 删除所有dispatch    有2个表：ST_Cost_dispatchList  ST_Cost_dispatchLists
        # 不需要delete后面必须更where了？？？？
        # 然后写入新数据
        
        deleteHead = "DELETE FROM ST_Cost_dispatchList"
        deleteBody = "DELETE FROM ST_Cost_dispatchLists"
        
        insertHead = "INSERT INTO ST_Cost_dispatchList VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insertBody = """INSERT INTO ST_Cost_dispatchLists (AutoID,DLID,cInvCode,cInvName,cDefine22,cDefine23,cDefine25,cDefine26,iQuantity,iMoney,iTax,iSum,cComUnitName,cDefine29,cInvCName)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
#        (140536, 1000047688, '01507', 'TOSO百叶帘 无需安装 单色', '0.49', '1.43', 'TB-601 右拉 1280', 0.7, 1.0, 319.66, 54.34, 374.0, '平方米', None, 'IB')
        
        cursor = self.conn.cursor()
        
        # 删除
        cursor.execute(deleteHead)
        cursor.execute(deleteBody)
        
        # 添加
        cursor.executemany(insertHead, headList)
        cursor.executemany(insertBody, bodyList)
        
        self.conn.commit()
        
        cursor.close()


    def ST_get_personNameList(self):
        # 取得担当者的列表
        sqlstr = """
                SELECT DISTINCT
                    ST_Cost_dispatchList.cPersonName
                FROM
                    ST_Cost_dispatchList
                """
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        
        lst = ["公司汇总", ]      # 第一个总是 “公司汇总”
        for rec in result:
            lst.append(rec[0])
        
        return lst
    
    
    def ST_get_customer(self):
        # 取得客户汇总（不含成本）
        # 不按照担当分行。
        sqlstr = """
                SELECT
                    cusCode,
                    cusAbbName,
                    ccName,
                    total_amount,
                    IB,
                    RB,
                    CR,
                    RS,
                    FH,
                    DII,
                    TA
                FROM
                    cus_summary
                ORDER BY
                    total_amount DESC
                """
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        
        return result
    
    
    
    def ST_get_customerWithCost(self):
        # 取得客户汇总（含成本）
        sqlstr = """
                SELECT
                    cusCode,
                    cusAbbName,
                    ccName,
                    personName,
                    total_amount,
                    total_cost,
                    total_profit,
                    profit_rate,
                    IB,
                    IBC,
                    IBP,
                    RB,
                    RBC,
                    RBP,
                    CR,
                    CRC,
                    CRP,
                    RS,
                    RSC,
                    RSP,
                    FH,
                    FHC,
                    FHP,
                    DII,
                    DIIC,
                    DIIP,
                    TA,
                    TAC,
                    TAP
                FROM
                    cus_summary_with_cost
                ORDER BY
                    total_amount DESC
                """
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr)
        result = cursor.fetchall()
        
        return result
    
    
    def ST_get_personByDay(self, personName):
        # 取得按日汇总
        # 数据库定义了2个view
        # by_day_all 对所有数据按日排列，忽略担当者（view中没有personName字段）
        # by_day_person 对所有数据按日按担当排列（view中有personName字段）
        if personName == '公司汇总':
            sqlstr = """
                    SELECT
                        dDate,
                        weekday,
                        total_amount,
                        total_cost,
                        total_profit,
                        IB,
                        IBC,
                        IBP,
                        RB,
                        RBC,
                        RBP,
                        CR,
                        CRC,
                        CRP,
                        RS,
                        RSC,
                        RSP,
                        FH,
                        FHC,
                        FHP,
                        DII,
                        DIIC,
                        DIIP,
                        TA,
                        TAC,
                        TAP
                    FROM
                        by_day_all
                    """
            cursor = self.conn.cursor()
            cursor.execute(sqlstr)
            result = cursor.fetchall()
        
        else:
            sqlstr = """
                    SELECT
                        dDate,
                        weekday,
                        total_amount,
                        total_cost,
                        total_profit,
                        IB,
                        IBC,
                        IBP,
                        RB,
                        RBC,
                        RBP,
                        CR,
                        CRC,
                        CRP,
                        RS,
                        RSC,
                        RSP,
                        FH,
                        FHC,
                        FHP,
                        DII,
                        DIIC,
                        DIIP,
                        TA,
                        TAC,
                        TAP
                    FROM
                        by_day_person
                    WHERE
                        personName=%s
                    """
            cursor = self.conn.cursor()
            cursor.execute(sqlstr, (personName,))
            result = cursor.fetchall()
        
        return result
    
    
    
    def ST_Cost_appendCost(self):
        # 追加所有成本信息（最后3列）
        cursor = self.conn.cursor()
        
        #1、从ST_Cost_BomList取得成本
        sqlstr = """
                UPDATE
                    (ST_Cost_dispatchLists INNER JOIN ST_Cost_BomList ON ST_Cost_dispatchLists.cInvCode=ST_Cost_BomList.invCode)
                SET
                    ST_Cost_dispatchLists.UnitCost = ST_Cost_BomList.unitCost,
                    ST_Cost_dispatchLists.Cost = round(ST_Cost_BomList.unitCost*iQuantity,2)
                """
        cursor.execute(sqlstr)
        
        #2、从inventory取得成本
        sqlstr = """
                UPDATE
                    (ST_Cost_dispatchLists INNER JOIN inventory ON ST_Cost_dispatchLists.cInvCode=inventory.invCode)
                SET
                    ST_Cost_dispatchLists.UnitCost = inventory.invRCost,
                    ST_Cost_dispatchLists.Cost = round(inventory.invRCost*iQuantity,2)
                WHERE
                    ST_Cost_dispatchLists.UnitCost is null
                """
        cursor.execute(sqlstr)
        
        #3、从costrate取得成本
        sqlstr = """
                UPDATE
                    (ST_Cost_dispatchLists INNER JOIN ST_Cost_CostRate ON ST_Cost_dispatchLists.cInvCode=ST_Cost_CostRate.invCode)
                SET
                    ST_Cost_dispatchLists.Cost = round(ST_Cost_CostRate.costRate*iMoney,2),
                    ST_Cost_dispatchLists.CostRateFlag='Y'
                WHERE
                    ST_Cost_dispatchLists.UnitCost is null
                """
        cursor.execute(sqlstr)
        
        self.conn.commit()
        
        cursor.close() 
        
        
        
        
        
        
    
    def ST_Cost_getInvInfo(self, invCode):
    # 取得inv条目
    # 返回5列。'存货编码', '存货名称', '存货大类', '单位', 单位原价
        sqlstr = """
            SELECT
                inventory.invCode,
                inventory.invName,
                inventory.invCName,
                inventory.comUnitName,
                inventory.invRCost
            FROM inventory
            WHERE inventory.invCode=%s
                """
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr, (invCode,))
        
        result = cursor.fetchall()
        
        cursor.close()
        self.disconnect()
        
        if result:
            return result[0]
        else:
            return ()


    def ST_Cost_getBom(self, invCode):
    # 取得Bom，包括头和体
    # 返回字典 {'head':(), 'body':[(),(),...]}
    # head'存货编码', '存货名称', '存货大类', '单位', 单位原价
#        {'head': ('68136', 'FH F-27双轨', 'FH', '米', 3.12, 1.0, 3.12, 143.34, 45.94, 'aaa'),
#        'body': [('93132', 1.04, 0.08), ('93101', 62.0, 0.0), ('93131', 7.0, 0.0), ('92001', 14.0, 0.0), ('92002', 14.0, 0.0), ('83435', 2.0, 0.0), ('83436', 2.0, 0.0), ('93124', 4.0, 0.0), ('93106', 2.0, 0.0), ('89201', 1.04, 0.03)]}

        rst = {'head':None, 'body':None}
        
        sqlstr_head = """
            SELECT
                ST_Cost_BomList.invCode,
                inventory.invName,
                inventory.invCName,
                inventory.comUnitName,
                ST_Cost_BomList.avgW,
                ST_Cost_BomList.avgH,
                ST_Cost_BomList.avgSize,
                ST_Cost_BomList.totalCost,
                ST_Cost_BomList.UnitCost,
                ST_Cost_BomList.memo
            FROM
                ST_Cost_BomList
            INNER JOIN inventory ON ST_Cost_BomList.invCode = inventory.invCode
            WHERE
                ST_Cost_BomList.invCode=%s
                """
        sqlstr_body = """
            SELECT
                ST_Cost_BomLists.invCodeMX,
                ST_Cost_BomLists.invName,
                ST_Cost_BomLists.invCata,
                ST_Cost_BomLists.quantity,
                ST_Cost_BomLists.comUnitName,
                ST_Cost_BomLists.lossRate,
                ST_Cost_BomLists.invRCost,
                ST_Cost_BomLists.cost
            FROM
                ST_Cost_BomLists
            WHERE
                ST_Cost_BomLists.invCode=%s
            ORDER BY ST_Cost_BomLists.rowNO ASC
                """
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr_head, (invCode,))
        result = cursor.fetchall()
        
        rst['head'] = result[0]
        
        cursor.execute(sqlstr_body, (invCode,))
        result = cursor.fetchall()
        
        rst['body'] = result
        
        cursor.close()
        self.disconnect()

        return rst


    def ST_Cost_getAllList(self):
    # 取得物料计算的条目
    # 返回7列。'存货编码', '存货名称', '存货大类', '平均尺寸', '单位', 'SET原价', '单位原价'
        sqlstr = """
            SELECT
                ST_Cost_BomList.invCode,
                inventory.invName,
                inventory.invCName,
                ST_Cost_BomList.avgSize,
                inventory.comUnitName,
                ST_Cost_BomList.totalCost,
                ST_Cost_BomList.unitCost,
                ST_Cost_BomList.memo
            FROM
                ST_Cost_BomList
            INNER JOIN inventory ON ST_Cost_BomList.invCode = inventory.invCode
                """
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sqlstr)
        
        rst = cursor.fetchall()
        
        cursor.close()
        self.disconnect()

        return rst


    def ST_Cost_saveBom(self, data):
        self.connect()
        cursor = self.conn.cursor()
        
        invCode = data['head'][0]
        
        # 检查invcode是否已经存在
        cursor.execute('SELECT count(invCode) AS C FROM ST_Cost_BomList WHERE invCode=%s', (invCode,))
        result = cursor.fetchone()  # (0,)
        
        # 表头
        cursor.execute('REPLACE INTO ST_Cost_BomList (invCode, avgW, avgH, avgSize, totalCost, unitCost, memo) VALUES (%s, %s, %s, %s, %s, %s, %s)', data['head'])
        
        # 表体删旧
        if result[0] != 0:
            cursor.execute('DELETE FROM ST_Cost_BomLists WHERE invCode=%s', (invCode,))
        
        # 表体新增
        cursor.executemany("INSERT INTO ST_Cost_BomLists (invCode, rowNO, invCodeMX, invName, invCata, quantity, comUnitName, lossRate, invRCost, cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data['body'])
        
        self.conn.commit()
        
        cursor.close()
        self.disconnect()
        

    def BOM_get_invCost(self, invCode):
        '''
        输入invCode，返回存货单价
        找不到返回None
        '''
        result = None
        
        sqlstr = """
            SELECT
                inventory.invRCost
            FROM
                inventory
            WHERE
                inventory.invCode=%s
            LIMIT 1
            """
        cursor = self.conn.cursor()
        
        cursor.execute(sqlstr, (invCode,))
        
#        fetchone是一个tuple (20.3,)，拆包到result，所以要加逗号
        result, = cursor.fetchone()
        
        cursor.close()
        
        return result




class Template:
    
    def __init__(self):
        self.printData = []
        self.template = {}
    
    
    def loadTemplate(self, fullName):
        # 读取时，只设置sourceData
#        filepath, tempfilename = os.path.split(FileName)
#        shortname, extension = os.path.splitext(tempfilename)
#        self.template['ReportName'] = shortname
        
        _, shortName = os.path.split(fullName)
        
        self.template['ReportName'] = shortName
        
        tree = ET.parse(fullName)
        root = tree.getroot()
        
        # 读入Canvas
        canvasE = root.find('Canvas')
        self.template['Canvas'] = (float(canvasE.find('W').text),
                                   float(canvasE.find('H').text),
                                   float(canvasE.find('OffsetX').text),
                                   float(canvasE.find('OffsetY').text),
                                   canvasE.find('PrinterName').text,
                                   int(canvasE.find('Landscape').text))
        
        # 读入Sectiones
        lst = []
        sectionE = root.find('Section')
        for itm in list(sectionE):
            tp = (
                    itm.find('SecName').text,
                    itm.find('SecText').text,
                    float(itm.find('L').text),
                    float(itm.find('T').text),
                    float(itm.find('W').text),
                    float(itm.find('H').text),
                    itm.find('FontName').text,
                    int(itm.find('FontSize').text),
                    int(itm.find('AlignH').text),
                    int(itm.find('AlignV').text),
                    int(itm.find('TextWrap').text),
                    int(itm.find('BorderWidth').text),
                    int(itm.find('BorderPenStyle').text)
                )
            lst.append(tp)
        self.template['Section'] = lst
        
        # 读入Lines
        lst = []
        lineE = root.find('Line')
        for itm in list(lineE):
            tp = (
                    itm.find('LineName').text,
                    float(itm.find('X1').text),
                    float(itm.find('Y1').text),
                    float(itm.find('X2').text),
                    float(itm.find('Y2').text),
                    float(itm.find('Width').text)
                 )
            lst.append(tp)
        self.template['Line'] = lst
        
        # 读入Images
        lst = []
        imageE = root.find('Image')
        for itm in list(imageE):
            tp = (
                    itm.find('ImageName').text,
                    float(itm.find('L').text),
                    float(itm.find('T').text),
                    float(itm.find('W').text),
                    float(itm.find('H').text),
                    itm.find('Image').text
                 )
            lst.append(tp)
        self.template['Image'] = lst
        
        # 读入Table  node.get('key')方法查询属性值
        tableE = root.find('Table')
        if tableE.get('L') is None:
            self.template['Table'] = ()
            self.template['TableColumn'] = []
        else:
            self.template['Table'] = (
                                        float(tableE.get('L')),
                                        float(tableE.get('T')),
                                        float(tableE.get('W')),
                                        float(tableE.get('H')),
                                        int(tableE.get('BorderWidth')),
                                        int(tableE.get('BorderPenStyle')),
                                        int(tableE.get('Head_h')),
                                        int(tableE.get('Body_h')),
                                        int(tableE.get('Subtotal_h')),
                                        int(tableE.get('Total_h'))
                                     )
            # 读入TableColumn
            lst = []
            colsE = tableE.getchildren()
            for itm in list(colsE):
                tp = (
                        int(itm.find('ColumnIndex').text),
                        itm.find('ColumnName').text,
                        itm.find('ColumnShowName').text,
                        int(itm.find('Width').text),
                        itm.find('FontName').text,
                        int(itm.find('FontSize').text),
                        int(itm.find('AlignH').text),
                        int(itm.find('AlignV').text),
                        int(itm.find('TextWrap').text),
                        int(itm.find('IsSum').text)
                     )
                lst.append(tp)
            self.template['TableColumn'] = lst
        
        
        # 读入Footer
        footerE = root.find('Footer')
        if footerE.find('Text') is None:
            self.template['Footer'] = ()
        else:
            self.template['Footer'] = (
                                        footerE.find('Text').text,
                                        float(footerE.find('L').text),
                                        float(footerE.find('T').text),
                                        float(footerE.find('W').text),
                                        float(footerE.find('H').text),
                                        footerE.find('FontName').text,
                                        int(footerE.find('FontSize').text),
                                        int(footerE.find('AlignH').text),
                                        int(footerE.find('AlignV').text),
                                        int(footerE.find('TextWrap').text),
                                        int(footerE.find('BorderWidth').text),
                                        int(footerE.find('BorderPenStyle').text)
                                      )
        return self.template
        
        
        
    def saveTemplate(self, fileName, templateDict):

        # 注意 Canvas Table Footer并不采用列表

        # 创建根节点
        root = ET.Element('template')
        tree = ET.ElementTree(root)
        
        #设置1级子节点
        canvasE = ET.SubElement(root, 'Canvas')
        sectionE = ET.SubElement(root, 'Section')
        lineE = ET.SubElement(root, 'Line')
        imageE = ET.SubElement(root, 'Image')
        footerE = ET.SubElement(root, 'Footer')
        tableE = ET.SubElement(root, 'Table')
        
        # 创建Canvas（唯一，必须存在）
        nodes = ['W', 'H', 'OffsetX', 'OffsetY', 'PrinterName', 'Landscape']
        tp = templateDict['Canvas']
        for i, node in enumerate(nodes):
            ele = ET.SubElement(canvasE, node)
            #转为str，遇None写空值
            ele.text = str(tp[i]) if tp[i] is not None else ''
            

        # 创建Footer（唯一，非必须存在）
        nodes = ['Text', 'L', 'T', 'W', 'H', 'FontName', 'FontSize', 'AlignH', 'AlignV', 'TextWrap', 'BorderWidth', 'BorderPenStyle']
        tp = templateDict['Footer']  #可能为()，所以下面要用if
        if tp:
            for i, node in enumerate(nodes):
                ele = ET.SubElement(footerE, node)
                ele.text = str(tp[i]) if tp[i] is not None else ''
        
        
        # 创建table（唯一，非必须存在）
        tp = templateDict['Table']
        nodes = ['L', 'T', 'W', 'H', 'BorderWidth', 'BorderPenStyle', 'Head_h', 'Body_h', 'Subtotal_h', 'Total_h']
        if tp:
            # 创建table table参数用属性存储
            for i, node in enumerate(nodes):
                tableE.set(node, str(tp[i]) if tp[i] is not None else '')
            
            # 创建tablecolumn（非唯一，跟table走）
            nodes = ['ColumnIndex', 'ColumnName', 'ColumnShowName', 'Width', 'FontName', 'FontSize', 'AlignH', 'AlignV', 'TextWrap', 'IsSum']
            columnList = templateDict['TableColumn']
            for tp in columnList:
                record = ET.SubElement(tableE, 'Column')
                for i, node in enumerate(nodes):
                    ele = ET.SubElement(record, node)
                    ele.text = str(tp[i]) if tp[i] is not None else ''
        
        # 创建Section（非唯一）
        nodes = ['SecName', 'SecText', 'L', 'T', 'W', 'H', 'FontName', 'FontSize', 'AlignH', 'AlignV', 'TextWrap', 'BorderWidth', 'BorderPenStyle']
        sectionList = templateDict['Section']
        for tp in sectionList:
            record = ET.SubElement(sectionE, 'RECORED')
            for i, node in enumerate(nodes):
                ele = ET.SubElement(record, node)
                ele.text = str(tp[i]) if tp[i] is not None else ''
        
        # 创建Line（非唯一）
        nodes = ['LineName', 'X1', 'Y1', 'X2', 'Y2', 'Width']
        lineList = templateDict['Line']
        for tp in lineList:
            record = ET.SubElement(lineE, 'RECORED')
            for i, node in enumerate(nodes):
                ele = ET.SubElement(record, node)
                ele.text = str(tp[i]) if tp[i] is not None else ''
        
        # 创建Image（非唯一）
        nodes = ['ImageName', 'L', 'T', 'W', 'H', 'Image']
        imageList = templateDict['Image']
        for tp in imageList:
            record = ET.SubElement(imageE, 'RECORED')
            for i, node in enumerate(nodes):
                ele = ET.SubElement(record, node)
                # Image内容是一串base64编码后的字符串
                ele.text = str(tp[i]) if tp[i] is not None else ''
        
        # 最后写入文件
        tree.write(fileName, 'UTF-8', xml_declaration=True)
    
    
    # 此处包含ColumnArrange
    def setPrintData(self, oriData):
        if 'tableColumn' in oriData.keys():
            if oriData['tableColumn']:
                colList = [tp[1] for tp in self.template['TableColumn']]
                prtData = SO_dataColumnArrange(copy.deepcopy(oriData), colList)
        else:
            prtData = copy.deepcopy(oriData)
        
        self.printData = prtData
    
    
    @pyqtSlot(QtGui.QPrinter)
    def render(self, printer):
        
        if self.template == {}:
            return
        
        if self.printData == []:
            return
        
        # 取得模板
        template = self.template
        
        # 取得需打印数据
        printData = self.printData
        
        p = QtGui.QPainter(printer)
        
        
#        if printer.printRange() == QtGui.QPrinter.AllPages:
#            from_page = 1
#            to_page   = data_count
#        elif printer.printRange() == QtGui.QPrinter.PageRange:    
#            from_page = printer.fromPage()
#            to_page   = printer.toPage()
        
#         render内，canvas设定好像都没用。（这些设定是用在打印机的，在调用render之前已经完成）
#        label_w, label_h, label_offset_x, label_offset_y, printer_name, landscape = template['Canvas']
        
        content_pen = QtGui.QPen()
        border_pen = QtGui.QPen()
        
        #                        0      1       2       3    4  5   6   7   8   9
        # template['Table'] =  (46.25, 194.25, 1027.5, 442.0, 0, 1, 25, 40, 30, 30)    
        # 计算printData需要几页，得到 n totalPage
        if template['Table'] == ():
            totalPage = 1
            n = 0
        else:
            tableRef = template['Table']
            # table数据解析
            L = tableRef[0]
            T = tableRef[1]
#            W = tableRef[2]
            H = tableRef[3]
            BorderWidth = tableRef[4]
            BorderPenStyle = tableRef[5]
            Head_h = tableRef[6]
            Body_h = tableRef[7]
            Subtotal_h = tableRef[8]
            Total_h = tableRef[9]
            
            # 取得column列表
            Columns = template['TableColumn']
            
            # 每页最多容纳n行数据 （表格高 扣表头  扣小计  扣合计
            n = int( (H - Head_h - Subtotal_h - Total_h) / Body_h )
            
            # 计算printData需要几页
            totalPage = math.ceil( len(printData['table']) / n )
        
        
        # 以表格数据为第一出发点，首先考虑要画几张表格，必须算出totalPage数，最小为1
        # 每张表格都需要画上表头内容
        
        # 绘制表格，每页最大打印n行，循环totalPage次
        table_body_place = 0
        
        for currentPage in range(1, totalPage+1):
            # ---------------画section------------------
            for itm in template['Section']:
                
                p.setPen(content_pen)
                
                name = itm[0]
                rect = QtCore.QRectF(itm[2], itm[3], itm[4], itm[5])
                
                font = QtGui.QFont(itm[6], itm[7])
                p.setFont(font)
                
                # txt需要从printData取值, 如果有对应，则取值，否则就按原面值
                if name in printData.keys():
                    txt = printData[name]
                else:
                    txt = itm[1]
                    
                align_h  = itm[8]
                align_v  = itm[9]
                textwrap = itm[10]
                align    = align_h | align_v | textwrap
                    
                p.drawText(rect, align, txt)
                
                # 画边框
                border_pen.setWidth( itm[11] )
                border_pen.setStyle( itm[12] )
                p.setPen(border_pen)
                p.drawRect(rect)
            
            # ---------------画line--------------------
            for itm in template['Line']:
                pen = QtGui.QPen()
                pen.setWidth(itm[5])
                p.setPen(pen)
                
                line = QtCore.QLineF(itm[1], itm[2], itm[3], itm[4])
                p.drawLine(line)
            
            # ---------------画image-------------------
            for itm in template['Image']:
                pix = QtGui.QPixmap()
                pix.loadFromData(itm[5])
                
                t_rect = QtCore.QRectF(itm[1], itm[2], itm[3], itm[4])
                s_rect = QtCore.QRectF(pix.rect())
                p.drawPixmap(t_rect, pix, s_rect)
            
            
            # -------------画表格--------------------
            if template['Table'] != ():
                tableMX = printData['table']
                #  确定本页打印行数。最后一页去余调整
                if totalPage == 1:
                    print_rows = len(tableMX)
                elif currentPage < totalPage:
                    print_rows = n
                else:
                    print_rows = len(tableMX) - ((currentPage-1) * n)    #最后一页打印时，需要把前面的行数都去除
                
                # 设置画笔，如果style是0的话，就是nopen
                border_pen.setWidth(BorderWidth)
                border_pen.setStyle(BorderPenStyle)
                p.setPen(border_pen)
                
                # 画表头数据
                x = L
                y = T
                
                if Head_h > 0:
                    #     0      1       2    3     4    5   6   7   8     9
                    #    (0, 'rowNO', '行号', 40, '宋体', 9, 4, 128, 8192, 0)
                    #  3 ColumnWidth
                    #  5 FontSize
                    for i, col in enumerate(Columns):
#                        # 确定位置
                        rect = QtCore.QRectF(x, y, col[3], Head_h)
#                        # 确定字体（字号固定）
                        font = QtGui.QFont(col[4], 9)
                        p.setFont(font)
#                        # 确定对齐方式 （表头都是居中，不自动换行）
                        align = 4 | 128 | 256
#                        # 确定内容
                        txt = col[2]
#                        # 绘制
                        p.drawText(rect, align, txt)                    
                        p.drawRect(rect)
#                        # x, y调整
                        x += col[3]
                
                # 画表体数据（先竖后横，可以少设置很多字体和对齐方式）
                x = L
                y = T + Head_h
                
                for i, col in enumerate(Columns):
                    # 确定字体
                    font = QtGui.QFont(col[4], col[5])
                    p.setFont(font)
                    # 确定对齐方式
                    align = col[6] | col[7] | col[8]
                    # 列宽
                    Body_w = col[3]
                    
                    for j in range(print_rows):
                        # 确定位置
                        rect = QtCore.QRectF(x, y, Body_w, Body_h)
                        # 确定内容     此处加上 table_body_place 以记忆位置
                        txt = tableMX[j+table_body_place][i]
                        
                        if type(txt) == float:
                            txt = '{:.2f}'.format(txt)
                        elif type(txt) == int:
                            txt = str(txt)
                        elif txt is None:
                            txt = ''
                        
                        # 绘制      添加padding
                        # a=QRect(10,10,50,50).adjusted(3,3,-3,-3)   >>>>     QRect(13, 13, 44, 44)
                        p.drawText(rect.adjusted(2, 2, -2, -2), align, txt)
                        p.drawRect(rect)
                    
                        # x, y调整
                        y += Body_h
                    
                    # i循环赋值
                    x += Body_w
                    y = T + Head_h
                
                
                # 画小计栏（和画表头很象，横向画过去）
                x = L
                y = T + Head_h + (print_rows * Body_h)
                
                if Subtotal_h > 0:
                    for i, col in enumerate(Columns):
                        # 确定位置
                        rect = QtCore.QRectF(x, y, col[3], Subtotal_h)
                        # 确定字体
                        font = QtGui.QFont(col[4], col[5])
                        p.setFont(font)
                        # 确定对齐方式
                        align = col[6] | col[7] | col[8]
                        
                        if i == 0:
                            txt = '小计:'
                        elif col[9] == 1:        # 统计当前页的小计值,数据库设置为1则要计算sum 在tp第8项
                            subtotal = 0.0
                            for j in range(print_rows):
                                subtotal += tableMX[j+table_body_place][i]
                            txt = '{:.2f}'.format(subtotal)
                        else:
                            txt = ''
                        # 绘制
                        p.drawText(rect.adjusted(2, 2, -2, -2), align, txt)
                        p.drawRect(rect)
                        # x, y调整
                        x += col[3]
                
                
                # 画总计栏
                x = L
                y = T + Head_h + (print_rows * Body_h) + Subtotal_h
                
                if Total_h > 0:
                    for i, col in enumerate(Columns):
                        # 确定位置
                        rect = QtCore.QRectF(x, y, col[3], Total_h)
                        # 确定字体
                        font = QtGui.QFont(col[4], col[5])
                        p.setFont(font)
                        # 确定对齐方式
                        align = col[6] | col[7] | col[8]
                        
                        if i == 0:
                            txt = '合计:'
                        elif col[9] == 1:  # 统计总计值   先把此列的值都提取为一个列表，然后sum累加
                            total = sum( [tp[i] for tp in tableMX] )
                            txt = '{:.2f}'.format(total)
                        else:
                            txt = ''
                        # 绘制
                        p.drawText(rect.adjusted(2, 2, -2, -2), align, txt)
                        p.drawRect(rect)
                        # x, y调整
                        x += col[3]
            
            
            # -----------------画页脚（如果为空tuple，就是没有页脚，当然也就不打印）
            # ('第{&cp}页 共{&tp}页', 38.0, 741.0, 102.0, 20.0, '宋体', 8, 128, 4, 256, 0, 0, 1)
            footer_tp = template['Footer']
            if footer_tp:
                rect = QtCore.QRectF(footer_tp[1], footer_tp[2], footer_tp[3], footer_tp[4])
                font = QtGui.QFont(footer_tp[5], footer_tp[6])
                p.setFont(font)
                
                # txt替换  一共有2种标签，{&cp} 和 {&tp}   用replace替换，不用format
                txt = footer_tp[0]
                txt = txt.replace('{&cp}', str(currentPage))
                txt = txt.replace('{&tp}', str(totalPage))
                
                align_h  = footer_tp[7]
                align_v  = footer_tp[8]
                textwrap = footer_tp[9]
                align    = align_h | align_v | textwrap
                
                # 打印文本
                p.setPen(content_pen)
                p.drawText(rect, align, txt)
                # 画边框
                border_pen.setWidth( footer_tp[10] )
                border_pen.setStyle( footer_tp[11] )
                p.setPen(border_pen)
                p.drawRect(rect)
            
            # ------------------------------------------------------------
            # 单页打印完毕，占位符位置刷新，为以后循环做准备
            table_body_place = (currentPage) * n

            if currentPage < totalPage:
                printer.newPage()
        
        p.end()



def SO_dataColumnArrange(data: dict, toColumns: list):
    """
    把原先的tableColumn和table，按照toColumns顺序重新排列
    需要把整张单据传入，因为可能有表头项目
    tableColumn和table是单据独有
    """
    
#       原始 colsName = ['rowNO', 'invCode', 'invName', 'ggxh', 'kuan', 'gao', 'dingjia', 'koulv', 'hsdj', 'quantity', 'unitName', 'iMoney', 'iTax', 'iSum', 'scyq', 'memo', 'sccc']
    oriTableColumn = data['tableColumn']
    oriTable = data['table']
    
    # 重排明细（可以放入表头的栏目）
    # 按现有cols顺序，取得原位置号的列表  需要注意：允许存在空值列
    mxCount = len(oriTable)
    arrangedTable = []
    
    # 先放入同等数量的空tuple
    for i in range(mxCount):
        arrangedTable.append( () )
    
    
    for colName in toColumns:
        
        if colName in oriTableColumn:
            # 原先就在table栏目内的，直接取得
            # 先取得索引号
            idx = oriTableColumn.index(colName)
            for i in range(mxCount):
                value = oriTable[i][idx]
                arrangedTable[i] += (value,)
        
        elif colName in data:
            # 如果是这里，说明就是表头栏目了
            # 但是有个问题，如果表头和表体，字段同名，则永远都取不到表头字段
            for i in range(mxCount):
                value = data[colName]
                arrangedTable[i] += (value,)
        else:
            # 如果在此处，说明都找不到，比如放入了空串
            for i in range(mxCount):
                value = ''
                arrangedTable[i] += (value,)
    
    data['tableColumn'] = toColumns
    data['table'] = arrangedTable
    
    return data




class TableModelCreater:
    """
    先按columnRef数据生成表头
    再把dataList数据按表头顺序生成（dataList可能为空）
    最后设置合计行
    """
    def create(self, columnRef, dataList=[]):
#        columnRef = [('dbCode', '发货单号', 110, 'CHECK_STYLE', 0),
#                     ('cusCode', '客户编码', 65, None, 0),
#                     ('cusAbbName', '客户简称', 90, None, 0),
#                     ('iMoney', '无税金额', 80, 'MONEY_STYLE', 1),
#                     ('iTax', '税额', 80, 'MONEY_STYLE', 1),
#                     ('iSum', '价税合计', 80, 'MONEY_STYLE', 1),
#                     ('memo', '备注', 230, None, 0),
#                     ('dbDate', '发货单日期', 90, None, 0),
#                     ('soCode', '订单号', 60, None, 0)]

        model = QtGui.QStandardItemModel()
        
        model.setSortRole(QtCore.Qt.UserRole)
        model.setHorizontalHeaderLabels( [tp[1] for tp in columnRef] )
        
        rowCount = len(dataList) if dataList else 0
        colCount = len(columnRef)
        
        if dataList:
            # 纯data设置到userrole（目的是以后可以按照userrole排序）
            for i, tp in enumerate(dataList):
                for j in range(len(tp)):
                    itm = QtGui.QStandardItem()
                    # 注意：需要把None全部转为空串，否则None是不参与排序的。但是0.0不能变）
                    value =   tp[j] if tp[j] is not None else ''
                    itm.setData(value, QtCore.Qt.UserRole)
                    itm.setData(value, QtCore.Qt.DisplayRole)   # 同样设置displayrole
                    model.setItem(i, j, itm)
            
            # 针对所有CHECK_STYLE的列设置
            for i, style in enumerate( [tp[3] for tp in columnRef] ):
                if style == 'CHECK_STYLE':
                    for j in range(rowCount):
                        itm = model.item(j, i)
                        itm.setCheckable(True)   # 一定要设置此句，才能点击
                        itm.setCheckState(QtCore.Qt.Unchecked)
            
            # 针对所有MONEY_STYLE的列设置
            for i, style in enumerate( [tp[3] for tp in columnRef] ):
                if style == 'MONEY_STYLE':
                    for j in range(rowCount):
                        itm = model.item(j, i)
                        amount = itm.data(QtCore.Qt.UserRole)
                        itm.setData('{:,.2f}'.format(amount), QtCore.Qt.DisplayRole)
                        itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            
            # 针对所有NUMBER_STYLE的列设置
            for i, style in enumerate( [tp[3] for tp in columnRef] ):
                if style == 'NUMBER_STYLE':
                    for j in range(rowCount):
                        itm = model.item(j, i)
                        amount = itm.data(QtCore.Qt.UserRole)
                        itm.setData('{:.2f}'.format(amount), QtCore.Qt.DisplayRole)
                        itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        # 无论是否有明细数据，最后一行添加合计行（设置所有userrole为None，就可以不参与排序，一直在最后一行）
        for i in range(colCount):
            itm = QtGui.QStandardItem()
            itm.setData(None, QtCore.Qt.UserRole)
#            itm.setData('', QtCore.Qt.UserRole)
            itm.setData(QtGui.QBrush(QtGui.QColor(253, 236, 212)), QtCore.Qt.BackgroundRole)
            model.setItem(rowCount, i, itm)            
        
        # 合计行设置合计值
        for i, isSum in enumerate( [tp[4] for tp in columnRef] ):
            if isSum == 1:
                total = sum([tp[i] for tp in dataList]) if dataList else 0.0
                itm = model.item(rowCount, i)
                itm.setData('{:,.2f}'.format(total), QtCore.Qt.DisplayRole)   # 同样设置displayrole
                itm.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        return model
    
    
    
class SettingReader:
    
    def __init__(self):
        self.settingDir = os.path.split(os.path.realpath(__file__))[0] + '\\setting\\'
        self.shortName = 'setting.xml'
        self.fullName = self.settingDir + self.shortName
        
        
    def load_SO_HEAD(self):
        tree = ET.parse(self.fullName)
        root = tree.getroot()
        
        # 读入SO_HEAD setting
        soHeadE = root.find('SO_HEAD')
        lst = []
        for itm in list(soHeadE):
            tp = (
                    itm.find('Name').text,
                    itm.find('Text').text,
                    int(itm.find('Width').text),
                    itm.find('Style').text,
                    int(itm.find('IsSum').text)
                )
            lst.append(tp)
        return lst
    
    
    def load_DB_HEAD(self):
        tree = ET.parse(self.fullName)
        root = tree.getroot()
        
        # 读入DB_HEAD setting
        dbHeadE = root.find('DB_HEAD')
        lst = []
        for itm in list(dbHeadE):
            tp = (
                    itm.find('Name').text,
                    itm.find('Text').text,
                    int(itm.find('Width').text),
                    itm.find('Style').text,
                    int(itm.find('IsSum').text)
                )
            lst.append(tp)
        return lst
    
    
    def load_SO(self):
        tree = ET.parse(self.fullName)
        root = tree.getroot()
        
        # 读入DB_HEAD setting
        soE = root.find('SO')
        lst = []
        for itm in list(soE):
            tp = (
                    itm.find('Name').text,
                    itm.find('Text').text,
                    int(itm.find('Width').text),
                    itm.find('Style').text,
                    int(itm.find('IsSum').text)
                )
            lst.append(tp)
        return lst
    
    
    def load_DB(self):
        tree = ET.parse(self.fullName)
        root = tree.getroot()
        
        # 读入DB_HEAD setting
        dbE = root.find('DB')
        lst = []
        for itm in list(dbE):
            tp = (
                    itm.find('Name').text,
                    itm.find('Text').text,
                    int(itm.find('Width').text),
                    itm.find('Style').text,
                    int(itm.find('IsSum').text)
                )
            lst.append(tp)
        return lst
