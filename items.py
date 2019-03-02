# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy import Field


class LibraryItem(scrapy.Item):
    header = Field()
    id_num = Field()
    conventional_data = Field()
    title_and_response = Field()
    publisher = Field()
    ZTXT = Field()
    language = Field()
    common_remark = Field()
    content_abstract = Field()
    title = Field()
    subject = Field()
    category = Field()
    writer = Field()
    append = Field()
    library_collection = Field()
