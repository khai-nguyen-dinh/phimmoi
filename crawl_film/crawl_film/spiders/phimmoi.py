# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib

__author__ = 'khainguyen'
import re
from crawl_film.items import CrawlFilmItem
import scrapy


class Phimmoi(scrapy.Spider):
    name = "phimmoi"
    allowed_domains = ["phimmoi.net"]
    start_urls = [
        "http://www.phimmoi.net/phim-le/"
    ]

    def parse(self, response):
        for element in response.xpath('//li[@class="movie-item"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(element), callback=self.parse_film)

        next_page = response.xpath(u'//ul[@class="pagination pagination-lg"]//a[contains(.,'
                                   u'"Trang kế")]/@href').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)


    def parse_film(self, response):
        item = CrawlFilmItem()
        item['title'] = response.xpath('//span[@class="title-1"]/text()').extract_first('').strip().lower()
        item['url'] = response.url
        item['url_sha1'] = hashlib.sha1(item['url'].encode()).hexdigest()
        tmp = response.xpath('//div[@class="movie-l-img"]/img/@src').extract_first('').strip()
        item['image'] = re.search(r"http:(.*).jpg", tmp).group()
        item['type'] = response.xpath(u'//dd[preceding-sibling::dt[contains(.,"Ngôn ngữ:")]][1]//text()').extract_first(
            '').strip()
        item['quality'] = response.xpath(u'//dd[preceding-sibling::dt[contains(.,"Độ phân giải:")]][1]/text('
                                         u')').extract_first(
            '').strip()
        item['year'] = response.xpath(u'//dd[preceding-sibling::dt[contains(.,"Năm:")]][1]//text()').extract_first(
            '').strip()
        item['category'] = ','.join(response.xpath(u'//dd[preceding-sibling::dt[contains(.,"Thể loại:")]][1]//text()[not('
                                             u'contains(.,","))]').extract())
        item['tags'] = ','.join(response.xpath('//ul[@class="tag-list"]//text()').extract())
        item['time'] = response.xpath(
            u'//dd[preceding-sibling::dt[contains(.,"Thời lượng:")]][1]//text()').extract_first('').strip()
        item['actor'] = ','.join(response.xpath('//ul[@id="list_actor_carousel"]//span[@class="actor-name-a"]/text('
                                                ')').extract())
        item['imdb'] = response.xpath('//dd[@class="movie-dd imdb"][1]/text()').extract_first('').strip()
        item['country'] = response.xpath(
            u'//dd[preceding-sibling::dt[contains(.,"Quốc gia:")]][1]//text()').extract_first('').strip()
        item['view'] = response.xpath(u'//dd[preceding-sibling::dt[contains(.,"Lượt xem:")]][1]//text()').extract_first(
            '').strip()
        item['description'] = response.xpath('string(//div[@class="content"])').extract_first('').strip()
        item['crawl_at'] = datetime.utcnow()
        item['source'] = 'phimmoi.net'
        yield item
