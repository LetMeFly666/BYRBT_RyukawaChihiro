'''
Author: LetMeFly
Date: 2024-09-01 09:40:17
LastEditors: LetMeFly
LastEditTime: 2024-09-01 09:44:43
'''
class Config:
    def __init__(self) -> None:
        self.cookie = '123'
        self._passkey = None
    
    @property
    def passkey(self) -> str:
        if not self._passkey:
            from BYR import getPasskeyByCookie
            self._passkey = getPasskeyByCookie(self.cookie)
        return self._passkey

CONFIG = Config()