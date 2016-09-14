__author__ = 'Fang.Xu'

import urllib2
import bs4
import urlparse
import time
import random
import string
import gl
from util import target_urls
from util.user_agents import user_agent_list

class NewsSpider(object):
    def __init__(self):
        pass

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

    def parse_list(self, url, news_type):
        print 'grab ing ' + url
        should_continue = True
        content = self.__load_html(url)
        while content is None:
            content = self.__load_html(url)
        soup = bs4.BeautifulSoup(content, "html.parser")
        li = soup.find('li', class_ = 'pane active')
        news = li.findAll('a')
        for a in news:
            href = a['href']
            date, nid = self.__get_date_id_of_per_new(href)
            item = dict()
            item['date'] = date
            item['nid'] = nid
            newslogo = a.find('div', class_ = 'news_logo')
            background = ''
            if newslogo is not None:
                background = urlparse.urljoin(url, newslogo.img['src'])
            item['background'] = background
            newsmsg = a.find('div', class_ = 'news_msg')
            title = ''
            h2 = newsmsg.find('h2', class_ = 'title')
            if h2 is not None:
                title = string.strip(h2.string)
                title = string.replace(title, '"', '')
                title = string.replace(title, "'", '')
            item['title'] = title
            pcontent = newsmsg.find('p', class_ = 'content')
            description = ''
            if pcontent is not None:
                description = pcontent.string
                description = string.strip(description)
                description = string.replace(description, '"', '')
                description = string.replace(description, "'", '')
            item['description'] = description
            pdate = newsmsg.find('p', class_ = 'date')
            time = ''
            if pdate is not None:
                time = pdate.string
            item['time'] = time

            if gl.sql_operator.is_news_in_db(news_type, nid) is False:
                gl.sql_operator.insert_news_in_table(news_type, item)
            else:
                should_continue = False
                break
        return should_continue

    def get_next_news_page_url(self, url):
        dot_index = url.rindex('.')
        prefix = url[:dot_index]
        suffix = url[dot_index:]#.htm
        x_index = prefix.rindex('x')
        url_index = string.atoi(prefix[x_index + 1:])
        prefix = prefix[:x_index + 1]
        next_url_index = url_index + 1
        next_url = prefix + str(next_url_index) + suffix
        return next_url

    def __get_date_id_of_per_new(self, href):
        dot_index = href.rindex('.')
        sprit_index2 = href.rindex('/')
        sprit_index1 = href.rindex('/', 0, sprit_index2)
        nid = href[sprit_index2 + 1:dot_index]
        date = href[sprit_index1 + 1:sprit_index2]
        return date, nid

    def grab_news(self, news_type):

        def get_url(news_type):
            url = None
            if news_type == 'news':
                url = target_urls.dota2_news
            if news_type == 'updates':
                url = target_urls.dota2_update
            return url

        url = get_url(news_type)
        while True:
            should_continue = self.parse_list(url, news_type)
            url = self.get_next_news_page_url(url)
            if should_continue is False or url is None:
                break
        print 'grab news finish'
