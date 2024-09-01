'''
Author: LetMeFly
Date: 2024-09-01 09:40:21
LastEditors: LetMeFly
LastEditTime: 2024-09-01 09:45:32
'''
from config import CONFIG

def main():
    print(CONFIG.cookie)
    print(CONFIG.passkey)

def getPasskeyByCookie(cookie: str) -> str:
    return f'{cookie}123'

if __name__ == '__main__':
    main()
