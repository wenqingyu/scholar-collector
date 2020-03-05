# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scholar.items import ArticalItem
from urllib import  parse
from urllib.parse import parse_qs
import re

class EmeraldSpider(scrapy.Spider):
    name = 'emerald'
    start_urls = [
        'http://www.emerald.com/insight/search?q=Hospitality&fromYear=2020',
        'http://www.emerald.com/insight/search?q=tourism&fromYear=2020',
        'http://www.emerald.com/insight/search?q=travel&fromYear=2020',
        'http://www.emerald.com/insight/search?q=tourist&fromYear=2020',
        'http://www.emerald.com/insight/search?q=hotel&fromYear=2020'
        ]

    def parse(self, response):
        item = ArticalItem()
        try:
            articles = response.xpath('//section[@id="search_results__list"]//div[@class="intent_search_result container card-shadow is-animated Search-item__wrapper"]')
            urlResult = parse.urlparse(response.url)
            queryResult = parse_qs(urlResult.query)
            if urlResult.path == '/insight/search':
                #添加文章详情链接
                for article in articles:
                    contentUrl = article.xpath(
                    './div//a[@class="intent_link"]/@href').extract()[0]
                    if contentUrl:
                        contentUrl = 'https://www.emerald.com' + contentUrl
                    yield Request(contentUrl + '?' + 'q=' + queryResult['q'][0])
                #添加下一页链接
                nextUrl = response.xpath('//a[@class="intent_next_page_link page-link pl-2"]/@href').extract()
                if nextUrl:
                    nextUrl = 'http://www.emerald.com/insight/' + nextUrl[0]
                    yield Request(nextUrl)
            else:
                #获取具体文章内容
                titleRegex = response.xpath('.').re("intent_article_title[^>]+>([^<]+)")
                item['title'] = titleRegex[0] if titleRegex else ''
                item['keywordContains'] = queryResult['q'][0]
                item['journalName'] = urlResult.hostname
                abstractResult = response.xpath(
                    '//*[@id="abstract"]//p/text()').extract()
                item['abstract'] = abstractResult if abstractResult else ''
                dateRegex = response.xpath('.').re("\d+\s*[a-zA-Z]+\s*2020")
                item['date'] = dateRegex[1] if dateRegex else ''
                referenceResult = response.xpath(
                    '//section[@class="Citation mb-2"]/p').extract()
                item['referenceList'] = referenceResult[0] if referenceResult else ''

                keywordsResult = response.xpath(
                    '//*[@id="keywords_list"]/ul/li//span[@class="intent_text"]/text()').extract()
                item['keywords'] = keywordsResult if referenceResult else ''
                authorLabel = response.xpath(
                    '//*[@id="intent_contributors"]//a[@class="contrib-search"]')
                item['authors']=[ ]
                for label in authorLabel:
                    author = label.xpath('.//span/text()').extract()
                    item['authors'].append(' '.join(author))
                
                item['citeByNumber']=''
                item['citeBy']=''
                yield item
                pass   
        except:
            print('')