"""
@author:zyf
@time:2019/09/29
@filename:xcu.py
"""
import requests
from datetime import datetime,timedelta
from random import Random
import hashlib
import xmltodict
import time
class WXPay():
    def __init__(self,openid):
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        # self.openid = "oKJfI5Zxs3Rb1wO5JP0tmu5aGjrk"
        self.openid = openid
        self.mch_id = "1555774801"
        self.appid = "wx89158d2f92715d25"
        self.key = "megene2019xupeng2019megene2019xp"



    def pay(self,ip,nonce_str,total_fee,out_trade_no):
        data = {
            "appid": self.appid, # 小程序ID
            "mch_id": self.mch_id, # 商户号
            "nonce_str":nonce_str, # 随机字符串
            "body": "Megenex-Megenex", # 商品描述
            "out_trade_no": out_trade_no, # 商户订单号
            "total_fee": total_fee,         # 标价金额
            "spbill_create_ip":ip,   # 终端IP
            "notify_url": "https://api.zhaoyunfei.vip/getpay/", # 通知地址
            "trade_type": "JSAPI", # 交易类型
            "openid": self.openid # 用户openid
        }

        stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        data["sign"] = sign.upper()

        xml = []
        for k in sorted(data.keys()):
            v = data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        xml = '<xml>{}</xml>'.format(''.join(xml))
        response = requests.post(self.url, data=xml)
        redata = response.content

        wx_redata = dict(xmltodict.parse(redata, encoding="utf-8"))
        wx_redata["xml"]["openid"] = self.openid
        # wx_redata["out_trade_no"] = self.
        return wx_redata["xml"]

    def get_paysign(self, prepay_id,nonceStr):
        pay_data = {
            'appId': self.appid,
            'nonceStr': nonceStr,
            'package': "prepay_id=" + prepay_id,
            'signType': 'MD5',
            'timeStamp':str(int(time.time()))
        }
        import hashlib
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper() # 返回给小程序的签名

class WXPcPlay():
    def __init__(self):
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        self.openid = "oKJfI5Zxs3Rb1wO5JP0tmu5aGjrk"
        self.mch_id = "1555774801"
        self.appid = "wx89158d2f92715d25"
        self.key = "megene2019xupeng2019megene2019xp"

    def pay(self, ip, nonce_str, total_fee, out_trade_no):
        data = {
            "appid": self.appid,  # 小程序ID
            "mch_id": self.mch_id,  # 商户号
            "nonce_str": nonce_str,  # 随机字符串
            "body": "Megenex-Megenex",  # 商品描述
            "out_trade_no": out_trade_no,  # 商户订单号
            "total_fee": total_fee,  # 标价金额
            "spbill_create_ip": ip,  # 终端IP
            "notify_url": "https://api.zhaoyunfei.vip/getpay/",  # 通知地址
            "trade_type": "JSAPI",  # 交易类型
            "openid": self.openid  # 用户openid
        }
        stringA = '&'.join(["{0}={1}".format(k, data.get(k)) for k in sorted(data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        data["sign"] = sign.upper()

        xml = []
        for k in sorted(data.keys()):
            v = data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        xml = '<xml>{}</xml>'.format(''.join(xml))
        response = requests.post(self.url, data=xml)
        redata = response.content

        wx_redata = dict(xmltodict.parse(redata, encoding="utf-8"))
        return wx_redata["xml"]

    def get_paysign(self, prepay_id,nonceStr):
        pay_data = {
            'appId': self.appid,
            'nonceStr': nonceStr,
            'package': "prepay_id=" + prepay_id,
            'signType': 'MD5',
            'timeStamp':str(int(time.time()))
        }
        import hashlib
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper() # 返回给小程序的签名


