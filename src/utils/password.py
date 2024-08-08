'''
Author: LetMeFly
Date: 2024-08-08 15:34:16
LastEditors: LetMeFly
LastEditTime: 2024-08-08 17:01:45
'''
from os import name as osName
if osName == 'nt':
    import msvcrt
else:
    import termios
    import tty

import sys
stdout = sys.stdout
stdin = sys.stdin
del sys


if osName == 'nt':  # Windows
    def password(prompt='Password: ', mask='*'):
        password = ''
        stdout.write(prompt)
        stdout.flush()
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:  # Enter key
                stdout.write('\n')
                return password
            elif ch == b'\x08':  # Backspace key
                if len(password) > 0:
                    stdout.write('\b \b')
                    stdout.flush()
                    password = password[:-1]
            elif ch == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt
            else:
                password += ch.decode('utf-8')
                stdout.write(mask)
                stdout.flush()

else:  # Linux and other Unix-like systems
    def password(prompt='Password: ', mask='*'):
        fd = stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO

        try:
            tty.setraw(fd)
            stdout.write(prompt)
            stdout.flush()
            password = ''
            while True:
                ch = stdin.read(1)
                if ch == '\n' or ch == '\r':
                    stdout.write('\r\n')  # 光标移动到行首
                    stdout.flush()
                    break
                elif ch == '\x7f':  # Handle backspace
                    if len(password) > 0:
                        stdout.write('\b \b')
                        stdout.flush()
                        password = password[:-1]
                else:
                    password += ch
                    stdout.write(mask)
                    stdout.flush()
            return password
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == '__main__':
    pwd = password('请输入密码: ')
    print(pwd)
    print(input('normal input: '))
