# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import random
import json
from scrapy import Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scholar.settings import USER_AGENT_LIST
from scholar.proxies import GetProxy
from scholar.proxyhelper import GetProxyAddress

class ScholarSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ScholarDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class GetFailedUrl(RetryMiddleware):
    def __init__(self, settings):
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
        # 将爬取失败的URL存下来，你也可以存到别的存储
            with open(str(spider.name) + ".txt", "a") as f:
                f.write(response.url + "\n")
            return response
        return response

    def process_exception(self, request, exception, spider):
        self.proxy_ip = False
        ## 针对超时和无响应的reponse,获取新的IP,设置到request中，然后重新发起请求
        if '61' in str(exception) or '60' in str(exception):
            self.proxy_ip = GetProxyAddress()
            
        if self.proxy_ip:
            current_proxy = f'http://{self.proxy_ip}'
            request.meta['proxy'] = current_proxy
        
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

class RotateUserAgentMiddleware(UserAgentMiddleware):
    '''
    用户代理中间件（处于下载中间件位置）
    '''
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            request.headers.setdefault('Access-Control-Allow-Credentials', 'false' )
            print(f"User-Agent:{user_agent}")

class MyProxyMidleware(object):
    def process_request(self, request, spider):
        proxy = GetProxy()
        request.headers.setdefault('Proxy-Authorization', proxy['Proxy-Authorization'])
        request.meta["proxy"] = proxy['proxy']

class addressProxyMiddleware(object):
    def process_request(self, request, spider):
        # proxy = random.choice(my_proxies.PROXY)
        # f = open("my_proxies.json", encoding='utf-8') 
        # proxy = json.load(f)
        # request.meta['proxy']  = "http://" + proxy["ip"]+ ':' + proxy["port"]
        request.meta['proxy'] = GetProxy()['proxy']['https']