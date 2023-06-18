import json
import urllib3
http=urllib3.PoolManager()

def getInfo(cookie):
    info = json.loads(http.request('GET', 'https://icodecontest-online-api.youdao.com/api/user/info',
                                   headers={'Cookie': cookie,
                                            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 "
                                                          "Firefox/6.0"}).data.decode(
        'utf-8'))
    return info