#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *

context.terminal='zsh'
pty = process.PTY

for x in range(10):
    for y in range(10):
        sh = process('./lucky_numbers', stdin=pty, stdout=pty, level='error')
        firstNumber = str(x)
        secondNumber = str(y)
        sh.sendline(firstNumber+secondNumber)
        line2 = sh.recvline()

        if b'Good' in line2:
            print('Found it... {x}{y}'.format(x=x, y=y))

