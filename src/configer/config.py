'''
Author: LetMeFly
Date: 2024-08-08 10:31:43
LastEditors: LetMeFly
LastEditTime: 2024-08-15 11:03:24
'''
import sys
append = sys.path.append
del sys
from os.path import join, exists
from os import getcwd, mkdir
# 上方较为敏感的包，只引入需要的部分好了
import webbrowser
import time
from src.utils import password


class Config:
    def __init__(self):
        # print('hello from config')
        try:
            append(join(getcwd(), 'config'))
            import secret
            self.cookie = secret.cookie
            self.passkey = secret.passkey
            self.client_ip = secret.client_ip
            if self.client_ip.endswith('/'):
                self.client_ip = self.client_ip[:-1]
            self.client_username = secret.client_username
            self.client_password = secret.client_password
            self.maxDiskUsage = int(secret.maxDiskUsage * 1024 * 1024 * 1024)
            try:
                self.savePath = secret.savePath
            except:
                self.savePath = None
            try:
                self.refreshTime = secret.refreshTime
            except:
                self.refreshTime = 121
            try:
                self.forceDeleteFile = secret.forceDeleteFile
            except:
                self.forceDeleteFile = True
            try:
                self.forceDeleteFile_maxWait = float(secret.forceDeleteFile_maxWait)
            except:
                self.forceDeleteFile_maxWait = 15.0
        except Exception as e:
            print(e)
            print('\n')
            print('看起来你并没有按照说明进行配置')
            print('但是没关系，流川千寻将引导你完成配置')
            print('\n')
            time.sleep(2.5)
            print('现在你只需要关注`如何使用`的第2步')
            time.sleep(2)
            webbrowser.open('https://ryukawachihiro.letmefly.xyz/#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8')
            self._getCookie()
            self._getPasskey()
            self._getClient()
            self._getMaxDiskUsage()

            self.savePath = None
            self.refreshTime = 121
            
            self._saveConfig()
    
    def _saveConfig(self):
        configDir = join(getcwd(), 'config')
        if not exists(configDir):
            mkdir(configDir)
        toWrite = '# generated by 流川千寻\n'
        toWrite += '# how to use: https://ryukawachihiro.letmefly.xyz/\n'
        toWrite += f'cookie = "{self.cookie}"\n'
        toWrite += f'passkey = "{self.passkey}"\n'
        toWrite += f'client_ip = "{self.client_ip}"\n'
        toWrite += f'client_username = "{self.client_username}"\n'
        toWrite += f'client_password = "{self.client_password}"\n'
        toWrite += f'maxDiskUsage = "{self.maxDiskUsage}"\n'
        toWrite += f'savePath = "{self.savePath}"\n'
        toWrite += f'refreshTime = "{self.refreshTime}"\n'
        with open(join(configDir, 'secret.py'), 'w', encoding='utf-8') as f:
            f.write(toWrite)

    def _getCookie(self):
        print('\n')
        print('1. 登录BYRBT: https://byr.pt/')
        print('2. 打开开发人员选项: 空白处右键->检查 OR 按F12 OR 按Fn+F12 OR 按Ctrl+Shift+I')
        print('3. 找到应用选项卡: 点击“应用”或“Application”（可能藏在>>里面）')
        print('4. 找到Cookies: 点击左侧的Cookie->https://byr.pt')
        print('5. 复制Cookie: `auth_token`对应的`值/Value`即为所需')
        print()
        self.cookie = input('你的cookie是：')
    
    def _getPasskey(self):
        print('\n\n')
        print('现在你可以开始关注刚才打开网页的`如何使用`的第3步')
        print()
        print('1. 访问BYRBT的控制面板: https://byr.pt/usercp.php')
        print('2. 复制passkey: 找到`passkey`并复制右边一串字符即为所需')
        print()
        self.passkey = input('你的passkey是：')

    def _getClient(self):
        print('\n\n')
        print('现在你可以开始关注刚才打开网页的`如何使用`的第4步')
        print()
        print('1. 打开qBittorrent客户端，点击“齿轮图标”')
        print('2. 点击“Web用户界面”或“Web UI”')
        print('3. 勾选“Web用户界面（远程控制）”，输入用户名和密码')
        print()
        self.client_ip = input('你设置的ip和端口【例如 http://127.0.0.1:8080】：')
        if self.client_ip.endswith('/'):
            self.client_ip = self.client_ip[:-1]
        self.client_username = input('你设置的用户名是：')
        self.client_password = password('你设置的密码是：')
    
    def _getMaxDiskUsage(self):
        print('\n\n')
        while True:
            try:
                self.maxDiskUsage = int(float(input('你设置的最大磁盘使用量是(单位GB): ')) * 1024 * 1024 * 1024)
                break
            except:
                print('请输入数字，例如525.25')


CONFIG = Config()