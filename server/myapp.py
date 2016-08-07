#-*- coding:utf-8 -*-

__author__ = 'Fang.Xu'

from flask import Flask
from spider.video_detail_processor import VideoDetailProcessor
from data.data_center import DataCenter
from spider.article_detail_processor import ArticleDetailProcessor
from sql.sql_operator import SqlOperator
from util import api
import gl

app = Flask(__name__)
app.debug = True


from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

@app.before_request
def before_request():
    global article_detail_spider
    global video_detail_spider
    article_detail_spider = ArticleDetailProcessor()
    video_detail_spider = VideoDetailProcessor()
    gl.sql_operator = SqlOperator()
    gl.sql_operator.connect()


@app.route(api.newsrefresh, methods=['GET'])
def refresh_news():
    return DataCenter.refresh_news('news')


@app.route(api.newsloadmore, methods=['GET'])
def load_more_news(nid):
    return DataCenter.load_more_news('news', nid)


@app.route(api.updatesrefresh, methods=['GET'])
def refresh_updates():
    return DataCenter.refresh_news('updates')


@app.route(api.updatesloadmore, methods=['GET'])
def load_more_updates(nid):
    return DataCenter.load_more_news('updates', nid)


@app.route(api.strategyrefresh, methods=['GET'])
def refresh_strategy(strategy_type):
    return DataCenter.refresh_strategy(strategy_type)


@app.route(api.strategyloadmore, methods=['GET'])
def load_more_strategy(strategy_type, nid):
    return DataCenter.load_more_strategy(strategy_type, nid)


@app.route(api.videorefresh, methods=['GET'])
def refresh_video(video_type):
    return DataCenter.refresh_video(video_type)


@app.route(api.videoloadmore, methods=['GET'])
def load_more_video(video_type, vid):
    return DataCenter.load_more_video(video_type, vid)


@app.route(api.videoset, methods=['GET'])
def get_video_set(date, vid):
    return video_detail_spider.parse_video_set(date, vid)


@app.route(api.videoykvid, methods=['GET'])
def get_video_youku_vid(date, vid):
    return video_detail_spider.parse_ykvid(date, vid)


@app.route(api.newsdetail, methods=['GET'])
def get_news_detail(date, nid):
    return article_detail_spider.get_news_detail_html_body(date, nid)
