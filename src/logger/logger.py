'''
Author: LetMeFly
Date: 2024-08-10 18:39:43
LastEditors: LetMeFly
LastEditTime: 2024-08-10 19:24:19
'''
import sys
stdout = sys.stdout
del sys
from os.path import join, exists, dirname
from os import makedirs, getcwd


"""首先将光标移动到这一行的行首，然后清空这一行，再输出字符串，不回车"""
def clearBeforePrint(message: str) -> None:
    # 将光标移动到当前行的行首
    stdout.write('\r')
    # 清空当前行的内容
    stdout.write('\033[K')
    # 输出新的日志信息
    stdout.write(message)
    # 确保立即刷新输出到终端
    stdout.flush()


"""
首先判断config/log.txt是否存在，若不存在则创建
之后写一个log方法，接受一个字符串，将其输出到控制台，并写入到文件中
如果这次的字符串和上次的相同，则不进行任何操作
"""
class Logger:
    def __init__(self):
        self.logFilePath = join(getcwd(), 'config', 'log.txt')
        if not exists(dirname(self.logFilePath)):
            makedirs(dirname(self.logFilePath))
        if not exists(self.logFilePath):
            with open(self.logFilePath, 'w', encoding='utf-8') as file:
                pass
        self.historyLogs = self._loadHistoryLogs()

    def _loadHistoryLogs(self):
        logs = set()
        if exists(self.logFilePath):
            with open(self.logFilePath, 'r', encoding='utf-8') as file:
                for line in file:
                    logs.add(line.strip())
        return logs

    def log(self, message: str, notShowAgain: bool = True) -> None:
        if notShowAgain and message in self.historyLogs:
            return
        clearBeforePrint(message)
        print()  # 回车后上一行信息不会被覆盖
        with open(self.logFilePath, 'a', encoding='utf-8') as file:
            file.write(message + '\n')
        self.historyLogs.add(message)


if __name__ == '__main__':
    logger = Logger()
    logger.log("This is the first log message.")
    logger.log("This is the first log message.")  # 不会重复写入
    logger.log("This is the second log message.")
    logger.log("This is the first log message.")  # 会重复写入

    clearBeforePrint("Loading... 50%")
    # 模拟进度更新
    import time
    time.sleep(1)
    clearBeforePrint("Loading... 75%")
    time.sleep(1)
    clearBeforePrint("Loading... 100%")
    time.sleep(1)
    clearBeforePrint("Done!")


logger = Logger()