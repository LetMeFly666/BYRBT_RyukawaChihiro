'''
Author: LetMeFly
Date: 2024-08-10 10:36:45
LastEditors: LetMeFly
LastEditTime: 2024-08-10 11:15:47
'''
from os.path import join
from os import getcwd
import json


"""
Cacher类修饰器，接受cacherName作为参数（只能修饰一个参数的函数）
首先判断是否存在文件，如果存在则读取，否则则创建文件。
每次函数被调用时，首先判断这个参数是否在cache中，如果是则直接返回，否则调用函数并将结果存入cache中，然后返回结果。
"""
class Cacher:
    def __init__(self, cacherName: str):
        self.filePath = join(getcwd(), 'config', f'cacher_{cacherName}.json')
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
                assert isinstance(self.cache, dict)
        except (FileNotFoundError, json.JSONDecodeError, AssertionError):
            self.cache = dict()
            with open(self.filePath, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f)
    
    def __call__(self, func):
        def wrapper(arg):
            if arg in self.cache:
                return self.cache[arg]
            result = func(arg)
            self.cache[arg] = result
            with open(self.filePath, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False)
            return result
        return wrapper
