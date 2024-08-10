'''
Author: LetMeFly
Date: 2024-08-10 18:15:01
LastEditors: LetMeFly
LastEditTime: 2024-08-10 18:25:45
'''
from datetime import datetime


"""将字节数转为人类可阅读的字符串 | 例如：21.51 GiB"""
def convertBytes2humanReadable(size_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    index = 0
    while size_bytes >= 1024 and index < len(units) - 1:
        size_bytes /= 1024.0
        index += 1
    return f"{size_bytes:.2f} {units[index]}"


"""将时间戳转为人类可阅读的字符串 | 例如：2024-08-10 18:15:01"""
def convertTimestamp2humanReadable(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")