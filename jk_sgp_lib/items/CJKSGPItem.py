# -*- coding: utf-8 -*-


import scrapy
import json
import hashlib
# import pymysql
# import time
# import datetime
# import sys

class CJKSGPItem(scrapy.Item):
    '''
    scrapy.Item 的子类
    '''
    
    # 如下是标识列
    t_signkey = scrapy.Field()  # 数据库唯一标识
    t_group = scrapy.Field() # 数据库分组
    t_status = scrapy.Field() # 数据库分组状态

	
    # 构造方法
    def __init__(self, tgroup, tstatus = 1):
        '''
        重写父类构造方法，用来构建特殊的Item 类，主要是构造方法要求必须传入分组信息
        并且这个类增加了 setDbSignKey(signkey) 的方法，用来添加一个用来识别的信息
        如果没有设置setDbSignKey，那么会根据Item 里面所有字段的MD5串生成识别信息，这时候的意义就是数据没有更新不会额外的占用数据列，但是如果数据更新了就会跟着更新
        '''
        super(CJKSGPItem, self).__init__()
        # self['t_group'] = tgroup
        # self['t_status'] = tstatus
        self.setDbGroup(tgroup)
        self.setDbStatus(tstatus)

    def setDbSignKey(self, signkey = '') :
        '''
        signkey 可以不传入，默认是空字符串 ''
        signkey 传入空字符串表示使用数据JSON 作为MD5索引，这时候的意义就是数据没有更新不会额外的占用数据列，但是如果数据更新了就会跟着更新
        '''
        tosignkey = ''
        if '' == signkey :
            tosignkey = self.getMD5Sign(self.getJsonStr())
        else :
            tosignkey = self.getMD5Sign(signkey)
            
        self['t_signkey'] = tosignkey
        return self
    
    def setDbStatus(self, tstatus ) :
        '''
        设置数据库库表状态索引列，默认值为1
        返回值：本类对象
        '''
        self['t_status'] = tstatus
        return self

    def setDbGroup(self, tgroup ) :
        '''
        设置数据库库表分组索引列
        返回值：本类对象
        '''
        if '' == tgroup :
            tgroup = 'DEFAULT'
        self['t_group'] = tgroup
        return self

    def getJsonStr(self) :
        '''
        获取JSON 字符串，这会序列化本对象
        返回值：string
        '''
        return json.dumps(dict(self), ensure_ascii=False)
    
    def getMD5Sign(self, makestr) :
        '''
        获取MD5 标识符号
        返回值：string
        '''
        return hashlib.md5(bytes(makestr)).hexdigest()
