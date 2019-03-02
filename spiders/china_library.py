# -*- coding: utf-8 -*-
import scrapy
import re
from library.settings import ITEM_DIC
from scrapy import Request
from library.items import LibraryItem
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


key = 'CLC = "p4?"'
start_url = 'http://opac.nlc.cn/F/'
query_params = 'func=short-jump&jump='


class ChinaLibrarySpider(scrapy.Spider):
    # 20min刷新
    name = 'china_library'
    allowed_domains = ['opac.nlc.cn/F']
    base_url = 'http://opac.nlc.cn/F'
    index = 1

    def start_requests(self):
        browser = webdriver.Chrome()
        browser.get(self.base_url)
        span = browser.find_element_by_xpath('//*[@id="indexpage"]/form/div[1]/table/tbody/tr/td[3]/span')
        action = ActionChains(browser)
        action.move_to_element(span)

        # 悬浮在span后显示菜单栏
        search_btn = browser.find_element_by_xpath('//*[@id="advlist"]/a[4]')
        action.click(search_btn)
        action.perform()
        search_input = browser.find_element_by_xpath('//*[@id="small"]/input')
        submit_btn = browser.find_element_by_xpath('//*[@id="baseinfo"]/table/tbody/tr[5]/td[2]/input')
        search_input.clear()
        search_input.send_keys(key)
        submit_btn.click()
        now_url = browser.current_url

        # 获得防伪码
        url_code = self.parse_url(now_url)
        # 当前页x对应 的url： jump=(x-1)*10+1
        for i in range(1, 101):
            # [1-100]
            jump = (i - 1) * 10 + 1
            page_url = 'http://opac.nlc.cn/F/{}?func=short-jump&jump={}'.format(url_code, jump)
            print('url解析完成...')
            yield Request(page_url, callback=self.parse_first, dont_filter=True)

    def parse_first(self, response):
        print('解析第一步....')
        selector = response.selector
        a_tags = selector.xpath('//div[@class="itemtitle"]/a[1]/@href')
        for a in a_tags:
            detail_url = a.extract()
            yield Request(detail_url, callback=self.parse_article, dont_filter=True)

    def parse_article(self, response):
        print('开始解析文章.....')
        collection = False
        res_item = LibraryItem()
        selector = response.selector
        items_name = selector.xpath('//*[@id="bold"]/text()')
        items_value = selector.xpath('//*[@id="td"]/tr/td[2]').xpath('string(.)')

        for name, value in zip(items_name, items_value):
            # 去除换行
            n = name.extract().strip().replace("\n", '').replace("\r", '')
            if n in ITEM_DIC:
                v = value.extract().strip().replace("\n", '').replace("\r", '')
                key = ITEM_DIC[n]

                if key == 'library_collection':

                    # 判断是否第一次抓取馆藏信息
                    if collection:
                        temp = res_item[key]
                        res_item[key] = temp + v + " "
                    else:
                        res_item[key] = v
                        collection = True
                else:
                    res_item[key] = v
        print('已爬取{}条数据'.format(self.index))
        self.index += 1
        yield res_item

    @staticmethod
    def parse_url(url):
        """
        :param url: 目标url
        :return:  返回url 防伪码
        """
        res = re.findall('http://opac.nlc.cn/F/(.*?)\\?', url)[0]
        return res
