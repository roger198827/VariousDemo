#!/usr/bin/env python
#coding=utf-8

import pymysql
import json
import datetime
import time
from time import mktime

conn = pymysql.connect(host='ec2-54-195-115-4.eu-west-1.compute.amazonaws.com', user='root', passwd='devenv0001',
                       db='sumsum', charset='utf8')
#conn = pymysql.connect(host='localhost', user='root', passwd='devenv0001', db='sumsum', charset='utf8',
#                       unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock')

cursor = conn.cursor()

count = cursor.execute('select id from content_item limit 100')

#print count

cursor.scroll(0, mode='absolute')

results = cursor.fetchall()

keylist = []
for r in results:
    keylist.append(r[0])

#print len(keylist)



for k in keylist:
    sql = 'SELECT n.*,t.name FROM content_item n left join topic t on t.code=n.topic where n.id= ' + str(
        k) + ' limit 100'
    count = cursor.execute(sql)
    rs = cursor.fetchall()
    for r in rs:
        out = {}
        out['id'] = r[0]

        out['data'] = {}
        out['data']['title'] = r[1]
        try:
            out['data']['date'] = r[4].strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            out['data']['date'] = str(r[4])
        out['data']['content'] = r[7]

        out['data']['topic'] = r[14]

        out['lang'] = r[9]
        out['area'] = r[10]
        out['src'] = r[12]

        # print r[14]
        print json.dumps(out, ensure_ascii=False).encode('utf8')

conn.close()
