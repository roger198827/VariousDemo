#!/usr/bin/env python
#coding=utf-8

import sys
sys.path.append("..")
import json
import urllib2

import rake

rakers = {}

#initKeyword extractor
rakers['en-gb'] = rake.Rake('./SmartStoplist.txt')
rakers['en-us'] = rake.Rake('./SmartStoplist.txt')
rakers['sv'] = rake.Rake('./sw-sv.txt')

print 'argv len', len(sys.argv)
if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    file_name = 'OutputJson.dat'

f = open(file_name, 'r')

for line in f:
    obj = json.loads(line, encoding="utf8")
    #print obj
    url = "http://localhost:9200/news/" + str(obj['lang']) + "/" + str(obj['id'])
    lang = obj['lang']
    if lang in rakers:
        kw_can = rakers[lang].run(obj['data']['content'])
        kw_list = []
        for k in kw_can:
            if k[1] > 4.0:
                kw_list.append(k[0])
        obj['data']['keyword'] = kw_list
        #print kw_list
    else:
        continue

    data = json.dumps(obj['data']).encode('utf-8')

    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})

    f = urllib2.urlopen(req)
    response = f.read()
    print response
    f.close()




