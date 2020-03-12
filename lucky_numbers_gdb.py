#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdb

gdb.execute('file ./lucky_numbers')

gdb.execute('b *0x804903a') # start
gdb.execute('b *0x8049066') # jump
gdb.execute('b *0x804907e') # after compare
gdb.execute('b *0x8049083') # after compare

# lets rock babe
gdb.execute('run')
gdb.execute('jump *0x8049066')

flag = ''

for a in "0123456789":
    for b in "0123456789":
        gdb.execute("set *0x804a024='{n}'".format(n=a))
        gdb.execute("set *0x804a025='{n}'".format(n=b))

        gdb.execute('continue') # will stop at 0x804907e

        eflags = gdb.selected_frame().read_register('eflags').format_string()
        al = gdb.selected_frame().read_register('eax')
        bl = gdb.selected_frame().read_register('ebx')

        message = 'al={al}({a}), bl={bl}({b}), eflags={eflags}'.format(a=a,b=b,al=hex(al),bl=hex(bl),eflags=eflags)

        if 'ZF' in eflags:
            gdb.execute('continue') # will stop at 0x804907e
            eflags = gdb.selected_frame().read_register('eflags').format_string()

            if 'ZF' in eflags:
                flag = '{a}{b}'.format(a=a,b=b)
                print('Good numbers')
                print('Flag:', flag)
                exit(0)

            gdb.execute('jump *0x8049066')
        else:
            gdb.execute('jump *0x8049066')


