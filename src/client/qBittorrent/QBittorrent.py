'''
Author: LetMeFly
Date: 2024-08-08 10:27:43
LastEditors: LetMeFly
LastEditTime: 2024-08-09 17:55:46
'''
from src.configer import CONFIG
import requests
import time


class QBittorrent:
    def __init__(self) -> None:
        # print('hello from QBittorrent')
        self._login()

    def _login(self) -> None:
        ip = CONFIG.client_ip
        username = CONFIG.client_username
        password = CONFIG.client_password
        response = requests.post(f'{ip}/api/v2/auth/login', data={'username': username, 'password': password})  # 此时还无self.sid，无法使用self._request_post()
        print(response)
        print(response.text)

        self.sid = response.cookies.get('SID')
        # if not self.sid:
        #     raise Exception('Login failed')
    
    def _request_get(self, url: str, data: dict) -> requests.Response:
        return requests.get(url, params=data, cookies={'SID': self.sid})
    
    def _request_post(self, url: str, data: dict) -> requests.Response:
        return requests.post(url, data=data, cookies={'SID': self.sid})
    
    """获取qBittorrent版本号"""
    def getApplicationVersion(self) -> str:
        response = self._request_get(f'{CONFIG.client_ip}/api/v2/app/version', {})
        version = response.text
        return version
    
    """获取qBittorrent默认保存路径"""
    def getDefaultSavePath(self) -> str:
        response = self._request_get(f'{CONFIG.client_ip}/api/v2/app/defaultSavePath', {})
        path = response.text
        return path
    
    """获取qBittorrent日志"""
    def getLog(self) -> str:
        response = self._request_get(f'{CONFIG.client_ip}/api/v2/log/main', {'warning': 'true'})
        log = response.text
        return log
    
    """获取qBittorrent种子列表"""
    def getTorrentList(self, filter: dict) -> list:
        response = self._request_get(f'{CONFIG.client_ip}/api/v2/torrents/info', filter)
        torrentList = response.json()
        return torrentList
    
    """获取qBittorrent种子列表 | hash为hashes"""
    def getTorrentList_byHash(self, hashes: str) -> list:
        # 其中多个hash可用`|`分隔
        return self.getTorrentList({'hashes': hashes})

    """获取qBittorrent种子列表 | tag为tag"""
    def getTorrentList_byTag(self, tag: str) -> list:
        return self.getTorrentList({'tag': tag})
    
    """添加新种子"""
    def addNewTorrent(self, torrentId: str) -> None:
        torrentURL = f'https://byr.pt/download.php?id={torrentId}&passkey={CONFIG.passkey}'
        # print(torrentURL)
        if CONFIG.savePath:
            savePath = CONFIG.savePath
        else:
            savePath = self.getDefaultSavePath()
        response = self._request_post(f'{CONFIG.client_ip}/api/v2/torrents/add', {'urls': torrentURL, 'savepath': savePath, 'tags': 'sc'})
        print(response)
        print(response.text)
    
    """种子打标签"""
    def addTorrentTags(self, hashes: str, tags: str) -> None:
        response = self._request_post(f'{CONFIG.client_ip}/api/v2/torrents/addTags', {'hashes': hashes, 'tags': tags})
        print(response)
        print(response.text)
    
    """强制重新汇报"""
    def forceReannounce(self, hashes: str) -> None:
        response = self._request_post(f'{CONFIG.client_ip}/api/v2/torrents/reannounce', {'hashes': hashes})
        print(response)
        print(response.text)

    """暂停种子"""
    def pauseTorrents(self, hashes: str) -> None:
        response = self._request_post(f'{CONFIG.client_ip}/api/v2/torrents/pause', {'hashes': hashes})
        print(response)
        print(response.text)

    """删除种子"""
    def deleteTorrents(self, hashes: str) -> None:
        self.forceReannounce(hashes)
        time.sleep(5)
        self.pauseTorrents(hashes)
        time.sleep(5)
        response = self._request_post(f'{CONFIG.client_ip}/api/v2/torrents/delete', {'hashes': hashes, 'deleteFiles': True})
        print(response)
        print(response.text)
