'''
Author: LetMeFly
Date: 2024-08-15 11:36:35
LastEditors: LetMeFly
LastEditTime: 2024-08-15 11:43:41
'''
from os.path import isfile, islink, isdir
from os import remove
from shutil import rmtree

"""删除文件(夹)，返回是否删除成功"""
def forceDelete(path: str) -> bool:
    """
    强制删除指定路径的文件或文件夹。

    参数:
    path (str): 文件或文件夹的路径。

    返回:
    bool: 如果删除成功返回 True，否则返回 False。
    """
    try:
        if isfile(path) or islink(path):
            remove(path)
        elif isdir(path):
            rmtree(path)
        else:
            # 如果路径既不是文件也不是文件夹，则返回 False
            return False
        return True
    except Exception as e:
        print(f"删除失败: {path}. 错误: {e}")
        return False


if __name__ == '__main__':
    # 示例使用
    if forceDelete("/path/to/your/file_or_directory"):
        print("删除成功")
    else:
        print("删除失败或路径不存在")