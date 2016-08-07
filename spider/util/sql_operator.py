# -*- coding:utf-8 -*-

__author__ = 'Fang.Xu'

from gl import sqlFunc
import MySQLdb


class SqlOperator(object):
    def __init__(self):
        self.db = None
        pass

    def connect(self):
        self.db = MySQLdb.connect(host="sqld.duapp.com", port=4050, user='57cc357cec9f4e7f967d7d0634b9f550', passwd='4419c65057f2449e927aaaf278c2fd0f', db='IuWJWwYetToPtPVdYftO')
        # self.db = MySQLdb.connect('localhost', 'xufang', '123456', 'dota2')
        self.db.ping(True)
        dbc = self.db.cursor()
        self.db.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')
        # self._create_tables()

    # add
    @sqlFunc
    def insert_video_in_table(self, video_type, item):
        table = self.__get_video_table_name(video_type)
        sql = "insert into %s (ykvid, vid, date, background, title, publishin, videolength) " \
              "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (table, item['ykvid'], item['vid'], item['date'], item['background'], item['title'], item['publishin'], item['videolength'])
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    # query
    @sqlFunc
    def is_video_in_db(self, video_type, vid):
        table = self.__get_video_table_name(video_type)
        sql = "select * from %s where vid='%s'" % (table, vid)
        cursor = self.db.cursor()
        cursor.execute(sql)
        video = cursor.fetchone()
        return video is not None

    def __get_video_table_name(self, video_type):
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

    @sqlFunc
    def is_strategy_in_db(self, strategy_type, nid):
        table = self.__get_strategy_table_name(strategy_type)
        sql = "select * from %s where nid='%s'" % (table, nid)
        cursor = self.db.cursor()
        cursor.execute(sql)
        strategy = cursor.fetchone()
        return strategy is not None

    @sqlFunc
    def insert_strategy_in_table(self, strategy_type, item):
        table = self.__get_strategy_table_name(strategy_type)
        sql = "insert into %s (date, nid, background, description, title) " \
              "values ('%s', '%s', '%s', '%s', '%s')" \
              % (table, item['date'], item['nid'], item['background'], item['description'], item['title'])
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

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

    @sqlFunc
    def is_news_in_db(self, news_type, nid):
        table = self.__get_news_table_name(news_type)
        sql = "select * from %s where nid='%s'" % (table, nid)
        cursor = self.db.cursor()
        cursor.execute(sql)
        news = cursor.fetchone()
        return news is not None

    @sqlFunc
    def insert_news_in_table(self, news_type, item):
        table = self.__get_news_table_name(news_type)
        sql = "insert into %s (date, nid, background, description, title, time) " \
              "values ('%s', '%s', '%s', '%s', '%s', '%s')" \
              % (table, item['date'], item['nid'], item['background'], item['description'], item['title'], item['time'])
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()

    def __get_news_table_name(self, news_type):
        table = None
        if news_type == 'news':
            table = 'NEWS'
        if news_type == 'updates':
            table = 'UPDATES'
        return table

    def _create_tables(self):
        cursor = self.db.cursor()
        video_table_list = ['VIDEO_ALL', 'VIDEO_BEGINNER', 'VIDEO_QUWEI', 'VIDEO_JIESHUO', 'VIDEO_CELEBRITY', 'VIDEO_BISAI', 'VIDEO_ADVANCED']
        for table in video_table_list:
            sql = """create table if not exists %s(
                id int auto_increment,
                ykvid varchar(255),
                vid varchar(255),
                date varchar(255),
                background varchar(255),
                title varchar(255),
                publishin varchar(255),
                videolength varchar(255),
                primary key (id))""" % (table)
            cursor.execute(sql)
        strategy_table_list = ['STRATEGY_ALL', 'STRATEGY_NEWER', 'STRATEGY_STEP', 'STRATEGY_SKILL']
        for table in strategy_table_list:
            sql = """create table if not exists %s(
                id int auto_increment,
                date varchar(255),
                nid varchar(255),
                background varchar(255),
                description varchar(255),
                title varchar(255),
                primary key (id))""" % (table)
            cursor.execute(sql)
        news_table_list = ['NEWS', 'UPDATES']
        for table in news_table_list:
            sql = """create table if not exists %s(
                id int auto_increment,
                date varchar(255),
                nid varchar(255),
                background varchar(255),
                description varchar(255),
                title varchar(255),
                time varchar(255),
                primary key (id))""" % (table)
            cursor.execute(sql)
        cursor.close()
