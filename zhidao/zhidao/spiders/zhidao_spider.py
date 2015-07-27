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
from scrapy.linkextractors.sgml import SgmlLinkExtractor as sle

from datetime import *

class ZhidaoSpider(CrawlSpider):
    name = "zhidao"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://zhidao.baidu.com"
        ########   "http://zhidao.baidu.com/question/491451027.html"
    ]
    rules = [
        Rule(sle(allow=(r'/question/\d+\.html')), follow=True, callback='parse_item')
    ]

    def parse_item(self, response):
        dt = datetime.now()
        dt_default = "\n" + dt.strftime("%Y-%m-%d %H:%M") + "\n"
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)

        item = ZhidaoItem()
        item['address'] = base_url
        # item['question'] = sel.xpath('//div[@id="wgt-ask"]/h1/span/text()').extract_first(default='')
        # item['questionDetail'] = sel.xpath('//*[@id="wgt-ask"]/pre/text()').extract_first(default='')
        # item['answerDetail'] = sel.css('.line .content > pre::text').extract_first(default='')
        # item['praiseNumber'] = sel.css('div.grid-r.f-aid.mt-15 .evaluate-num-fixed::text').extract()

        # Node: answerDate
        if(len(sel.css('span.grid-r.f-aid.pos-time::text').extract()) > 1):
            item['answerDate'] = sel.css('span.grid-r.f-aid.pos-time::text').extract()[1]
        else:
            item['answerDate'] = sel.css('span.grid-r.f-aid.pos-time::text').extract_first(default=dt_default)

        items.append(item)
        info('parsed ' + str(response))
        return items

    def close_spider(self):
        self.close(CrawlSpider,"Manual Stop...")
