# -*- coding: utf-8 -*-
import hashlib

from datetime import datetime

__author__ = 'khainguyen'
from crawl_film.items import CrawlFilmItem
import scrapy


class Hdonline(scrapy.Spider):
    name = "hdonline"
    allowed_domains = ["http://hdonline.vn/"]
    start_urls = [
        "http://hdonline.vn/danh-sach/phim-le.html"
    ]

    def parse(self, response):
        for element in response.xpath('//div[@class="tn-bxitem"]'):
            item = CrawlFilmItem()
            item['image'] = element.xpath('a/span[@class="bxitem-img"]/img/@src').extract_first()
            url = response.urljoin(element.xpath('a/@href').extract_first())
            request = scrapy.Request(url, callback=self.parse_film, dont_filter=True)
            request.meta['film'] = item
            yield request
        next_page = response.xpath('//a[contains(.,"Trang Sau")]/@href').extract_first()
        if next_page:
            url = next_page
            yield scrapy.Request(url, callback=self.parse)

    def parse_film(self, response):
        item = response.meta['film'].copy()
        item['title'] = response.xpath(u'//li[contains(.,"Tên Phim:")]/h1//text()').extract_first('').strip().lower()
        item['url'] = response.url
        item['url_sha1'] = hashlib.sha1(item['url'].encode()).hexdigest()
        item['type'] = 'sub'
        item['quality'] = 'HD'
        item['year'] = response.xpath(u'//li[contains(.,"Năm sản xuất")]/a/text()').extract_first(
            '').strip()
        item['category'] = ','.join(response.xpath(u'//li[contains(.,"Thể loại")]//a/text()').extract())
        item['tags'] = ','.join(response.xpath(u'//div[@class="tn-tagfin" and contains(.,"Từ khóa:")]//a/text('
                                               u')').extract())
        tmp = response.xpath(u'//li[contains(.,"Thời lượng:")]/text()').extract_first('').strip()
        tmp = tmp.split(':')[1]
        item['time'] = tmp.strip()
        item['actor'] = ','.join(response.xpath('//a[@class="tn-pcolor1"]//text()').extract())
        item['imdb'] = response.xpath(
            '//li[img[contains(@src,"http://static.hdonline.vn/templates/frontend/images/imdb.png")]]//text()').extract_first(
            '').strip()
        item['country'] = response.xpath(u'//li[contains(.,"Quốc gia:")]//a/text()').extract_first('').strip()
        item['view'] = response.xpath('//div[@class="film_view_count"]/text()').extract_first('').strip()
        item['description'] = response.xpath('string(//div[@class="tn-contentmt maxheightline-6"])').extract_first(
            '').strip()
        item['crawl_at'] = datetime.utcnow()
        item['source'] = 'hdonline.vn'
        yield item
