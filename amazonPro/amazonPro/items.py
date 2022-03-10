# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonproItem(scrapy.Item):

    title = scrapy.Field()
    rank = scrapy.Field()
    keyword_rank = scrapy.Field()
    asin = scrapy.Field()
