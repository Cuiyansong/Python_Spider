# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

class ZhidaoItem(Item):
    addr = Field()
    question = Field()
    questionDetail = Field()
    answerDetail = Field()
    praiseNumber = Field()
    answerTime = Field()
    pass