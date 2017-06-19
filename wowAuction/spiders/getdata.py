# -*- coding: utf-8 -*-
import scrapy


class GetdataSpider(scrapy.Spider):
    name = "getdata"
    allowed_domains = ["battlenet.com.cn"]
    start_urls = ['http://battlenet.com.cn/']

    def parse(self, response):
        pass
