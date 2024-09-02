'''
Author: LetMeFly
Date: 2024-08-09 23:26:37
LastEditors: LetMeFly
LastEditTime: 2024-09-02 12:28:15
'''
import requests
from bs4 import BeautifulSoup
from src.configer import CONFIG
from src.utils import untilSuccess, Cacher
import re
from src.logger import logger


"""
真正的重新登录的函数
依据CONFIG中的账号密码登录BYRPT，获取COOKIE并存储在CONFIG中。
"""
def _login() -> None:
    response = requests.post('https://byr.pt/takelogin.php', data={'logintype': 'username', 'userinput': CONFIG.BYRBT_username, 'password': CONFIG.BYRBT_password, 'autologin': 'yes'}, allow_redirects=False)
    cookie = response.cookies.get_dict().get('auth_token')
    CONFIG.cookie = cookie
    with open('config/secret.py', 'a') as f:
        f.write(f'\ncookie = \'{cookie}\'')


"""
除登录外，所有对于BYRPT的请求必须使用此函数！
此函数在COOKIE过期时会重新登录并获取新的COOKIE。
当前仅支持GET请求。
"""
def _baseFunction_requestWithCookieCheck(url: str) -> requests.Response:
    response = requests.get(url, cookies={'auth_token': CONFIG.cookie})
    # 因为cookie中没有设置语言，所以一定会返回中文页面
    mustList = ['未登录!', '注册', '该页面必须在登录后才能访问', '次连续登录失败将导致你的IP地址被禁用!']
    for thisWord in mustList:  # 所有
        if thisWord not in response.text:
            return response
    logger.log('COOKIE过期，重新登录', notShowAgain=False)
    _login()
    return requests.get(url, cookies={'auth_token': CONFIG.cookie})


@untilSuccess(5)
@Cacher('id2hash')
def getHashById(id: str) -> str:    
    logger.log(f'get hash by id({id})')
    response = _baseFunction_requestWithCookieCheck(f'https://byr.pt/details.php?id={id}')
    pattern = re.compile(r'Hash码.*?\s*[:：]\s*<[^>]*>\s*(?:&nbsp;)*\s*([a-z0-9]+)')  # Hash码 数个空格 中文或英文冒号 HTML标签 数个空格 数个&nbsp; 数个空格 小写字母或数字字符串
    match = pattern.search(response.text)
    result = match.group(1)
    return result


"""
在所有的tr中，找到符号如下条件的tr：
    1. tr中具有一个div，其class为'icons sticky-three inverse-y'或'icons sticky-buy inverse-y'或'icons sticky-one inverse-y'或'icons sticky-two inverse-y'
    2. tr中具有一个img，其class为'pro_free'或'pro_free2up'
"""
def _findTopFreeBySoupList(torrents: list) -> list:
    divClasses = [
        'icons sticky-three inverse-y',
        'icons sticky-buy inverse-y',
        'icons sticky-one inverse-y',
        'icons sticky-two inverse-y'
    ]
    imgClasses = ['pro_free', 'pro_free2up']
    ans = []
    for torrent in torrents:
        div = torrent.find('div', class_=divClasses)
        img = torrent.find('img', class_=imgClasses)
        if div and img:
            ans.append(torrent)
    return ans


def _convertSize2bytes(sizeStr: str) -> int:
    # print(sizeStr)
    match = re.match(r"([0-9.]+)([a-zA-Z]+)", sizeStr)
    size = float(match.group(1))
    unit = match.group(2)
    units = {"KiB": 1024, "MiB": 1024 ** 2, "GiB": 1024 ** 3, "TiB": 1024 ** 4}
    return int(size * units[unit])


