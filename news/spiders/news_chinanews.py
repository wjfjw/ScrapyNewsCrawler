# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news.items import NewsItem


class NewschinanewsSpider(CrawlSpider):
    name = 'news.chinanews'
    allowed_domains = [
        'www.chinanews.com'
    ]
    # start_urls = [
    #     'http://www.chinanews.com/scroll-news/2017/1101/news.shtml'
    # ]
    # start_uls = ['http://www.chinanews.com/scroll-news/2017/110' + str(i) + '/news.shtml' for i in range(1, 9)]
    rules = (
        Rule(
            LinkExtractor(allow=('/scroll-news/2017/112\d/news\.(html|htm|shtml)')),
            callback='parse_pass',
            follow=True
        ),
        Rule(
            LinkExtractor( allow=('/(gj|gn|sh|cj|ga|fortune|life)/2017/11-2\d/\d+\.(html|htm|shtml)')),
            callback='parse_newschinanews',
            follow=True
        )
    )

    def start_requests(self):
        pages = []
        for i in range(1, 9):
            url = 'http://www.chinanews.com/scroll-news/2017/112' + str(i) + '/news.shtml'
            page = scrapy.Request(url)
            pages.append(page)
        return pages

    def parse_pass(self, response):
        pass

    def parse_newschinanews(self, response):
        url = self.get_url(response)
        title = self.get_title(response)
        time = self.get_time(response)
        source = '中国新闻网'
        content = self.get_content(response)
        if url and title and time and content:
            item = NewsItem()
            item['url'] = url
            item['title'] = title
            item['time'] = time
            item['source'] = source
            item['content'] = content
            yield {
                'url': item['url'],
                'title': item['title'],
                'time': item['time'],
                'source': item['source'],
                'content': item['content'],
            }

    def get_url(self, response):
        return response.url

    def get_title(self, response):
        title = response.xpath('//div[@id="cont_1_1_2"]/h1/text()').extract_first()
        if title:
            title = re.sub(r'\s+', "", title)
        return title

    def get_time(self, response):
        time = response.xpath('//div[@class="left-t"]/text()').extract_first()
        if time:
            time = re.sub(r'[^0-9]', "", time)
        return time

    def get_content(self, response):
        texts = response.xpath('//div[@class="left_zw"]/p/text()').extract()
        content = ''
        for text in texts:
            content += text
        if content:
            content = re.sub(r'.{0,15}(\d{1,2}月\d{1,2}日)?([电讯]|消息|报道)', "", content)
            content = re.sub(r'[(（【].{0,20}记者.{0,20}[)）】]', "", content)
            content = re.sub(r'[（(].{0,10}[)）]', "", content)
            content = re.sub(r'[\s 　]+', "", content)
            content = content.replace(",", "，")
        return content