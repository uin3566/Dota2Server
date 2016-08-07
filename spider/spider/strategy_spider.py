# -*- coding:utf8 -*-

__author__ = 'Fang.Xu'

import urllib2
import bs4
import urlparse
import string
import random
import time
from util import target_urls
from util.user_agents import user_agent_list
import gl


class StrategySpider(object):
    def __init__(self):
        self.total_page_count = None

    def __load_html(self, url):
        try:
            req = urllib2.Request(url)
            user_agent = random.choice(user_agent_list)
            req.add_header('User-Agent', user_agent)
            resp = urllib2.urlopen(req)
            content = resp.read()
            return content.decode('utf-8')
        except:
            time.sleep(random.randint(10, 15))
            return None

    def get_total_strategy_page_count(self, url):
        content = self.__load_html(url)
        while content is None:
            content = self.__load_html(url)
        soup = bs4.BeautifulSoup(content, "html.parser")
        div = soup.find('div', class_ = 'page')
        strong = div.findAll('strong')
        total_pages = int(strong[1].string)
        return total_pages

    def __get_next_strategy_page_url(self, url):
        dot_index = url.rindex('.')
        prefix = url[:dot_index]
        suffix = url[dot_index:]#.htm
        x_index = prefix.rindex('x')
        url_index = string.atoi(prefix[x_index + 1:])
        prefix = prefix[:x_index + 1]
        next_url_index = url_index + 1
        if self.total_page_count is None:
            self.total_page_count = self.get_total_strategy_page_count(url)
        if next_url_index > self.total_page_count:
            next_url = None
        else:
            next_url = prefix + str(next_url_index) + suffix
        return next_url

    def parse_strategy_list(self, url, strategy_type):

        def get_date_id_of_per_strategy(href):
            dot_index = href.rindex('.')
            sprit_index2 = href.rindex('/')
            sprit_index1 = href.rindex('/', 0, sprit_index2)
            nid = href[sprit_index2 + 1:dot_index]
            date = href[sprit_index1 + 1:sprit_index2]
            return date, nid

        print 'grab ing ' + url
        should_continue = True
        content = self.__load_html(url)
        while content is None:
            content = self.__load_html(url)
        soup = bs4.BeautifulSoup(content, "html.parser")
        div = soup.find('div', class_="hd_li")
        strategies = div.findAll('dl', class_="hd_ps hd_pic")
        for s in strategies:
            item = dict()
            u = urlparse.urlparse(s.dt.a['href'])
            if u.scheme is '':
                item['background'] = urlparse.urljoin(url, s.dt.a.img['src'])
                href = s.dt.a['href']
                date, nid = get_date_id_of_per_strategy(href)
                item['date'] = date
                item['nid'] = nid
                title = string.strip(s.dd.h2.a.string)
                title = string.replace(title, '"', '')
                title = string.replace(title, "'", '')
                description = s.dd.p.string
                if description is None:
                    description = ''
                else:
                    description = string.strip(description)
                    description = string.replace(description, '"', '')
                    description = string.replace(description, "'", '')
                item['title'] = title
                item['description'] = description
                if gl.sql_operator.is_strategy_in_db(strategy_type, nid) is False:
                    gl.sql_operator.insert_strategy_in_table(strategy_type, item)
                else:
                    should_continue = False
                    break
        return should_continue

    @staticmethod
    def __get_strategy_start_url_by_type(tp):
        url = None
        if tp == 'all':
            url = target_urls.dota2_strategy_all
        if tp == 'newer':
            url = target_urls.dota2_strategy_newer
        if tp == 'step':
            url = target_urls.dota2_strategy_step
        if tp == 'skill':
            url = target_urls.dota2_strategy_skill
        return url

    def __get_page_prefix_suffix(self, url):
        dot_index = url.rindex('.')
        prefix = url[:dot_index]
        suffix = url[dot_index:]  # .htm
        x_index = prefix.rindex('x')
        prefix = prefix[:x_index + 1]
        return prefix, suffix

    def __get_strategy_page_url_by_id(self, tp, strategy_list_id):
        url = self.__get_strategy_start_url_by_type(tp)
        prefix, suffix = self.__get_page_prefix_suffix(url)
        if strategy_list_id > self.get_total_strategy_page_count(url):
            url = None
        else:
            url = prefix + str(strategy_list_id) + suffix
        return url

    def grab_strategy(self, strategy_type):

        def get_url(strategy_type):
            url = None
            if strategy_type == 'all':
                url = target_urls.dota2_strategy_all
            if strategy_type == 'newer':
                url = target_urls.dota2_strategy_newer
            if strategy_type == 'step':
                url = target_urls.dota2_strategy_step
            if strategy_type == 'skill':
                url = target_urls.dota2_strategy_skill
            return url

        self.total_page_count = None
        url = get_url(strategy_type)
        while True:
            should_continue = self.parse_strategy_list(url, strategy_type)
            url = self.__get_next_strategy_page_url(url)
            if should_continue is False or url is None:
                break
        print 'grab strategy finish'
