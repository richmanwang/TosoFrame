# -*- coding: utf-8 -*-
'''
Created on Mon Jul 16 14:30:52 2012

@author: Administrator
'''

import base64

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot

from PyQt4.QtCore import QPointF
from PyQt4.QtCore import QRectF

from ui_Editor_Main import Ui_Editor_Main
from ui_Editor_Report import Ui_Editor_Report
from ui_Editor_Section import Ui_Editor_Section
from ui_Editor_Line import Ui_Editor_Line
from ui_Editor_Table import Ui_Editor_Table
from ui_Editor_Footer import Ui_Editor_Footer

from core import Template

#import pdb


class Frm_Editor_Main(QtGui.QDialog, Ui_Editor_Main):
     
    def __init__(self, parent=None):
        super(Frm_Editor_Main, self).__init__(parent)
        self.setupUi(self)
        
        self.print_data = {}
        
        self.View = MyView(parent=self)
        
        rect = QtCore.QRectF(self.View.rect())
        self.scene = MyScene(rect)
        
        self.View.setScene(self.scene)
    
    
    @pyqtSlot()
    def on_btn_new_clicked(self):
        if self.scene.myLabel:
            self.scene.selectionChanged.disconnect(self.scene.selectionCgd)
            self.scene.removeItem(self.scene.myLabel)
            self.scene.selectionChanged.connect(self.scene.selectionCgd)        
        
        self.label_filename.setText('New File')
        
        rpt = MyReport()
        self._showReport( rpt.newReportDict() )
    
    
    @pyqtSlot()
    def on_btn_open_clicked(self):
        '''open template'''
        fullName = QtGui.QFileDialog.getOpenFileName(self, 'Choose a file', '.', 'Template Files (*.lab); All Files (*.*)')
        
        if fullName:
#            filePath, shortFileName = os.path.split(fullName)
            if self.scene.myLabel is not None:
                self.scene.selectionChanged.disconnect(self.scene.selectionCgd)
                self.scene.removeItem(self.scene.myLabel)
                self.scene.selectionChanged.connect(self.scene.selectionCgd)
            
            tpt = Template()
            templateDict = tpt.loadTemplate(fullName)
            self._showReport(templateDict)
            self.label_filename.setText(fullName)
    
    
    @pyqtSlot()
    def on_btn_save_clicked(self):
        
        tpt = Template()
        rpt = self.scene.myLabel
        templateDict = rpt.data_dict()
        
        fileName = self.label_filename.text()
        
        if fileName == 'New File':
            fileName = QtGui.QFileDialog.getSaveFileName(self, '新建', '.', 'Template Files (*.xml)')
        
        if fileName:
            # save内包含删除旧数据
            tpt.saveTemplate(fileName, templateDict)
            self.label_filename.setText(fileName)
            print('Saved.')
    
    
    @pyqtSlot()
    def on_btn_add_sec_clicked(self):
        '''增加文本框'''
        sec_num = 0
        
        sec_name_list = [sec.prop['SecName'] for sec in self.scene.myLabel.getSecList()]
        
        while 'Sec%s' % (sec_num+1) in sec_name_list:
            sec_num += 1
        
        # 放入时，要设置BackgroundSection为parent
        # 已经以bgs为parent，scene也跟着走（不用scene.addItem）
        for itm in self.scene.myLabel.getSecList():
            itm.setSelected(False)
        
        a = MySection(parent=self.scene.myLabel)
        a.prop['SecName'] = 'Sec%s' % (sec_num+1)
        a.prop['SecText'] = 'Sec%s' % (sec_num+1)
        a.updateByProp()
        a.setSelected(True)


    @pyqtSlot()
    def on_btn_add_line_clicked(self):
        '''增加线条'''
        line_num = 0
        
        line_name_list = [line.prop['LineName'] for line in self.scene.myLabel.getLineList()]
        
        while 'Line%s' % (line_num+1) in line_name_list:
            line_num += 1
        
        # 放入时，要设置BackgroundSection为parent
        # 已经以bgs为parent，scene也跟着走（不用scene.addItem）
        for itm in self.scene.myLabel.getItemList():
            itm.setSelected(False)
        
        a = MyLine(parent=self.scene.myLabel)
        a.prop['LineName'] = 'Line%s' % (line_num+1)
        a.updateByProp()
        a.setSelected(True)
    
    
    @pyqtSlot()
    def on_btn_add_image_clicked(self):
        '''添加图片'''
        imageName = QtGui.QFileDialog.getOpenFileName(self, 'Choose a file', '.', 'Image Files (*.jpg; *.png; *.gif)')
        
        if imageName == '':
            return
        
        num = 0
        
        image_name_list = [image.prop['ImageName'] for image in self.scene.myLabel.getImageList()]
        
        while 'Image%s' % (num+1) in image_name_list:
            num += 1
        
        # 放入时，要设置BackgroundSection为parent
        # 已经以bgs为parent，scene也跟着走（不用scene.addItem）
        for itm in self.scene.myLabel.getItemList():
            itm.setSelected(False)
        
        a = MyImage(parent=self.scene.myLabel)
        
        a.prop['ImageName'] = 'Image%s' % (num+1)
        
        # 这里换用base64值更新'ImageBlob'，本质是个字符串
#        a.prop['ImageBlob'] = open(imageName, 'rb').read()
        f = open(imageName, 'rb')
        ls_f = base64.b64encode(f.read())
        a.prop['ImageBlob'] = ls_f.decode()     # prop内保存的是字符串
        a.updateByProp()
        a.setSelected(True)


    @pyqtSlot()
    def on_btn_add_table_clicked(self):
        '''增加表格，表格最多只有1个'''
        # 放入时，要设置BackgroundSection为parent
        # 已经以bgs为parent，scene也跟着走（不用scene.addItem）
        if self.scene.myLabel.getTable():
            print('模板内已经有表格，不能增加')
        else:
            for itm in self.scene.myLabel.getItemList():
                itm.setSelected(False)
            
            a = MyTable(parent=self.scene.myLabel)
            a.updateByProp()
            a.setSelected(True)
    
    
    @pyqtSlot()
    def on_btn_add_footer_clicked(self):
        '''增加页脚，最多只有1个'''
        # 放入时，要设置BackgroundSection为parent
        # 已经以bgs为parent，scene也跟着走（不用scene.addItem）
        
        if self.scene.myLabel.getFooter():
            print('模板内已经有页脚，不能增加')
        else:
            for itm in self.scene.myLabel.getItemList():
                itm.setSelected(False)
            
            a = MyFooter(parent=self.scene.myLabel)
            a.updateByProp()
            a.setSelected(True)
    
    
    @pyqtSlot()
    def on_btn_print_preview_clicked(self):
        
        fileName = self.template_dir + '\\' + self.list_template.currentItem().text()
        
        tpt = Template()
        tpt.loadTemplate(fileName)
        
        # 放入data
        self.print_data = {
        'cSOCode': '106095',
        'cCusAbbName': '剪刀石头布',
        'koulv': '40',
        'CusPO': 'PO00169365',
        'cVerifier': '马晓莹',
        'SODate': '2016-08-04',
        'cCusCode': '1032',
        'cMaker': '戴汉云',
        'cMemo': None,
        'cPersonName': '刘浩',
        'dPreDateBT': '2016-08-09',
        'cSCName': '送货（东装）',
        'table': [('106095', '剪刀石头布', 1, '01111', '赛璐菲易弯 单轨', '顶装', '5.3', '1', '135', '40', 54.0, 5.3, '米', 244.62, 41.58, 286.2, '分为2.65米和2.65米单独两根，磁碰不配。', '01SVJ14611 地下影视厅'),
                  ('106095', '剪刀石头布', 2, '01111', '赛璐菲易弯 单轨', '顶装', '1.68', '1', '135', '40', 54.0, 1.68, '米', 77.54, 13.18, 90.72, None, '01SVJ14611 地下影视厅'),
                  ('106095', '剪刀石头布', 3, '01111', '赛璐菲易弯 单轨', '顶装', '1.68', '1', '135', '40', 54.0, 1.68, '米', 77.54, 13.18, 90.72, None, '01SVJ14611 地下影视厅'),
                  ('106095', '剪刀石头布', 4, '01111', '赛璐菲易弯 单轨', '顶装', '1.7', '1', '135', '40', 54.0, 1.7, '米', 78.46, 13.34, 91.8, None, '01SVJ14611 地下影视厅'),
                  ('106095', '剪刀石头布', 5, '01111', '赛璐菲易弯 单轨', '顶装', '2.18', '1', '135', '40', 54.0, 2.18, '米', 100.62, 17.1, 117.72, '分为1.09米和1.09米单独两根，磁碰不配。', '01SVJ14611 地下健身房'),
                  ('106095', '剪刀石头布', 6, '01111', '赛璐菲易弯 单轨', '顶装', '1.98', '1', '135', '40', 54.0, 1.98, '米', 91.38, 15.54, 106.92, None, '01SVJ14611 地下健身房'),
                  ('106095', '剪刀石头布', 7, '01111', '赛璐菲易弯 单轨', '顶装', '1.76', '1', '135', '40', 54.0, 1.76, '米', 81.23, 13.81, 95.04, None, '01SVJ14611 2F女儿房'),
                  ('106095', '剪刀石头布', 8, '01111', '赛璐菲易弯 单轨', '顶装', '1.76', '1', '135', '40', 54.0, 1.76, '米', 81.23, 13.81, 95.04, None, '01SVJ14611 2F女儿房'),
                  ('106095', '剪刀石头布', 9, '01111', '赛璐菲易弯 单轨', '顶装', '1.76', '1', '135', '40', 54.0, 1.76, '米', 81.23, 13.81, 95.04, None, '01SVJ14611 2F儿子房'),
                  ('106095', '剪刀石头布', 10, '01111', '赛璐菲易弯 单轨', '顶装', '1.76', '1', '135', '40', 54.0, 1.76, '米', 81.23, 13.81, 95.04, None, '01SVJ14611 2F儿子房'),
                  ('106095', '剪刀石头布', 11, '01111', '赛璐菲易弯 单轨', '顶装', '4.28', '1', '135', '40', 54.0, 4.28, '米', 197.54, 33.58, 231.12, '分为2.14米和2.14米单独两根，磁碰不配。', '01SVJ14611 主卧大窗'),
                  ('106095', '剪刀石头布', 12, '01111', '赛璐菲易弯 单轨', '顶装', '4.08', '1', '135', '40', 54.0, 4.08, '米', 188.31, 32.01, 220.32, None, '01SVJ14611 主卧大窗'),
                  ('106095', '剪刀石头布', 13, '01111', '赛璐菲易弯 单轨', '顶装', '1.86', '1', '135', '40', 54.0, 1.86, '米', 85.85, 14.59, 100.44, None, '01SVJ14611 主卧小窗'),
                  ('106095', '剪刀石头布', 14, '01111', '赛璐菲易弯 单轨', '顶装', '1.76', '1', '135', '40', 54.0, 1.76, '米', 81.23, 13.81, 95.04, None, '01SVJ14611 主卧小窗'),
                  ('106095', '剪刀石头布', 15, '01111', '赛璐菲易弯 单轨', '顶装', '1.42', '1', '135', '40', 54.0, 1.42, '米', 65.54, 11.14, 76.68, None, '01SVJ14611 主卧门'),
                  ('106095', '剪刀石头布', 16, '01111', '赛璐菲易弯 单轨', '顶装', '1.32', '1', '135', '40', 54.0, 1.32, '米', 60.92, 10.36, 71.28, None, '01SVJ14611 主卧门'),
                  ('106095', '剪刀石头布', 17, '01111', '赛璐菲易弯 单轨', '顶装', '1.15', '1', '135', '40', 54.0, 1.15, '米', 53.08, 9.02, 62.1, None, '01SVJ14611 阁楼立面窗'),
                  ('106095', '剪刀石头布', 18, '01103', '静音新德拉克 单轨', '顶装', '5.09', '1', '148', '40', 59.2, 5.09, '米', 257.55, 43.78, 301.33, None, '01SVJ14611 客厅'),
                  ('106095', '剪刀石头布', 19, '01103', '静音新德拉克 单轨', '顶装', '5.09', '1', '148', '40', 59.2, 5.09, '米', 257.55, 43.78, 301.33, None, '01SVJ14611 客厅'),
                  ('106095', '剪刀石头布', 20, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 21, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 22, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 23, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 24, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 25, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 26, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 27, '01103', '静音新德拉克 单轨', '顶装', '1.5', '1', '148', '40', 59.2, 1.5, '米', 75.9, 12.9, 88.8, None, '01SVJ14611 书房'),
                  ('106095', '剪刀石头布', 28, '01709', 'TOSO Creaty 单帘 板式', '右拉', '0.69', '1.65', '390', None, 150.0, 1.14, '平方米', 146.15, 24.85, 171.0, None, '01SVJ14611 女儿衣帽间'),
                  ('106095', '剪刀石头布', 29, '01709', 'TOSO Creaty 单帘 板式', '右拉', '0.6', '1.86', '390', None, 150.0, 1.12, '平方米', 143.59, 24.41, 168.0, None, '01SVJ14611 儿子衣帽间'),
                  ('106095', '剪刀石头布', 30, '01709', 'TOSO Creaty 单帘 板式', '右拉', '0.7', '1.66', '390', None, 150.0, 1.16, '平方米', 148.72, 25.28, 174.0, None, '01SVJ14611 主卧衣帽间')]
        }
        
        # 设置源数据
        tpt.setSourceData(self.print_data)
        
        # 改变数据形状
        tpt.dataTransform()
        
        # 取得canvas参数
        w, h, offset_x, offset_y, printerName, landscape = tpt.template['Canvas'][0]
        
        # 指定打印机
        if printerName in [None, '']:
            prt = QtGui.QPrinter( QtGui.QPrinterInfo().defaultPrinter() )
        else:
            for prt_info in  QtGui.QPrinterInfo().availablePrinters():
                if prt_info.printerName() == printerName:
                    prt = QtGui.QPrinter(prt_info)
                    break

        prt.setPaperSize(QtCore.QSizeF(w, h), prt.DevicePixel)
        
        if landscape == 1:
            prt.setOrientation(prt.Landscape)
        
        prt.setPageMargins(0.0, 0.0, 0.0, 0.0, prt.Millimeter)
        
        prt_preview = QtGui.QPrintPreviewDialog(prt)
        
        # void paintRequested (QPrinter*)
        prt_preview.paintRequested.connect(tpt.render)
        
        if prt_preview.exec_() == 1:
            pass

    
    
    def _showReport(self, templateDict):
        # 创建Canvas
        canvas_tp = templateDict['Canvas']
        self.scene.myLabel = MyReport(scene=self.scene)
        self.scene.myLabel.load_prop_from_tuple(canvas_tp)
        
        # 创建Section
        for sec in templateDict['Section']:
            # 放入时，要设置myLabel为parent，scene也跟着走（不用scene.addItem）
            a = MySection(parent=self.scene.myLabel)
            a.load_prop_from_tuple(sec)
        
        # 创建Line
        for line in templateDict['Line']:
            b = MyLine(parent=self.scene.myLabel)
            b.load_prop_from_tuple(line)

        # 创建Image
        for img in templateDict['Image']:
            i = MyImage(parent=self.scene.myLabel)
            i.load_prop_from_tuple(img)
        
        # 创建Table，只允许1个，所以不需要循环
        tabledef_tp = templateDict['Table']
        if tabledef_tp:
            t = MyTable(parent=self.scene.myLabel)
            cols = templateDict['TableColumn']
            t.load_prop_from_tuple(tabledef_tp, cols)
        
        # 创建Footer
        footer_tp = templateDict['Footer']
        # 入时，要设置myLabel为parent，scene也跟着走（不用scene.addItem）
        if footer_tp:
            a = MyFooter(parent=self.scene.myLabel)
            a.load_prop_from_tuple(footer_tp)
        
        self.View.setFocus()



