import hashlib
import http.client
import json
import random
import urllib

from Translator.translator import Translator


class Baidu(Translator):
    label = 'baidu'
    name = '百度'
    key = 'text_baidu_translate'

    def __init__(self, config):
        self.update_config(config)

    def update_config(self, config):
        self.working = config['baidu']
        self.appid = config['baidu_appid']
        self.key = config['baidu_key']

    def errorhandel(self, code):
        MAPPING = {
            '52003': "Error:52003 | APP ID或密钥错误",
            '54003': "Error:54003 | 请求过快，你看得似乎有点快",
            '54004': "Error:54004 | 账户余额不足",
            '54005': "Error:54005 | 文本过长",
            '58000': "Error:58000 | 客户端IP非法，请检查百度翻译后台-个人资料中的'IP地址限制'",
            '58002': "Error:58002 | 翻译服务已经关闭，请前往'管理控制台'开启",
            '90107': "Error:90107 | 实名认证未通过或未生效",
        }
        try:
            s = MAPPING[code]
            return s
        except Exception as e:
            print(e)
            return "未知错误"

    def translate(self, text, **kw):
        appid = self.appid
        secretKey = self.key
        httpClient = None
        myurl = '/api/trans/vip/translate'
        fromLang = 'auto'  # 原文语种
        toLang = 'zh'  # 译文语种
        salt = random.randint(32768, 65536)
        q = text
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = (
            myurl
            + '?appid='
            + appid
            + '&q='
            + urllib.parse.quote(q)
            + '&from='
            + fromLang
            + '&to='
            + toLang
            + '&salt='
            + str(salt)
            + '&sign='
            + sign
        )
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            res = json.loads(response.read().decode("utf-8"))
            try:
                code = res['error_code']
                return self.errorhandel(code)
            except Exception as e:
                return res['trans_result'][0]['dst']
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
