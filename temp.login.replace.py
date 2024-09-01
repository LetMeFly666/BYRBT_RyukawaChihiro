'''
Author: LetMeFly
Date: 2024-09-01 12:01:45
LastEditors: LetMeFly
LastEditTime: 2024-09-01 12:04:38
'''
import random
import string

cookie = 'YGI8yzPptledp3PXccUMuVpFMAUhknSiTfn3.qZImd3OkmeTBpQyXCCyoUKV6ktK2CWKsTdYtgoyEYXfgBSf2tiXRUZZ4zlaKPaP2eSf1PeD7RwYnWVKZYhv9yPekvrYrKH27wKN7ZCVXCAYYuOm5mJTgYIscojs9giE1oSy1sQbNidgwws1.SdbCxtjTsVfhKThN0rBO4892QLcxafns5kzDH9TwiWn_yvXSX8AK6wQII3FZ4uBM3y512fKBVxu9eeoPx_I21k'
cookie = list(cookie)
for th, ch in enumerate(cookie):
    if ch in string.ascii_letters:
        cookie[th] = random.choice(string.ascii_letters)
    elif ch in string.digits:
        cookie[th] = random.choice(string.digits)
    else:
        cookie[th] = ch
cookie = ''.join(cookie)
print(cookie)