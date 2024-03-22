# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    upload_user = scrapy.Field()
    upload_time = scrapy.Field()
    novel_name = scrapy.Field()
    novel_href = scrapy.Field()
    novel_context = scrapy.Field()
