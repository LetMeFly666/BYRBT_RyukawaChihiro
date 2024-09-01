'''
Author: LetMeFly
Date: 2024-08-10 12:06:04
LastEditors: LetMeFly
LastEditTime: 2024-09-01 09:51:31
'''
from src.configer import CONFIG
from src.getter import BYR
from src.client import QBittorrent
from src.utils import convertBytes2humanReadable, convertTimestamp2humanReadable
from src.logger import logger, clearBeforePrint
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
                logger.log(f'不再是TopFree：{seed["name"]}，该种子将被打上toDel标签，在合适的时间被删除')
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
    def _download(self, nowDiskUsage: int, toDownloadSeeds: dict, toDelSeeds: list, qBittorrent: QBittorrent) -> None:
        toDownloadSeeds = self._sortToDownloadSeeds(toDownloadSeeds)
        toDelSeeds = self._sortToDelSeeds(toDelSeeds)
        for seed in toDownloadSeeds:
            maxFree = sum(thisSeed['size'] for thisSeed in toDelSeeds)
            if CONFIG.maxDiskUsage - nowDiskUsage + maxFree < seed['size']:
                logger.log(f'最大空间使用{convertBytes2humanReadable(CONFIG.maxDiskUsage)}，当前空间使用{convertBytes2humanReadable(nowDiskUsage)}，最多释放空间{convertBytes2humanReadable(maxFree)}，小于所需空间{convertBytes2humanReadable(seed["size"])}，无法下载种子{seed["name"]}')
                continue
            requireToFree = seed['size'] - (CONFIG.maxDiskUsage - nowDiskUsage)
            freedSpace = 0
            reallyToDel = []
            for thisToDelSeed in toDelSeeds:
                if freedSpace >= requireToFree:
                    break
                freedSpace += thisToDelSeed['size']
                reallyToDel.append(thisToDelSeed)
            rollbackSeeds = []
            for thisToDelSeed in reversed(reallyToDel):
                if freedSpace - thisToDelSeed['size'] >= requireToFree:
                    rollbackSeeds.append(thisToDelSeed)  # 这个可以不删
                    freedSpace -= thisToDelSeed['size']
            reallyToDel = [seed for seed in reallyToDel if seed not in rollbackSeeds]
            for thisToDelSeed in reallyToDel:
                logger.log(f'删除种子：{thisToDelSeed["name"]} | 添加于：{convertTimestamp2humanReadable(thisToDelSeed["added_on"])}({convertBytes2humanReadable(thisToDelSeed["size"])})', notShowAgain=False)
                qBittorrent.deleteTorrent(thisToDelSeed)
                toDelSeeds.remove(thisToDelSeed)
            logger.log(f'下载种子：{seed["name"]} ({convertBytes2humanReadable(seed["size"])}) | 做种者：{seed["seeders"]} | 下载者：{seed["leechers"]}', notShowAgain=False)
            qBittorrent.addNewTorrent(seed['id'])
            nowDiskUsage += seed['size']

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
        if not toDownloadSeeds:
            clearBeforePrint('没有需要下载的种子')
            return
        nowDiskUsage = self._getNowDiskUsage(scSeeds)
        self._download(nowDiskUsage, toDownloadSeeds, toDelSeeds, qBittorrent)
    
    def run(self) -> None:
        # TODO: remove this log
        print(f'print passkey in TopAndFree: {CONFIG.passkey}')
        print(f'print passkey in TopAndFree, 2: {CONFIG.passkey}')
        exit(0)
        logger.log('流川千寻 · 启动！', notShowAgain=False)
        # self._runOnce()
        while True:
            try:
                clearBeforePrint('新种判断')
                self._runOnce()
            except Exception as e:
                logger.log(f'{e}', notShowAgain=False)
            finally:
                nowSleep = 0
                while nowSleep < CONFIG.refreshTime:
                    thisSleep = min(CONFIG.refreshTime - nowSleep, 1)
                    clearBeforePrint(f'sleep {nowSleep}/{CONFIG.refreshTime} s')
                    time.sleep(thisSleep)
                    nowSleep += thisSleep
