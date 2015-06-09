from pycassa.pool import ConnectionPool
from pycassa.columnfamilymap import ColumnFamilyMap
from pycassa.columnfamily import ColumnFamily


if __name__ == '__main__':
    #['10.15.62.100:9160','10.15.62.101:9160','10.15.62.102:9160'] 
    pool = ConnectionPool('Cassandra_Test',['10.107.4.187:9160'])
    print pool
#    cf_map = ColumnFamilyMap(User, pool, 'Users')
    col_fam =  ColumnFamily(pool, 'Users')
    print col_fam.get('author')
    print col_fam.get_count('author')
    col_fam.insert('row_key', {'col_name': 'col_val'})
    col_fam.insert('row_key', {'col_name':'col_val', 'col_name2':'col_val2'})
    col_fam.batch_insert({'row1': {'name1': 'val1', 'name2': 'val2'},'row2': {'foo': 'bar'}})
    #col_fam.insert('super_key', {'key':{'col_name':'col_val', 'col_name2':'col_val2'}})
    print col_fam.get_count('row_key', columns=['foo', 'bar'])
    print col_fam.get_count('row_key', column_start='foo') 
    print col_fam.multiget_count(['fib0', 'fib1', 'fib2', 'fib3', 'fib4'])
    print col_fam.multiget_count(['fib0', 'fib1', 'fib2', 'fib3', 'fib4'],columns=['col1', 'col2', 'col3'])
    print col_fam.multiget_count(['fib0', 'fib1', 'fib2', 'fib3', 'fib4'],column_start='col1', column_finish='col3')
    print col_fam.get_count('row_key')
    print col_fam.get('row_key')
    print col_fam.get('author')
    print col_fam.get('row_key', columns=['col_name', 'col_name2'])
    print col_fam.get('row_key', column_reversed=True, column_count=3)
    print col_fam.multiget(['row1', 'row2'])
    for i in range(1, 10):
        col_fam.insert('row_key', {str(i): 'val'})
    print col_fam.get('row_key', column_start='5', column_finish='7')
    result = col_fam.get_range(start='row_key5', finish='row_key7') 
    for key, columns in result:
        print key, '=>', columns
    #Supper column
#    col_fam = pycassa.ColumnFamily(pool, 'Super1')
#    col_fam.insert('row_key', {'supercol_name': {'col_name': 'col_val'}})
    print col_fam.get('row_key')
#    col_fam = pycassa.ColumnFamily(pool, 'Letters')
#    col_fam.insert('row_key', {'super': {'a': '1', 'b': '2', 'c': '3'}})
#    print col_fam.get('row_key', super_column='super')
#    print col_fam.get('row_key', super_column='super', columns=['a', 'b'])
#    print col_fam.get('row_key', super_column='super', column_start='b')
#    print col_fam.get('row_key',super_column='super',column_finish='b',column_reversed=True) 
