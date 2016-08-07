# -*- coding:utf8 -*-

__author__ = 'Fang.Xu'

import gl


class DataCenter(object):
    @staticmethod
    def refresh_video(video_type):
        return gl.sql_operator.get_videos_from_table(video_type, None, 20)

    @staticmethod
    def load_more_video(video_type, begin_vid):
        return gl.sql_operator.get_videos_from_table(video_type, begin_vid, 20)

    @staticmethod
    def refresh_strategy(strategy_type):
        return gl.sql_operator.get_strategies_from_table(strategy_type, None, 20)

    @staticmethod
    def load_more_strategy(strategy_type, begin_nid):
        return gl.sql_operator.get_strategies_from_table(strategy_type, begin_nid, 20)

    @staticmethod
    def refresh_news(news_type):
        return gl.sql_operator.get_news_from_table(news_type, None, 20)

    @staticmethod
    def load_more_news(news_type, begin_nid):
        return gl.sql_operator.get_news_from_table(news_type, begin_nid, 20)
