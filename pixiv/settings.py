# -*- coding: utf-8 -*-
import os
import time

BOT_NAME = 'pixiv'

SPIDER_MODULES = ['pixiv.spiders']
NEWSPIDER_MODULE = 'pixiv.spiders'

#Pixiv Login Data

PIXIV_ID = 'joker012'#your pixiv id
PASSWORD = 'monburan012'#your pixiv password

#Get Yesterday

YESTERDAY = str(int(time.strftime("%Y%m%d",time.localtime(time.time())))-1)

#set media pipeline

ITEM_PIPELINES = {'pixiv.pipelines.ImageDownloadPipeline': 1}

LOG_LEVEL = "ERROR"

FILES_STORE = os.getcwd()+'/'

#set download
DOWNLOAD_DELAY = '1'