class Frm_Editor_Report(QtGui.QDialog, Ui_Editor_Report):
     
    def __init__(self, parent=None):
        super(Frm_Editor_Report, self).__init__(parent)
        self.setupUi(self)
        
        self.prop = {}
        
        # 打印机分辨率
        self.dpi = 96
        self.cmFromInch = 2.54
        self.pointPerCm = self.dpi/self.cmFromInch
        
        # 添加所有打印机名称（第一个添加空值）
        printerNameList = ['',] + [prtInfo.printerName() for prtInfo in QtGui.QPrinterInfo().availablePrinters()]
        self.list_printer.insertItems(0, printerNameList)
        
    
    def setReportProp(self, reportProp):
        # 传入一个字典
        self.prop = reportProp
        
        rect = self.prop['Rect']
        self.lineEdit_width.setText( str(rect.width()) )
        self.lineEdit_height.setText( str(rect.height()) )
        
        self.lineEdit_offset_x.setText( str(self.prop['OffsetX']) )
        self.lineEdit_offset_y.setText( str(self.prop['OffsetY']) )
        
        self.list_printer.setEditText(self.prop['PrinterName'])
        
    
    @pyqtSlot()
    def on_btn_ok_clicked(self):
        # 属性框内暂时不涉及到rect及pos内容，所以只更新其他项目
        rect = QRectF( 0.0, 0.0, float(self.lineEdit_width.text()), float(self.lineEdit_height.text()) )
        self.prop['Rect'] = rect
        self.prop['OffsetX'] = float(self.lineEdit_offset_x.text())
        self.prop['OffsetY'] = float(self.lineEdit_offset_y.text())
        self.prop['PrinterName'] = self.list_printer.currentText()
        self.accept()


    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        # 抛弃改动
        self.reject()
    
    
    @pyqtSlot()
    def on_btn_unit_change_clicked(self):
        # 初始状态是Point
        if self.label_unit.text() == 'Point':
            self.lineEdit_width.setText( str(round(float(self.lineEdit_width.text())/self.pointPerCm, 2)) )
            self.lineEdit_height.setText( str(round(float(self.lineEdit_height.text())/self.pointPerCm, 2)) )
            self.lineEdit_offset_x.setText( str(round(float(self.lineEdit_offset_x.text())/self.pointPerCm, 2)) )
            self.lineEdit_offset_y.setText( str(round(float(self.lineEdit_offset_y.text())/self.pointPerCm, 2)) )
            self.label_unit.setText('CM')
        
        elif self.label_unit.text() == 'CM':
            self.lineEdit_width.setText( str(round(float(self.lineEdit_width.text())*self.pointPerCm, 2)) )
            self.lineEdit_height.setText( str(round(float(self.lineEdit_height.text())*self.pointPerCm, 2)) )
            self.lineEdit_offset_x.setText( str(round(float(self.lineEdit_offset_x.text())*self.pointPerCm, 2)) )
            self.lineEdit_offset_y.setText( str(round(float(self.lineEdit_offset_y.text())*self.pointPerCm, 2)) )
            self.label_unit.setText('Point')



class Frm_Editor_Section(QtGui.QDialog, Ui_Editor_Section):
     
    def __init__(self, parent=None):
        super(Frm_Editor_Section, self).__init__(parent)
        self.setupUi(self)
        
        self.prop = {}
        
        self.align_h_dict = {'靠左':1, '靠右':2, '居中':4, '两端对齐':8}
        self.align_h_dict_reverse = {1:'靠左', 2:'靠右', 4:'居中', 8:'两端对齐'}
        
        self.align_v_dict = {'靠上':32, '靠下':64, '居中':128}
        self.align_v_dict_reverse = {32:'靠上', 64:'靠下', 128:'居中'}
        
        self.textwrap_dict = {'单行':256, '自动换行':8192}
        self.textwrap_dict_reverse = {256:'单行', 8192:'自动换行'}
        
        self.combo_align_h.addItems(['靠左', '靠右', '居中', '两端对齐'])
        self.combo_align_v.addItems(['靠上', '靠下', '居中'])
        self.combo_textwrap.addItems(['单行', '自动换行'])
        
        
    def setSecProp(self, secProp):
        # 传入sec属性字典
        self.prop = secProp
        
        # 设置 内容 页
        self.lineEdit_secName.setText(self.prop['SecName'])
        self.lineEdit_secText.setText(self.prop['SecText'])
        
        # 设置 字体及边框 页
        ft = QtGui.QFont(self.prop['FontName'])
        self.box_secFontName.setCurrentFont(ft)
        self.lineEdit_fontSize.setText( str(self.prop['FontSize']) )
        self.lineEdit_borderWidth.setText( str(self.prop['BorderWidth']) )
        self.lineEdit_borderPenStyle.setText( str(self.prop['BorderPenStyle']) )
        
        # 设置 尺寸 页
        pos = self.prop['Pos']
        rect = self.prop['Rect']
        self.lineEdit_x.setText('%.2f' % pos.x())
        self.lineEdit_y.setText('%.2f' % pos.y())
        self.lineEdit_width.setText('%.2f' % rect.width())
        self.lineEdit_height.setText('%.2f' % rect.height())
        
        # 设置 对齐 页
        align_h_str = self.align_h_dict_reverse[self.prop['AlignH']]
        h_index = self.combo_align_h.findText(align_h_str)
        self.combo_align_h.setCurrentIndex(h_index)
        
        align_v_str = self.align_v_dict_reverse[self.prop['AlignV']]
        v_index = self.combo_align_v.findText(align_v_str)
        self.combo_align_v.setCurrentIndex(v_index)
        
        textwrap_str = self.textwrap_dict_reverse[self.prop['TextWrap']]
        textwrap_index = self.combo_textwrap.findText(textwrap_str)
        self.combo_textwrap.setCurrentIndex(textwrap_index)
        
    
    @pyqtSlot()
    def on_btn_ok_clicked(self):
        # 属性更新
        self.prop['SecName'] = self.lineEdit_secName.text()
        self.prop['SecText'] = self.lineEdit_secText.text()
        self.prop['FontName'] = self.box_secFontName.currentText()
        self.prop['FontSize'] = int(self.lineEdit_fontSize.text())
        self.prop['BorderWidth'] = int(self.lineEdit_borderWidth.text())
        self.prop['BorderPenStyle'] = int(self.lineEdit_borderPenStyle.text())
        
        self.prop['Pos'] = QPointF( float('%.2f' % float(self.lineEdit_x.text())), float('%.2f' % float(self.lineEdit_y.text())) )
        
        self.prop['Rect'] = QRectF(0.0, 0.0, float('%.2f' % float(self.lineEdit_width.text())), float('%.2f' % float(self.lineEdit_height.text())))
        
        self.prop['AlignH'] = self.align_h_dict[ self.combo_align_h.currentText() ]
        self.prop['AlignV'] = self.align_v_dict[ self.combo_align_v.currentText() ]
        self.prop['TextWrap'] = self.textwrap_dict[ self.combo_textwrap.currentText() ]
        
        self.accept()


    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        # 抛弃改动
        self.reject()



