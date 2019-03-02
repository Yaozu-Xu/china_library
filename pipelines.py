# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging
import time
from library.settings import ITEM_DIC

logger = logging.getLogger(__name__)


class LibraryPipeline(object):

    def __init__(self):
        self.library_set = set()
        self.db = pymysql.connect(
            host='localhost',
            user='xyz',
            passwd='131865apple',
            db='china_library',
            charset='utf8',
        )
        self.cursor = None

    def open_spider(self, spider):

        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # 检验 是否有数据遗留, 给未捕获的数据赋值空字符串
        for key in ITEM_DIC.values():
            if key not in item:
                item[key] = ''
        try:
            if item['id_num'] not in self.library_set:

                sql_command = "insert into linkdetails(header, id_num, conventional_data, title_and_response, publisher, ZTXT, `language`, common_remark, content_abstract, subject, title, category, writer, append, library_collection) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
                    .format(item['header'], item['id_num'], item['conventional_data'], item['title_and_response'], item['publisher'], item['ZTXT'], item['language'], item['common_remark'], item['content_abstract'], item['subject'], item['title'], item['category'], item['writer'], item['append'], item['library_collection'])
                self.cursor.execute(sql_command)
                self.db.commit()
                print('已入库.......')

            self.library_set.add(item['id_num'])

        except Exception as e:
            logger.warning(time.strftime('%Y-%m-%d %H:%M:%S'))
            logger.warning(e)

    def close_spider(self, spider):

        self.db.close()

