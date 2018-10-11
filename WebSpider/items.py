# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from w3lib.html import remove_tags


def remove_splash(value):
    return value.replace('/', '')


class WebspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GamerskyNewItem(scrapy.Item):
    name = scrapy.Field()
    text = scrapy.Field()
    front_image_url = scrapy.Field()


class GamerskyReviewItem(scrapy.Item):
    rev_title = scrapy.Field()
    rev_text = scrapy.Field()

    rev_image_urls = scrapy.Field()
    rev_images = scrapy.Field()

class GamerskyGameItem(scrapy.Item):
    title = scrapy.Field()
    engtitle = scrapy.Field()
    text = scrapy.Field()

    new_title = scrapy.Field()
    new = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()