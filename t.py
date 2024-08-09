'''
Author: LetMeFly
Date: 2024-08-09 23:46:03
LastEditors: LetMeFly
LastEditTime: 2024-08-09 23:49:43
'''

import re

# 给定的HTML段落
html_content = open('temp.html', 'r', encoding='utf-8').read()


# 正则表达式匹配Hash码
pattern = re.compile(r'Hash码\s*:\s*</b>\s*&nbsp;\s*([a-f0-9]+)')
match = pattern.search(html_content)

# 如果匹配成功，输出Hash码
if match:
    hash_value = match.group(1)
    print(f'Hash码: {hash_value}')
else:
    print('Hash码未找到')
