# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImageDownloadPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
        if 'image_url' in item.keys():
            for image_url in item['image_url']:
                yield scrapy.Request(
                    image_url,
                    headers={'Referer': item['image_referer'], 'User-Agent': user_agent})

    def file_path(self, request, response=None, info=None):

        # use id + page num to name file
        media_guid = request.url.split('/')[-1]
        print media_guid
        return 'image/%s' % media_guid