class Frm_Editor_Line(QtGui.QDialog, Ui_Editor_Line):
     
    def __init__(self, parent=None):
        super(Frm_Editor_Line, self).__init__(parent)
        self.setupUi(self)
        
        self.prop = {}
    
    
    def setProp(self, prop):
        # 传入属性字典
        self.prop = prop
        
        # 设置 尺寸 页
        self.lineEdit_x1.setText('%.2f' % self.prop['X1'])
        self.lineEdit_y1.setText('%.2f' % self.prop['Y1'])
        self.lineEdit_x2.setText('%.2f' % self.prop['X2'])
        self.lineEdit_y2.setText('%.2f' % self.prop['Y2'])
        self.lineEdit_width.setText('%.2f' % self.prop['Width'])
        
        
    @pyqtSlot()
    def on_btn_ok_clicked(self):
        # 属性更新
        self.prop['X1'] = float('%.2f' % float(self.lineEdit_x1.text()))
        self.prop['Y1'] = float('%.2f' % float(self.lineEdit_y1.text()))
        self.prop['X2'] = float('%.2f' % float(self.lineEdit_x2.text()))
        self.prop['Y2'] = float('%.2f' % float(self.lineEdit_y2.text()))
        self.prop['Width'] = float('%.2f' % float(self.lineEdit_width.text()))
        
        self.accept()
    
    
    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        # 抛弃改动
        self.reject()




class Frm_Editor_Table(QtGui.QDialog, Ui_Editor_Table):
     
    def __init__(self, parent=None):
        super(Frm_Editor_Table, self).__init__(parent)
        self.setupUi(self)
        
        self.prop = {}
        
        head_str = ['ColumnIndex', 'ColumnName', 'ColumnShowName', 'Width', 'FontName', 'FontSize', 'AlighH', 'AlighV', 'TextWarp', 'IsSum']
        head_width = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
        
        self.tableWidgetColumn.setColumnCount( len(head_str) )
        self.tableWidgetColumn.setHorizontalHeaderLabels(head_str)
        
        for i in range( len(head_str) ):
            self.tableWidgetColumn.setColumnWidth(i, head_width[i])
        
        
    def setTableProp(self, tableProp):
        # 传入sec属性字典
        self.prop = tableProp
                
        # 设置 尺寸 页
        pos = self.prop['Pos']
        rect = self.prop['Rect']
        self.lineEdit_x.setText('{:.2f}'.format(pos.x()))
        self.lineEdit_y.setText('{:.2f}'.format(pos.y()))
        self.lineEdit_width.setText('{:.2f}'.format(rect.width()))
        self.lineEdit_height.setText('{:.2f}'.format(rect.height()))
        self.lineEdit_borderWidth.setText( str(self.prop['BorderWidth']) )
        self.lineEdit_borderPenStyle.setText( str(self.prop['BorderPenStyle']) )
        
        self.lineEdit_Head_h.setText( str(self.prop['Head_h']) )
        self.lineEdit_Body_h.setText( str(self.prop['Body_h']) )
        self.lineEdit_Subtotal_h.setText( str(self.prop['Subtotal_h']) )
        self.lineEdit_Total_h.setText( str(self.prop['Total_h']) )
        
        # 设置 栏目 页
        cols = self.prop['Column']
        self.tableWidgetColumn.setRowCount(len(cols))
        for i, tp in enumerate(cols):
            for j, value in enumerate(tp):
                itm = QtGui.QTableWidgetItem()
                value = '' if value is None else str(value)
                itm.setText(value)
                self.tableWidgetColumn.setItem(i, j, itm)
    
    
    @pyqtSlot()
    def on_btn_addRow_clicked(self):
        rowCount = self.tableWidgetColumn.rowCount()
        self.tableWidgetColumn.setRowCount(rowCount + 1)
        
        
    @pyqtSlot()
    def on_btn_removeRow_clicked(self):
        currentRow = self.tableWidgetColumn.currentRow()
        self.tableWidgetColumn.removeRow(currentRow)
        
    
    def __refreshRowIndex(self):
        for i in range(self.tableWidgetColumn.rowCount()):
            itm = self.tableWidgetColumn.item(i, 0)
            itm.setText( str(i) )
    
    
    @pyqtSlot()
    def on_btn_ok_clicked(self):
        # 属性更新
        self.prop['Pos'] = QPointF( float('{:.2f}'.format(float(self.lineEdit_x.text()))), float('{:.2f}'.format(float(self.lineEdit_y.text()))) )
        self.prop['Rect'] = QRectF(0.0, 0.0, float('{:.2f}'.format(float(self.lineEdit_width.text()))), float('{:.2f}'.format(float(self.lineEdit_height.text()))) )
        self.prop['BorderWidth'] = int(self.lineEdit_borderWidth.text())
        self.prop['BorderPenStyle'] = int(self.lineEdit_borderPenStyle.text())
        
        self.prop['Head_h'] = int(self.lineEdit_Head_h.text())
        self.prop['Body_h'] = int(self.lineEdit_Body_h.text())
        self.prop['Subtotal_h'] = int(self.lineEdit_Subtotal_h.text())
        self.prop['Total_h'] = int(self.lineEdit_Total_h.text())
        
        # 刷新表格index
        self.__refreshRowIndex()
        
        # 设置Columns
        lst = []
        t = self.tableWidgetColumn
        rows = t.rowCount()
        
        for i in range(rows):
            # (0, 'soCode', '订单号', 60, '宋体', 12, 1, 128, 8192, 0)
            tp = (
                    int(t.item(i, 0).text()),
                    t.item(i, 1).text(),
                    t.item(i, 2).text(),
                    int(t.item(i, 3).text()),
                    t.item(i, 4).text(),
                    int(t.item(i, 5).text()),
                    int(t.item(i, 6).text()),
                    int(t.item(i, 7).text()),
                    int(t.item(i, 8).text()),
                    int(t.item(i, 9).text())
                 )
            lst.append(tp)
        
        self.prop['Column'] = lst
        self.accept()
    
    
    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        # 抛弃改动
        self.reject()



class Frm_Editor_Footer(QtGui.QDialog, Ui_Editor_Footer):
     
    def __init__(self, parent=None):
        super(Frm_Editor_Footer, self).__init__(parent)
        self.setupUi(self)
        
        self.prop = {}
        
        self.align_h_dict = {'靠左':1, '靠右':2, '居中':4, '两端对齐':8}
        self.align_h_dict_reverse = {1:'靠左', 2:'靠右', 4:'居中', 8:'两端对齐'}
        
        self.align_v_dict = {'靠上':32, '靠下':64, '居中':128}
        self.align_v_dict_reverse = {32:'靠上', 64:'靠下', 128:'居中'}
        
        self.textwrap_dict = {'单行':256, '自动换行':8192}
        self.textwrap_dict_reverse = {256:'单行', 8192:'自动换行'}
        
        self.combo_align_h.addItems(['靠左', '靠右', '居中', '两端对齐'])
        self.combo_align_v.addItems(['靠上', '靠下', '居中'])
        self.combo_textwrap.addItems(['单行', '自动换行'])
        
        
    def setFooterProp(self, footerProp):
        # 传入sec属性字典
        self.prop = footerProp

        # 设置 内容 页
        self.lineEdit_text.setText(self.prop['Text'])
        
        # 设置 字体及边框 页
        ft = QtGui.QFont(self.prop['FontName'])
        self.box_secFontName.setCurrentFont(ft)
        self.lineEdit_fontSize.setText( str(self.prop['FontSize']) )
        self.lineEdit_borderWidth.setText( str(self.prop['BorderWidth']) )
        self.lineEdit_borderPenStyle.setText( str(self.prop['BorderPenStyle']) )
        
        # 设置 尺寸 页
        pos = self.prop['Pos']
        rect = self.prop['Rect']
        self.lineEdit_x.setText('%.2f' % pos.x())
        self.lineEdit_y.setText('%.2f' % pos.y())
        self.lineEdit_width.setText('%.2f' % rect.width())
        self.lineEdit_height.setText('%.2f' % rect.height())
        
        # 设置 对齐 页
        align_h_str = self.align_h_dict_reverse[self.prop['AlignH']]
        h_index = self.combo_align_h.findText(align_h_str)
        self.combo_align_h.setCurrentIndex(h_index)
        
        align_v_str = self.align_v_dict_reverse[self.prop['AlignV']]
        v_index = self.combo_align_v.findText(align_v_str)
        self.combo_align_v.setCurrentIndex(v_index)
        
        textwrap_str = self.textwrap_dict_reverse[self.prop['TextWrap']]
        textwrap_index = self.combo_textwrap.findText(textwrap_str)
        self.combo_textwrap.setCurrentIndex(textwrap_index)
    
    
    @pyqtSlot()
    def on_btn_ok_clicked(self):
        # 属性更新
        self.prop['Text'] = self.lineEdit_text.text()
        self.prop['FontName'] = self.box_secFontName.currentText()
        self.prop['FontSize'] = int(self.lineEdit_fontSize.text())
        self.prop['BorderWidth'] = int(self.lineEdit_borderWidth.text())
        self.prop['BorderPenStyle'] = int(self.lineEdit_borderPenStyle.text())
        
        self.prop['Pos'] = QPointF(
                                    float('%.2f' % float(self.lineEdit_x.text())),
                                    float('%.2f' % float(self.lineEdit_y.text()))
                                    )
        
        self.prop['Rect'] = QRectF(0.0, 0.0, float('%.2f' % float(self.lineEdit_width.text())), float('%.2f' % float(self.lineEdit_height.text())))
        
        self.prop['AlignH'] = self.align_h_dict[ self.combo_align_h.currentText() ]
        self.prop['AlignV'] = self.align_v_dict[ self.combo_align_v.currentText() ]
        self.prop['TextWrap'] = self.textwrap_dict[ self.combo_textwrap.currentText() ]
        
        self.accept()


    @pyqtSlot()
    def on_btn_cancel_clicked(self):
        # 抛弃改动
        self.reject()






