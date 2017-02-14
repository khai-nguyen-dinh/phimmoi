# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib

__author__ = 'khainguyen'
from crawl_film.items import CrawlFilmItem
import scrapy


class Mphim(scrapy.Spider):
    name = "mphim"
    allowed_domains = ["mphim.net"]
    start_urls = [
        "http://mphim.net/phim-le.html"
    ]

    def parse(self, response):
        for element in response.xpath('//ul[@class="list_m"]/li//a/@href').extract():
            yield scrapy.Request(element, callback=self.parse_film)

        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page:
            url = next_page
            yield scrapy.Request(url, callback=self.parse)

    def parse_film(self,response):
        item = CrawlFilmItem()
        item['title'] = response.xpath('//h1[@class="movie-title"]/text()').extract_first('').strip().lower()
        item['url'] = response.url
        item['url_sha1'] = hashlib.sha1(item['url'].encode()).hexdigest()
        item['type'] = response.xpath('//span[@class="m-label lang"]/text()').extract_first('').strip()
        item['quality'] = response.xpath('//span[@class="m-label q"]/text()').extract_first('').strip()
        item['year'] = response.xpath(u'//p[contains(.,"Năm sản xuất:")]/span/text()').extract_first(
            '').strip()
        item['category'] = ','.join(response.xpath(u'//p[contains(.,"Thể loại:")]/span//text()[not(contains(.,",'
                                                   u'"))]').extract())

        item['time'] = response.xpath('//span[@class="m-label ep"]/text()').extract_first('').strip()
        item['actor'] = ','.join(response.xpath(u'//p[contains(.,"Diễn viên:")]/span//text()[not(contains(.,",'
                                                u'"))]').extract())
        item['imdb'] = response.xpath('//span[@class="m-label imdb"]/text()').extract_first('').strip()
        item['country'] = response.xpath(u'//p[contains(.,"Quốc gia:")]/span//text()').extract_first(
            '').strip()
        item['view'] = '0'
        item['description'] = response.xpath('//div[@class="entry entry-m"]/p/text()').extract_first(
            '').strip()
        item['image'] = response.xpath('//img[@class="photo"]/@src').extract_first('').strip()
        item['crawl_at'] = datetime.utcnow()
        item['source'] = 'mphim.net'
        yield item
