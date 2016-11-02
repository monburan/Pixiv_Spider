# -*- coding: utf-8 -*-
import scrapy


class Rank(scrapy.Item):
    """
    this is a item to save pic info
    """
    data_title = scrapy.Field()
    data_rank = scrapy.Field()
    data_score = scrapy.Field()
    data_view = scrapy.Field()
    data_date = scrapy.Field()
    user_name = scrapy.Field()
    illust_id = scrapy.Field()
    illust_type = scrapy.Field()
    illust_details = scrapy.Field()
    details_referer = scrapy.Field()
    image_url = scrapy.Field()
    image_referer = scrapy.Field()