"""
```
<tr class="free_bg"><td class="rowfollow nowrap" style="vertical-align: middle"><a href="upload.php?quote=318884" title="引用该种子发布"><div class="icons quote"></div></a></td><td class="rowfollow nowrap" style="padding: 0; vertical-align: middle"><div class="cat-icon-merge">
<span class="cat-icon cat-404">
<a class="cat-link" href="torrents.php?cat=404">动漫</a>
</span>
<span class="secocat-icon cat-404">
<a class="secocat-link" href="torrents.php?cat=404&amp;secocat=19">动画</a>
</span>
</div></td>
<td class="rowfollow"><table class="torrentname full transparentbg"><tr><td class="embedded" style="padding-right: 5px"><div class="icons sticky-three inverse-y" title="三
级置顶至2024-08-11 00:11:58"></div></td><td class="embedded" style="width: 99%"><a href="details.php?id=318884&amp;hit=1" target="_self" title="[TV][mawen1250][CLANNAD][S1+S2+Movie+SP Fin][1080p/720p][BDRip/DVDRip][MKV][2007.10][日漫]"><span class="bold">[TV][mawen1250][CLANNAD][S1+S2+Movie+SP Fin][1080p/720p][BDRip/DVDRip][MKV][2007.10][日
漫]</span></a> <img alt="" class="pro_free" src="/pic/trans.gif" title="不计下载量"/><br/>七夕一赏 | 家族 / 克兰娜德 / CLANNAD -クラナド- mawen1250(增补版) 转自U2 </td><td class="embedded" style="text-align: right; "><a href="download.php?id=318884"><div class="icons download ml-4 mb-4" title="下载本种"></div></a><br/><a href="javascript: bookmark(318884,0);" id="bookmark0"><div class="icons delbookmark ml-2" style="display: inline-block" title="收藏"></div></a></td>
</tr></table></td><td class="rowfollow"><span title="无新评论">0</span></td><td class="rowfollow nowrap">2022-03-01<br/>08:35:10</td><td class="rowfollow">125.62<br/>GiB</td><td class="rowfollow"><b><a href="details.php?id=318884&amp;hit=1&amp;dllist=1#seeders">41</a></b></td>
<td class="rowfollow"><b><a href="details.php?id=318884&amp;hit=1&amp;dllist=1#leechers">2</a></b></td>
<td class="rowfollow"><a href="viewsnatches.php?id=318884"><b>288</b></a></td>
<td class="rowfollow"><span style="font-style: italic; font-weight: normal">匿名</span></td></tr>
```

从类似如上的HTML中提取以下信息：
    1. 种子名。如：	[TV][mawen1250][CLANNAD][S1+S2+Movie+SP Fin][1080p/720p][BDRip/DVDRip][MKV][2007.10][日漫]
    2. 种子id。如：318884
    3. free剩余时长。如：2024-08-11 00:11:58
    4. 种子大小（可能会是TiB、GiB、MiB、KiB，统一换为字节）。如：125.62 GiB
    5. 做种者数。如：41
    6. 下载者数。如：2

之后调用getHashById函数获取种子hash
"""
def _getTorrentInfoBySoup(torrent: BeautifulSoup) -> dict:
    info = dict()
    # 1. 种子名
    info['name'] = torrent.select_one('td.embedded > a > span.bold').text
    # 2. 种子id
    info['id'] = torrent.select_one('td.embedded > a')['href'].split('id=')[1].split('&')[0]
    # 3. free剩余时长
    stickyDiv = torrent.select_one('div.icons.sticky-three.inverse-y, div.icons.sticky-buy.inverse-y, div.icons.sticky-one.inverse-y, div.icons.sticky-two.inverse-y')
    info['freeUntil'] = stickyDiv['title'].split('至')[1].strip()
    # 4. 种子大小（转换为字节）
    sizeStr = torrent.select('td.rowfollow')[5].get_text(strip=True).replace('<br/>', ' ')
    info['size'] = _convertSize2bytes(sizeStr)
    # 5. 做种者数
    seedersText = torrent.select('td.rowfollow')[6].get_text(strip=True)
    info['seeders'] = int(seedersText)
    # 6. 下载者数
    leechersText = torrent.select('td.rowfollow')[7].get_text(strip=True)
    info['leechers'] = int(leechersText)
    # 7. 种子hash
    info['hash'] = getHashById(info['id'])
    return info


"""
获取topFree的种子，返回种子列表。
列表每个元素是一个字典，代表一个种子。
字典的键值为：name、id、freeUntil、size、seeders、leechers、hash
"""
@untilSuccess(CONFIG.refreshTime)
def getTopFree() -> list:
    response = _baseFunction_requestWithCookieCheck('https://byr.pt/torrents.php')
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    torrentTable = soup.select_one('table.torrents.coltable.full')
    torrents = torrentTable.find_all('tr', recursive=False)  # 只查找一级tr，不要tr中的tr
    topFree = _findTopFreeBySoupList(torrents)
    ans = []
    for torrent in topFree:
        ans.append(_getTorrentInfoBySoup(torrent))
    return ans


"""
通过CONFIG.cookie获取passkey
"""
def getPasskey() -> str:
    response = _baseFunction_requestWithCookieCheck('https://byr.pt/usercp.php')
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    passkey_td = soup.find('td', text='passkey')
    passkey_value = passkey_td.find_next_sibling('td').text
    return passkey_value
