# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field 

class Postltem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'posts'
    pid = Field()
    title = Field()
    thumbnail = Field()
    preview = Field()
    video = Field()
    category = Field()
    created_at = Field()
    duration = Field()
    play_counts = Field()
    like_counts = Field()
    description = Field()
    video_format = Field()


class Commentltem(scrapy.Item):
    table_name = 'comments'
    commentid = Field()
    pid = Field()
    cid = Field()
    avatar = Field()
    uname = Field()
    created_at = Field()
    like_counts = Field()
    content = Field()
    reply = Field()


class Composerltem(scrapy.Item):
    table_name = 'composers'
    cid = Field()
    banner = Field()
    avatar = Field()
    name = Field()
    verified = Field()
    intro = Field()
    like_counts = Field()
    fans_counts = Field()
    follow_counts = Field()
    location = Field()
    career  = Field()


class Copyrightltem(scrapy.Item):
    table_name = 'copyrights'
    pcid = Field()
    pid = Field()
    cid = Field()
    roles = Field()
