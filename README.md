<!--
 * @Author: LetMeFly
 * @Date: 2024-08-07 12:13:14
 * @LastEditors: LetMeFly
 * @LastEditTime: 2024-08-08 22:47:34
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

1. 安装好Python：[python.org](https://www.python.org/downloads/)直接下载无脑安装即可
2. 登录BYRBT，获取你的cookie：

    ![获取cookie](docs/img/howToFindCookie.jpg)

3. 登录BYRBT，获取你的passkey：
    
    访问[`https://byr.pt/usercp.php`](https://byr.pt/usercp.php)，找到`passkey`并将后面的一串值复制

    ![获取passkey](docs/img/getPasskey.jpg)

4. 开启BT客户端的Web用户界面，以qBittorrent为例(当前仅支持这一个客户端)：

    如果按图示设置ip则`client_ip`可以为`http://127.0.0.1:8080`

    ![qbittorrent web settings](docs/img/qbittorrentWeb.jpg)

5. 在`config`目录下新建文件`secret.py`，输入以下内容：
    
    ```python
    cookie = 'eyJ0eXA...第2步获取到的值'
    passkey = '第3步获取到的值'
    client_ip = 'http://127.0.0.1:8080'  # 被控制的客户端的web ip
    client_username = 'RyukawaChihiro'   # bt客户端web的用户名
    client_password = '666'              # bt客户端web的密码
    savePath = ''                        # 【可选】默认保存路径
    ```

## 开发文档





## TODO


- [x] 头像：[https://cdn.letmefly.xyz/img/ACG/AIGC/BYRBT_RyukawaChihiro/avatar_00.jpg](https://cdn.letmefly.xyz/img/ACG/AIGC/BYRBT_RyukawaChihiro/avatar_00.jpg)、avatar_01.jpg、avatar_02.jpg、...
- [ ] 磁盘空间考虑，这就需要优先级考虑

## End

+ 仓库地址：[Github@LetMeFly666/BYRBT_RyukawaChihiro](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro)
+ 在线浏览：[RyukawaChihiro.LetMeFly.XYZ](https://ryukawachihiro.letmefly.xyz/)
+ [我的流量条](https://byr.pt/mybar.php?userid=371930&bgpic=3)