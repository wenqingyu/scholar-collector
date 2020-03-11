#!/usr/bin/python
#coding=utf-8
# 新用户只需要替换14行和15行的orderno和secret即可运行

import sys
import time
import hashlib
import requests

def GetProxy():
    _version = sys.version_info

    is_python3 = (_version[0] == 3)

    # 个人中心获取orderno与secret
    orderno = "DT20190528162256iazAC0ZK"    
    secret = "d154fd7868cc58396f52a4d9b758bc51"
    ip = "dynamic.xiongmaodaili.com"
    #按量订单端口
    port = "8088"
    #按并发订单端口
    #port = "8089"

    ip_port = ip + ":" + port

    timestamp = str(int(time.time()))                # 计算时间戳
    txt = ""
    txt = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        txt = txt.encode()

    md5_string = hashlib.md5(txt).hexdigest()                 # 计算sign
    sign = md5_string.upper()                              # 转换成大写
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp + "&change=true"

    #http协议的网站用此配置
    # proxy = {}
    #https协议的网站用此配置
    proxy = {
        "https": "https://" + ip_port,
        "http":"http://" + ip_port
    }
    result = {
        "Proxy-Authorization":auth,
        "proxy":proxy
    }
    return result