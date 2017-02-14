# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib

__author__ = 'khainguyen'
from crawl_film.items import CrawlFilmItem
import scrapy


class Hdviet(scrapy.Spider):
    name = "hdviet"
    allowed_domains = ["movies.hdviet.com"]
    start_urls = [
        "http://movies.hdviet.com/phim-le.html"
    ]

    def parse(self, response):
        for element in response.xpath(u'//ul[@class="cf box-movie-list"]/li'):
            item = CrawlFilmItem()
            item['image'] = element.xpath(u'.//img/@src').extract_first()
            url =element.xpath(u'.//a/@href').extract_first()
            request = scrapy.Request(url, callback=self.parse_film)
            request.meta['film'] = item
            yield request

        next_page = response.xpath('//li[preceding-sibling::li/a[@class="active"]][1]//a/@href').extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)

    def parse_film(self,response):
        item = response.meta['film'].copy()
        item['title'] = response.xpath('//h1[@class="h2-ttl4"]/text()').extract_first('').strip().lower()
        item['url'] = response.url
        item['url_sha1'] = hashlib.sha1(item['url'].encode()).hexdigest()
        item['type'] = 'Vietsub'
        item['quality'] = response.xpath('string(//p[@class="list-icon"])').extract_first('').strip()
        item['year'] = response.xpath(u'//div[span[contains(.,"Năm sản xuất")]]/a/text()').extract_first(
            '').strip()
        item['category'] = ','.join(response.xpath(u'//div[p[contains(.,"Thể loại")]]/a/text()').extract())

        item['time'] = '0'
        item['actor'] = ','.join(response.xpath(u'//div[p[contains(.,"Diễn viên")]]/a/text()').extract())
        item['imdb'] = response.xpath(u'//div[p[contains(.,"Đánh giá")]]/text()[2]').extract_first('').strip()
        item['country'] = response.xpath(u'//div[p[contains(.,"Quốc gia")]]/a/text()').extract_first(
            '').strip()
        item['view'] = '0'
        item['description'] = response.xpath(u'//div[p[contains(.,"Nội dung phim")]]/span/text()').extract_first(
            '').strip()
        item['crawl_at'] = datetime.utcnow()
        item['source'] = 'hdviet.com'
        yield item
