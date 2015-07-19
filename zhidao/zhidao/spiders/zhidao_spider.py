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
        #Rule(sle(allow=("/question/^\d$.html\?fr=iks&word=^\w+$&ie=gbk")), follow=True, callback='parse_item')
        #Rule(sle(allow=("/question/\d+\.html")), follow=True, callback='parse_item')
        #http://zhidao.baidu.com/question/491451027.html
        Rule(sle(allow=("/question/491451027.html")), callback='parse_item')
    ]

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)

        item = ZhidaoItem()
        item['addr'] = base_url
        item['question'] = sel.css('#wgt-ask > h1 > span::text').extract()
        item['questionDetail'] = sel.css('#wgt-ask > pre:not(#selectsearch-icon)::text').extract()
        item['answerDetail'] = sel.css('.line .content > pre::text').extract()
        # item['praiseNumber'] = sel.css('#wgt-ask > h1 > span').extract()
        item['answerDate'] = sel.css('span.grid-r.f-aid.pos-time.mt-15:nth-child(1)::text').extract()
        items.append(item)

        #sites = sel.css('ask-title')
        #sites_even = sel.css('table.tablelist tr.even')
        # for site in sites_even:
        #     item = ZhidaoItem()
        #     item['name'] = site.css('.l.square a').xpath('text()').extract()[0]
        #     relative_url = site.css('.l.square a').xpath('@href').extract()[0]
        #     item['detailLink'] = urljoin_rfc(base_url, relative_url)
        #     item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()[0]
        #     item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()[0]
        #     item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()[0]
        #     item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()[0]
        #     items.append(item)
        #     #print repr(item).decode("unicode-escape") + '\n'
        #
        # sites_odd = sel.css('table.tablelist tr.odd')
        # for site in sites_odd:
        #     item = ZhidaoItem()
        #     item['name'] = site.css('.l.square a').xpath('text()').extract()[0]
        #     relative_url = site.css('.l.square a').xpath('@href').extract()[0]
        #     item['detailLink'] = urljoin_rfc(base_url, relative_url)
        #     item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()[0]
        #     item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()[0]
        #     item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()[0]
        #     item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()[0]
        #     items.append(item)
        #     #print repr(item).decode("unicode-escape") + '\n'

        info('parsed ' + str(response))
        return items


    def _process_request(self, request):
        info('process ' + str(request))
        return request

