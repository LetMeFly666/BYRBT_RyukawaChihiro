<!--
 * @Author: LetMeFly
 * @Date: 2024-09-01 23:25:35
 * @LastEditors: LetMeFly
 * @LastEditTime: 2024-09-01 23:43:21
-->
CONFIG写配置文件的时候错误，将maxDiskUsage写成了字符串，导致`* 1024 * 1024 * 1024`时占据内存过大


我记得之前测试过呀，今天再次测试用户默认配置失败的情景（一步一步引导用户配置，并将结果写入配置文件），本应该写入浮点类型，错误地写入了字符串类型。

这就导致了GB转字节变成了字符串倍增，直接占用十几个G的内存（以及Windows微软输入法的BUG）。

BUG引入来源：[this line](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/blob/fd4cd5eda1be53b5c8be7b01d4d2d885f58cb23b/src/configer/config.py#L71)、[a commit](https://github.com/LetMeFly666/BYRBT_RyukawaChihiro/commit/fd4cd5eda1be53b5c8be7b01d4d2d885f58cb23b#r146072123)

---

微软输入法的BUG：打字的时候有的候选词重叠了，有的变成方块了。但是输入后的文字正常。

《由于bug导致内存将满导致系统读写占满机械硬盘，最终微软输入法出现BUG。视频发布的话记得回来更新issue.mkv》