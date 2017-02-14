# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from crawl_film import settings
from sqlalchemy import *
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CrawlFilmPipeline(object):
    def __init__(self):
        db = create_engine(URL(**settings.DATABASE))
        self.logger = logging.getLogger()
        Session = sessionmaker(bind=db)
        Session.configure(bind=db)
        session = Session()
        Base.metadata.create_all(db)
        self.session = session

    def process_item(self, item, spider):
        self.insert_data(item)
        return item

    def insert_data(self, item):
        if not self.check_exist(item):
            return
        try:
            phim = Phim(url_sha1=item.get('url_sha1'),
                        title=item.get('title').encode('utf-8'),
                        url=item.get('url'),
                        image=item.get('image'),
                        type=item.get('type'),
                        quality=item.get('quality'),
                        year=item.get('year'),
                        category=item.get('category'),
                        tags=item.get('tags'),
                        description=item.get('description'),
                        time=item.get('time'),
                        actor=item.get('actor'),
                        imdb=item.get('imdb'),
                        view=item.get('view'),
                        country=item.get('country'),
                        source=item.get('source'),
                        crawl_at=item.get('crawl_at')
                        )
            self.session.add(phim)
            self.session.commit()
        except Exception as e:
            self.logger.error(e)

    def check_exist(self, item):
        tmp = self.session.query(Phim).filter_by(url_sha1=item.get('url_sha1')).first()
        if tmp:
            return False
        return True


class Phim(Base):
    __tablename__ = 'films'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url_sha1 = Column(String(40, collation='utf8_bin'))
    title = Column(Text(collation='utf8_bin'))
    url = Column(String(2083, collation='utf8_bin'))
    image = Column(String(2083, collation='utf8_bin'))
    type = Column(String(255, collation='utf8_bin'))
    quality = Column(String(100, collation='utf8_bin'))
    year = Column(String(10, collation='utf8_bin'))
    category = Column(Text(collation='utf8_bin'))
    tags = Column(Text(collation='utf8_bin'))
    description = Column(Text(collation='utf8_bin'))
    time = Column(String(10, collation='utf8_bin'))
    actor = Column(Text(collation='utf8_bin'))
    imdb = Column(String(40, collation='utf8_bin'))
    view = Column(String(10, collation='utf8_bin'))
    country = Column(String(255, collation='utf8_bin'))
    source = Column(String(255, collation='utf8_bin'))
    crawl_at = Column(DateTime)
