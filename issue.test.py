'''
Author: LetMeFly
Date: 2024-08-15 11:54:52
LastEditors: LetMeFly
LastEditTime: 2024-08-15 11:55:07
'''
from src.client import QBittorrent
qBittorrent = QBittorrent()
seedInfo: dict = qBittorrent.getTorrentList_byHash('c3377e71ad4f9d25a2905cf53232ae158a97c3da')[0]
print(seedInfo)
qBittorrent.deleteTorrent(seedInfo)