class MyView(QtGui.QGraphicsView):
    
    def __init__(self, parent):
        super(MyView, self).__init__(parent)
        
        self.setGeometry(20, 50, 1181, 791)
    
    
    def wheelEvent(self, QWheelEvent):

#Constant	Value	Description
#Qt.SHIFT	Qt.ShiftModifier	The Shift keys provided on all standard keyboards.
#Qt.META	Qt.MetaModifier	The Meta keys.
#Qt.CTRL	Qt.ControlModifier	The Ctrl keys.
#Qt.ALT	Qt.AltModifier	The normal Alt keys, but not keys like AltGr.

        if QWheelEvent.modifiers() == QtCore.Qt.ControlModifier:
            
            if QWheelEvent.delta() > 0:
                # 每向上推一格，为120
                self.scale(1.25, 1.25)
                
            else:
                self.scale(0.8, 0.8)
        



class MyScene(QtGui.QGraphicsScene):
    
    def __init__(self, sceneRect, parent=None):
        super(MyScene, self).__init__(sceneRect, parent)
        
        self.selectionChanged.connect(self.selectionCgd)
        
        
        # 设置初始值（为了添加sec时自动生成name用）
        #每次新增sec时，自动+1取号（第一个为  Sec1）
        self.secMaxValue = 0
        
        # 这里设置一个scene的变量，在myLabel初始化时会赋值的
        self.myLabel = None
        
        # 设置背景色
#        bg_brush = QtGui.QBrush(QtCore.Qt.yellow)
#        self.setBackgroundBrush(bg_brush)

        
    
    def selectionCgd(self):
        # 好像是放在这里比较好
        # 可以取得焦点，也可以放弃
        for itm in self.myLabel.getItemList():
            itm.removeHandles()
        
        for itm in self.selectedItems():
            itm.createHandles()
    
    
    def keyPressEvent(self, key_event):
        
        labelW = self.myLabel.rect().width()
        labelH = self.myLabel.rect().height()
        
        for itm in self.selectedItems():
            
            if key_event.key() == QtCore.Qt.Key_Delete:
                self.removeItem(itm)
            
            elif key_event.key() == QtCore.Qt.Key_Left:
                itm.posMoveBy('L', labelW, labelH)
                
            elif key_event.key() == QtCore.Qt.Key_Right:
                itm.posMoveBy('R', labelW, labelH)
                
            elif key_event.key() == QtCore.Qt.Key_Up:
                itm.posMoveBy('U', labelW, labelH)
                
            elif key_event.key() == QtCore.Qt.Key_Down:
                itm.posMoveBy('D', labelW, labelH)
        
        
        if key_event.modifiers() == QtCore.Qt.ControlModifier:
            if key_event.key() == QtCore.Qt.Key_A:
                for itm in self.myLabel.getItemList():
                    itm.setSelected(True)




class MyReport(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        # 所有的其他图形都以此方块为parent
        # 初始化时，scene已指定
        # 这里可以执行页面设置等操作
        super(MyReport, self).__init__(parent, scene)
        
        # 用一个字典，维护属性
        self.prop = {'Rect': QRectF(0.0, 0.0, 400.0, 400.0),
                     'OffsetX': 0.0,
                     'OffsetY': 0.0,
                     'PrinterName': None,
                     'Landscape': 0}
        
        # 设置初始大小
        self.setRect(self.prop['Rect'])
        
        # 设置初始位置（此属性固定，留出上方和左方的空间给刻度尺，这样就不用再设置itemsBoundingRect了。因为默认是从0,0开始显示的）
#        self.setPos(0.0, 0.0)
        
        # 设置颜色
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        brush = QtGui.QBrush(QtGui.QColor(255,255,200))
        self.setBrush(brush)
        
        # 打印机分辨率
        self.dpi = 96
        self.cmFromInch = 2.54
        self.pointPerCm = self.dpi/self.cmFromInch
        
        # 设置刻度尺
        self.ruler_top  = MyRulerTop(parent=self)
        self.ruler_left = MyRulerLeft(parent=self)
        
        # 为了选取区域Sec，设置1个Rect
        self.selectRect = None
    
    
    
    def load_prop_from_tuple(self, tp):
        w, h, offset_x, offset_y, printerName, landscape = tp
        self.prop = {'Rect': QRectF(0.0, 0.0, w, h),
                     'OffsetX': offset_x,
                     'OffsetY': offset_y,
                     'PrinterName': printerName,
                     'Landscape': landscape}
        self.updateByProp()
    
    
    def updateByProp(self):
        rect = self.prop['Rect']
        
#        横向纸张需转置
        if self.prop['Landscape'] == 1:
            rect = QRectF(0.0, 0.0, rect.height(), rect.width())
        
        self.setRect(rect)
        
        # update刻度尺
        self.ruler_top.setScaleTop()
        self.ruler_left.setScaleLeft()
        
        boundRect = self.scene().itemsBoundingRect()
        self.scene().setSceneRect( boundRect.adjusted(-40.0, -40.0, 40.0, 40.0) )
    
    
    def getSecList(self):
        return [itm for itm in self.childItems() if type(itm)==MySection]
        
    
    def getLineList(self):
        return [itm for itm in self.childItems() if type(itm)==MyLine]
    

    def getImageList(self):
        return [itm for itm in self.childItems() if type(itm)==MyImage]


    def getFooter(self):
        # 只有1个，不返回list
        for itm in self.childItems():
            if type(itm) == MyFooter:
                return itm
        return None
    
    
    def getTable(self):
        # 只有1个表，所以不返回list
        for itm in self.childItems():
            if type(itm) == MyTable:
                return itm
        return None
    
    
    def getItemList(self):
#        lst = []
#        for itm in self.childItems():
#            if (type(itm) != MyRulerTop) and (type(itm) != MyRulerLeft):
#                lst.append(itm)
#        return lst
        return [itm for itm in self.childItems() if type(itm) not in [MyRulerTop, MyRulerLeft]]
        
    
    def newReportDict(self):
        self.prop = {'Canvas': (400.0, 400.0, 0.0, 0.0, None, 0), 'Section': [], 'Line': [], 'Image': [], 'Table': (), 'TableColumn': [], 'Footer': ()}
        return self.prop
        
        
    def data_dict(self):
        
        data_dict = {'Canvas': (), 'Section': [], 'Line': [], 'Image': [], 'Table': (), 'TableColumn': [], 'Footer': ()}
        
        # 获取Canvas信息
        rect = self.prop['Rect']
        w = rect.width()
        h = rect.height()
        offset_x = self.prop['OffsetX']
        offset_y = self.prop['OffsetY']
        printer_name = self.prop['PrinterName']
        landscape = self.prop['Landscape']
        data_dict['Canvas'] = (w, h, offset_x, offset_y, printer_name, landscape)
        
        # 获取Sec信息
        lst = []
        for sec in self.getSecList():
            p = sec.prop
            tp = (p['SecName'],
                  p['SecText'],
                  p['Pos'].x(),
                  p['Pos'].y(),
                  p['Rect'].width(),
                  p['Rect'].height(),
                  p['FontName'],
                  p['FontSize'],
                  p['AlignH'],
                  p['AlignV'],
                  p['TextWrap'],
                  p['BorderWidth'],
                  p['BorderPenStyle'])
            lst.append(tp)
        data_dict['Section'] = lst
        
        # 获取Line信息
        lst = []
        for line in self.getLineList():
            p = line.prop
            tp = (p['LineName'],
                  p['X1'],
                  p['Y1'],
                  p['X2'],
                  p['Y2'],
                  p['Width'])
            lst.append(tp)
        data_dict['Line'] = lst
        
        # 获取Image信息
        lst = []
        for img in self.getImageList():
            p = img.prop
            tp = (p['ImageName'],
                  p['Pos'].x(),
                  p['Pos'].y(),
                  p['Rect'].width(),
                  p['Rect'].height(),
                  p['ImageBlob'])
            lst.append(tp)
        data_dict['Image'] = lst
        
        # 获取Table信息
        tbl = self.getTable()
        if tbl is not None:
            p = tbl.prop
            tp = (p['Pos'].x(),
                  p['Pos'].y(),
                  p['Rect'].width(),
                  p['Rect'].height(),
                  p['BorderWidth'],
                  p['BorderPenStyle'],
                  p['Head_h'],
                  p['Body_h'],
                  p['Subtotal_h'],
                  p['Total_h'])
            data_dict['Table'] = tp
            data_dict['TableColumn'] = tbl.prop['Column']   # 获取TableColumn信息
        
        # 获取Footer信息
        footer = self.getFooter()
        if footer:
            p = footer.prop
            data_dict['Footer'] = (
                                  p['Text'],
                                  p['Pos'].x(),
                                  p['Pos'].y(),
                                  p['Rect'].width(),
                                  p['Rect'].height(),
                                  p['FontName'],
                                  p['FontSize'],
                                  p['AlignH'],
                                  p['AlignV'],
                                  p['TextWrap'],
                                  p['BorderWidth'],
                                  p['BorderPenStyle']
                                  )
        return data_dict



    def mouseDoubleClickEvent(self, e):
        # QGraphicsSceneMouseEvent
        # 打开属性框（parent设定在view上，否则会出任务框）
        a = Frm_Editor_Report(parent=self.scene().views()[0])
        a.setReportProp(self.prop)
        
        dialog_code = a.exec_()
        
        # enum DialogCode { Rejected, Accepted }
        if dialog_code == QtGui.QDialog.Accepted:
            self.prop = a.prop
            self.updateByProp()
        else:
            pass

    
    def mousePressEvent(self, e):
        self.selectRect = QtGui.QGraphicsRectItem()
        pen = QtGui.QPen(QtCore.Qt.DashLine)
        self.selectRect.setPen(pen)
        self.scene().addItem(self.selectRect)
    
    
    def mouseMoveEvent(self, e):
        '''
        4种情况
        1、左上到右下，x2-x1为正，y2-y1为正，x1, y1, width, height
        2、右下到左上，x2-x1为负，y2-y1为负，x2, y2, width, height
        3、右上到左下，x2-x1为负，y2-y1为正，x2, y1, width, height
        4、左下到右上，x2-x1为正，y2-y1为负，x1, y2, width, height
        '''
        down_pos = e.buttonDownPos(QtCore.Qt.LeftButton)
        now_pos  = e.pos()
        
        x1, y1 = down_pos.x(), down_pos.y()
        x2, y2 = now_pos.x(), now_pos.y()
     
        width  = abs(x2-x1)
        height = abs(y2-y1)
        
        if x2-x1>0.0 and y2-y1>0.0:
            self.selectRect.setRect(x1, y1, width, height)
            
        elif x2-x1<0.0 and y2-y1<0.0:
            self.selectRect.setRect(x2, y2, width, height)
        
        elif x2-x1<0.0 and y2-y1>0.0:
            self.selectRect.setRect(x2, y1, width, height)
        
        elif x2-x1>0.0 and y2-y1<0.0:
            self.selectRect.setRect(x1, y2, width, height)
    
    
    def mouseReleaseEvent(self, e):
        
        for itm in self.getItemList():
            itm.setSelected(False)
        
        for itm in self.selectRect.collidingItems():
            itm.setSelected(True)

        self.scene().removeItem(self.selectRect)





class MyRulerTop(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MyRulerTop, self).__init__(parent, scene)
        
        # 设置初始大小
        self.setRect(0.0, 0.0, 10.0, 10.0)

        # 设置颜色
        self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        
        # 固定参数
        self.h = 20
        self.interval = 5
        
        # 打印机分辨率，从parentItem（mylabel）提取
#        self.dpi = 96
#        self.cmFromInch = 2.54
#        self.pointPerCm = self.dpi/self.cmFromInch
        self.pointPerCm = self.parentItem().pointPerCm
        
        
        self.line_long_length = 15
        self.line_short_length = 6

        
        self.w = self.parentItem().rect().width()
        
        self.setRect(0.0, 0.0, self.w, self.h)
        self.setPos(0.0, 0.0-self.h-self.interval)
        
        

    def setScaleTop(self):
        # 设置在标签上方，从（0,0）开始，一直到标签宽度
        self.w = self.parentItem().rect().width()
    
        self.setRect(0.0, 0.0, self.w, self.h)
        self.setPos(0.0, 0.0-self.h-self.interval)
        
    
    # 浮点数不支持range函数，自己定义一个类似的
    def __floatrange(self, start, stop, steps):
        lst = []
        
        steps = float(steps)
        start = float(start)
        stop  = float(stop)
        
        num   = start
        
        while num < stop:
            lst.append(num)
            num += steps
        
        return lst


    def paint(self, painter, option, widget):
    # QGraphicsItem.paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)
        # 此行保留，之下开始画刻度
        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)    
        
        p = painter
        
        pen = QtGui.QPen(QtCore.Qt.darkMagenta)
        p.setPen(pen)
        
        # 画长刻度，并画数字
        for i in self.__floatrange(0.0, self.w, self.pointPerCm):
            # 从下往上画
            lx1, ly1 = i, self.h
            lx2, ly2 = i, self.h-self.line_long_length
            p.drawLine( QPointF(lx1, ly1), QPointF(lx2, ly2) )
            # 写字适当调节一些尺寸
            p.drawText(QPointF(lx2+2, ly2+7), str(int(i/self.pointPerCm)))
        
        # 画短刻度

        for i in self.__floatrange(0.0, self.w, self.pointPerCm/10.0):
            sx1, sy1 = i, self.h
            sx2, sy2 = i, self.h-self.line_short_length
            p.drawLine( QPointF(sx1, sy1), QPointF(sx2, sy2) )
        
        
        
