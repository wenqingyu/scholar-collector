#!/usr/bin/python
#coding=utf-8
# 新用户只需要替换14行和15行的orderno和secret即可运行

import base64

def GetProxy():
    # 代理服务器
    proxyServer = "http://http-dyn.abuyun.com:9020"

    # 代理隧道验证信息
    proxyUser = "H1QJT362FBD9I3ND"
    proxyPass = "C58999C0B4576944"

    proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
    result = {
        "Proxy-Authorization":proxyAuth,
        "proxy":proxyServer
    }
    return result