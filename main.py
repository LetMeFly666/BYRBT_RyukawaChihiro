'''
Author: LetMeFly
Date: 2024-08-07 12:12:02
LastEditors: LetMeFly
LastEditTime: 2024-08-09 12:24:11
'''
from src.configer import CONFIG
from src.client import QBittorrent
import requests


qBittorrent = QBittorrent()
# print(qBittorrent.getApplicationVersion())
# qBittorrent.addTorrentTags('a2917e2eecf9fc0f9830323d28d6870e874d0adb', 'keep')
# qBittorrent.addTorrentTags('all', 'keep')
# for sid in [398032, 423007, 398028, 397991, 397992, 398013, 397989, 398021, 397988, 398011, 398038, 397987, 398036, 397983, 352449, 397972, 397967, 397965, 397956, 397957, 402621, 407835, 411182, 380118, 423012, 415834, 415835, 403112, 416046]:
#     qBittorrent.addNewTorrent(sid)