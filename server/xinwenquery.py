# -*- coding: utf-8 -*-

import os
from threading import Thread
from datetime import date, timedelta
import ytsearch as search

#string used to build search queries
xwlb = u'新闻联播'

#returns yt link for xwlb associated with date
def get_xwlb_vid(date):
    query = date + ' ' + xwlb
    result = search.search_by_keyword(query, 1)
    if(result != None
        and result['items'][0]['snippet']['channelTitle'] == 'TV 1080'):
        return 'https://youtu.be/' + result['items'][0]['id']['videoId']

def get_today_xwlb():
    today = date.today().strftime("%Y%m%d")
    return get_xwlb_vid(today)

def get_yesterday_xwlb():
    yesterday = (date.today() - timedelta(1)).strftime("%Y%m%d")
    return get_xwlb_vid(yesterday)

#calls system methods for chromecasting
#requres youtube-dl and castnow
def play_video(vlink):
    os.system('youtube-dl -o - ' + vlink + ' | castnow --quiet -')

#main method
def play_xwlb():
    vlink = get_today_xwlb()
    #if today's segment is not uploaded yet, use yesterday's
    if(vlink is None):
        vlink = get_yesterday_xwlb()
    if(vlink is not None):
        #start video in seperate thread so sucess response can be given
        thread = Thread(target = play_video, args=(vlink, ))
        thread.start()
        return True
    #failed to get a video
    return False

if __name__ == '__main__':
    print(play_xwlb())
