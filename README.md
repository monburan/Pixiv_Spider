Pixiv_Spider
=========================
基于scrapy框架<br />
* 自动登录<br />
* 自动爬取前一天的综合榜TOP50<br />
* 自动下载<br />
* 由于网络原因不能保证每次都能成功下载动图的zip文件<br />
* 功能正在完善中

##使用说明：
<b>使用前请安装python环境,安装Scrapy框架</b><br />

<b>使用前请填写账号名和密码。</b><br />
编辑pixiv文件夹下的settings.py文件<br />
PIXIV_ID 是你的账号名<br />
PASSWORD 是你的账号密码<br />
<b>注意:</b>请将内容填写在 ' ' 中。<br />

使用时，将本程序放入任意路径下<br/>
在命令行下移动至<b>程序所在路径</b>，输入scrapy crawl pixiv启动爬取

##开发过程：
[Pixiv_Spider——创建一个框架](http://www.monburan.cn/?p=327)<br />
[Pixiv_Spider——模拟登陆](http://www.monburan.cn/?p=367)<br />
[Pixiv_Spider——使用Xpath和Items配合提取信息](http://www.monburan.cn/?p=334)<br />
[Pixiv_Spider——分类，下载](http://www.monburan.cn/?p=398&preview_id=398)
