# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scholar.items import ArticalItem
from urllib import  parse
from urllib.parse import parse_qs
import re
import json
import requests

start_urls = [
]

qs_list = [
    'leader',
    'leadership',
    'supervisior',
    'followership',
    'follower'
]

pub_list = [
    'Hospitality',
    'tourism',
    'travel',
    'tourist',
    'hotel'
]

for qs in qs_list:
    for pub in pub_list:
        start_urls.append('https://www.sciencedirect.com/search/advanced?qs={0}&pub={1}&date=2000-2020&sortBy=date'.format(qs,pub))



class ScienceSpider(scrapy.Spider):
    name = 'science'
    start_urls = start_urls

    def parse(self, response):
        item = ArticalItem()
        try:
            urlResult = parse.urlparse(response.url)
            queryResult = parse_qs(urlResult.query)
            if urlResult.path == '/search/advanced':
                articles = response.xpath('//ol[@class="search-result-wrapper"]//a[@class="result-list-title-link u-font-serif text-s"]')
                #添加文章详情链接
                for article in articles:
                    contentUrl = article.xpath(
                    '@href').extract()[0]
                    if contentUrl:
                        contentUrl = 'https://www.sciencedirect.com' + contentUrl
                    yield Request(contentUrl + '?' + 'qs=' + queryResult['qs'][0] + '&' + 'pub=' + queryResult['pub'][0])
                #添加下一页链接
                nextUrl = response.xpath('//a[@data-aa-name="srp-next-page"]/@href').extract()
                if nextUrl:
                    nextUrl = 'https://www.sciencedirect.com' + nextUrl[0]
                    yield Request(nextUrl)
            elif '/science/article' in urlResult.path:
                #获取具体文章内容
                articleid = re.search(r'pii/([^?]+)', response.url).group(1)
                titleRegex = response.xpath('.').re('title-text">([^<]+)')
                item['title'] = titleRegex[0] if titleRegex else ''
                item['keywordContains'] = queryResult['qs'][0]
                journalNameResult = response.xpath(
                    '//*[@id="publication-title"]/a/@title').extract()
                item['journalName'] = journalNameResult[0] if journalNameResult else ''
                abstractResult = response.xpath(
                    '//div[@class="abstract author"]//div').extract()
                item['abstract'] = abstractResult if abstractResult else ''
                dateRegex = response.xpath('.').re('Publication date":"([^"]+)')
                item['date'] = dateRegex[0] if dateRegex else ''
                referenceResult = response.xpath(
                    '//*[@class="reference"]').extract()
                item['referenceList'] = referenceResult[0] if referenceResult else ''
                # entitledToken = response.xpath('.').re('entitledToken":"([^"]+)')[0]
                # referenceUrl ='https://www.sciencedirect.com/sdfe/arp/pii/'+articleid+'/references?entitledToken='+entitledToken
                # yield Request(referenceUrl)
                keywordsResult = response.xpath(
                    '//*[@class="keyword"]//span/text()').extract()
                item['keywords'] = keywordsResult if keywordsResult else ''
                authorLabel = response.xpath(
                    '//div[@class="author-group"]//a[@class="author size-m workspace-trigger"]')
                item['authors']=[ ]
                for label in authorLabel:
                    author = label.xpath('.//span/text()').extract()
                    item['authors'].append(' '.join(author))
                citeurl = 'https://www.sciencedirect.com/sdfe/arp/pii/'+articleid+'/citingArticles?creditCardPurchaseAllowed=true&preventTransactionalAccess=false&preventDocumentDelivery=true'
                yield Request(citeurl)
                item['articleId'] = articleid
                item['citeByNumber'] = 0
                item['citeBy']=''
                yield item
                pass   
            else:
                articleid = re.search(r'pii/([^/]+)', response.url).group(1)
                citenumber = json.loads(response.text)
                item['articleId'] = articleid
                item['citeByNumber']= citenumber['hitCount'] if citenumber else 0
                item['citeBy']= citenumber['articles'] if citenumber else 0
                yield item
                pass 
        except:
            print('')