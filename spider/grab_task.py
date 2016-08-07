# -*- coding:utf-8 -*-

__author__ = 'Fang.Xu'

import sys
import time

sys.path.append('/home/bae/app/deps')

from util.sql_operator import SqlOperator
from spider.video_spider import VideoSpider
from spider.strategy_spider import StrategySpider
from spider.news_spider import NewsSpider
import gl


def grab_task():
    gl.sql_operator = SqlOperator()
    gl.sql_operator.connect()

    spider = VideoSpider()
    video_types = ['all', 'jieshuo', 'quwei', 'celebrity', 'bisai', 'advanced', 'beginner']
    for t in video_types:
        spider.grab_videos(t)

    spider2 = StrategySpider()
    strategy_types = ['all', 'newer', 'step', 'skill']
    for t in strategy_types:
        spider2.grab_strategy(t)

    spider3 = NewsSpider()
    news_types = ['news', 'updates']
    for t in news_types:
        spider3.grab_news(t)


while True:
    grab_task()
    time.sleep(10800)
