'''
Author: LetMeFly
Date: 2024-08-10 10:28:18
LastEditors: LetMeFly
LastEditTime: 2024-08-10 11:45:44
'''
def convert_bytes_to_human_readable(size_bytes: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    index = 0
    while size_bytes >= 1024 and index < len(units) - 1:
        size_bytes /= 1024.0
        index += 1
    return f"{size_bytes:.2f} {units[index]}"

# 示例使用
print(convert_bytes_to_human_readable(134883447930))  # 输出: 125.62 GiB





from bs4 import BeautifulSoup

html = """
<table>
    <tr>
        <td>
            <div class="icons sticky-three inverse-y"></div>
            <img class="pro_free" />
        </td>
    </tr>
    <tr>
        <td>
            <div class="icons sticky-buy inverse-y"></div>
            <img class="pro_free2up" />
        </td>
    </tr>
    <tr>
        <td>
            <div class="icons other-class"></div>
            <img class="pro_free" />
        </td>
    </tr>
    <tr>
        <td>
            <div class="icons sticky-one inverse-y"></div>
        </td>
    </tr>
    <tr>
        <td>
            <img class="pro_free2up" />
        </td>
    </tr>
</table>
"""

soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table')

# 条件1的div class列表
div_classes = [
    'icons sticky-three inverse-y',
    'icons sticky-buy inverse-y',
    'icons sticky-one inverse-y',
    'icons sticky-two inverse-y'
]

# 条件2的img class列表
img_classes = ['pro_free', 'pro_free2up']

# 查找符合条件的tr
matching_trs = []
for tr in table.find_all('tr'):
    div = tr.find('div', class_=div_classes)
    img = tr.find('img', class_=img_classes)
    if div and img:
        matching_trs.append(tr)

# 输出符合条件的tr
for tr in matching_trs:
    print(tr)
