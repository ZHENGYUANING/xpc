# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class HelloSpider(scrapy.Spider):
    name = 'hello'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    def parse(self, response):
        post_url = "http//:www.jd.com"
        url_list = response.xpath('//ul[@class="JS_navCtn cate_menu"]/li') 
        # print(url_list)
        for post in url_list:
            pid = post.xpath('./a/@href').get()
            request = Request("https:" + pid,callback=self.parse_post)
            request.meta['contain'] = post.xpath("./a/text()").extract_first()
            request.meta['cid'] = post.xpath("./a/@data-index").extract_first()
            print(request)
            yield request 
    def parse_post(self,response):
        urls = response.xpath('//ul[@class="c-list"]/li/a/text()').extract_first()
        
