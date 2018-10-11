# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import Settings as settings

from scrapy.pipelines.images import ImagesPipeline
from WebSpider import settings
from scrapy.exceptions import DropItem
from scrapy.http import Request
import codecs
import json
from scrapy.exporters import JsonItemExporter


class WebspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("localhost", "root", "root", "webspider", charset='utf8', )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 要执行的插入sql语句
        insert_sql = """
                        insert into gamerskyreview(rev_title,rev_text,rev_image_urls)
                        VALUES(%s,%s,%s)
                    """

        # 执行sql语句,注意后面是元组，将Item中的数据格式化填充到插入语句中
        self.cursor.execute(insert_sql, (item["rev_title"], item["rev_text"], item["rev_image_urls"]))

        # 将sql语句提交到数据库执行
        self.conn.commint()


# class JsonWithEncondingPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('web.json', 'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False) + '\n'
#         self.file.write(line)
#         return item
#
#     def spider_closed(self, spider):
#         self.file.close()

class JsonExporterPipleline(object):
    # 调用Scrapy的JSON
    def __init__(self):
        self.file = open('webnext.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]  # ok判断是否下载成功
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item
