# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ArticlesPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        #读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],  
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
        )
        db = pymysql.connect(dbparams["host"],dbparams["user"],dbparams["passwd"],dbparams["db"],use_unicode=True, charset="utf8" )
        return cls(db)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        cursor= self.dbpool.cursor()

        if item["citeBy"]:
            citeByStr = ''.join(str(v) for v in item["citeBy"])
            cursor.execute('INSERT INTO articles (articles.articleId, articles.citeBy, articles.citeByNumber) VALUES (%s, %s,%s) ON  DUPLICATE KEY UPDATE  citeBy=%s, citeByNumber=%s;',(item["articleId"],citeByStr,item["citeByNumber"],citeByStr,item["citeByNumber"]))
            self.dbpool.commit()
        else:
            cursor.execute('INSERT INTO articles (articles.articleId, keywordContains,title,journalName,abstract,keywords,referenceList,citeByNumber,citeBy,authors,articles.date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON  DUPLICATE KEY UPDATE   keywordContains = %s,title =%s,journalName =%s,abstract=%s,keywords=%s,referenceList=%s,citeByNumber=%s,citeBy=%s,authors=%s,articles.date=%s;',(item["articleId"],item["keywordContains"],item["title"],item["journalName"],' '.join(item["abstract"]),' '.join(item["keywords"]),item["referenceList"],item["citeByNumber"],item["citeBy"],' '.join(item["authors"]),item["date"],item["keywordContains"],item["title"],item["journalName"],' '.join(item["abstract"]),' '.join(item["keywords"]),item["referenceList"],item["citeByNumber"],item["citeBy"],''.join(item["authors"]),item["date"]))
            self.dbpool.commit()
        return item  # 必须实现返回

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print(failue)
