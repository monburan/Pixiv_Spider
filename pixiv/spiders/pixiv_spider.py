# -*- coding: utf-8 -*-

import os
import re
import scrapy
import json
import time
from pixiv.items import Rank

class PixivSpider(scrapy.Spider):

	name = "pixiv"
	#get first response from server,this response have a token"postkey",we can't login without postkey.
	start_urls = ["https://accounts.pixiv.net/login?return_to=http%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=accounts&view_type=page&ref="]

	def parse(self,response):
	#use postkey and first response to login in.
		postkey = self.get_postkey(response)
		return scrapy.FormRequest.from_response(
			response,
			formdata = {
				'pixiv_id':self.settings['PIXIV_ID'],
				'password':self.settings['PASSWORD'],
				'captcha':'',
				'g_recaptcha_response':'',
				'post_key':postkey,
				'source':'pc'
			},
			callback = self.after_login	
		)

	def after_login(self,response):
		
		url = "http://www.pixiv.net/ranking.php?mode=daily&date=%s"%(self.settings['YESTERDAY'])
		yield scrapy.Request(url,callback = self.get_data)

	#get postkey in response.
	def get_postkey(self,response):
		
		value = response.xpath('//input[@class="json-data"]/@value').extract()
		return [j for i,j in json.loads(value[0]).items() if i == "pixivAccount.postKey"][0]

	#make url for this spider,it will return a string or list for image_url.
	#config is a tuple,you can write any what you want.
	#example:config = ("multiple",illust_id,small_pic_url,pic_num)
	def get_data(self,response):	
		
		top50 = response.xpath('//div[@class="ranking-items adjust"]/section')
		for i,section in enumerate(top50):
			item = Rank()
			item["data_title"] = section.xpath('@data-title').extract()[0]
			item["user_name"] = section.xpath('@data-user-name').extract()[0]
			item["illust_id"] = section.xpath('@data-id').extract()[0]
			item["data_rank"] = section.xpath('@data-rank').extract()[0]
			item["data_score"] = section.xpath('@data-total-score').extract()[0]
			item["data_view"] = section.xpath('@data-view-count').extract()[0]
			item["data_date"] = section.xpath('@data-date').extract()[0]
			self.illust_type(item,section)
			referer = item["details_referer"] if "details_referer" in item.keys() else response.url
			yield scrapy.Request(
				item["illust_details"],
				headers = {"Referer": referer},
				meta = {'item':item},
				callback = self.illust_details
				)
	def illust_type(self,item,section):
		_type = section.xpath('div/a/@class').extract()[0]
		domain = 'http://www.pixiv.net/'
		#single
		if _type == 'work  _work ':
			item["illust_type"] = "single"
			item["illust_details"] = domain + '&'.join(section.xpath('div/a/@href').extract()[0].split('&')[0:2])
		
		#multipe and manga multiple
		if _type in ['work  _work multiple ','work  _work manga multiple ']:
			item["illust_type"] = "multiple"
			details = domain + '&'.join(section.xpath('div/a/@href').extract()[0].split('&')[0:2])
			item["illust_details"] = re.sub("medium","manga",details)
		
		#like a manga book
		if _type == 'work  _work multiple rtl ':
			item["illust_type"] = "multiple rtl"
			details = domain + '&'.join(section.xpath('div/a/@href').extract()[0].split('&')[0:2])
			item["illust_details"] = re.sub("medium","manga",details)
		
		#manga
		if _type == 'work  _work manga ':
			item["illust_type"] = "manga"
			details = domain + '&'.join(section.xpath('div/a/@href').extract()[0].split('&')[0:2])
			item["illust_details"] = re.sub("medium","big",details)
			item["details_referer"] = details
	
		#ugoku
		if _type == 'work  _work ugoku-illust ':
			item["illust_type"] = "ugoku"
			item["illust_details"] = domain + '&'.join(section.xpath('div/a/@href').extract()[0].split('&')[0:2])

	def make_url(self,response):
		item = response.meta['item']
		pages = response.meta['page']
		url = response.xpath('//img/@src').extract()[0].split('p0')
		item["image_url"] = ["%sp%s%s"%(url[0],str(page),url[1]) for page in range(int(pages))]
		
		if self.check_file(item["image_url"]) == False:
				yield item
	def illust_details(self,response):
		item = response.meta['item']
		item['image_referer'] = response.url
				
		if item["illust_type"] == "single":
			item["image_url"] = response.xpath('//img[@class="original-image"]/@data-src').extract()

		if item["illust_type"] == "multiple":
			page = response.xpath('//span[@class="total"]/text()').extract()[0]
			url = re.sub("manga","manga_big",response.url) + '&page=0'
			yield scrapy.Request(
					url,
					meta ={'item':item,'page':page},
					callback = self.make_url
			)

		if item["illust_type"] == "manga":
			item["image_url"] = response.xpath('//img/@src').extract()

		if item["illust_type"] == "video":
			findzip =[zip for zip in response.xpath('//script').extract() if 'ugokuIllust' in zip]
			result = re.compile('ugokuIllustFullscreenData.*?:"(.*?)",').search(findzip[0]).group(1)
			#result like this -> http:\/\/i1.pixiv.net\/img-zip-ugoira\/img\/2016\/08\/08\/22\/42\/55\/58329284_ugoira1920x1080.zip
			#we need  process it
			item["image_url"] = re.sub(r"\\","",result)

		if item["illust_type"] == "multiple rtl":
			pass
		try:		
			if self.check_file(item["image_url"]) == False:
				yield item
		except KeyError:
			pass
		#this item will like this
		#{'data_date': u'2016\u5e7408\u670810\u65e5 00:02',
		# 'data_rank': u'18',
 		# 'data_score': u'6791',
		# 'data_title': u'\u7121\u984c',
  		# 'data_view': u'11167',
		# 'illust_id': u'58351449',
 		# 'image_url': [u'http://i2.pixiv.net/img-original/img/2016/08/10/01/38/56/58351449_p0.jpg'],
        # 'referer_url': 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=58351449',
        # 'user_name': u'avamone'}

	def check_file(self,image_url):
		filename = image_url[0].split('/')[-1]
		if os.path.exists(self.settings['FILES_STORE'].decode("utf-8")+'image/'+filename):
			print "exist"
			return True
		else:
			return False
