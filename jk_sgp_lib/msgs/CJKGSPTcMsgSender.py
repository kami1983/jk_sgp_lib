# -*- coding: utf-8 -*-

from qcloudsms_py import SmsMultiSender
from qcloudsms_py.httpclient import HTTPError

class CJKGSPTcMsgSender(object) :
    '''
    这个API 用来发送腾讯的短信服务消息
    使用如下配置：
    # 短信发送配置段落
    MSG_CONFIG = {
        'tencent' : {
            # 短信应用 SDK AppID
            'appid' : '1400XXXXX' ,
            # 短信应用 SDK AppKey
            'appkey' : "554d1de0bXXXXXXXXXXXXXXXXX" ,
            # 需要发送短信的手机号码
            'phone_numbers' : ['182XXXXXXXX'] ,
            # 短信模板ID，需要在短信控制台中申请
            'template_id' : '142678' ,
            # 签名
            'sms_sign' : 'KAMI1983',
        }
    }
    '''

    @classmethod
    def SetConfig(cls) :
        '''
        设置配置参数
        '''
    
        msg_config = cls.GasConfig()
        if "tencent" not in msg_config.keys() :
            return cls

        # 从项目的配置文件中读取相应的参数
        # msg_config = crawler.settings.get("MSG_CONFIG", '{}')
        cls.appid = msg_config['tencent']['appid']
        cls.appkey = msg_config['tencent']['appkey']
        cls.phone_numbers = msg_config['tencent']['phone_numbers']
        cls.template_id = msg_config['tencent']['template_id']
        cls.sms_sign = msg_config['tencent']['sms_sign']
        cls.sms_zone = msg_config['tencent']['sms_zone']

        return cls()
    
    @classmethod
    def HasConfig(cls) :
        '''
        判断配置参数是否存在
        @return boolean
        '''
        # 参数赋值
        msg_config = cls.GasConfig()

        if "tencent" not in msg_config.keys() :
            return False
        
        tencent_config_keys = msg_config['tencent'].keys()
        if "appid" not in tencent_config_keys or \
            "appkey" not in tencent_config_keys or \
            "phone_numbers" not in tencent_config_keys or \
            "template_id" not in tencent_config_keys or \
            "sms_sign" not in tencent_config_keys or \
            "sms_zone" not in tencent_config_keys :
            return False
        
        return True

    @classmethod
    def GasConfig(cls) :
        # msg_config = {
        #     'tencent' : {
        #         # 短信应用 SDK AppID
        #         'appid' : 'XXXXX' ,
        #         # 短信应用 SDK AppKey
        #         'appkey' : "XXXXXXX" ,
        #         # 需要发送短信的手机号码
        #         'phone_numbers' : ['XXXXXX'] ,
        #         # 短信模板ID，需要在短信控制台中申请
        #         'template_id' : '142678' ,
        #         # 签名
        #         'sms_sign' : 'XXXXX',
        #         # 短信发送区域
        #         'sms_zone' : '86',
        #     }
        # } 
        msg_config = crawler.settings.get("MSG_CONFIG", {})
        return msg_config

    def sendMsg(self, params) :
        '''
        发送短信消息，传入的params 是短信的参数
        '''
        
        # 参数赋值
        self.SetConfig()
        # print('------ A')
        # print(self.appkey)
        # print('------ B')

        # 短信应用 SDK AppID
        appid = self.appid  # SDK AppID 以1400开头
        # 短信应用 SDK AppKey
        appkey = self.appkey
        # 需要发送短信的手机号码
        phone_numbers = self.phone_numbers
        # 短信模板ID，需要在短信控制台中申请
        template_id = self.template_id  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请
        # 签名
        sms_sign = self.sms_sign  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请
        # 短信区域，中国区域填写86就对了
        sms_zone = self.sms_zone 

        msender = SmsMultiSender(appid, appkey)
        # params = ["页面校对失败"]

        result = msender.send_with_param(sms_zone, phone_numbers,
                template_id, params, sign=sms_sign, extend="", ext="")

        return result
