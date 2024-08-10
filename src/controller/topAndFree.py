'''
Author: LetMeFly
Date: 2024-08-10 12:06:04
LastEditors: LetMeFly
LastEditTime: 2024-08-10 18:28:52
'''
from src.configer import CONFIG
from src.getter import BYR
from src.client import QBittorrent
from src.utils import convertBytes2humanReadable, convertTimestamp2humanReadable
import time

class TopAndFree:
    def __init__(self) -> None:
        pass

    """将哈希列表拼接成hash字符串"""
    def _connectHashStr_byHashList(self, hashList: list) -> str:
        ans = ''
        for hash in hashList:
            if ans:
                ans += '|'
            ans += hash
        return ans

    """将种子列表拼接成hash字符串"""
    def _connectHashStr_byTorrent(self, torrents: list) -> str:
        return self._connectHashStr_byHashList([torrent['hash'] for torrent in torrents])
    
    """给sc标签的不是topFree的种子打上toDel标签"""
    def _addToDelTag(self, scSeeds: list, topFreeHashes: str, qBittorrent: QBittorrent) -> None:
        notTopfreeHashList = []
        for seed in scSeeds:
            if seed['hash'] not in topFreeHashes:
                notTopfreeHashList.append(seed['hash'])
        if not notTopfreeHashList:
            return
        notTopfreeHashes = self._connectHashStr_byHashList(notTopfreeHashList)
        qBittorrent.addTorrentTags(notTopfreeHashes, 'toDel')
    
    """获取topFree但是还没被下载的种子"""
    def _getToDownloadSeeds(self, topFree: list, alreadyHashes: str) -> list:
        ans = []
        for seed in topFree:
            if seed['hash'] not in alreadyHashes:
                ans.append(seed)
        return ans
    
    """尝试下载"""
    def _download(self, nowDiskUsage: int, toDownloadSeeds: dict, toDelSeeds: list) -> None:
        toDownloadSeeds = self._sortToDownloadSeeds(toDownloadSeeds)
        toDelSeeds = self._sortToDelSeeds(toDelSeeds)
        for seed in toDownloadSeeds:
            maxFree = sum(thisSeed['size'] for thisSeed in toDelSeeds)
            if CONFIG.maxDiskUsage - nowDiskUsage + maxFree < seed['size']:
                print(f'最大空间使用{convertBytes2humanReadable(CONFIG.maxDiskUsage)}，当前空间使用{convertBytes2humanReadable(nowDiskUsage)}，最多释放空间{convertBytes2humanReadable(maxFree)}，小于所需空间{convertBytes2humanReadable(seed["size"])}，无法下载种子{seed["name"]}')
                continue
            while CONFIG.maxDiskUsage - nowDiskUsage < seed['size']:
                thisToDelSeed = toDelSeeds.pop(0)
                nowDiskUsage -= thisToDelSeed['size']
                print(f'删除种子：{thisToDelSeed["name"]} | 添加于：{convertTimestamp2humanReadable(thisToDelSeed["added_on"])}({convertBytes2humanReadable(thisToDelSeed["size"])})')
                # QBittorrent.deleteTorrents([thisToDelSeed['hash']])
            print('下载种子：', seed['name'])
            # QBittorrent.addNewTorrent(seed['id'])

    """获取当前sc种子占据的磁盘空间"""
    def _getNowDiskUsage(self, scTorrents: list) -> int:
        ans = 0
        for torrent in scTorrents:
            ans += int(torrent['size'])
        return ans
    
    """排序需要下载的种子：有做种者的优先，无做种者的其次。对于有做种者：下载者数/做种者数越大越优先"""
    def _sortToDownloadSeeds(self, toDownloadSeeds: list) -> list:
        toDownloadSeeds.sort(key=lambda x: (
            -1 if x['seeders'] else 1,
            -x['leechers'] / x['seeders'] if x['seeders'] else -x['leechers']
        ))
        return toDownloadSeeds
    
    """排序具有toDel标签的种子：种子添加时间早的优先"""
    def _sortToDelSeeds(self, toDelSeeds: list) -> list:
        toDelSeeds.sort(key=lambda x: x['added_on'])
        return toDelSeeds

    def _runOnce(self) -> None:
        topFree = BYR.getTopFree()
        topfreeHashes = self._connectHashStr_byTorrent(topFree)
        qBittorrent = QBittorrent()  # 每次重新登录好了
        qBittorrent.addTorrentTags(topfreeHashes, 'sc')
        scSeeds = qBittorrent.getTorrentList_byTag('sc')
        scseedsHahses = self._connectHashStr_byTorrent(scSeeds)
        self._addToDelTag(scSeeds, topfreeHashes, qBittorrent)
        toDelSeeds = qBittorrent.getTorrentList_byTag('toDel')
        toDownloadSeeds = self._getToDownloadSeeds(topFree, scseedsHahses)
        nowDiskUsage = self._getNowDiskUsage(scSeeds)
        self._download(nowDiskUsage, toDownloadSeeds, toDelSeeds)
        
        


    def run(self) -> None:
        # self._runOnce()
        while True:
            try:
                self._runOnce()
            except Exception as e:
                print(e)
            finally:
                time.sleep(CONFIG.refreshTime)
