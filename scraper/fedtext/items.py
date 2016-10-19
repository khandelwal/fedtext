# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FedtextItem(scrapy.Item):
    title = scrapy.Field()

    # This is the final URL after all redirects
    response_url = scrapy.Field()

    # The original URL we made our request with
    request_url = scrapy.Field()
    text_list = scrapy.Field()
    word_list = scrapy.Field()
    word_frequency = scrapy.Field()
