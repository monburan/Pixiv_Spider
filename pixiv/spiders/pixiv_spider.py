# -*- coding: utf-8 -*-
import scrapy
import json
import time
import re
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
		
		yield scrapy.Request(self.make_url(config = "yesterday"),callback = self.get_data)

	#get postkey in response.
	def get_postkey(self,response):
		
		value = response.xpath('//input[@class="json-data"]/@value').extract()
		return [j for i,j in json.loads(value[0]).items() if i == "pixivAccount.postKey"][0]

	#make url for this spider,it will return a string or list for image_url.
	#config is a tuple,you can write any what you want.
	#example:config = ("multiple",illust_id,small_pic_url,pic_num)
	def make_url(self,config):

		if "yesterday" in config:
			return "http://www.pixiv.net/ranking.php?mode=daily&date=%s"%(self.settings['YESTERDAY'])
		
		if "detail_url" in config:
			return "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s"%(config[1])
		
		if "multiple" in config:
			domain = config[2].split('/')[2]
			date = "/".join(config[2].split('/')[-7:-1])
			image_type = config[2].split('.')[-1]
			return ["http://%s/img-original/img/%s/%s_p%s.%s"%(domain,date,config[1],page,image_type) for page in range(config[3])]
	
		if "manga" in config:
			return "http://www.pixiv.net/%s"%(config[1])
		
	def get_data(self,response):	
		
		top50 = response.xpath('//div[@class="ranking-items adjust"]/section')
		for i,one in enumerate(top50):
			item = Rank()
			item["data_title"] = one.xpath('@data-title').extract()[0]
			item["user_name"] = one.xpath('@data-user-name').extract()[0]
			item["illust_id"] = one.xpath('@data-id').extract()[0]
			item["data_rank"] = one.xpath('@data-rank').extract()[0]
			item["data_score"] = one.xpath('@data-total-score').extract()[0]
			item["data_view"] = one.xpath('@data-view-count').extract()[0]
			item["data_date"] = one.xpath('@data-date').extract()[0]
			yield scrapy.Request(
				self.make_url(("detail_url",item["illust_id"])),
				headers = {"Referer":response.url},
				meta = {'item':item},
				callback = self.illust_details
				)

	def illust_details(self,response):
		item = response.meta['item']
		item['referer_url'] = response.url
		
		#check this illust's type
		sinple = response.xpath('//img[@class="original-image"]/@data-src').extract()
		multiple = response.xpath('//ul[@class="meta"]/li').re("(\d+)P")
		manga = response.xpath('//a[@class=" _work manga "]/@href').extract()
		video = response.xpath('//div[@class="player toggle"]').extract()
		
		if sinple:
			item["image_url"] = sinple
		
		if multiple:
			small = response.xpath('//div[@class="_layout-thumbnail"]/img/@src').extract()[0]
			item["image_url"] = self.make_url(("multiple",item["illust_id"],small,int(multiple[0])))
		
		if manga:
			item["image_url"] = [self.make_url(("manga",manga[0]))]
		
		if video:
			findzip =[zip for zip in response.xpath('//script').extract() if 'ugokuIllust' in zip]
			result = re.compile('ugokuIllustFullscreenData.*?:"(.*?)",').search(findzip[0]).group(1)
			#result like this -> http:\/\/i1.pixiv.net\/img-zip-ugoira\/img\/2016\/08\/08\/22\/42\/55\/58329284_ugoira1920x1080.zip
			#we need  process it
			item["video_zip"] = re.sub(r"\\","",result)

		yield item
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
