<!--
 * @Author: LetMeFly
 * @Date: 2024-08-07 12:13:14
 * @LastEditors: LetMeFly
 * @LastEditTime: 2024-09-01 23:50:31
-->

<img src="https://cdn.letmefly.xyz/img/ACG/AIGC/BYRBT_RyukawaChihiro/avatar_02.jpg" alt="Logo" align="right" width="150" style="padding: 10px;">

# BYRBT_RyukawaChihiro

流川千寻(Ryukawa Chihiro) - [BRYBT](https://byr.pt)小小刷流姬 - 只会下载(和删除)首页Top且Free的种子。

## 前言

<details><summary>BYRBT是什么？</summary>

大概就是一个<i>只有教育网/外网的ipv6可以访问</i>的种子网站，里面有很多ZiYuan。

</details>

<details><summary>为什么要刷流？</summary>

<ol>
<li>有上传量才能愉快地下载；</li>
<li>上传量达4T可永久保留账号；</li>
<li>看着上传量蹭蹭往上涨，それでいい。</li>
</ol>

</details>

<details><summary>为何重造轮子？</summary>

<p><b>最初</b>是想起来的时候手动刷新一下看看有没有新的top且free的种子，<b>后面</b>写了个小爬虫每121秒帮我看一次新种子，<b>后面</b>懒得手动增删种子了决定交给<i>流川千寻</i>来完成。</p>

所以<i>流川千寻</i>是一只简单纯粹的佛系刷流姬。

</details>

<details><summary>为什么起这个名字？</summary>

因为<del>我想(bushi</del>

</details>

## 如何使用

1. 环境准备：
    
    1. 安装好Python：[python.org](https://www.python.org/downloads/)直接下载无脑安装即可
    2. 安装所需包：`pip install -r requirements.txt`
    3. 下载[源代码](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/archive/refs/heads/master.zip)
    4. 安装[qBittorrent](https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent_4.6.5_x64_setup.exe)（当前支持≥v4.1.x，低版本可能有部分api无法得到完全支持，推荐v4.6.5）

2. **这一步可以跳过**。登录BYRBT，获取你的cookie：

    ![获取cookie](docs/img/howToFindCookie.jpg)

3. star本仓库，要不然，要不然流川千寻就哭给你看！[![star数](https://unv-shield.librian.net/api/unv_shield?repo=LetMeFly666/BYRBT_RyukawaChihiro)](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro)

4. 开启BT客户端的Web用户界面，以qBittorrent为例(当前仅支持这一个客户端)：

    如果按图示设置ip则`client_ip`可以为`http://127.0.0.1:8080`

    ![qbittorrent web settings](docs/img/qbittorrentWeb.jpg)

5. 在`config`目录下新建文件`secret.py`，输入以下内容（可参考[配置说明](#配置说明)部分进行配置）：
    
    ```python
    byrbt_username = 'Tisfy'             # BYRBT的账号
    byrbt_password = 'letmefly.xyz'      # BYRBT的密码
    client_ip = 'http://127.0.0.1:8080'  # 被控制的客户端的web ip
    client_username = 'RyukawaChihiro'   # bt客户端web的用户名
    client_password = '666'              # bt客户端web的密码
    maxDiskUsage = 525.25                # 最大磁盘空间使用量(单位GB)
    ```

6. 执行命令`python main.py`，开始愉快地刷流吧。

## 配置说明

|参数|类型|描述|示例|
|:--:|:--:|:--:|:--:|
|`cookie` *可选*|string|byrpt网页端的cookie，可参考[如何使用](#如何使用)第2步获取。指定cookie可以减少一次登录，若不指定或所指定cookie已过期，流川千寻会依据账号密码登录并将cookie保存在配置文件中|`'eyJ0eXA45454jkjsiu...'`|
|`byrbt_username`|string|BYRBT的账号|`'Tisfy'`|
|`byrbt_password`|string|BYRBT的密码|`'letmefly.xyz'`|
|`client_ip`|string|qBittorrent客户端web ui的地址，可参考[如何使用](#如何使用)第4步进行配置|`'http://127.0.0.1:8080'`|
|`client_username`|string|qBittorrent客户端web ui的用户名，可参考[如何使用](#如何使用)第4步进行配置|`'RyukawaChihiro'`|
|`client_password`|string|qBittorrent客户端web ui的密码，可参考[如何使用](#如何使用)第4步进行配置|`'666'`|
|`maxDiskUsage`|float|为TopFree的种子预留的最大空间（超过此空间的种子将依据一定的策略进行下载或增删），单位GB。请确保预留足够的空间|`525.25`|
|`savePath` *可选*|string|文件要保存到的位置。若不选，则将保存在客户端中设置的默认位置|`''`|
|`refreshTime` *可选*|integer|每隔多长时间查询一次是否有新种子，单位秒。若不选，则默认121s访问一次byrpt|`121`|
|`forceDeleteFile` *可选*|boolean|是否监控文件是否删除成功。如果`True`，则`forceDeleteFile_maxWait`秒后文件仍然在磁盘上的话，开始调用系统命令强制删除本地文件。原因见[#3](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/3)。若勾选，请确保种子文件在本机；默认值为`True`|`True`|
|`forceDeleteFile_maxWait` *可选*|float|调用种子客户端api删除种子及文件多少秒后文件仍在本地，才会强制删除本地文件。只有当`forceDeleteFile`为`True`时此项才会启用。默认值为`15.0`(s)|`15`|

## 运行逻辑

### 标签判定

流川千寻会对种子打上如下标签：

1. `sc`：所有的TopFree的（或流川千寻工作期间TopFree过的）种子都会被打上`sc`标签。这些种子将会被认为不是长期做种的种子，可能会随着过期策略被删除。
2. `toDel`：在TopFree过的种子中，由于免费时长到期等原因，已经不是TopFree的种子。这些种子将优先被删除。如果你不想要某个种子了，你可以手动将其添加toDel标签，流川千寻会在合适的时间删除它。

### 种子判定

[种子判定](#种子判定)每隔`refreshTime`秒进行一次。

判定时访问一次byrpt，返回所有的TopFree种子，包括：种子id、free剩余时长、种子大小、做种者数、下载者数、种子hash。

依据TopFree种子的hash，筛选客户端中的种子。对客户端中所有已经存在的TopFree的种子打一次`sc`标签。

筛选客户端中所有具有`sc`标签的种子。如果已经不在TopFree中，则将被打上`toDel`标签。对于所有具有`sc`标签的种子，统计总磁盘占用。

筛选客户端中所有具有`toDel`标签的种子。

若有TopFree的种子还未下载，则进入[种子下载](#种子下载)。

### 种子下载

对所有待下载的种子，执行下面操作：

```python
当前磁盘总占用, 需下载种子, 具有toDel标签的种子 = 种子判定()
需下载种子.sortBy(有做种者的优先，无做种者的其次。对于有做种者：下载者数/做种者数越大越优先)
具有toDel标签的种子.sortBy(种子添加时间)  # 下载较早的种子优先
for seed in 需下载种子:
    tryToDownload(seed)

def tryToDownload(seed):
    if maxDiskUsage - 当前磁盘总占用 + sum(thisSeed.size for thisSeed in 具有toDel标签的种子) < seed.size:
        return  # “最大占用 - 已经使用 + 可释放” 仍然小于待下载种子，放弃下载 | TODO: 此处可有更优策略
    # 假如按照下载时间从早到晚的顺序种子大小为[1G, 2G, 7G, xxx]，需要释放的空间为8G
    # 则(1+2+7)=10≥8，之后从后往前回滚，10-7<8，10-2=8≥8（不删2），8-1<8，最终决定删除[1G, 7G]的种子
    真正要被删除的种子 = 下载早的优先_直至释放足够空间_从后往前回滚_移除可以不被删的种子()
    for 这次被删除的种子 in 真正要被删除的种子:
        当前磁盘总占用 -= 这次被删的种子.size
        控制客户端删除种子(这次被删的种子)
    reallyDownload(seed)

def reallyDownload(seed):
    当前磁盘总占用 += seed.size
    控制客户端下载种子_并_打上sc标签(seed)
```

## 开发文档

如果你想~~成为流川千寻的一部分~~（想贡献代码），你可以阅读开发文档，流川千寻会非常地高兴。

```
.
├─config                配置目录
├─docs                  文档
└─src                   源码
    ├─client            控制种子客户端的行为
    │  └─qBittorrent    控制qBittorrent下载、删除种子等。如果你想写一个能控制LetBittorrent客户端的功能，可以参考qBittorrent的api接口写一个
    ├─configer          读取和处理配置文件
    ├─controller        策略。当前策略是Readme中所说的FreeTop策略。你也可以新写一个策略
    ├─getter            获取种子信息
    │  └─getBYR         获取BYRBT的种子信息。如果你想获取TJUPT等的种子信息，你也可以参考getBYR的api接口写一个
    ├─logger            日志处理
    └─utils             一些基础工具（函数）
```

## TODO

### 总体需求

- [x] 头像：[https://cdn.letmefly.xyz/img/ACG/AIGC/BYRBT_RyukawaChihiro/avatar_00.jpg](https://cdn.letmefly.xyz/img/ACG/AIGC/BYRBT_RyukawaChihiro/avatar_00.jpg)、avatar_01.jpg、avatar_02.jpg、...
- [x] 磁盘空间考虑
- [x] controller
- [x] Logger
- [x] [fix](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/pull/2): [log失败的问题](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/1) - 磁盘剩余可用空间为0，log写入文件失败
- [x] [fix](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/pull/4): [种子删除失败的问题](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/3) - 即使删除种子时告诉客户端同时删除本地文件，但有时候客户端仍然会把文件保留在磁盘上。现在已经是暂停做种5秒后才删了
- [x] [chore](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/pull/10): [通过cookie获取passkey](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/8) - 这样用户就可以少配置一个东西了:+(
- [x] [fix](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/pull/12): [写入配置文件格式出错](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/11)，然后内存就爆了
- [ ] [多线程删除文件](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/5)：如果`forceDeleteFile_maxWait`秒后文件仍未被删除切手动删除失败，则启动一个后台进程监控文件的状态，当文件可以被释放时删除并结束这个线程
- [ ] [避免产生额外下载量的问题](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/6)：距离Free结束还有10分钟时若还在下载则暂停下载、若某TopFree突然被移除但还在下载则立刻停止下载
- [ ] 账号密码登录byr，在cookie失效时[自动刷新cookie](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/7)
- [ ] [增加配置——最大做种比](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/issues/9)：若一个TopFree的“做种者/下载者”很大则跳过该种子。（例如黑神话悟空之前Top过一次，过了一周左右再次Top了，这时有100多做种者和十来个下载者，且需要占据100多G硬盘空间，可能会导致没有足够的空间下载其他种子。）
- [ ] 更好的种子优先级考虑：下载优先级、上传优先级。emm，挺麻烦的。但是，应该快开学全站Free了。

### 具体细节

- [x] 客户端 - 依据hash获取种子
- [x] 客户端 - 依据标签获取种子
- [x] 客户端 - 依据hash打标签
- [x] 客户端 - 依据种子id下载一个byr种子
- [x] 客户端 - 删除一个本地种子：汇报、暂停、删除 每次操作间隔5秒，防止文件被占用删除失败
- [x] byr - 根据种子id获取hash：此处需有cache
- [x] byr - 获取TopFree种子的信息：种子名、种子id、free剩余时长、种子大小、做种者数、下载者数、种子hash（假设TopFree的种子不会超过一页）
- [x] 通过账号密码登录：config.py：处理cookie和账号密码问题
- [ ] 通过账号密码登录：README：配置说明x2、总体需求勾选
- [ ] 通过账号密码登录：写一个replace函数，替换secret.py中的cookie。正则大概是少不了了，注意不要给用户的注释覆盖了，只能改cookie对应的值

## End

+ 仓库地址：[Github@LetMeFly666/BYRBT_RyukawaChihiro](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro)
+ 在线浏览：[RyukawaChihiro.LetMeFly.XYZ](https://ryukawachihiro.letmefly.xyz/)
+ [我的流量条(教育网/Wai网 ipv6可看)](https://byr.pt/mybar.php?userid=371930&bgpic=3)