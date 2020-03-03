# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keywordContains = scrapy.Field()
    title = scrapy.Field()
    journalName = scrapy.Field()
    abstract  = scrapy.Field()
    keywords = scrapy.Field()
    referenceList = scrapy.Field()
    cityByNumber = scrapy.Field()
    cityBy = scrapy.Field()
    authors = scrapy.Field()
    date = scrapy.Field()
    pass
