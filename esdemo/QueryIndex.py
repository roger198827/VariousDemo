#!/usr/bin/env python
#coding=utf-8


import sys
import json
import urllib2

keyword = sys.argv[1]
#keyword = 'google'

obj = {'query': {'query_string': {'query': keyword}}}

obj['query']['query_string']['fields'] = ['keyword']

url = "http://localhost:9200/news/_search"

data = json.dumps(obj).encode('utf-8')

print data
req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

f = urllib2.urlopen(req)
response = f.read()
print response
f.close()


