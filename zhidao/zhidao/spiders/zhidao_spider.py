import re
import json

from zhidao.items import *
from zhidao.misc.log import *

from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

class ZhidaoSpider(CrawlSpider):
    name = "zhidao"
    allowed_domains = ["baidu.com"]
    start_urls = [
        #"http://zhidao.baidu.com"
        "http://zhidao.baidu.com/question/491451027.html"
    ]
    rules = [
        #Rule(sle(allow=("/question/\d+\.html")), follow=True, callback='parse_item')
        Rule(sle(allow=("/question/491451027.html")), callback='parse_item')
    ]

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)

        item = ZhidaoItem()
        # item['address'] = base_url
        # item['question'] = sel.css('#wgt-ask > h1 > span::text').extract()
        # item['questionDetail'] = sel.css('#wgt-ask > pre:not(#selectsearch-icon)::text').extract()
        # item['answerDetail'] = sel.css('.line .content > pre::text').extract()
        item['praiseNumber'] = sel.css('div.grid-r.f-aid.mt-15 .evaluate-num-fixed::text').extract_first(default='0')
        item['answerDate'] = sel.css('span.grid-r.f-aid.pos-time.mt-15').xpath('text()').extract()
        items.append(item)

        info('DEBUG--> ' + str(item['praiseNumber']))
        info('parsed ' + str(response))
        return items


    def _process_request(self, request):
        info('process ' + str(request))
        return request

