# -*- coding: utf-8 -*-

import scrapy
# import json
# import hashlib
# import pymysql
# import time
# import datetime
# import sys


class AbsJKSGPSpider(scrapy.spiders.Spider):
    # page_idens = []
    check_idens = []
    xpath_idens = []

    name = ""
    allowed_domains = ["basic.10jqka.com.cn"]
    start_urls = [
        "http://basic.10jqka.com.cn/datacenter/cpi.html"
    ]

    def __init__(self, name=None, **kwargs):
        '''
        重写父类构造方法主要是在stat_requests 之前调用 initPageIdenInfo 方法用来初始化页面标识信息
        '''
        super(AbsJKSGPSpider, self).__init__(name)
        
        if '' == self.name :
            raise('ERROR_CONTENT::类内部需要定义爬虫名称 name ERROR_CODE::202001301426')

        self.initPageIdenInfo()

    def start_requests(self):

        '''
        开始请求的方法：
        1、调用 appendCheckInfo(xpath, string) 添加要核验的目标值和目标区域
        '''

        for url in self.start_urls:
            yield scrapy.Request(url=url,method='GET',callback=self.parse_request)

    # def parse(self, response):
    #     pass

    # scrapy.Request 请求的回调方法
    def parse_request(self, response):
        # 强制检查页面标识信息
        self.checkIden(response)
        return self.parseItems(response)
        # print("数据提取ing ....")

    def parseItems(self, response):
        '''
        解析数据项，通过yield 关键字返回对应数据，这个方法是抽象类的抽象方法
        '''
        raise NotImplementedError('需要实现：parseItems (response) 方法，用来返回Item 对象')

    def initPageIdenInfo(self) :
        
        '''
        初始化页面标识信息，通过类内容方法：self.appendCheckInfo(checkxpath, checkcontent) 实现
        参数1：checkxpath 是页面匹配的xpath。
        参数2：checkcontent 是页面匹配的内容值，也就是xpath 解析的内容。
        return void()
        '''
        raise NotImplementedError('需要实现：initPageIdenInfo () 方法，用来添加checkInfo 通过类方法：self.appendCheckInfo(checkxpath, checkcontent) 进行信息追加。')
        
        
    def appendCheckInfo(self, checkxpath, checkcontent) :
        '''
        添加一个匹配数组，checkxpath 是要捕获的xpath ，checkcontent 是对应匹配的内容
        如上两个参数被顺序追加到 self.xpath_idens self.check_idens 里面

        return self
        '''
        # 加入待提取的xpath
        self.xpath_idens.append(checkxpath)
        # 加入后两端追加@ 耳朵符号，以便区别空格
        self.check_idens.append('@' + checkcontent+ '@')
        return self

    # 获取被抓取页面的标识
    def getPageIdens(self, response):
        '''
        通过xpath 获取页面标识的iden 信息，这些信息是实时解析到的。
        
        '''
        page_idens = []
        for getxpath in self.xpath_idens :
             page_idens.append('@' + response.xpath(getxpath).extract()[0].encode('utf-8') + '@')
       
        return page_idens
        
    # 获取要爬取的表格或者页面的标识
    def getCheckIdens(self) :
        return self.check_idens

    def compIdens(self, response) :
        result = True
        check_idens = self.getCheckIdens()
        
        for siden in self.getPageIdens(response) :
            # print(type(check_idens[0].encode('utf-8')))
            if siden not in check_idens :
                result = False

        return result

    # 标识检查函数，如果比对的页面标识出现变化这个函数会直接raise 一个异常信息到页面上
    def checkIden(self, response) :
        if not(self.compIdens(response)) :
            raise Exception("ERROR::数据抓取时检测到页面校对区域发生变化，为了保险起见中断了爬虫的继续运行。 CODE::202001282318")

