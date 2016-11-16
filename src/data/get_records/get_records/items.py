# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecordItem(scrapy.Item):
    # Metadata associated once with each record
    # date of plenary
    date = scrapy.Field()
    contributions = scrapy.Field()
