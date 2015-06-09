#!/usr/bin/env python
#coding=utf-8

import sys
import json
import urllib2

f = open(sys.argv[1], 'r')

for line in f:
    obj = json.loads(line, encoding="utf8")
    #print obj
    url = "http://localhost:9200/news/" + str(obj['lang']) + "/" + str(obj['id'])
    print url

    data = json.dumps(obj['data']).encode('utf-8')

    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

    f = urllib2.urlopen(req)
    response = f.read()
    print response
    f.close()



