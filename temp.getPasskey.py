'''
Author: LetMeFly
Date: 2024-08-31 23:37:37
LastEditors: LetMeFly
LastEditTime: 2024-08-31 23:37:41
'''
from bs4 import BeautifulSoup

# 假设这是你要解析的HTML内容
html_content = """
<tr><td style="width: 1%" class="rowhead nowrap">passkey</td><td class="rowfollow" style="text-align: left">54sieiouihsihfiu8y3ihsjkhfk</td></tr>
"""

# 解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 找到包含"passkey"文本的<td>标签
passkey_td = soup.find('td', text='passkey')

# 如果找到了该<td>，则获取它的下一个<td>标签内容
if passkey_td:
    passkey_value = passkey_td.find_next_sibling('td').text
    print(passkey_value)
else:
    print("没有找到passkey的值")
