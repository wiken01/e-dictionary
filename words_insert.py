#dict.py
'''
Item:a part of e-dictionary
Programmer:wiken
Date:2018-09-28
Note:The function is update the source words of dictionary 
to mysql database
'''
import pymysql
import re
# 
db = pymysql.connect(host = "localhost",port = 3306,
            user = "root",password = "123456",
            database = "dict")
cursor = db.cursor()


with open('dict.txt') as f:    
    while True:        
        data = f.readline()
        if not data:
            break
        r = re.compile('\w+')
        r1 = re.compile("[ ][\S+][\s+\S+\b]+")
        word = r.match(data).group()
        interpret = r1.search(data).group()          
        sql = "insert into words (word,interpret) \
        values('%s','%s')"%(word,interpret)        
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        '''
        text method to deal with string
        with open('dict.txt') as f:
            for line in f:
                l = re.split(r'\s+',line)
                word = l[0]
                intrpret = ' '.split(l[1:])
        '''






