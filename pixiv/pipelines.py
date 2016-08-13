# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImageDownloadPipeline(FilesPipeline):
	def get_media_requests(self,item,info):
		if 'video_zip' in item.keys():
			yield scrapy.Request(
				item['video_zip'],
				headers = {
					'Referer':item['referer_url'],
					'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
				}
			)
		if 'image_url' in item.keys():
			for image_url in item['image_url']:
				yield scrapy.Request(
					image_url,
					headers = {
						'Referer':item['referer_url'],
						'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
					}
				)
	
	def file_path(self,request,response=None,info=None):
		media_guid = request.url.split('/')[-1]
		print media_guid
		return 'image/%s' % media_guid
	
	def item_completed(self,results,item,info):
		image_paths = [x['path'] for ok,x in results if ok]
		if not image_paths:
			raise DropItem("Item contains no images")
		return item	
