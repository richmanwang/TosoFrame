# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:21:26 2016

@author: 008
"""

#import numpy as np
import pdb


class Bom:
    
    '''
    BOM模块，用来计算各个产品耗材
    
    ---- 关键词约定 ----
    w 成品宽
    h 成品高
    op 操作侧，l或者r
    op_h 拉珠，拉绳长度（是否也可指定百叶棒长？）
    setup 安装方法（顶装c 墙装w） 
    split 分段（轨道用）整数
    
    默认所有成品长度单位为米
    '''
    
    OP_LEFT = 'l'
    OP_RIGHT = 'r'
    
    SETUP_CEILING = 'c'
    SETUP_WALL = 'w'
    
    
    
#    def p_out(self, final_dict):
#        
##        {
##        'data_dict': {'w': 0.49, 'invcode': '01708', 'sosid': 1000204722, 'h': 1.2, 'u8tuple': ('104915', 1000204722, '01708', 0.49, 1.2, '右拉', None), 'socode': '104915'},
##        'mat': {'84112': 1, '89301': 0.51, '84123': 0.49, '84102': 1, '84131': 0.16, '84033': 14.0, '84111': 1, '84122': 1, '89309': 0.08, '85254': 2, '84024': 2, '84135': 0.09, '84121': 2.4, '84115': 2.7, '84104': 2, '84032': 2.8, '84103': 1},
##        'add': {'drums': 2, 'swag_width': 0.31999999999999995, 'swag': 1}
##        }
#        
#        data_dict = final_dict['data_dict']
#        mat = final_dict['mat']
#        add = final_dict['add']
#        
#        print('-----INFO-----')
#        print('u8tuple', data_dict['u8tuple'])
#        
#        
#        print('-----BOM-----')
#        l = sorted(mat.items(), key=lambda d:d[0])
#        
#        for k, v in l:
#            print(k, '\t', v)
#        
#        print('-----ADDITION-----')
#        for k, v in add.items():
#            print(k, '\t', v)
    
    
    def cacu(self, all_inv_list, guige):
        # 用 getattr 函数，动态调用函数，就不用生成一个dict来对应函数名了
        # 只需要一个全部材料清单
#        getattr(object, name[, default]) -> value
#        Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y. 
#        When a default argument is given, it is returned when the attribute doesn't 
#        exist; without it, an exception is raised in that case.
        lst = []
        for invCode in all_inv_list:
            fstr = 'f_01709_' + invCode
            func = getattr(self, fstr)
            value = func(**guige)
            lst.append((invCode, value))
        return lst
    
    
    
    def __piece_func(self, key_value, splitlist, choicelist):
        '''
        对于输入的key_value,按照condlist不同，返回choicelist里的一个值
        splitlist第一位是下限，然后是节点
        '''
#        [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4]
#            [1,   2,   3,   4,   5,   6,   7,   8]
        
#        swag = self.__piece_func(w, [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
        
        # 查找key_value在list内位置并返回结果
        for i, split in enumerate(splitlist):
            if key_value < split:
                return choicelist[i-1]

        # 如果key比任何节点都大，返回最大结果
        return choicelist[-1]
    
    
    
    def define_01709(self):
        """
        定义制作01709所需要的所有的材料清单（每个项目，必须要有函数对应）
        定义为list，通过 getattr 函数，动态调用对应函数 f_01709_xxxxx 并计算出结果
        """
        lst = [
            '89309', #上轨
            '84131', #六角棒1
            '84132', #六角棒2
            '84135', #下轨
            '85254', #绕线轮1
            '84110', #绕线轮2
            '84024', #绳调节器
            '84115', #升降绳
            '84121', #拉珠
            '84122', #拉珠连接器
            '84111', #减速器1
            '84113', #减速器2
            '84102', #端套(薄)
            '84112', #停控
            '84103', #拉珠头
            '84039', #板式管
            '84034', #管布带
            '89301', #毛粘扣
            '84123',  #钩面
            '84104' #吊架
            ]
        return lst
        
        
    def f_01709_89309(self, **kw):
        #上轨
        return (kw['w']-0.0175)/6.0
    
    def f_01709_84131(self, **kw):
        #六角棒1
        value = 0.0
        if kw['w'] <= 3.0:
            value = (kw['w']-0.02)/3.0
        return value
    
    
    def f_01709_84132(self, **kw):
        #六角棒2
        value = 0.0
        if kw['w'] > 3.0:
            value = (kw['w']-0.02)/4.0
        return value
    
    def f_01709_84135(self, **kw):
        #下轨
        return (kw['w']-0.05)/5.0
    
    def f_01709_85254(self, **kw):
        # 绕线轮  需要计算drums
        w = kw['w']
        h = kw['h']
        value = 0
        if (w<1.01 and h<1.59):
            # --计算间距 swag, 及间距宽度swag_width
            swag = self.__piece_func(w, [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
            # --计算绕线轮个数 drums
            drums = swag + 1
            value = drums
        return value
    
    def f_01709_84110(self, **kw):
        # 绕线轮  需要计算drums
        w = kw['w']
        h = kw['h']
        value = 0
        if not (w<1.01 and h<1.59):
            # --计算间距 swag, 及间距宽度swag_width
            swag = self.__piece_func(w, [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
            # --计算绕线轮个数 drums
            drums = swag + 1
            value = drums
        return value
    
    def f_01709_84024(self, **kw):
        # 绳调节器  需要计算drums
        swag = self.__piece_func(kw['w'], [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
        # --计算绕线轮个数 drums
        drums = swag + 1
        value = drums
        return value
    
    def f_01709_84115(self, **kw):
        # 升降绳  需要计算drums  每一个drum一根绳子 每根长度为h+150mm
        swag = self.__piece_func(kw['w'], [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
        # --计算绕线轮个数 drums
        drums = swag + 1
        value = (kw['h']+0.15)*drums
        return value
    
    def f_01709_84121(self, **kw):
        # 拉珠
        return kw['h']*2.0
    
    def f_01709_84122(self, **kw):
        #拉珠连接器
        return 1
    
    def f_01709_84111(self, **kw):
        #减速器1
        value = 0
        if kw['h'] <= 1.4:
            value = 1
        return value
    
    def f_01709_84113(self, **kw):
        #减速器2
        value = 0
        if kw['h'] > 1.4:
            value = 1
        return value
    
    def f_01709_84102(self, **kw):
        #端套
        return 1
    
    def f_01709_84112(self, **kw):
        #停控
        return 1
        
    def f_01709_84103(self, **kw):
        #拉珠头
        return 1
        
    def f_01709_84039(self, **kw):
        #板式管 米数
        # --板式管根数 shapers (向下取整可以直接用int函数)
        w = kw['w']
        h = kw['h']
        if h < 1.01:
            shapers = int(h/0.12)-2
        elif 1.01 <= h <= 4.0:
            shapers = int(h/0.15)-2
        else:
            shapers = int(h/0.3)-2
        value = (w-0.03)*shapers
        return value
    
    def f_01709_84034(self, **kw):
        #管布带 米数
        # --板式管根数 shapers (向下取整可以直接用int函数)
        w = kw['w']
        h = kw['h']
        if h < 1.01:
            shapers = int(h/0.12)-2
        elif 1.01 <= h <= 4.0:
            shapers = int(h/0.15)-2
        else:
            shapers = int(h/0.3)-2
        value = (w+0.02)*shapers
        return value
    
    def f_01709_89301(self, **kw):
        #毛粘扣
        return kw['w'] + 0.02
    
    def f_01709_84123(self, **kw):
        # 钩面
        return kw['h']
    
    def f_01709_84104(self, **kw):
        # 吊架
        brackets = self.__piece_func(kw['w'], [0.0, 1.2, 2.0, 3.0], [2, 3, 4, 5])
        return brackets
        
    
    
    
    
    
    
    
    
    def RS_01709(self, data_dict):
#        对于01709，专有内容只有w和h
        w = float(data_dict['w'])
        h = float(data_dict['h'])
        
        #输出结果集，mat为材料清单，add为补充工艺参数
        mat = {}
        add = {'swag':0, 'swag_width':0, 'drums':0, 'shapers':0}
        
        # 1 上轨
        mat['89309'] = (w-0.0175)/6.0
        
        # 2 六角棒
        if w <= 3.0:
            mat['84131'] = (w-0.02)/3.0
        else:
            mat['84132'] = (w-0.02)/4.0
        
        # 3 下轨
        mat['84135'] = (w-0.05)/5.0
        
        # --计算间距 swag, 及间距宽度swag_width
        swag = self.__piece_func(w, [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
        
        add['swag'] = swag
        add['swag_width'] = (w-0.17)/swag
        
        # --计算绕线轮个数 drums
        drums = swag+1
        add['drums'] = drums
        
        
        # 4 绕线轮
        if (w<1.01 and h<1.59):
            mat['85254'] = drums
        else:
            mat['84110'] = drums
        
        # 5 绳调节器
        mat['84024'] = drums
        
        # 6 升降绳，每一个drum一根绳子 每根长度为h+150mm
        mat['84115'] = (h+0.15)*drums
        
        # 7 拉珠
#        if op_h:
#            mat['84121'] = op_h*2.0
#        else:
        mat['84121'] = h*2.0
        
        # 8 拉珠连接器
        mat['84122'] = 1
        
        # 9 减速器
        if h <= 1.4:
            mat['84111'] = 1
        else:
            mat['84113'] = 1
        
        # 10 端套(薄)
        mat['84102'] = 1
        
        # 11 停控
        mat['84112'] = 1
        
        # 12 拉珠头
        mat['84103'] = 1
    
        # --板式管根数 shapers (向下取整可以直接用int函数)
        if h < 1.01:
            shapers = int(h/0.12)-2
        elif 1.01 <= h <= 4.0:
            shapers = int(h/0.15)-2
        else:
            shapers = int(h/0.3)-2
        add['shapers'] = shapers
        
        # 13 板式管
        mat['84039'] = (w-0.03)*shapers
        
        # 14 管布带
        mat['84034'] = (w+0.02)*shapers
        
        # 15 毛粘扣
        mat['89301'] = w+0.02
        
        # 16 钩面
        mat['84123'] = w
        
        # 17 吊架
        brackets = self.__piece_func(w, [0.0, 1.2, 2.0, 3.0], [2, 3, 4, 5])
        mat['84104'] = brackets

        
        # 返回
        return {'data_dict':data_dict, 'mat':mat, 'add':add}
        






    def RS_01708(self, data_dict):
        # 必须参数 w, h
        w = float(data_dict['w'])
        h = float(data_dict['h'])
        
        #输出结果集，mat为材料清单，add为补充工艺参数
        mat = {}
        add = {'swag':0, 'swag_width':0, 'drums':0}
        
        # 1 上轨
        mat['89309'] = (w-0.0175)/6.0
        
        # 2 六角棒
        if w <= 3.0:
            mat['84131'] = (w-0.02)/3.0
        else:
            mat['84132'] = (w-0.02)/4.0
        
        # 3 下轨
        mat['84135'] = (w-0.05)/5.0
        
        # --计算间距swag, 及间距宽度swag_width
        swag = self.__piece_func(w, [0.0, 0.5, 0.9, 1.4, 1.9, 2.4, 2.9, 3.4], [1, 2, 3, 4, 5, 6, 7, 8])
        
        add['swag'] = swag
        add['swag_width'] = (w-0.17)/swag
        
        # --计算绕线轮个数 drums
        drums = swag+1
        add['drums'] = drums
        
        # 4 绕线轮
        if (w<1.01 and h<1.59):
            mat['85254'] = drums
        else:
            mat['84110'] = drums
        
        # 5 绳调节器
        mat['84024'] = drums
        
        # 6 升降绳，每一个drum一根绳子 每根长度为h+150mm
        mat['84115'] = (h+0.15)*drums
        
        # 7 拉珠
#        if op_h:
#            mat['84121'] = op_h*2.0
#        else:
        mat['84121'] = h*2.0
        
        # 8 拉珠连接器
        mat['84122'] = 1
        
        # 9 减速器
        if h <= 1.4:
            mat['84111'] = 1
        else:
            mat['84113'] = 1
        
        # 10 端套(薄)
        mat['84102'] = 1
        
        # 11 停控
        mat['84112'] = 1
        
        # 12 拉珠头
        mat['84103'] = 1
        
        # 13 圈布带
        mat['84032'] = (h+0.2)*drums
        
        # 14 塑环
        mat['84033'] = (round(h/0.15, 0)-1)*drums
        
        # 15 毛粘扣
        mat['89301'] = w+0.02
        
        # 16 钩面
        mat['84123'] = w
        
        # 17 吊架
        brackets = self.__piece_func(w, [0.0, 1.2, 2.0, 3.0], [2, 3, 4, 5])
        mat['84104'] = brackets
        
        # 保留2位小数
        mat = self.__round_dict(mat)
        
        # 返回
        return {'data_dict':data_dict, 'mat':mat, 'add':add}
        


