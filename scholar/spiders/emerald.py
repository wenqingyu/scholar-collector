# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scholar.items import ArticalItem
from urllib import  parse

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
        articles = response.xpath('//section[@id="search_results__list"]//div[@class="intent_search_result container card-shadow is-animated Search-item__wrapper"]')
        urlResult = parse.urlparse(response.url)
        if urlResult.path == '/insight/search':
            #添加文章详情链接
            for article in articles:
                contentUrl = article.xpath(
                './div//a[@class="intent_link"]/@href').extract()[0]
                if contentUrl:
                    contentUrl = 'https://www.emerald.com' + contentUrl
                yield Request(contentUrl)
            #添加下一页链接
            nextUrl = response.xpath('//a[@class="intent_next_page_link page-link pl-2"]/@href').extract()
            if nextUrl:
                nextUrl = 'http://www.emerald.com/insight/' + nextUrl[0]
                yield Request(nextUrl)
        else:
            #获取具体文章内容
            item['title'] = response.xpath(
                '//*[@id="mainContent"]//h1[@class="intent_article_title mt-0 mb-3"]/text()').extract()[0]
            item['keywordContains'] = ''
            item['journalName'] = urlResult.hostname
            item['abstract'] = response.xpath(
                '//*[@id="abstract"]//p/text()').extract()
            item['date'] = response.xpath(
                '//*[@id="mainContent"]/div[1]/div/div/header/div/div[1]/p[3]/span[1]/text()').extract()[0]
            item['referenceList'] = response.xpath(
                '//section[@class="Citation mb-2"]/p').extract()[0]
            item['keywords'] = response.xpath(
                '//*[@id="keywords_list"]/ul/li//span[@class="intent_text"]/text()').extract()
            authorLabel = response.xpath(
                '//*[@id="intent_contributors"]//a[@class="contrib-search"]')
            item['authors']=[ ]
            for label in authorLabel:
                author = label.xpath('.//span/text()').extract()
                item['authors'].append(' '.join(author))
            
            item['cityByNumber']='123'
            item['cityBy']='123'
            yield item
            pass   