# -*- coding: utf-8 -*-
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from pycassa.cassandra.ttypes import NotFoundException, ConsistencyLevel

import MySQLdb
import sys
import datetime
import io
import os
import random
import logging
import re
import getopt

reload(sys)
sys.setdefaultencoding('utf-8')

path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=os.path.join(os.getcwd(), path + '/../log/mysql2cassawithinsert.log'), level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s: %(message)s')
log = logging.getLogger('root')

class MysqlImport():
    def __init__(self):
        self.conn = MySQLdb.connect(host="10.107.4.187",user="root",passwd="root",db="contentdb",charset="utf8")
        self.pool = ConnectionPool(keyspace='contentptsp', server_list=['10.107.4.187:9160'], prefill=False)
        #self.pool = ConnectionPool(keyspace='Cassandra_Test', server_list=['10.107.4.187:9160'], prefill=False)
        #pycassa.cassandra.ttypes.NotFoundException: NotFoundException(_message=None, why='Column family content_item not found.')
        #create column family content_item with comparator=UTF8Type and default_validation_class=UTF8Type and key_validation_class=UTF8Type;
        self.columnfamily = ColumnFamily(self.pool, 'content_item')

    def getPageCount(self, table_name, perpage):
        curcount = self.conn.cursor(MySQLdb.cursors.DictCursor)
        sqlstr = 'SELECT count(*) FROM %s' % table_name
        log.info( 'sql statment %s' % sqlstr)
        #equal to result count
        resultcount = curcount.execute(sqlstr)
        if resultcount > 1:
            log.info('get result count success Result count for pagenumber query is \
            : %d' % resultcount)    
        result = curcount.fetchall()
	#############################################################
	#         #Bugs: error, only can fetchall once              #
	# #        print curcount.fetchall()[0]                     #
	# #        print type(curcount.fetchall()[0])               #
	# #        print curcount.fetchall()[0].items()             #
	# #        print str(curcount.fetchall()[0].values())       #
	# #        print curcount.fetchall()[0][0]                  #
	# #        print curcount.fetchall()[0].has_key('count(*)') #
	# #        count = curcount.fetchall()[0]['count(*)']       #
	#############################################################
        count = result[0]['count(*)']
        pagecount = count/perpage
        
        if count%perpage !=0:
            pagecount += 1
        
        log.info('Total %d records, in %d pages' % (count , pagecount ))
        return pagecount
        

    def table(self, table_name):
        #DBG: for debug break point
        #raw_input('check if success')
        cursor    = self.conn.cursor(MySQLdb.cursors.DictCursor)
        ipageidx = 1
        perpage = 100

        pagecount = self.getPageCount(table_name, perpage)

        #IMP : Process by pages, insert record to cassandra, don't put too big page size, it will be send SIGKILLED by system
        for i in range(1, pagecount):
            log.info('current page index is %d' % ipageidx)
            #TODO : Using format string instead '+' for string construction
            #sqlstr = 'SELECT * FROM ' + table_name + ' ORDER BY `id` DESC LIMIT ' \
            #          + str((ipageidx-1)*perpage) + ',' + str((ipageidx)*perpage)
            sqlstr = 'SELECT * FROM %s ORDER BY `id` LIMIT %s, %s' % \
                     (table_name, str((ipageidx-1)*perpage), str((ipageidx)*perpage))
            log.info('SQL Statement is %s' % sqlstr)
            #statement is the result count for this sqlstatment only different than fetchall()
            statement = cursor.execute(sqlstr)
            log.info('query result for sql statement %s is : %d' % (sqlstr, statement))
            if statement <=0 :
                log.error('error in execute sql statement %s, result count = : %d' % (sqlstr, statement))
                #better to be continue, it may failed in middle
                continue
            #########################################################################################
            # #Qz: what's the different?                                                            #
            # #result    = cursor.fetchallDict()                                                    #
            # #Qz: result allways = to all fetched record, not only record count fetch by this time #
            #########################################################################################
            result    = cursor.fetchall()
            log.info('get the len of result count : %d' % len(result))

            for content_item in result:
                #TODO: too many and big, need to remove after release
                log.info('content_item :  %r' % content_item)
                self.insert(content_item)

            ipageidx += 1
            #for debug purpose
            ###########################################
            # c = raw_input('Continue?')              #
            # #if not c == 'Y' or not c == 'y': break #
            # log.info('Input: %r' % c )              #
            # if c == 'Y' or c == 'y':                #
            #     log.info('Input: %r' % c)           #
            #     continue                            #
            # else:                                   #
            #     break                               #
            ###########################################

    def insert(self, data):
        #TODO need to using try catch
        content_item = {}
        for key in data.keys():
            if key != 'id' : content_item[key] = unicode(data[key])
        log.info('constructed content_item dict is :%r ' % content_item)
        self.columnfamily.insert(str(data['id']), content_item)

def usage():
    print "Useage: ..."

if __name__ == '__main__':
    print "script name : ", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "Param : ",  i , sys.argv[i]
    # Long opt "version, file", short opt "h, i, o"
    opts, args = getopt.getopt(sys.argv[1:],  "hi:o:f:t:", ["version", "file="])
    input_file = ''
    output_file = ''
    fromnno = 0
    tono = 0

    for op, value in opts:
        if op == "-i":
            input_file = value
            print 'has -i', input_file
        if op == "-o":
            output_file = value
            print 'has -o', output_file
        if op == "--version":
            print "has --version"
        if op == "--file":
            print "has -- file"
            filename = value
            print filename
        if op == "-h":
            usage()
        if op == "-f":
            fromno = value
            print fromno
        if op == "-t":
            tono = value
            print tono
#    sys.exit()
    raw_input('for debug:')
    c = MysqlImport()
    c.table('content_item')
    
