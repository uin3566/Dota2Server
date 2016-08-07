# -*- coding:utf8 -*-

__author__ = 'Fang.Xu'

import MySQLdb
import string
import json


class SqlOperator(object):
    def __init__(self):
        self.db = None
        pass

    def connect(self):
        self.db = MySQLdb.connect(host="sqld.duapp.com", port=4050, user='57cc357cec9f4e7f967d7d0634b9f550', passwd='4419c65057f2449e927aaaf278c2fd0f', db='IuWJWwYetToPtPVdYftO')
        # self.db = MySQLdb.connect('localhost', 'xufang', '123456', 'dota2')
        dbc = self.db.cursor()
        self.db.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

    # query
    def get_videos_from_table(self, video_type, from_vid, size):
        table = self._get_video_table_name(video_type)
        cursor = self.db.cursor()
        video_list = []
        if from_vid is None or from_vid is '':
            sql = "select * from %s order by vid desc limit %d" % (table, size)
            cursor.execute(sql)
            videos = cursor.fetchall()
            for video in videos:
                video_dict = self._convert_video_list_to_dict(video)
                video_list.append(video_dict)
        else:
            sql = "select * from %s where vid='%s'" % (table, from_vid)
            cursor.execute(sql)
            key = cursor.fetchone()
            vid = key[2]
            sql = "select * from %s where vid < '%s' order by vid desc limit %d" % (table, vid, size)
            cursor.execute(sql)
            videos = cursor.fetchall()
            for video in videos:
                video_dict = self._convert_video_list_to_dict(video)
                video_list.append(video_dict)
        video_list_dict = dict()
        video_list_dict['videos'] = video_list
        json_data = json.dumps(video_list_dict)
        print json_data
        return json_data

    def get_strategies_from_table(self, strategy_type, from_nid, size):
        table = self.__get_strategy_table_name(strategy_type)
        cursor = self.db.cursor()
        strategy_list = []
        if from_nid is None or from_nid is '':
            sql = "select * from %s order by nid desc limit %d" % (table, size)
            cursor.execute(sql)
            strategies = cursor.fetchall()
            for strategy in strategies:
                strategy_dict = self.__convert_strategy_list_to_dict(strategy)
                strategy_list.append(strategy_dict)
        else:
            sql = "select * from %s where nid='%s'" % (table, from_nid)
            cursor.execute(sql)
            key = cursor.fetchone()
            nid = key[2]
            sql = "select * from %s where nid < '%s' order by nid desc limit %d" % (table, nid, size)
            cursor.execute(sql)
            strategies = cursor.fetchall()
            for strategy in strategies:
                strategy_dict = self.__convert_strategy_list_to_dict(strategy)
                strategy_list.append(strategy_dict)
        strategy_list_dict = dict()
        strategy_list_dict['strategies'] = strategy_list
        json_data = json.dumps(strategy_list_dict)
        print json_data
        return json_data

    def get_news_from_table(self, news_type, from_nid, size):
        table = self.__get_news_table_name(news_type)
        cursor = self.db.cursor()
        news_list = []
        banner_list = []
        if from_nid is None or from_nid is '':
            last_banner_nid = None
            if news_type == 'news':
                sql = "select * from %s order by nid desc limit %d" % (table, 3)
                cursor.execute(sql)
                banners = cursor.fetchall()
                last_banner = None
                for n in banners:
                    banner_dict = self.__convert_banner_list_to_dict(n)
                    banner_list.append(banner_dict)
                    last_banner = n
                last_banner_nid = last_banner[2]
            if last_banner_nid is None:
                sql = "select * from %s order by nid desc limit %d" % (table, size)
            else:
                sql = "select * from %s where nid < '%s' order by nid desc limit %d" % (table, last_banner_nid, size)
            cursor.execute(sql)
            news = cursor.fetchall()
            for n in news:
                news_dict = self.__convert_news_list_to_dict(n)
                news_list.append(news_dict)
        else:
            sql = "select * from %s where nid='%s'" % (table, from_nid)
            cursor.execute(sql)
            key = cursor.fetchone()
            nid = key[2]
            sql = "select * from %s where nid < '%s' order by nid desc limit %d" % (table, nid, size)
            cursor.execute(sql)
            news = cursor.fetchall()
            for n in news:
                news_dict = self.__convert_news_list_to_dict(n)
                news_list.append(news_dict)
        news_list_dict = dict()
        news_list_dict['banner'] = banner_list
        news_list_dict['news'] = news_list
        json_data = json.dumps(news_list_dict)
        print json_data
        return json_data

    def __convert_banner_list_to_dict(self, banner):
        banner_dict = dict()
        banner_dict['date'] = banner[1]
        banner_dict['nid'] = banner[2]
        banner_dict['background'] = banner[3]
        banner_dict['description'] = banner[4]
        banner_dict['title'] = banner[5]
        banner_dict['time'] = banner[6]
        return banner_dict

    def __convert_news_list_to_dict(self, news):
        news_dict = dict()
        news_dict['date'] = news[1]
        news_dict['nid'] = news[2]
        news_dict['background'] = news[3]
        news_dict['description'] = news[4]
        news_dict['title'] = news[5]
        news_dict['time'] = news[6]
        return news_dict

    def __convert_strategy_list_to_dict(self, strategy):
        strategy_dict = dict()
        strategy_dict['date'] = strategy[1]
        strategy_dict['nid'] = strategy[2]
        strategy_dict['background'] = strategy[3]
        strategy_dict['description'] = strategy[4]
        strategy_dict['title'] = strategy[5]
        return strategy_dict

    def _convert_video_list_to_dict(self, video):
        video_dict = dict()
        video_dict['ykvid'] = video[1]
        video_dict['vid'] = video[2]
        video_dict['date'] = video[3]
        video_dict['background'] = video[4]
        video_dict['title'] = video[5]
        video_dict['publishin'] = video[6]
        video_dict['videolength'] = video[7]
        return video_dict

    def __get_news_table_name(self, news_type):
        table = None
        if news_type == 'news':
            table = 'NEWS'
        if news_type == 'updates':
            table = 'UPDATES'
        return table

    def __get_strategy_table_name(self, strategy_type):
        table = None
        if strategy_type == 'all':
            table = 'STRATEGY_ALL'
        if strategy_type == 'newer':
            table = 'STRATEGY_NEWER'
        if strategy_type == 'step':
            table = 'STRATEGY_STEP'
        if strategy_type == 'skill':
            table = 'STRATEGY_SKILL'
        return table

    def _get_video_table_name(self, video_type):
        table = None
        if video_type == 'all':
            table = 'VIDEO_ALL'
        if video_type == 'beginner':
            table = 'VIDEO_BEGINNER'
        if video_type == 'quwei':
            table = 'VIDEO_QUWEI'
        if video_type == 'jieshuo':
            table = 'VIDEO_JIESHUO'
        if video_type == 'celebrity':
            table = 'VIDEO_CELEBRITY'
        if video_type == 'bisai':
            table = 'VIDEO_BISAI'
        if video_type == 'advanced':
            table = 'VIDEO_ADVANCED'
        return table
