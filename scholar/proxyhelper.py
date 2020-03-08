import requests
import re,os
import telnetlib
import json


def GetProxyAddress():
    try:
        f = open("my_proxies.json", encoding='utf-8') 
        proxy = json.load(f)
        # 测试是否能使用
        telnetlib.Telnet(proxy["ip"], port=proxy["port"], timeout=3)
    except Exception:
        print('unconnected')
        url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=d154fd7868cc58396f52a4d9b758bc51&orderNo=GL20181101134635BxdyEdia&count=1&isTxt=0&proxyType=1'
        res=requests.get(url).json()
        proxyaddress ={
            "ip":res['obj'][0]["ip"],
            "port":res['obj'][0]["port"]
        } 
        filename='my_proxies.json'
        with open(filename,'w') as file_obj:
            json.dump(proxyaddress,file_obj)
        return proxyaddress
    else:
        print('connected successfully')
        return proxy["ip"]+ ':' + proxy["port"]
