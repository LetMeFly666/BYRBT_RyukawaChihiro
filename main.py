'''
Author: LetMeFly
Date: 2024-08-07 12:12:02
LastEditors: LetMeFly
LastEditTime: 2024-08-09 18:00:42
'''
from src.configer import CONFIG
from src.client import QBittorrent


qBittorrent = QBittorrent()

"""客户端 - 依据hash获取种子"""
# torrentList = qBittorrent.getTorrentList_byHash('b8847ce3975bb0a28e58851b13dc7b6bf1d74f31|8a61a54b524b076cf6ea58ee96aa13fc1373d1ed|6a617e0a58bbab70ea50417ec49984535f02ce41')  # 存在|存在|已删除
# print(torrentList)

"""客户端 - 依据标签获取种子"""
# import json
# torrentList = qBittorrent.getTorrentList_byTag('sc')
# print(json.dumps(torrentList, indent=4, ensure_ascii=False))

"""客户端 - 依据hash打标签"""
# qBittorrent.addTorrentTags('4c836303f4b77e7a1116af92f9acae0b2be8940d|d4f41f1247139f1a2d1c9ce1c0c530340c54d3bf', 'keep')

"""客户端 - 依据种子id下载一个byr种子"""
# qBittorrent.addNewTorrent('310018')

"""客户端 - 删除一个本地种子"""
# # # 强制汇报
# # qBittorrent.forceReannounce('a2917e2eecf9fc0f9830323d28d6870e874d0adb')
# # # 暂停做种
# # qBittorrent.pauseTorrents('e305bd401fedb196ae7cac54b5d9f5f7767eccdc')
# qBittorrent.deleteTorrents('688ccbbadcef9569b7fa2dbe4ea6e1a1d2d0f92b')