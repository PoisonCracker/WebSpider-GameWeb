# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from WebSpider.items import GamerskyReviewItem, GamerskyNewItem, GamerskyGameItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class GamewebSpider(CrawlSpider):
    name = 'gameweb'
    allowed_domains = ['www.gamersky.com']
    start_urls = ['http://www.gamersky.com/']

    rules = (
        Rule(LinkExtractor(allow=r'pcgame/.*'), follow=True),
        # Rule(LinkExtractor(allow=r'news/.*'), callback='parse_news', follow=True),
        Rule(LinkExtractor(allow=r'review/.*'), callback='parse_review', follow=True),
        # Rule(LinkExtractor(allow=r'z/.*'), callback='parse_game', follow=True),
    )

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='C:\Code\Python\Selenium\geckodriver.exe')
        super(GamewebSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print('Spider Closed')
        self.driver.quit()

    def parse_news(self, response):
        news = GamerskyNewItem()
        news['name'] = response.css('.Mid2L_tit h1::text').extract()
        news['text'] = response.css('.Mid2L_con p::text', ).extract()
        print(news)
        yield news

    def parse_review(self, response):
        item = GamerskyReviewItem()
        item['rev_title'] = response.css('.con .tit::text').extract()
        item['rev_text'] = response.css('.MidLcon p::text').extract()
        item['rev_image_urls'] = response.css('.picact::attr(src)').extract()
        print(item)
        yield item

    def parse_game(self, response):
        item_loader = ItemLoader(item=GamerskyGameItem(), response=response)
        item_loader.add_css('title', '.CHtit::text')
        item_loader.add_css('engtitle', '.ENtit::text')
        item_loader.add_css('text', '..YXXX > li:nth-child(6) > div:nth-child(2) > a:nth-child(1)::attr(href)')
        item_loader.add_value('URL', response.url)
        for new_title in response.css('li.li1 > div.t1 > a::text'):
            return item_loader.add_value('new_title', new_title)
        for new in response.css('li.li1 > div.t2 > a::text'):
            return item_loader.add_value('new', new)
        yield item_loader.load_item()
