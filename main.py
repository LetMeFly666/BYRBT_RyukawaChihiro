'''
Author: LetMeFly
Date: 2024-08-07 12:12:02
LastEditors: LetMeFly
LastEditTime: 2024-08-08 10:22:02
'''
import random
import string
a = '3o7jekpbc0tt9bcehm1f5zm38823rguv'
toChoose = string.ascii_lowercase + string.digits
print(toChoose)
b = ''.join(random.choices(toChoose, k=len(a)))
print(b)

# from src