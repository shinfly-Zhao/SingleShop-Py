"""
@author:zyf
@time:2019/09/03
@filename:YunPian.py
"""
import requests
import json


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【赵云飞】小北  您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        # 同一个手机号同一验证码模板每30秒只能发送一条
        # {'code': 0, 'msg': '发送成功', 'count': 1, 'fee': 0.05, 'unit': 'RMB', 'mobile': '18919488449', 'sid': 45696452454}
        # {'http_status_code': 400, 'code': 2, 'msg': '请求参数格式错误', 'detail': '参数 mobile 格式不正确，mobile:189194884497'}
        return re_dict


# if __name__ == "__main__":
#     yun_pian = YunPian(MPBILEAPIKEY)
#     yun_pian.send_sms("2017", "")
