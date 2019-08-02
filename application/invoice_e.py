"""
增值税电子发票识别
"""
from apphelper.image import union_rbox
import re
import numpy as np

class invoice_e:
    """
    增值税电子发票结构化识别
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.code()                             #发票代码
        self.number()                           #发票号码
        self.date()                             #开票日期
        self.price()                            #税后金额（小写）
        self.check_code()                         #校验码


    def code(self):
        """
        发票代码识别
        """
        No = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ', '')
            txt = txt.replace(' ', '')
            res = re.findall('代码:\d*', txt)
            res += re.findall('代码\d*', txt)
            if len(res) > 0:
                No['发票代码'] = res[0].replace('代码:', '').replace('代码','')
                self.res.update(No)
                break

    def number(self):
        """
        识别发票号码
        """
        nu = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall('号码:\d*',txt)
            res += re.findall('号码\d*',txt)
            if len(res) > 0:
                nu["发票号码"] = res[0].replace('号码:','').replace('号码','')
                self.res.update(nu)
                break

    def date(self):
        """
        识别开票日期
        """
        da = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall('日期:[0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日',txt)
            res += re.findall('日期:[0-9]{8}', txt)
            res += re.findall('日期[0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日',txt)
            res += re.findall('日期[0-9]{8}', txt)
            if len(res) > 0:
                da["开票日期"] = res[0].replace('日期:','').replace('日期','')
                self.res.update(da)
                break

    def price(self):
        """
        识别税后金额（小写）
        """
        pri = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res5 = re.findall('￥[0-9]{1,8}.[0-9]{1,2}',txt)
#             res5 += re.findall('[0-9]{1,8}.[0-9]{1,2}', txt)
            if len(res5) > 0:
                pri["税后金额"] = res5[0].replace('￥','')
                self.res.update(pri)
                break

    def check_code(self):
        """
        校验码识别
        """
        check = {}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall('校验码:[0-9]{1,20}',txt)
            res += re.findall('校验码[0-9]{1,20}', txt)
            if len(res) > 0:
                check['校验码'] = res[0].replace('校验码:','').replace('校验码','')
                self.res.update(check)
                break
                
                
                
            
            




