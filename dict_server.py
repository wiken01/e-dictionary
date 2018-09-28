#dict_server.py
'''
name:wiken
date:2018-09-28
email:302856076@qq.com
modules:pymongo
this is an e-dictionary 
'''
from socket import *
import os 
import time
import signal
import pymysql
import sys

def do_child(c,db):
    # receive request from clint looply
    BUFFER = 4096
    while True:
        data = c.recv(BUFFER).decode()        
        print(c.getpeername(),":",data)        
        if (not data) or (data[0] =='E'):
            c.close()
            sys.exit(0)
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)



def do_register(c,db,data):
    print("register operation")
    l = data.split(" ")
    print(l,'l')
    name = l[1]
    password = l[2]
    cursor = db.cursor()
    sql = "select name from user where name = '%s'"%name
    # check name  in database
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        c.send(b'EXISTS')
        return
    # user does not exist    
    sql = "insert into user (name,password)\
    values('%s','%s')"%(name,password)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'ok')
    except:
        db.rollback()
        c.send(b'FALL')
    else:
        print()

def do_query(c,db,data):
    l = data.split(" ")
    print(l,'l')
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():        
        tm = time.ctime()
        sql = "insert into hist (name,word,time)\
        values('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            db.rollback()            

    # here query in text for example
    try:
        f = open('dict.txt')
    except:
        c.send(b"FALL")
        return
    for line in f:
        tmp = line.split(" ")[0]
        if tmp > word:
            c.send(b'FALL')
            f.close()
            return
        elif tmp == word:
            c.send(b'ok')
            insert_history()
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            return
    s.send(b'FALL')    
    f.close()

def do_hist(c,db,data):
    print("words history")
    l = data.split(" ")    
    name = l[1]    
    cursor = db.cursor()
    sql = "select word from hist where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    #
    # r = cursor.fetchmany(10)
    if not r:
        c.send(b'FALL')
        return
    else:
        c.send(b'ok')
    for i in r:
        time.sleep(0.1)
        msg = " %s"%i
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')

def do_login(c,db,data):    
    print("login")    
    l = data.split(" ")    
    name = l[1]
    password = l[2]
    cursor = db.cursor()
    sql = "select name from user where name = '%s'\
    and password = '%s'"%(name,password)
    # check name  in database
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'ok')    


# define global variables
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

# process control
def main():
    # create connection of database
    db = pymysql.connect\
    ('localhost','root','123456','dict')

    # create socket
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    # ignore the signal from child process 
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            print("waiting for connecting")
            c,addr = s.accept()
            print("Connect form",addr)
        # when keyboard enter 'ctrl+c'
        except KeyboardInterrupt:            
            s.close()
            sys.exit("Server exit")
        except Exception as e :
            print(e)
            continue

        # create child process
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c,db)
            print("handle with child process")
            sys.exit()
        else:
            c.close()
            continue
main()