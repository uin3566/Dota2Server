# -*- coding:utf8 -*-

__author__ = 'Fang.Xu'

import urllib2
import util.target_urls
import bs4
import urlparse
import string

class ArticleDetailProcessor(object):
    def __init__(self):
        self.__user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def __load_html(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.__user_agent)
        resp = urllib2.urlopen(req)
        content = resp.read()
        return content.decode('utf-8')

    def get_news_detail_html_body(self, date, nid):
        url = self.__make_url_by_date_sid(date, nid)
        html = self.__load_html(url)
        soup = bs4.BeautifulSoup(html, "html.parser")
        newsart = soup.find('div', class_='newsart')
        div_list = newsart.findAll('div')
        title = div_list[0]
        title['style'] = 'text-align: center;font-size: 10px'
        span = title.h3.span
        if span is not None:
            span.decompose()
        hr = soup.new_tag('hr')
        hr['style'] = 'height:1px;border:none;border-top:1px solid #888'
        title.append(hr)
        content = div_list[1]
        p_list = content.findAll('p')
        for p in p_list:
            obj = p.find('object')
            if obj is not None:
                param_lst = obj.findAll('param')
                if param_lst is not None:
                    for param in param_lst:
                        if param['name'] == 'movie':
                            value = param['value']
                            lindex = string.find(value, 'sid')
                            if lindex != -1:
                                lindex = string.index(value, '/', lindex)
                                lindex += 1
                                rindex = string.index(value, '/', lindex)
                                vid = value[lindex:rindex]
                                vid = vid.strip().strip('.')
                                return vid
            img_list = p.findAll('img')
            for imag in img_list:
                if imag is not None:
                    if imag.has_attr('style'):
                        del imag['style']
                    imag['src'] = urlparse.urljoin(url, imag['src'])
                    parent = imag.parent
                    if parent.has_attr('href'):
                        parent['href'] = urlparse.urljoin(url, parent['href'])
            video_list = p.findAll('iframe')
            for frame in video_list:
                if frame is not None:
                    if frame.has_attr('height'):
                        frame['height'] = '35%'
                    if frame.has_attr('width'):
                        frame['width'] = '100%'
            embed_list = p.findAll('embed')
            for embed in embed_list:
                if embed is not None:
                    if embed.has_attr('height'):
                        embed['height'] = '35%'
                    if embed.has_attr('width'):
                        embed['width'] = '100%'
        div_list = content.findAll('div', class_='youku_block')
        for div in div_list:
            if div.has_attr('style'):
                div['style'] = 'margin: 0px auto; width: 100%; height: 35%'
        body = "<body>" + str(title) + str(content) + "</body>"
        ass_style = "<style>img{max-width:100%;height:auto;}</style>"
        html = "<html><head>" + ass_style + "</head>" + body + "</html>"
        return html

    def __make_url_by_date_sid(self, date, sid):
        base = util.target_urls.dota2_article_detail_base
        url = base + date + '/' + sid + '.html'
        return url
