'''
Author: LetMeFly
Date: 2024-08-09 23:26:37
LastEditors: LetMeFly
LastEditTime: 2024-08-09 23:53:56
'''
import requests
from bs4 import BeautifulSoup
from src.configer import CONFIG
import re

cacher = dict()

def getHashById(id: str) -> str:
    if id in cacher:
        return cacher[id]
    print(f'get hash by id({id})')
    response = requests.get(f'https://byr.pt/details.php?id={id}', cookies={'auth_token': CONFIG.cookie})
    pattern = re.compile(r'Hash码\s*:\s*</b>\s*&nbsp;\s*([a-f0-9]+)')
    match = pattern.search(response.text)
    result = match.group(1)
    cacher[id] = result
    return result