class MyRulerLeft(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MyRulerLeft, self).__init__(parent, scene)
        
        # 设置初始大小
        self.setRect(0.0, 0.0, 10.0, 10.0)

        # 设置颜色
        self.setBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        
        # 固定参数
        self.w = 20
        self.interval = 5
        
        # 打印机分辨率，从parentItem（mylabel）提取
#        self.dpi = 96
#        self.cmFromInch = 2.54
#        self.pointPerCm = self.dpi/self.cmFromInch
        self.pointPerCm = self.parentItem().pointPerCm
        
        self.line_long_length = 15
        self.line_short_length = 6

        
        self.h = self.parentItem().rect().height()
        
        self.setRect(0.0, 0.0, self.w, self.h)
        self.setPos(0.0-self.w-self.interval, 0.0)
        
        

    def setScaleLeft(self):
        # 设置在标签左边，从（0,0）开始，一直到标签高度
        self.h = self.parentItem().rect().height()
    
        self.setRect(0.0, 0.0, self.w, self.h)
        self.setPos(0.0-self.w-self.interval, 0.0)
        
    
    # 浮点数不支持range函数，自己定义一个类似的
    def __floatrange(self, start, stop, steps):
        lst = []
        
        steps = float(steps)
        start = float(start)
        stop  = float(stop)
        
        num   = start
        
        while num < stop:
            lst.append(num)
            num += steps
        
        return lst
    
    
    def paint(self, painter, option, widget):
    # QGraphicsItem.paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)
        
        # 此行保留，之下开始画刻度
        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)    
        
        p = painter
        
        pen = QtGui.QPen(QtCore.Qt.darkMagenta)
        p.setPen(pen)
        
        # 画长刻度，并画数字
        for i in self.__floatrange(0.0, self.h, self.pointPerCm):
            # 从右边往左画
            lx1, ly1 = self.w, i
            lx2, ly2 = self.w-self.line_long_length, i
            p.drawLine( QPointF(lx1, ly1), QPointF(lx2, ly2) )
            # 写字适当调节一些尺寸
            p.drawText(QPointF(lx2+0, ly2+10), str(int(i/self.pointPerCm)))
        
        # 画短刻度
        for i in self.__floatrange(0.0, self.h, self.pointPerCm/10.0):
            sx1, sy1 = self.w, i
            sx2, sy2 = self.w-self.line_short_length, i
            p.drawLine( QPointF(sx1, sy1), QPointF(sx2, sy2) )


class MyTable(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MyTable, self).__init__(parent, scene)
        
        # 用一个字典，维护Table属性（TableName取消）
        self.prop = {
                     'Rect': QRectF(0.0, 0.0, 50.0, 30.0),
                     'Pos': QPointF(30.0, 30.0),
                     'BorderWidth': 0,
                     'BorderPenStyle': 1,
                     'Head_h': 20,
                     'Body_h': 35,
                     'Subtotal_h':25,
                     'Total_h':25,
                     'Column': [(0, 'Column1', 'ColumnShowName1', 40, '宋体', 8, 4, 128, 8192, 0),
                                (1, 'Column2', 'ColumnShowName2', 40, '宋体', 8, 4, 128, 8192, 0)]
                     }
        
        # 设置大小
        self.setRect(self.prop['Rect'])
        
        # 设置堆叠  The default Z-value is 0.
        self.setZValue(1.0)
        
        # 设置为白色，不要透明的
        brush = QtGui.QBrush(QtCore.Qt.white)
        self.setBrush(brush)
        
        # set hover enable
        self.setAcceptHoverEvents(True)
        
        # 设置可选择  需要加上ItemIsFocusable，才可以接受键盘事件
        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)


    def load_prop_from_tuple(self, tabledef_tp, cols):
        # 用一个字典，维护Table属性
        #                     0        1      2       3    4  5  6   7   8   9  10
        # tabledef_tp =    ( 46.25, 194.25, 1027.5, 442.0, 3, 0, 1, 25, 40, 30, 30  )
        
        tp = tabledef_tp
        
        self.prop = {
                     'Rect': QRectF(0.0, 0.0, tp[2], tp[3]),
                     'Pos': QPointF(tp[0], tp[1]),
                     'BorderWidth': tp[4],
                     'BorderPenStyle': tp[5],   # solid line
                     'Head_h': tp[6],
                     'Body_h': tp[7],
                     'Subtotal_h': tp[8],
                     'Total_h': tp[9],
                     'Column': cols
                     }
        self.updateByProp()


    def updateByProp(self):
        # 用此方法刷新
        # 本质是再次调用paint方法刷新
        self.update(self.rect())
        
        self.setPos(self.prop['Pos'])
        self.setRect(self.prop['Rect'])
        
        # 重排handles
        self._arrangeHandles()
    
    
    def posMoveBy(self, direction_str, areaW, areaH):
        # 用于 scene的keyPressEvent事件中
        
        pos = self.pos()
        posX = pos.x()
        posY = pos.y()
        
        rectW = self.rect().width()
        rectH = self.rect().height()
        
        if direction_str == 'L':
            new_posX = max(posX-1, 0)
            new_posY = posY
        elif direction_str == 'R':
            new_posX = min(posX+1, areaW-rectW)
            new_posY = posY
        elif direction_str == 'U':
            new_posX = posX
            new_posY = max(posY-1, 0)
        elif direction_str == 'D':
            new_posX = posX
            new_posY = min(posY+1, areaH-rectH)
        
        self.setPos(new_posX, new_posY)


    
    def paint(self, painter, option, widget):
    # QGraphicsItem.paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)
        
        # 此行还是保留，可以在选中时显示虚线
#        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)

        # 设置黑笔，画内容
#        k_pen = QtGui.QPen(QtCore.Qt.black)
#        painter.setPen(k_pen)
        
        # cols
        columnList  = self.prop['Column']
        columnCount = len(columnList)
        
        # Columns:  [(0, 'rowNO', '行号', 40, '宋体', 8, 4, 128, 8192, 0), ..... ]
        ColumnWidthList = [col[3] for col in columnList]
        FontNameList    = [col[4] for col in columnList]
        FontSizeList    = [col[5] for col in columnList]
        AlignHList      = [col[6] for col in columnList]
        AlignVList      = [col[7] for col in columnList]
        TextWrapList    = [col[8] for col in columnList]
        SumColumnList   = [col[9] for col in columnList]
        
        total_h = self.prop['Rect'].height()
#        total_w = self.prop['Rect'].width()
        head_h = self.prop['Head_h']
        body_h = self.prop['Body_h']
        Subtotal_h = self.prop['Subtotal_h']
        Total_h = self.prop['Total_h']
        
        # 外框线  drawRect (self, QRectF rect)
        painter.drawRect(self.rect())
        
        # 计算剩余高度能够打印多少行？   行数为n
        n = int( (total_h - head_h - Subtotal_h - Total_h) / body_h )
        
        # 画表头
        x = 0
        y = 0
        for i in range(columnCount):
            # 确定位置
            rect = QRectF(x, y, ColumnWidthList[i], head_h)
            
            # 确定字体（字号固定）
            font = QtGui.QFont(FontNameList[i], 9)
            painter.setFont(font)
            
            # 确定对齐方式  全部设为居中对齐（2个维度都是）
