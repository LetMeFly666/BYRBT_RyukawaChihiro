'''
Author: LetMeFly
Date: 2024-08-10 09:57:59
LastEditors: LetMeFly
LastEditTime: 2024-08-10 10:01:30
Description: 直到成功，否则休眠delay后重试
'''
import functools
import time


def untilSuccess(delay=121):
    def retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                time.sleep(delay)
        return wrapper
    return retry


if __name__ == '__main__':
    times = 0

    @untilSuccess(0.5)  # 间隔0.5s后重试
    def successUntil3rdTry():
        global times
        times += 1
        if times < 3:
            raise Exception('not success')
        return 'success'
    
    result = successUntil3rdTry()
    print(result)
