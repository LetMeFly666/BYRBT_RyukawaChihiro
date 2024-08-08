'''
Author: LetMeFly
Date: 2024-08-07 12:12:02
LastEditors: LetMeFly
LastEditTime: 2024-08-08 23:25:12
'''
from src.configer import CONFIG
from src.client import QBittorrent
import requests


qBittorrent = QBittorrent()
print(qBittorrent.getApplicationVersion())
# qBittorrent.addNewTorrent('397910')
# qBittorrent.addTorrentTags('a2917e2eecf9fc0f9830323d28d6870e874d0adb', 'keep')
qBittorrent.addTorrentTags('all', 'keep')