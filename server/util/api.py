# -*- coding:utf8 -*-

__author__ = 'Fang.Xu'

newsrefresh='/api/v1.0/news/refresh'
newsloadmore='/api/v1.0/news/loadmore/<string:nid>'
updatesrefresh='/api/v1.0/updates/refresh'
updatesloadmore='/api/v1.0/updates/loadmore/<string:nid>'
newsdetail='/api/v1.0/newsdetail/<string:date>/<string:nid>'
strategyrefresh='/api/v1.0/strategy/refresh/<string:strategy_type>'
strategyloadmore='/api/v1.0/strategy/loadmore/<string:strategy_type>/<string:nid>'
videorefresh='/api/v1.0/video/refresh/<string:video_type>'
videoloadmore='/api/v1.0/video/loadmore/<string:video_type>/<string:vid>'
videoset='/api/v1.0/video/videoset/<string:date>/<string:vid>'
videoykvid='/api/v1.0/video/youkuvid/<string:date>/<string:vid>'