#            align    = AlignHList[i] | AlignVList[i] | TextWrapList[i]
            align = QtCore.Qt.AlignCenter
            
            # 表头显示内容, tuple第3项为显示名称  Columns:  [(0, 'rowNO', '行号', 40, '宋体', 8, 4, 128, 8192, 0), ..... ]
            txt = columnList[i][2]
            
            # 绘制
            painter.fillRect(rect, QtGui.QBrush(QtCore.Qt.yellow))
            painter.drawText(rect, align, txt)
            painter.drawRect(rect)
            
            # x, y调整
            x += ColumnWidthList[i]
        
        # 画表体
        x = 0
        y = head_h
        for i in range(columnCount):
            # 表格展现时，每列只要画满n个格子就行了
            for j in range(n):
                # 确定位置
                rect = QRectF(x, y, ColumnWidthList[i], body_h)
                # 绘制填充色
                painter.fillRect(rect, QtGui.QBrush(QtCore.Qt.white))
                # 绘制框线
                painter.drawRect(rect)
                # x, y调整
                y += body_h
            
            # i循环赋值
            x += ColumnWidthList[i]
            y = head_h
        
        
        # 画小计栏
        x = 0
        y = head_h + (n * body_h)
        for i in range(columnCount):
            # 确定位置
            rect = QRectF(x, y, ColumnWidthList[i], Subtotal_h)
            
            # 确定字体
            font = QtGui.QFont(FontNameList[i], FontSizeList[i])
            painter.setFont(font)
            
            # 确定对齐方式
            align = AlignHList[i] | AlignVList[i] | TextWrapList[i]
            
            # 确定内容（第一列固定显示“小计:”字样，之后的只有需要合计栏才有内容，其他都为空白）
            # SumColumnList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
            if i == 0:
                txt = '小计：'
            elif SumColumnList[i] == 1:
                txt = '[Sum]'
            else:
                txt = ''
            
            # 绘制
            painter.fillRect(rect, QtGui.QBrush(QtCore.Qt.yellow))
            painter.drawText(rect, align, txt)
            painter.drawRect(rect)
        
            # x, y调整
            x += ColumnWidthList[i]


        # 画总计栏
        x = 0
        y = head_h + (n * body_h) + Subtotal_h
        for i in range(columnCount):
            # 确定位置
            rect = QRectF(x, y, ColumnWidthList[i], Total_h)
            
            # 确定字体
            font = QtGui.QFont(FontNameList[i], FontSizeList[i])
            painter.setFont(font)
            
            # 确定对齐方式
            align = AlignHList[i] | AlignVList[i] | TextWrapList[i]
            
            # 确定内容（第一列固定显示“小计:”字样，之后的只有需要合计栏才有内容，其他都为空白）
            # SumColumnList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
            if i == 0:
                txt = '总计：'
            elif SumColumnList[i] == 1:
                txt = '[Sum]'
            else:
                txt = ''
            
            # 绘制
            painter.fillRect(rect, QtGui.QBrush(QtCore.Qt.yellow))
            painter.drawText(rect, align, txt)
            painter.drawRect(rect)
            
            # x, y调整
            x += ColumnWidthList[i]
    
    
    def createHandles(self):
        
        lt = HandleSec(parent=self, scene=self.scene)
        lt.setLocationStr('LT')
        
        lm = HandleSec(parent=self, scene=self.scene)
        lm.setLocationStr('LM')
        
        lb = HandleSec(parent=self, scene=self.scene)
        lb.setLocationStr('LB')
        
        mt = HandleSec(parent=self, scene=self.scene)
        mt.setLocationStr('MT')
    
        mb = HandleSec(parent=self, scene=self.scene)
        mb.setLocationStr('MB')
    
        rt = HandleSec(parent=self, scene=self.scene)
        rt.setLocationStr('RT')
        
        rm = HandleSec(parent=self, scene=self.scene)
        rm.setLocationStr('RM')
        
        rb = HandleSec(parent=self, scene=self.scene)
        rb.setLocationStr('RB')
        
        for handle in [lt, lm, lb, mt, mb, rt, rm, rb]:
            handle.locate()
        
        self.setZValue(1.0)
    
    
    def removeHandles(self):
        for handle in self.childItems():
            self.scene().removeItem(handle)
        self.setZValue(0.0)
    
    
    def _arrangeHandles(self):
        for handle in self.childItems():
            handle.locate()
    
    
    def itemChange(self, change, value):
        # 这个需要的。否则鼠标拖动位置过后，再打开属性编辑，位置还是原来的（prop未更新）
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self.prop['Pos'] = self.pos()
        return QtGui.QGraphicsRectItem.itemChange(self, change, value)

    
    def mouseDoubleClickEvent(self, e):
        # QGraphicsSceneMouseEvent
        # 打开属性框（parent设定在view上，否则会出任务框）
        a = Frm_Editor_Table(parent=self.scene().views()[0])
        
        a.setTableProp(self.prop)
        
        dialog_code = a.exec_()
        
        # enum DialogCode { Rejected, Accepted }
        if dialog_code == QtGui.QDialog.Accepted:
            self.updateByProp()
        else:
            pass





class MySection(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MySection, self).__init__(parent, scene)
        
        # 用一个字典，维护Sec属性
        self.prop = {'SecName': '',
                     'SecText': '',
                     'Rect': QRectF(0.0, 0.0, 50.0, 30.0),
                     'Pos': QPointF(30.0, 30.0),
                     'FontName': '宋体',
                     'FontSize': 12,
                     'AlignH': 1,
                     'AlignV': 32,
                     'TextWrap': 256, # 256 singleline, 8192 wrap
                     'BorderWidth': 1,
                     'BorderPenStyle': 1}
        
        
        # 设置大小
        self.setRect(self.prop['Rect'])
        
        # 设置堆叠  The default Z-value is 0.
        self.setZValue(1.0)
        
        # 设置为白色，不要透明的
        brush = QtGui.QBrush(QtCore.Qt.white)
        self.setBrush(brush)
        
        # set hover enable
        self.setAcceptHoverEvents(True)
        
        # 设置可选择  需要加上ItemIsFocusable，才可以接受键盘事件
        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)
        
    
    def load_prop_from_tuple(self, tup):
        # 用一个字典，维护Sec属性
        
        self.prop = {'SecName': tup[0],
                     'SecText': tup[1],
                     'Rect': QRectF(0.0, 0.0, tup[4], tup[5]),
                     'Pos': QPointF(tup[2], tup[3]),
                     'FontName': tup[6],
                     'FontSize': tup[7],
                     'AlignH': tup[8],
                     'AlignV': tup[9],
                     'TextWrap': tup[10],
                     'BorderWidth': tup[11],
                     'BorderPenStyle': tup[12]}
                     
        self.updateByProp()
        
    
    def updateByProp(self):
        # 用此方法刷新Sec
        # 本质是再次调用paint方法刷新
        self.update(self.rect())
        
        self.setPos(self.prop['Pos'])
        self.setRect(self.prop['Rect'])
        
        # 重排handles
        self._arrangeHandles()
    
    
    def posMoveBy(self, direction_str, areaW, areaH):
        # 用于 scene的keyPressEvent事件中
        
        pos = self.pos()
        posX = pos.x()
        posY = pos.y()
        
        rectW = self.rect().width()
        rectH = self.rect().height()
        
        if direction_str == 'L':
            new_posX = max(posX-1, 0)
            new_posY = posY
        elif direction_str == 'R':
            new_posX = min(posX+1, areaW-rectW)
            new_posY = posY
        elif direction_str == 'U':
            new_posX = posX
            new_posY = max(posY-1, 0)
        elif direction_str == 'D':
            new_posX = posX
            new_posY = min(posY+1, areaH-rectH)
        
        self.setPos(new_posX, new_posY)
        
    
    def paint(self, painter, option, widget):
    # QGraphicsItem.paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)
#        pdb.set_trace()
        # 此行还是保留，可以在选中时显示虚线
#        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)
        
        # 设置黑笔，画内容
#        k_pen = QtGui.QPen(QtCore.Qt.black)
#        painter.setPen(k_pen)
        
        painter.fillRect(self.rect(), self.brush())
        
        
        font = QtGui.QFont(self.prop['FontName'], self.prop['FontSize'])
        painter.setFont(font)
        
        # 显示文本
        align_v  = self.prop['AlignV']
        align_h  = self.prop['AlignH']
        textwrap = self.prop['TextWrap']
        painter.drawText(self.rect(), align_v|align_h|textwrap, self.prop['SecText'])
        
        # 显示框线
        k_pen = QtGui.QPen(QtCore.Qt.black)
        k_pen.setWidth(self.prop['BorderWidth'])
        k_pen.setStyle(self.prop['BorderPenStyle'])
        painter.setPen(k_pen)
        painter.drawRect(self.rect())
    
        
    def createHandles(self):
        
        lt = HandleSec(parent=self, scene=self.scene)
        lt.setLocationStr('LT')
        
        lm = HandleSec(parent=self, scene=self.scene)
        lm.setLocationStr('LM')
        
        lb = HandleSec(parent=self, scene=self.scene)
        lb.setLocationStr('LB')
        
        mt = HandleSec(parent=self, scene=self.scene)
        mt.setLocationStr('MT')
    
        mb = HandleSec(parent=self, scene=self.scene)
        mb.setLocationStr('MB')
    
        rt = HandleSec(parent=self, scene=self.scene)
        rt.setLocationStr('RT')
        
        rm = HandleSec(parent=self, scene=self.scene)
        rm.setLocationStr('RM')
        
        rb = HandleSec(parent=self, scene=self.scene)
        rb.setLocationStr('RB')
        
        for handle in [lt, lm, lb, mt, mb, rt, rm, rb]:
            handle.locate()
        
        self.setZValue(1.0)
    
    
    def removeHandles(self):
        for handle in self.childItems():
            self.scene().removeItem(handle)
        self.setZValue(0.0)
    
    
    def _arrangeHandles(self):
        for handle in self.childItems():
            handle.locate()
    
    
    def itemChange(self, change, value):
        # 这个需要的。否则鼠标拖动位置过后，再打开属性编辑，位置还是原来的（prop未更新）
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self.prop['Pos'] = self.pos()
        return QtGui.QGraphicsRectItem.itemChange(self, change, value)

    
    def mouseDoubleClickEvent(self, e):
        # QGraphicsSceneMouseEvent
        # 打开属性框（parent设定在view上，否则会出任务框）
        a = Frm_Editor_Section(parent=self.scene().views()[0])
        
        a.setSecProp(self.prop)
        
        dialog_code = a.exec_()
        
        # enum DialogCode { Rejected, Accepted }
        if dialog_code == QtGui.QDialog.Accepted:
            self.updateByProp()
        else:
            pass
    
    
    def hoverEnterEvent(self, e):
        b = QtGui.QBrush(QtCore.Qt.lightGray)
        self.setBrush(b)
        self.update(self.boundingRect())
    
    
    def hoverLeaveEvent(self, e):
        b = QtGui.QBrush(QtCore.Qt.white)
        self.setBrush(b)
        self.update(self.boundingRect())




