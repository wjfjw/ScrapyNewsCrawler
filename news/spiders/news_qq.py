# -*- coding: utf-8 -*-
"""
import scrapy


class NewsQqSpider(scrapy.Spider):
    name = 'news.qq'
    allowed_domains = ['news.qq.com']
    start_urls = ['http://news.qq.com/']

    def parse(self, response):
        pass

"""

import scrapy
import re
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news.items import NewsItem


class NewsqqSpider(CrawlSpider):
    name = 'news.qq'
    allowed_domains = [
        'news.qq.com'
        # 'society.qq.com',
        # 'mil.qq.com',
        # 'cul.qq.com',
        # 'finance.qq.com',
        # 'tech.qq.com'
    ]
    start_urls = [
        'http://news.qq.com',
        'http://www.qq.com'
        #'http://news.qq.com/world_index.shtml',
        #'http://finance.qq.com',
        #'http://tech.qq.com',
    ]
    rules = (
        Rule(
            LinkExtractor( allow = ( '/a/201711\d{2}/\d+\.(htm|html)', )),
            callback = 'parse_newsqq',
            follow = True
        ),
    )

    def parse_newsqq(self, response):
        item = NewsItem()
        item['url'] = self.get_url(response)
        item['title'] = self.get_title(response)
        item['time'] = self.get_time(response)
        item['content'] = self.get_content(response)

        yield {
            'url':item['url'],
            'title':item['title'],
            'time':item['time'],
            'content':item['content'],
        }

    def get_url(self, response):
        if response.url:
            return response.url

    def get_title(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        if title:
            return title

    def get_time(self, response):
        if response.url:
            time = response.url.split('/')[-2]
            if time:
                return time

    def get_content(self, response):
        texts = response.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()').extract()
        content = ''
        for text in texts:
            content += text
        if content:
            pattern = re.compile('\s+')
            content = re.sub(pattern, '', content)
            content = content.replace(",", "，")
            return content

    def contains(self, content, keywords):
        if content:
            for keyword in keywords:
                if keyword in content:
                    return True
