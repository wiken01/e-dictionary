#!/usr/bin/python3
# tell system call the
#coding=utf-8
#dict_client.py
'''
name:wiken
date:2018-09-28
email:302856076@qq.com
modules:pymongo
this is an e-dictionary
'''
from socket import *
import os
import sys
# standard library
import getpass 


def main():
    # define size of bytes to receive
    BUFFER = 4098
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST,PORT))
        print('have connected')
    except Exception as e :
        print(e)
        return

    while True:
        print('''
        =============Welcome==============
        --1．注册　　--2.登录　　　　　3.退出 
        ==================================
            ''')
        try:
            cmd = int(input("select the num upside:"))
        except Exception as e:
            print(e)
            continue
        if cmd not in [1, 2, 3]:
            print("Incorrect input,Please re-enter")
            # clear input in buffer
            sys.stdin.flush()
        elif cmd == 1:
            name = do_register(s)
            print(name,'name')
            if type(name) is str:
                print("registert successfully")
                # enter secondary interface
                login(s,name)
            elif name == 1:
                print('user name is exist')
            else:
                print("register falsed")
        elif cmd == 2:
            name = do_login(s)            
            if name :
                print('Login successfully')
                # enter secondary interface
                login(s,name)                
            else:
                print('Incorrect user name or password ')
        elif cmd == 3:
            s.send(b'E')
            sys.exit("Thanks for using")

def do_register(s):
    while True:
        name = input("user:")
        # input password in a hide way
        password = getpass.getpass()
        password1 = getpass.getpass("Again:")
        if (" " in name) or (" " in password) :
            print("whitespace is not allowed.Please re-enter")
            continue
        if password != password1:
            print("twice enter not the same,Please re-enter")            
            continue
        msg = "R {} {}".format(name,password)
        # send msg to server
        s.send(msg.encode())
        # receive msg from server
        data = s.recv(128).decode()
        if data == 'ok':
            return name
        elif data =='EXIXTS':
            return 1
        else:
            return 2

def do_login(s):
    name = input('user:')
    password = getpass.getpass()
    msg = 'L {} {}'.format(name,password)
    s.send(msg.encode())
    data = s.recv(128).decode()

    if data == 'ok':
        return name
    else:
        # return None 
        return 

def login(s,name):
    while True:
        print('''
        =============Welcome==============
        --1．查词　　--2.历史记录　　　　　3.退出 
        ==================================
            ''')
        try:
            cmd = int(input("select the num upside:"))
        except Exception as e:
            print(e)
            continue
        if cmd not in [1, 2, 3]:
            print("Incorrect input,Please re-enter")
            continue
        elif cmd == 1:
            do_qurey(s,name)                       
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return
def do_qurey(c,name):
    while True:
        word = input("word:")        
        if word == "##":
            break
        c.send("Q {} {}".format(name,word).encode())
        data = c.recv(128).decode()
        if data == 'ok':
            data = c.recv(2048).decode()
            print(data)
        elif data =="FALL":
            print("Word is not exist")
            print("Re-enter again:")
            
def do_hist(s,name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'ok':
        while True:
            data = s.recv(1024).decode()
            if data == "##":
                print('transfer is complete')
                break
            print(data)

    else:
        print("No history yet")    


main()