class MyFooter(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MyFooter, self).__init__(parent, scene)
        
        # 用一个字典，维护Sec属性（FooterName已经取消）
        self.prop = {
                     'Text': '第{&cp}页 共{&tp}页',
                     'Rect': QRectF(0.0, 0.0, 150.0, 25.0),
                     'Pos': QPointF(30.0, 30.0),
                     'FontName': '宋体',
                     'FontSize': 10,
                     'AlignH': 1,
                     'AlignV': 32,
                     'TextWrap': 256, # 256 singleline, 8192 wrap
                     'BorderWidth': 1,
                     'BorderPenStyle': 0
                     }
        
        # 设置大小
        self.setRect(self.prop['Rect'])
        
        # 设置堆叠  The default Z-value is 0.
        self.setZValue(1.0)
        
        # 设置为白色，不要透明的
        brush = QtGui.QBrush(QtCore.Qt.white)
        self.setBrush(brush)
        
        # set hover enable
        self.setAcceptHoverEvents(True)
        
        # 设置可选择  需要加上ItemIsFocusable，才可以接受键盘事件
        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)
        
    
    def load_prop_from_tuple(self, tp):
        # 用一个字典，维护Sec属性        
        self.prop = {
                     'Text': tp[0],
                     'Rect': QRectF(0.0, 0.0, tp[3], tp[4]),
                     'Pos': QPointF(tp[1], tp[2]),
                     'FontName': tp[5],
                     'FontSize': tp[6],
                     'AlignH': tp[7],
                     'AlignV': tp[8],
                     'TextWrap': tp[9],
                     'BorderWidth': tp[10],
                     'BorderPenStyle': tp[11]
                     }
        self.updateByProp()
        
    
    def updateByProp(self):
        # 用此方法刷新Sec
        # 本质是再次调用paint方法刷新
        self.update(self.rect())
        
        self.setPos(self.prop['Pos'])
        self.setRect(self.prop['Rect'])
        
        # 重排handles
        self._arrangeHandles()
    
    
    def posMoveBy(self, direction_str, areaW, areaH):
        # 用于 scene的keyPressEvent事件中
        
        pos = self.pos()
        posX = pos.x()
        posY = pos.y()
        
        rectW = self.rect().width()
        rectH = self.rect().height()
        
        if direction_str == 'L':
            new_posX = max(posX-1, 0)
            new_posY = posY
        elif direction_str == 'R':
            new_posX = min(posX+1, areaW-rectW)
            new_posY = posY
        elif direction_str == 'U':
            new_posX = posX
            new_posY = max(posY-1, 0)
        elif direction_str == 'D':
            new_posX = posX
            new_posY = min(posY+1, areaH-rectH)
        
        self.setPos(new_posX, new_posY)
        
        
        
    
    def paint(self, painter, option, widget):
    # QGraphicsItem.paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)
        
        # 此行还是保留，可以在选中时显示虚线
#        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)

        # 设置黑笔，画内容
#        k_pen = QtGui.QPen(QtCore.Qt.black)
#        painter.setPen(k_pen)
        
        painter.fillRect(self.rect(), self.brush())
        
        font = QtGui.QFont(self.prop['FontName'], self.prop['FontSize'])
        painter.setFont(font)
        
        # 显示文本
        align_v  = self.prop['AlignV']
        align_h  = self.prop['AlignH']
        textwrap = self.prop['TextWrap']
        painter.drawText(self.rect(), align_v|align_h|textwrap, self.prop['Text'])
        
        # 显示框线
        border_pen = QtGui.QPen(QtCore.Qt.black)
        border_pen.setWidth(self.prop['BorderWidth'])
        border_pen.setStyle(self.prop['BorderPenStyle'])
        painter.setPen(border_pen)
        painter.drawRect(self.rect())
        
        # 保留原来的pen
        ori_pen = painter.pen()
        
        # 追加显示（右边显示F字样，和section区别开来）
        f_pen = QtGui.QPen(QtCore.Qt.blue)
        f_pen.setWidth(2)
        f_pen.setStyle(1)
        f_rect = QtCore.QRectF(self.rect().width()-10.0, 0.0, 10.0, 15.0)
        
        painter.setPen(f_pen)
        painter.drawText(f_rect, 1|32|256, 'F')
        
        painter.setPen(ori_pen)
        
        
        
    def createHandles(self):
        
        lt = HandleSec(parent=self, scene=self.scene)
        lt.setLocationStr('LT')
        
        lm = HandleSec(parent=self, scene=self.scene)
        lm.setLocationStr('LM')
        
        lb = HandleSec(parent=self, scene=self.scene)
        lb.setLocationStr('LB')
        
        mt = HandleSec(parent=self, scene=self.scene)
        mt.setLocationStr('MT')
    
        mb = HandleSec(parent=self, scene=self.scene)
        mb.setLocationStr('MB')
    
        rt = HandleSec(parent=self, scene=self.scene)
        rt.setLocationStr('RT')
        
        rm = HandleSec(parent=self, scene=self.scene)
        rm.setLocationStr('RM')
        
        rb = HandleSec(parent=self, scene=self.scene)
        rb.setLocationStr('RB')
        
        for handle in [lt, lm, lb, mt, mb, rt, rm, rb]:
            handle.locate()
        
        self.setZValue(1.0)
    
    
    def removeHandles(self):
        for handle in self.childItems():
            self.scene().removeItem(handle)
        self.setZValue(0.0)
    
    
    def _arrangeHandles(self):
        for handle in self.childItems():
            handle.locate()
    
    
    def itemChange(self, change, value):
        # 这个需要的。否则鼠标拖动位置过后，再打开属性编辑，位置还是原来的（prop未更新）
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self.prop['Pos'] = self.pos()
        return QtGui.QGraphicsRectItem.itemChange(self, change, value)

    
    def mouseDoubleClickEvent(self, e):
        # QGraphicsSceneMouseEvent
        # 打开属性框（parent设定在view上，否则会出任务框）
        a = Frm_Editor_Footer(parent=self.scene().views()[0])
        a.setFooterProp(self.prop)
        
        dialog_code = a.exec_()
        
        # enum DialogCode { Rejected, Accepted }
        if dialog_code == QtGui.QDialog.Accepted:
            self.updateByProp()
        

    def hoverEnterEvent(self, e):
        b = QtGui.QBrush(QtCore.Qt.lightGray)
        self.setBrush(b)
        self.update(self.boundingRect())

    def hoverLeaveEvent(self, e):
        b = QtGui.QBrush(QtCore.Qt.white)
        self.setBrush(b)
        self.update(self.boundingRect())

        
      
      
class MyLine(QtGui.QGraphicsLineItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MyLine, self).__init__(parent, scene)
        
        # 用一个字典，维护Sec属性
        self.prop = {'LineName': '',
                     'X1': 10,
                     'Y1': 10,
                     'X2': 80,
                     'Y2': 10,
                     'Width': 0.5}
        
        # line是直接继承自GraphicsItem的，所以也有pos函数
        # 设置线条时（setLine），要把起点设置在0,0，终点设置在dx，dy处才可
        dx = self.prop['X2'] - self.prop['X1']
        dy = self.prop['Y2'] - self.prop['Y1']
        self.setLine(0, 0, dx, dy)
        
        #再用设置Pos方法，放置在指定地点(x1, y1)
        self.setPos(self.prop['X1'], self.prop['Y1'])
        
        
        # 设置Pen
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(self.prop['Width'])
        self.setPen(pen)
        
        # set hover enable
#        self.setAcceptHoverEvents(True)
        
        # 设置可选择  需要加上ItemIsFocusable，才可以接受键盘事件
        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)
        
        
    
    
    def load_prop_from_tuple(self, tup):
        # 用一个字典，维护属性
        self.prop = {'LineName': tup[0],
                     'X1': tup[1],
                     'Y1': tup[2],
                     'X2': tup[3],
                     'Y2': tup[4],
                     'Width': tup[5]}
        self.updateByProp()
    
        
    
    def updateByProp(self):
        # 用此方法刷新Sec
        # 本质是再次调用paint方法刷新
        self.update()
        
        # line是直接继承自GraphicsItem的，所以也有pos函数
        # 设置线条时（setLine），要把起点设置在0,0，终点设置在dx，dy处才可
        dx = self.prop['X2'] - self.prop['X1']
        dy = self.prop['Y2'] - self.prop['Y1']
        self.setLine(0, 0, dx, dy)
        
        #再用设置Pos方法，放置在指定地点(x1, y1)
        self.setPos(self.prop['X1'], self.prop['Y1'])
        
        # 设置pen
        pen = self.pen()
        pen.setWidthF(self.prop['Width'])
        self.setPen(pen)
        
        # 重排handles
        self._arrangeHandles()
    
    
    def posMoveBy(self, direction_str, areaW, areaH):
        # 用于 scene的keyPressEvent事件中
        
        # 因为线条斜率不变，只需要调整pos就可
        pos = self.pos()
        posX = pos.x()
        posY = pos.y()
        
        line = self.line()
        dx = line.dx()
        dy = line.dy()
        
        if direction_str == 'L':
            new_pos = QPointF( max(posX-1, 0), posY )
            
        elif direction_str == 'R':
            new_pos = QPointF( min(posX+1, areaW-dx), posY )
            
        elif direction_str == 'U':
            new_pos = QPointF( posX, max(posY-1, 0) )
        
        elif direction_str == 'D':
            new_pos = QPointF( posX, min(posY+1, areaH-dy) )
        
        self.setPos(new_pos)
        
        # 只能这里重排一下，因为已经设了parent了，坐标不是parent坐标！
        self._arrangeHandles()
        
    
    
        
    def createHandles(self):
        
        l = HandleLine(parent=self, scene=self.scene)
        l.setLocationStr('L')
        
        r = HandleLine(parent=self, scene=self.scene)
        r.setLocationStr('R')
        
        for handle in [l, r]:
            handle.locate()
            
        self.setZValue(1.0)
        
        
    def removeHandles(self):
        for handle in self.childItems():
            self.scene().removeItem(handle)
        self.setZValue(0.0)
    
    
    def _arrangeHandles(self):
        for handle in self.childItems():
            handle.locate()
    
    
    def itemChange(self, change, value):
        # 这个需要的。否则鼠标拖动位置过后，再打开属性编辑，位置还是原来的（prop未更新）
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            
            pos = self.pos()
            line = self.line()
            
            self.prop['X1'] = pos.x()
            self.prop['Y1'] = pos.y()
            self.prop['X2'] = line.x2() + pos.x()
            self.prop['Y2'] = line.y2() + pos.y()
        
        return QtGui.QGraphicsLineItem.itemChange(self, change, value)

    
    def mouseDoubleClickEvent(self, e):
        # QGraphicsSceneMouseEvent
        # 打开属性框（parent设定在view上，否则会出任务框）
        
        a = Frm_Editor_Line(parent=self.scene().views()[0])
        
        a.setProp(self.prop)
        
        dialog_code = a.exec_()
        
        # enum DialogCode { Rejected, Accepted }
        if dialog_code == QtGui.QDialog.Accepted:
            self.updateByProp()



class MyImage(QtGui.QGraphicsRectItem):
    
    def __init__(self, parent=None, scene=None):
        
        super(MyImage, self).__init__(parent, scene)
        
        # 用一个字典，维护Sec属性
        self.prop = {'ImageName': '',
                     'Rect': QRectF(0.0, 0.0, 150.0, 100.0),
                     'Pos': QPointF(30.0, 30.0),
                     'ImageBlob': None}
        
        
        # 设置大小
        self.setRect(self.prop['Rect'])
        
        # 设置堆叠  The default Z-value is 0.
