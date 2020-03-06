# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scholar.items import ArticalItem
from urllib import  parse
from urllib.parse import parse_qs
import re

class ScienceSpider(scrapy.Spider):
    name = 'science'
    start_urls = [
        'https://www.sciencedirect.com/search/advanced?qs=Hospitality&date=2020-2021&sortBy=date',
        'https://www.sciencedirect.com/search/advanced?qs=tourism&date=2020-2021&sortBy=date',
        'https://www.sciencedirect.com/search/advanced?qs=travel&date=2020-2021&sortBy=date',
        'https://www.sciencedirect.com/search/advanced?qs=tourist&date=2020-2021&sortBy=date',
        'https://www.sciencedirect.com/search/advanced?qs=hotel&date=2020-2021&sortBy=date'
        ]

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
                    yield Request(contentUrl + '?' + 'qs=' + queryResult['qs'][0])
                #添加下一页链接
                nextUrl = response.xpath('//a[@data-aa-name="srp-next-page"]/@href').extract()
                if nextUrl:
                    nextUrl = 'https://www.sciencedirect.com' + nextUrl[0]
                    yield Request(nextUrl)
            else:
                #获取具体文章内容
                titleRegex = response.xpath('.').re('title-text">([^<]+)')
                item['title'] = titleRegex[0] if titleRegex else ''
                item['keywordContains'] = queryResult['qs'][0]
                item['journalName'] = urlResult.hostname
                abstractResult = response.xpath(
                    '//div[@class="abstract author"]//div').extract()
                item['abstract'] = abstractResult if abstractResult else ''
                dateRegex = response.xpath('.').re('Publication date":"([^"]+)')
                item['date'] = dateRegex[0] if dateRegex else ''
                referenceResult = response.xpath(
                    '//*[@id="cebib0010"]').extract()
                item['referenceList'] = referenceResult[0] if referenceResult else ''

                keywordsResult = response.xpath(
                    '//*[@class="keyword"]//span/text()').extract()
                item['keywords'] = keywordsResult if keywordsResult else ''
                authorLabel = response.xpath(
                    '//div[@class="author-group"]//a[@class="author size-m workspace-trigger"]')
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