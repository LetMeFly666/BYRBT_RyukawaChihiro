'''
Author: LetMeFly
Date: 2024-09-01 09:40:17
LastEditors: LetMeFly
LastEditTime: 2024-09-01 09:44:43
'''
class Config:
    def __init__(self) -> None:
        self.cookie = '123'
        from BYR import getPasskeyByCookie
        self.passkey = getPasskeyByCookie(self.cookie)

CONFIG = Config()