'''
Author: LetMeFly
Date: 2024-08-08 15:34:16
LastEditors: LetMeFly
LastEditTime: 2024-08-08 16:44:40
'''
from os import name as osName
import sys

if osName == 'nt':  # Windows
    import msvcrt
    def password(prompt='Password: ', mask='*'):
        password = ''
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:  # Enter key
                sys.stdout.write('\n')
                return password
            elif ch == b'\x08':  # Backspace key
                if len(password) > 0:
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    password = password[:-1]
            elif ch == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt
            else:
                password += ch.decode('utf-8')
                sys.stdout.write(mask)
                sys.stdout.flush()

else:  # Linux and other Unix-like systems
    import termios
    import tty

    def password(prompt='Password: ', mask='*'):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO

        try:
            tty.setraw(fd)
            sys.stdout.write(prompt)
            sys.stdout.flush()
            password = ''
            while True:
                ch = sys.stdin.read(1)
                if ch == '\n' or ch == '\r':
                    sys.stdout.write('\r\n')  # 光标移动到行首
                    sys.stdout.flush()
                    break
                elif ch == '\x7f':  # Handle backspace
                    if len(password) > 0:
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                        password = password[:-1]
                else:
                    password += ch
                    sys.stdout.write(mask)
                    sys.stdout.flush()
            return password
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


if __name__ == '__main__':
    pwd = password('请输入密码: ')
    print(pwd)
    print(input('normal input: '))
