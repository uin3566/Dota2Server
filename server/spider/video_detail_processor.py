__author__ = 'Fang.Xu'

import urllib2
import util.target_urls
import bs4
import zlib
import json
import string


class VideoDetailProcessor(object):
    def __init__(self):
        self.__user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def __load_html(self, url):
        request = urllib2.Request(url)
        request.add_header('User-Agent', self.__user_agent)
        request.add_header('Accept-encoding', 'gzip')
        opener = urllib2.build_opener()
        response = opener.open(request)
        opener.close()
        html = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            html = zlib.decompress(html, 16 + zlib.MAX_WBITS)
        return html

    def parse_video_set(self, date, vid):
        url = self.__make_url_by_date_vid(date, vid)
        html = self.__load_html(url)
        json_data_dict = dict()
        date_vid_list = []
        if 'player.youku.com' not in html and 'frameBox' not in html:
            json_data_dict['video_set'] = date_vid_list
            return json.dumps(json_data_dict).decode("unicode-escape")

        date_vid_dict = dict()
        date_vid_dict['date'] = date
        date_vid_dict['vid'] = vid
        date_vid_list.append(date_vid_dict)

        soup = bs4.BeautifulSoup(html, "html.parser")
        pages = soup.find('div', class_='page')
        if pages is not None:
            a = pages.findAll('a', class_='cms_pages')
            for page in a:
                href = page['href']
                date, vid = self.__get_date_vid_of_video(href)
                date_vid_dict = dict()
                date_vid_dict['date'] = date
                date_vid_dict['vid'] = vid
                date_vid_list.append(date_vid_dict)
        json_data_dict['video_set'] = date_vid_list
        json_data = json.dumps(json_data_dict).decode("unicode-escape")
        return json_data

    def __get_ykvid(self, soup):
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

    def parse_ykvid(self, date, vid):
        url = self.__make_url_by_date_vid(date, vid)
        html = self.__load_html(url)
        soup = bs4.BeautifulSoup(html, "html.parser")
        ykvid = self.__get_ykvid(soup)
        if ykvid is None:
            return ''
        else:
            return ykvid

    def __get_date_vid_of_video(self, url):
        dot_index = url.rindex('.')
        sprit_index2 = url.rindex('/')
        sprit_index1 = url.rindex('/', 0, sprit_index2)
        vid = url[sprit_index2 + 1:dot_index]
        date = url[sprit_index1 + 1:sprit_index2]
        return date, vid

    def __make_url_by_date_vid(self, date, vid):
        base = util.target_urls.dota2_video_detail_base
        url = base + date + '/' + vid + '.html'
        return url
