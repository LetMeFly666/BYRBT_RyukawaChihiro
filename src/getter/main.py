'''
Author: LetMeFly
Date: 2024-07-26 22:26:53
LastEditors: LetMeFly
LastEditTime: 2024-08-08 10:20:54
'''
import requests
import time
from bs4 import BeautifulSoup
import os
import re
import functools

getNow = lambda: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
IFDBG = False


def untilSuccess(delay=121):
    def retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                time.sleep(delay)
        return wrapper
    return retry


@untilSuccess()
def getTopFreeTorrents() -> list:
    if not IFDBG:
        response = requests.get(
            url='https://byr.pt/torrents.php',
            cookies={'auth_token': 'TODO:'}
        )
        print(response)
        html = response.text
        # print(response.text)
        # with open('result.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
    else:
        with open('result.html', 'r', encoding='utf-8') as f:
            html = f.read()

    soup = BeautifulSoup(html, 'lxml')
    torrentTable = soup.select_one('table.torrents.coltable.full')  
    torrents = torrentTable.select('tr')
    isTorrent = False
    topFreeTorrents = []
    for torrent in torrents:
        if not isTorrent:  # 间隔一行有一个torrent
            isTorrent = True
            continue
        else:
            isTorrent = False
        if torrent.get('class') == ['free_bg']:
            topFreeTorrents.append(torrent)
        else:
            break
    return topFreeTorrents


def getTorrentId(torrent: BeautifulSoup) -> str:
    tr4tr = torrent.select_one('tr')
    pattern = re.compile(r'details\.php\?id=\d+')  
    a = tr4tr.find('a', href=pattern, target='_self', title=True)
    match = re.search(r'details\.php\?id=(\d+)', a.get('href'))
    return match.group(1)


topFreeTorrents = getTopFreeTorrents()
getTorrentId(topFreeTorrents[0])
while True:
    time.sleep(121)
    newTopFreeTorrents = getTopFreeTorrents()
    oldIds = [getTorrentId(torrent) for torrent in topFreeTorrents]
    justNew = []
    for new in newTopFreeTorrents:
        if getTorrentId(new) not in oldIds:
            justNew.append(new)
    if justNew:
        print(f'New torrents found! | {getNow()}')
        print(justNew)
        os.system('start 爱心')
    else:
        print(f'No new torrents found. | {oldIds} | {getNow()}')
    topFreeTorrents = newTopFreeTorrents
