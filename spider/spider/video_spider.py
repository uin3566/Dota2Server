# -*- coding:utf8 -*-

__author__ = 'Fang.Xu'

import urllib2
import bs4
import zlib
import string
import time
import random
import gl
from util import target_urls
from util.user_agents import user_agent_list


class VideoSpider(object):
    def __init__(self):
        pass

    def __load_html(self, url):
        request = urllib2.Request(url)
        user_agent = random.choice(user_agent_list)
        request.add_header('User-Agent', user_agent)
        request.add_header('Accept-encoding', 'gzip')
        opener = urllib2.build_opener()
        response = opener.open(request)
        opener.close()
        html = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
        return html

    def grab_videos(self, video_type):
        def get_url_prefix_suffix(url):
            dot_index = url.rindex('.')
            prefix = url[:dot_index]
            suffix = url[dot_index:]  # .html
            return prefix, suffix

        def get_url(video_type):
            if video_type == 'all':
                return target_urls.dota2_video_all
            if video_type == 'beginner':
                return target_urls.dota2_video_beginner
            if video_type == 'quwei':
                return target_urls.dota2_video_quwei
            if video_type == 'jieshuo':
                return target_urls.dota2_video_jieshuo
            if video_type == 'celebrity':
                return target_urls.dota2_video_celebrity
            if video_type == 'bisai':
                return target_urls.dota2_video_bisai
            if video_type == 'advanced':
                return target_urls.dota2_video_advanced

        url = get_url(video_type)
        print url
        next_list_id = 1
        next_list_id = self.__grab_videos_to_db(video_type, next_list_id, url)
        prefix, suffix = get_url_prefix_suffix(url)
        while next_list_id is not None:
            if next_list_id == 1:
                url = get_url(video_type)
            else:
                url = prefix + '_' + str(next_list_id) + suffix
            print url
            next_list_id = self.__grab_videos_to_db(video_type, next_list_id, url)
        print 'grab videos finish'

    def __grab_videos_to_db(self, video_type, list_id, url):
        try:
            html = self.__load_html(url)
        except:
            time.sleep(random.randint(30, 60))
            return list_id
        soup = bs4.BeautifulSoup(html, "html.parser")
        next_list_id = self.__get_next_list_id(soup)
        div = soup.find('div', class_='newly newly897 clearfix')
        print next_list_id
        items = div.findAll('dl')
        for i in items:
            url = i.dt.a['href']
            date, vid = self.__get_date_vid_of_per_video(url)
            if gl.sql_operator.is_video_in_db(video_type, vid) is False:
                youku_vid = self.__get_youku_vid(url)
                if youku_vid is None:
                    continue
                video_item = dict()
                video_item['ykvid'] = youku_vid
                length = i.dt.a.strong
                if length is None:
                    video_item['videolength'] = '--:--'
                else:
                    video_item['videolength'] = length.string
                video_item['date'] = date
                video_item['vid'] = vid
                video_item['background'] = self.__get_background_url(i.dt.a['style'])
                title = i.dt.a['title']
                title = string.replace(title, "'", ' ')
                video_item['title'] = title
                video_item['publishin'] = i.dd.next_sibling.next_sibling.string
                gl.sql_operator.insert_video_in_table(video_type, video_item)
            else:
                return None
        if next_list_id is None:
            return None
        else:
            return int(next_list_id)

    def __get_date_vid_of_per_video(self, url):
        dot_index = url.rindex('.')
        sprit_index2 = url.rindex('/')
        sprit_index1 = url.rindex('/', 0, sprit_index2)
        vid = url[sprit_index2 + 1:dot_index]
        date = url[sprit_index1 + 1:sprit_index2]
        return date, vid

    def __get_next_list_id(self, soup):
        div = soup.find('div', class_='page')
        if div is not None:
            a = div.find('a', class_='selected')
            if a.next_sibling is not None:
                return a.next_sibling.string
            else:
                return None
        else:
            return None

    def __get_background_url(self, url):
        # background-image: url('http://img.178.com/dota2/201511/241827471049/241827723987.jpg');
        start_index = string.find(url, "'")
        end_index = string.rfind(url, "'")
        return url[start_index + 1:end_index]

    def __get_youku_vid(self, video_url):
        time.sleep(random.randint(2, 5))
        retry = 2
        html = ''
        while retry > 0:
            try:
                html = self.__load_html(video_url)
                print 'get youku_vid load html success, video_url=' + video_url + '  left retry times=' + str(retry - 1)
                break
            except:
                print 'get youku_vid load html exception, video_url=' + video_url
                time.sleep(random.randint(30, 60))
                retry -= 1
                if retry > 0:
                    continue
                else:
                    return None
        soup = bs4.BeautifulSoup(html, "html.parser")
        iframes = soup.find_all('iframe')
        if len(iframes) > 0:
            for iframe in iframes:
                play_url = iframe['src']
                if play_url.find('youku') == -1:
                    continue
                sprit_index = play_url.rindex('/')
                youku_vid = play_url[sprit_index + 1:]
                youku_vid = youku_vid.strip().strip('.')
                print youku_vid
                return youku_vid

        text = soup.find('div', id='text')
        if text is not None:
            for tag in text.descendants:
                if tag.name == 'embed':
                    play_url = tag['src']
                    index1 = string.find(play_url, 'sid')
                    if index1 == -1:
                        index1 = string.find(play_url, 'VideoIDS')
                        if index1 == -1:
                            continue
                        else:
                            index1 = string.index(play_url, '=', index1)
                            index2 = string.index(play_url, '&', index1)
                            youku_vid = play_url[index1 + 1:index2]
                            youku_vid = youku_vid.strip().strip('.')
                            print youku_vid
                            return youku_vid
                    else:
                        index1 = string.index(play_url, '/', index1)
                        index2 = play_url.rindex('/')
                        youku_vid = play_url[index1 + 1:index2]
                        youku_vid = youku_vid.strip().strip('.')
                        print youku_vid
                        return youku_vid
                if tag.name == 'a':
                    play_url = tag['href']
                    index1 = string.find(play_url, 'id_')
                    if index1 == -1:
                        continue
                    else:
                        index2 = string.index(play_url, '.', index1)
                        youku_vid = play_url[index1 + 3:index2]
                        youku_vid = youku_vid.strip().strip('.')
                        print youku_vid
                        return youku_vid

                if tag.name == 'div':
                    if tag.get('data-youku') is None:
                        continue
                    data_youku = tag['data-youku']
                    if data_youku is None:
                        continue
                    else:
                        index1 = string.find(data_youku, 'vid')
                        if index1 == -1:
                            continue
                        else:
                            index1 = string.index(data_youku, ':', index1)
                            youku_vid = data_youku[index1 + 1:]
                            youku_vid = youku_vid.strip().strip('.')
                            print youku_vid
                            return youku_vid

        def get_vid_from_script(script):
            index1 = string.find(script, 'vid:')
            if index1 is -1:
                return None
            index1 = string.index(script, "'", index1)
            index2 = string.index(script, "'", index1 + 1)
            youku_vid = script[index1 + 1: index2]
            youku_vid = youku_vid.strip().strip('.')
            print youku_vid
            return youku_vid

        framebox = soup.find('div', class_='frameBox')
        if framebox is not None:
            for tag in framebox.descendants:
                if tag.name == 'script':
                    script = str(tag.string)
                    vid = get_vid_from_script(script)
                    if vid is not None:
                        return vid
                    else:
                        continue
                if tag.name == 'div':
                    if tag.get('data-youku') is None:
                        continue
                    data_youku = tag['data-youku']
                    if data_youku is None:
                        continue
                    else:
                        index1 = string.find(data_youku, 'vid')
                        if index1 == -1:
                            continue
                        else:
                            index1 = string.index(data_youku, ':', index1)
                            youku_vid = data_youku[index1 + 1:]
                            youku_vid = youku_vid.strip().strip('.')
                            print youku_vid
                            return youku_vid

        video = soup.find('div', class_='video')
        if video is not None:
            for tag in video.descendants:
                if tag.name == 'script':
                    script = str(tag.string)
                    vid = get_vid_from_script(script)
                    if vid is not None:
                        return vid
                    else:
                        continue

        return None