#        self.setZValue(1.0)
        
        # 设置为白色，不要透明的
        brush = QtGui.QBrush(QtCore.Qt.white)
        self.setBrush(brush)
        
        # set hover enable
        self.setAcceptHoverEvents(True)
        
        # 设置可选择  需要加上ItemIsFocusable，才可以接受键盘事件
        self.setFlags( QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemSendsGeometryChanges | QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)
        
        pen = QtGui.QPen(QtCore.Qt.transparent)
        self.setPen(pen)
    
    
    def load_prop_from_tuple(self, tup):
        # 用一个字典，维护Sec属性
        self.prop = {'ImageName': tup[0],
                     'Rect': QRectF(0.0, 0.0, tup[3], tup[4]),
                     'Pos': QPointF(tup[1], tup[2]),
                     'ImageBlob': tup[5]}
        self.updateByProp()
    
    
    def updateByProp(self):
        # 用此方法刷新
        # 本质是再次调用paint方法刷新
        self.update(self.rect())
        
        self.setPos(self.prop['Pos'])
        self.setRect(self.prop['Rect'])
        
        # 重排handles
        self._arrangeHandles()
    

    def posMoveBy(self, direction_str, areaW, areaH):
        # 用于 scene的keyPressEvent事件中
        
        pos = self.pos()
        posX = pos.x()
        posY = pos.y()
        
        rectW = self.rect().width()
        rectH = self.rect().height()
#        pdb.set_trace()
        if direction_str == 'L':
            new_posX = max(posX-1, 0)
            new_posY = posY
        elif direction_str == 'R':
            new_posX = min(posX+1, areaW-rectW)
            new_posY = posY
        elif direction_str == 'U':
            new_posX = posX
            new_posY = max(posY-1, 0)
        elif direction_str == 'D':
            new_posX = posX
            new_posY = min(posY+1, areaH-rectH)
        
        self.setPos(new_posX, new_posY)


    def paint(self, painter, option, widget):
    # QGraphicsItem.paint (self, QPainter painter, QStyleOptionGraphicsItem option, QWidget widget = None)
#        pdb.set_trace()
        # 此行还是保留，可以在选中时显示虚线
        QtGui.QGraphicsRectItem.paint(self, painter, option, widget)
        
        # 直接可以从数据库数据生成图片
#        pix = QtGui.QPixmap()
#        pix.loadFromData(self.prop['ImageBlob'])
        
        img_str = self.prop['ImageBlob']
        img_blob = img_str.encode(encoding="utf-8")
        img_blob = base64.b64decode(img_blob)
        
        pix = QtGui.QPixmap()
        pix.loadFromData(img_blob)
        
        
        s_rect = QtCore.QRectF(pix.rect())
        t_rect = self.prop['Rect'].adjusted(1,1,-1,-1)
            
        painter.drawPixmap(t_rect, pix, s_rect)


    def createHandles(self):
        
        lt = HandleSec(parent=self, scene=self.scene)
        lt.setLocationStr('LT')
        
        lm = HandleSec(parent=self, scene=self.scene)
        lm.setLocationStr('LM')
        
        lb = HandleSec(parent=self, scene=self.scene)
        lb.setLocationStr('LB')
        
        mt = HandleSec(parent=self, scene=self.scene)
        mt.setLocationStr('MT')
    
        mb = HandleSec(parent=self, scene=self.scene)
        mb.setLocationStr('MB')
    
        rt = HandleSec(parent=self, scene=self.scene)
        rt.setLocationStr('RT')
        
        rm = HandleSec(parent=self, scene=self.scene)
        rm.setLocationStr('RM')
        
        rb = HandleSec(parent=self, scene=self.scene)
        rb.setLocationStr('RB')
        
        for handle in [lt, lm, lb, mt, mb, rt, rm, rb]:
            handle.locate()
        
        self.setZValue(1.0)
        
        
    def removeHandles(self):
        for handle in self.childItems():
            self.scene().removeItem(handle)
        self.setZValue(0.0)


    def _arrangeHandles(self):
        for handle in self.childItems():
            handle.locate()
    
    
    def itemChange(self, change, value):
        # 这个需要的。否则鼠标拖动位置过后，再打开属性编辑，位置还是原来的（prop未更新）
        if change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self.prop['Pos'] = self.pos()
        return QtGui.QGraphicsRectItem.itemChange(self, change, value)




class HandleSec(QtGui.QGraphicsEllipseItem):
    
    def __init__(self, parent, scene):
        super(HandleSec, self).__init__(parent)
        
        # 设置可拉动
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        
        radius = 3.0
        self.setRect( QRectF(-radius, -radius, radius*2, radius*2) )
        
        self.setAcceptHoverEvents(True)
        
        # 设置颜色
        self.setBrush(QtGui.QBrush(QtCore.Qt.green))
        
        # 设置堆叠
        self.setZValue(1.0)
        
        self.locationStr = ''
        
        self.parent = parent
        self.scene  = scene


    def setLocationStr(self, loc_str):
        self.locationStr = loc_str
    
    
    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        if self.locationStr in ['LT', 'RB']:
            cur = QtGui.QCursor(QtCore.Qt.SizeFDiagCursor)
        elif self.locationStr in ['LM', 'RM']:
            cur = QtGui.QCursor(QtCore.Qt.SizeHorCursor)
        elif self.locationStr in ['LB', 'RT']:
            cur = QtGui.QCursor(QtCore.Qt.SizeBDiagCursor)
        elif self.locationStr in ['MT', 'MB']:
            cur = QtGui.QCursor(QtCore.Qt.SizeVerCursor)
        self.setCursor(cur)
    
    
    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        cur = QtGui.QCursor(QtCore.Qt.ArrowCursor)
        self.setCursor(cur)
    
    
    def _parentWidth(self):
        return self.parent.rect().width()

        
    def _parentHeight(self):
        return self.parent.rect().height()
        
        
        
    def locate(self):
        
        loc_str = self.locationStr
        
        if loc_str == 'LT':
            self.setPos(0, 0)
        elif loc_str == 'LM':
            self.setPos(0, self._parentHeight()/2)
        elif loc_str == 'LB':
            self.setPos(0, self._parentHeight())
        elif loc_str == 'MT':
            self.setPos(self._parentWidth()/2, 0)
        elif loc_str == 'MB':
            self.setPos(self._parentWidth()/2, self._parentHeight())
        elif loc_str == 'RT':
            self.setPos(self._parentWidth(), 0)
        elif loc_str == 'RM':
            self.setPos(self._parentWidth(), self._parentHeight()/2)
        elif loc_str == 'RB':
            self.setPos(self._parentWidth(), self._parentHeight())

    
    def mouseMoveEvent(self, e):
        # 确定位置
        sp = e.scenePos()
        lsp = e.lastScenePos()
        
        # 取得单次偏移量
        dx = sp.x() - lsp.x()
        dy = sp.y() - lsp.y()
        
        # 设置框体新位置（顶排和左排需要设置，其他位点忽略）
        ori_pos = self.parent.pos()
        
        if self.locationStr == 'LT':
            d_pos = QPointF(dx, dy)
            new_pos = ori_pos + d_pos
            new_rect = self.parent.rect().adjusted(0, 0, -dx, -dy)
            
        elif self.locationStr == 'LM':
            d_pos = QPointF(dx, 0)
            new_pos = ori_pos + d_pos
            new_rect = self.parent.rect().adjusted(0, 0, -dx, 0)
            
        elif self.locationStr == 'LB':
            d_pos = QPointF(dx, 0)
            new_pos = ori_pos + d_pos
            new_rect = self.parent.rect().adjusted(0, 0, -dx, dy)
        
        elif self.locationStr == 'MT':
            d_pos = QPointF(0, dy)
            new_pos = ori_pos + d_pos
            new_rect = self.parent.rect().adjusted(0, 0, 0, -dy)
        
        elif self.locationStr == 'MB':
            d_pos = QPointF(0, dy)
            new_pos = ori_pos
            new_rect = self.parent.rect().adjusted(0, 0, 0, dy)
        
        elif self.locationStr == 'RT':
            d_pos = QPointF(0, dy)
            new_pos = ori_pos + d_pos
            new_rect = self.parent.rect().adjusted(0, 0, dx, -dy)
        
        elif self.locationStr == 'RM':
            d_pos = QPointF(dx, 0)
            new_pos = ori_pos
            new_rect = self.parent.rect().adjusted(0, 0, dx, 0)
        
        elif self.locationStr == 'RB':
            d_pos = QPointF(dx, dy)
            new_pos = ori_pos
            new_rect = self.parent.rect().adjusted(0, 0, dx, dy)
        
        
        self.parent.setPos(new_pos)
        self.parent.setRect(new_rect)
        
        self.parent.prop['Pos'] = new_pos
        self.parent.prop['Rect'] = new_rect
        
        # 刷新
        self.parent.updateByProp()


class HandleLine(QtGui.QGraphicsEllipseItem):
    
    def __init__(self, parent, scene):
        super(HandleLine, self).__init__(parent)
        
        # 设置可拉动
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        
        radius = 3.0
        self.setRect( QRectF(-radius, -radius, radius*2, radius*2) )
        
        self.setAcceptHoverEvents(True)
        
        # 设置颜色
        self.setBrush(QtGui.QBrush(QtCore.Qt.green))
        
        # 设置堆叠
        self.setZValue(1.0)
        
        self.locationStr = ''
        
        self.parent = parent
        self.scene  = scene


    def setLocationStr(self, loc_str):
        self.locationStr = loc_str
    
    
    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        cur = QtGui.QCursor(QtCore.Qt.SizeBDiagCursor)
        self.setCursor(cur)
    
    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        cur = QtGui.QCursor(QtCore.Qt.ArrowCursor)
        self.setCursor(cur)
    
        
        
    def locate(self):
        
        loc_str = self.locationStr
        
        # 这里奇怪啊，设定了parent了，应该是设在0 0才对啊
        # lineItem是直接从QGraphicsItem继承的，和Rect不一样。可能是这个原因
        if loc_str == 'L':
            self.setPos( self.parentItem().line().p1() )
        elif loc_str == 'R':
            self.setPos( self.parentItem().line().p2() )


    
    def mouseMoveEvent(self, e):
        # 确定位置
        sp = e.scenePos()
        lsp = e.lastScenePos()
        
        # 取得单次偏移量
        d_pos = sp - lsp
        
        # 设置框体新位置
        ori_line = self.parent.line()
        ori_p1 = ori_line.p1()
        ori_p2 = ori_line.p2()
        
        if self.locationStr == 'L':
            new_p1 = ori_p1+d_pos
            new_p2 = ori_p2

        elif self.locationStr == 'R':
            new_p1 = ori_p1
            new_p2 = ori_p2+d_pos
        
        new_line = QtCore.QLineF(new_p1, new_p2)
        self.parent.setLine(new_line)
        
        mapped_p1 = self.parent.mapToParent(new_p1)
        mapped_p2 = self.parent.mapToParent(new_p2)
        
        self.parent.prop['X1'] = mapped_p1.x()
        self.parent.prop['Y1'] = mapped_p1.y()
        self.parent.prop['X2'] = mapped_p2.x()
        self.parent.prop['Y2'] = mapped_p2.y()
        
        # 重排所有handles
        self.parent.updateByProp()

