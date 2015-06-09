# -*- coding: utf-8 -*-
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from pycassa.cassandra.ttypes import NotFoundException, ConsistencyLevel

import io
import MySQLdb
import sys
import os
import datetime
import random
import logging
import re
reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(os.getcwd(), path + '../log/cassa.log'), level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s: %(message)s')
log = logging.getLogger('root')

class CassaDataLoader():
    def __init__(self):
        try:
            self.pool = ConnectionPool(keyspace='sublime', server_list=['10.107.4.187:9160'], prefill=False)
            self.columnfamily = ColumnFamily(self.pool, 'Content_Item')
        except Exception, e:
            log.info( 'Catch exception : %r' % e)
        else:
            log.info( 'init success' )
        finally:
            log.info( 'init finally' )

    def insert(self, record):
        for key in data.keys():
            if key != 'id' : contentitem[key] = unicode(record[key])
        self.columnfamily.insert(str(record['id']),contentitem)

    def createdata(self, kvdict):
        #create batch insert file
        with io.open('./batchinsert.sql', 'w+', encoding='utf-8') as f:
            f.write(unicode('BEGIN BATCH'))
            f.write(unicode('\n'))
            #TODO write insert method here, there will be problem of key sequence
            f.write(unicode('APPLY BATCH;'))
            f.write(unicode('\n'))
        #create kvlst json file

    def sqlconvert(self, sqlfp, jsonfp):
        #data = open(urls_file, 'r').readlines()[:N]
        f = open(sqlfp, 'r+')
        #f.readline()
        for line in f:
            record = self.insertparser(line)
            log.info('find one record %r' % record)

    def writesql(self, fieldlst, valuelst):
        with io.open('testinsert.sql', 'w', encoding='utf-8') as f:
            f.write(unicode('use contentsp;\n'))
            f.close()
        for i in range(1, 2000000):
            idrad = random.randint(1, 9999999999)
            with io.open('testinsert.sql', 'a+', encoding='utf-8') as f:
                f.write(unicode('INSERT INTO '))
                f.write(unicode('content_items '))
                f.write(unicode('('))
                f.write(unicode(' '))
                i = 1
                for fd in fieldlst:
#                    f.write(unicode('`'))
                    f.write(unicode(fd))
#                    f.write(unicode('`'))
                    if not i == len(fieldlst) : f.write(unicode(','))
                    i += 1
                f.write(unicode(' )'))
                f.write(unicode(' VALUES ('))
                i = 1
                for v in valuelst:
                    if not v.isdigit(): f.write(unicode('\''))
                    if i == 1 : f.write(unicode(idrad))
                    else: f.write(unicode(v))
                    if not v.isdigit(): f.write(unicode('\''))
                    if not i == len(valuelst) : f.write(unicode(','))
                    i += 1
                f.write(unicode(');'))
                f.write(unicode('\n'))


    def insertparser(self, insertstr):
        if insertstr == None or insertstr.strip() == '':
            log.info('empty string or None String')
#        if not insertstr.strip().startswith('insert into') or not insertstr.strip().startswith('INSERT INTO'):
#            log.info('not insert line')
#            log.info('wrong insert grammer')
        if insertstr.find('INSERT INTO') == -1:
            log.info('not found insert into')
        else:
            #log.info('found insert into in line : %s') % insertstr
            log.info('found insert into in line with str.find()')
        p = re.compile(r'^INSERT INTO\s+`\w+`\s\((`\w+`,?\s?)+\)\s+VALUES\s+\(.*\)', re.I)
        m = p.search(insertstr)
        if m:
            log.info('find insert into expression, verify by regular expression')
            #print m.groups()   #print ('`content_type`',) why contain ',' at the end?
            #print m.group()    #print entile string
        else:
            log.info('not insert expression, verify by regular expression')
        ptablename = re.compile(r'`\w+`\s', re.I)
        pspace = re.compile(r'\s') #work but has some problem
        pkv = re.compile(r'\(\w+\)', re.I)
        pk = re.compile(r'\(`.+`\)', re.I) # success find key and field
        pv = re.compile(r'VALUES\s+\(.+\)', re.I)
        strTmp = insertstr.strip().replace('INSERT INTO', '')
        m = pk.match(strTmp)
        if m:
            log.info( m.group())
        else:
            log.info('not match, not found tablename in strTmp')
        #log.info(pspace.split(strTmp))
        #log.info(pkv.split(strTmp))
        #log.info(pkv.findall(strTmp))
        log.info(strTmp)
        log.info(pk.findall(strTmp))
        log.info(pv.findall(strTmp))
        keys = ''
        values = ''
        for str in pk.findall(strTmp):
            keys = str
        for str in pv.findall(strTmp):
            values = str.replace('VALUES', '').strip()
        #value = pv.findall(strTmp)[0].replace('VALUES', '').strip()     #??????
        keys.replace('(', '') # why failed to remove (
        keys.replace(')', '')
        values.replace('(', '')
        values.replace(')', '')
        log.info('key : %s' % keys) 
        log.info('value: %s'% values) 
        pfield = re.compile(r'`\w+`', re.I)
        log.info(pfield.findall(keys))
        pfieldname = re.compile(r'\w+', re.I)
        fieldlst = []
        for fd in pfield.findall(keys):
#            fd.replace('`', '') # again not working why ???
            m = pfieldname.search(fd)
            if m:
                log.info(m.group())
                fieldlst.append(m.group())
        log.info(fieldlst)
        #extra values
        values = values[1:-1]
        pvalue = re.compile(',', re.I)
        pstrwithcomma = re.compile('\'.*,.*\'', re.I)
        valuelst = []
        psi = re.compile('\'', re.I)
#        for v in pvalue.split(values):

        #BUGs: using  ' to split value still has bugs, since 2 int value was adjance
        for v in psi.split(values):
            if not v.strip() == ',':
                v = v.strip()
                if v.startswith(','):
                    v = v.replace(',', '')
                if v.endswith(','):
                    v = v.replace(',', '')
                    v = v.strip().rstrip(',')
                valuelst.append(v.strip())

        kv = {}
        startid = ''
        if len(fieldlst) == len(valuelst):
            log.info('key and values matched size')
            #add write sql file here
            self.writesql(fieldlst, valuelst)
            idx = 0
            for f in fieldlst:
                log.info(f)
                log.info(valuelst[idx])
                kv[f] = valuelst[idx]
                if f == 'id':
                    startid = valuelst[idx]
                    print 'start id: %s' % startid
                idx += 1
            log.info(kv)
            kvlst = []
            for i in range(1, 1000):
                #get randmon number
                idrandom = random.randint(1, 999999)
                tmpKV = {}
                for (d, x) in kv.items():
                    if d == 'id': 
                        tmpKV['id'] = idrandom
                    else:
                        tmpKV[d] = x
                kvlst.append(tmpKV)
            print 'len of result kv list: %d' % len(kvlst)
            log.info( kvlst )
            log.info('create kv data success')
            return kv
        else:
            log.info('size not match')
        ######################################
        # #test insert kv into cassa         #
        #                                    #
        # #create kv list modify the id only #
        # kvlst = []                         #
        # for i in range(100000):            #
        #     #copy kv                       #
        #     tmpKV =                        #
        #     #append to kvlst               #
        #     kvlst.append(tmpKV)            #
        ######################################

if __name__ == '__main__':
    log.info('Start to perpare data')
    log.info('Start to insert data in to Cassa')
    cl = CassaDataLoader();
    cl.sqlconvert('../data/insertdata.sql', '')
    d = {}
    cl.createdata(d)
