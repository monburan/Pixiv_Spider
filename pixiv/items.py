# -*- coding: utf-8 -*-
import scrapy

class Rank(scrapy.Item):
	data_title = scrapy.Field()
	user_name = scrapy.Field()
	illust_id = scrapy.Field()
	data_rank = scrapy.Field()
	data_score = scrapy.Field()
	data_view = scrapy.Field()
	data_date = scrapy.Field()
	referer_url = scrapy.Field()
	image_url = scrapy.Field()
	video_zip = scrapy.Field()
