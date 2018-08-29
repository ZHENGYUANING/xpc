# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request 
from xingpianchang.items import Postltem,Commentltem,Composerltem,Copyrightltem
def conver_int(s):
    if not s:
        return 0 
    return int(s.replace(',',''))
ci = conver_int
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']
    def parse(self, response):
        """d
        处理视频列表页面
        """
        post_url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        # 先取出所有的视频li节点
        post_list = response.xpath('//ul[@class="video-list"]/li')
        for post in post_list:
            # 提取视频ID
            pid = post.xpath('./@data-articleid').get()
            # 根据ID构造url，再根据url构造request对象
            request = Request(post_url % pid, callback=self.parse_post)
            request.meta['pid'] = pid
            request.meta['duration'] = post.xpath('./a/span/text()').extract_first()
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').extract_first()
            # 设置request.meta属性，传递缩略图、播放时长信息
            # print(request)
            yield request 
        other_pages = response.xpath('//div[@class="page"]/a/@href').extract()
        yield from[response.follow(page) for page in other_pages]
    def parse_post(self,response):
        post = Postltem()
        pid = response.meta['pid']
        post['pid'] = pid
        post['thumbnail'] = response.meta['thumbnail']
        # 视频标题
        post['title'] = response.xpath(
            '//div[@class="title-wrap"]/h3/text()').extract_first()
        # 视频的预览图，也就是刚打开页面看到的那张图
        post['preview'] = response.xpath(
            '//div[class="filmplay"]//img/@src').extract_first()
        # 视频URL
        post['video'] = response.xpath(
            '//a[@id="player"]/@href').get()
        # 视频所属分类
        cates = response.xpath(
            '//span[contains(@class,"cate")]//text()').get()
        
        post['category'] = ''.join([cate.strip() for cate in cates])
        # 发表时间
        post['created_at'] = response.xpath('//span[contains(@class,"update-time")]/i/text()').get()
        # 播放次数
        post['created_at'] = response.xpath('//i[contains(@class,"play-counts")]/@data-curplaycounts').get()
        # 被点赞次数
        post['like_counts'] = response.xpath('//span[contains(@class,"like-counts")]/@data-counts').get()
        duration = response.meta['duration']
        if duration:
            minutes,seconds,*_ = duration.split("'")
            post['duration'] = int(minutes) * 60 + int(seconds)
        # print(post)
        post['description'] = response.xpath('//p[contains(@class,"desc")]/text()').get()
        post['video_format'] = '1080p'
        yield post
        # 用户主页地址模板
        composer_url = 'http://www.xinpianchang.com/u%s?from=articleList'
        #获取当前视频的创作者节点列表
        composer_list = response.xpath(
            '//div[@class="user-team"]//ul[@class="creator-list"]/li'
        )
        #遍历所有的创作者
        for composer in composer_list:
            cr = Copyrightltem()
            cid = composer.xpath('./a/@data-userid').get()
            cr['pcid'] = '%s_%s'%(cid,pid)
            cr['cid'] = cid 
            cr['pid'] = pid 
            cr['roles'] = composer.xpath('.//span[contains(@class,"roles")]/text()').get()
            yield cr 
            # 构造用户主页的request，并yield
            request = Request(composer_url % cid,callback=self.parse_composer)
            request.meta['cid'] = cid
            # print(request)
            yield request
        # 评论信息的url模板
        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&ajax=0&page=1'
        request = Request(comment_url % pid, callback=self.parse_comment)
        print(request)
        yield request 
    def parse_composer(self, response):
        composer = Composerltem()
        composer['cid'] = response.meta['cid']
        # 用户主页的背景大图
        banner = response.xpath(
            '//div[@class="banner-wrap"]/@style').get()
        if banner:
            composer['banner'] = banner[21:-1]
        # 用户头像
        composer['avatar'] = response.xpath(
            '//span[@class="avator-wrap-s"]/img/@src').get()
        # 用户是否是官方认证用户
        composer['verified'] = response.xpath(
            '//span[@class="avator-wrap-s"]/span/@class').get()
        # 用户名称
        composer['name'] = response.xpath(
            '//p[contains(@class, "creator-name")]/text()').get()
        # 自我介绍
        composer['intro'] = response.xpath(
            '//p[contains(@class, "creator-desc")]/text()').get()
        # 用户被点赞的次数
        composer['like_counts'] = ci(response.xpath(
            '//span[contains(@class, "like-counts")]/text()').get())
        # 粉丝数量
        composer['fans_counts'] = response.xpath(
            '//span[contains(@class, "fans-counts")]/@data-counts').get()
        # 关注数量
        composer['follow_counts'] = ci(response.xpath(
            '//span[@class="follow-wrap"]/span[2]/text()').get())
        # 用户所在地区，定位到icon-location这个span,然后再取它相邻的下一个span
        location = response.xpath(
            '//span[contains(@class, "icon-location")]/following-sibling::span[1]/text()').get()
        if location:
            # 处理了一下特殊字符
            composer['location'] = location.strip().replace('\xa0', '-')
        # 用户的职业，xpath同上
        composer['career'] = response.xpath(
            '//span[contains(@class, "icon-career")]/following-sibling::span[1]/text()').get() or ''
        yield composer



    def parse_comment(self,response):
        # 因为是直接请求的接口，返回的都是json格式，直接用json.loads加载成python对象
        result = json.loads(response.text)
        comments = result['data']['list']
        for c in comments:
            comment = Commentltem()
            # 评论内容
            comment['content'] = c['content']
            # 评论ID
            comment['commentid'] = c['commentid']
            # 作品ID
            comment['pid'] = c['articleid']
            # 评论发表时间
            comment['created_at'] = c['addtime']
            # 评论被点赞的次数
            comment['like_counts'] = c['count_approve']
            # 发表评论的用户ID
            comment['cid'] = c['userInfo']['userid']
            # 发表评论的用户名称
            comment['uname'] = c['userInfo']['username']
            # 发表评论的用户头像
            comment['avatar'] = c['userInfo']['face']
            # 如果本条评论是回复另一条评论，则reply不为空
            if c['reply']:
                 # 把被回复的那条评论ID存在reply字段
                 comment['reply'] = c['reply']['commentid']
            yield comment
        next_page = result['data']['next_page_url']
        if next_page:
            yield Request(next_page,callback=self.parse_comment)   




    


