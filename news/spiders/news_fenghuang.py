# -*- coding: utf-8 -*-

import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from news.items import NewsItem


class NewsfenghuangSpider(CrawlSpider):
    name = 'news.fenghuang'
    allowed_domains = [
        'news.ifeng.com'
    ]
    start_urls = [
        # 'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml'
        'http://news.ifeng.com/listpage/11502/2017112' + str(i) + '/1/rtlist.shtml' for i in range(1, 9)
    ]
    rules = (
        Rule(
            LinkExtractor(allow=('/listpage/11502/2017112\d/\d+/rtlist\.(html|htm|shtml)')),
            callback='parse_pass',
            follow=True
        ),
        Rule(
            LinkExtractor( allow=('/a/2017112\d/\d+_0\.(html|htm|shtml)')),
            callback='parse_newsfenghuang',
            follow=True
        )
    )

    def parse_pass(self, response):
        pass

    def parse_newsfenghuang(self, response):
        if not self.category_filter(response):
            return
        url = self.get_url(response)
        title = self.get_title(response)
        time = self.get_time(response)
        source = '凤凰网'
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

    def category_filter(self, response):
        categories = response.xpath('//div[@class="theCurrent cDGray js_crumb"]/a/text()').extract()
        if categories and categories[1] in ['社会', '大陆', '国际', '军事', '港澳']:
            return True
        return False

    def get_url(self, response):
        return response.url

    def get_title(self, response):
        title = response.xpath('//h1[@id="artical_topic"]/text()').extract_first()
        return title

    def get_time(self, response):
        time = response.xpath('//div[@id="artical_sth"]/p/span[@class="ss01"]/text()').extract_first()
        if time:
            time = re.sub(r'[年月日:\s]', "", time)
            time = time[:12]
        return time

    def get_content(self, response):
        texts = response.xpath('//div[@id="main_content"]/p/text()').extract()
        content = ''
        for text in texts:
            if not '原标题' in text:
                content += text
        if content:
            content = re.sub(r'.{0,15}(\d{1,2}月\d{1,2}日)?([电讯]|消息|报道)', "", content)
            content = re.sub(r'[(（【].{0,20}记者.{0,20}[)）】]', "", content)
            content = re.sub(r'[（(].{0,10}[)）]', "", content)
            content = re.sub(r'[\s 　]+', "", content)
            content = content.replace(",", "，")
        return content
