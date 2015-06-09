from pycassa.pool import ConnectionPool
from pycassa.columnfamilymap import ColumnFamilyMap
from pycassa.columnfamily import ColumnFamily
import traceback
from pycassa.cassandra.ttypes import *
import pycassa

if __name__ == '__main__':
    pool = ConnectionPool('Cassandra_Test',['10.107.4.187:9160'])
    col_fam =  ColumnFamily(pool, 'Users')
    print col_fam.get('author')
    print col_fam.get_count('author')
    b = col_fam.batch(queue_size=10)
    b.insert('key1', {'col1':'value11', 'col2':'value21'})
    b.insert('key2', {'col1':'value12', 'col2':'value22'}, ttl=15)
    try:
        print 'get key1 before send : %r' % col_fam.get('key1')
    except pycassa.cassandra.ttypes.NotFoundException, e:
        print 'Catch not found Exception : %r' % e
    except Exception, e:
        print traceback.format_exc()
    else:
        print 'no exception'
    finally:
        print 'Final'
    b.remove('key1', ['col2'])
    b.remove('key2')
    b.send()
    print 'get key1 after send : %r' % col_fam.get('key1')
