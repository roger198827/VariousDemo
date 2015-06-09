# - coding: utf-8 -
from cassandra.cluster import Cluster
import uuid
import string

from cassandra import ConsistencyLevel


cluster = Cluster(['10.107.4.187', ])

session = cluster.connect();
#session.execute("CREATE KEYSPACE Datastax_Test")

#session = cluster.connect('Datastax_Test')
#session = cluster.connect('ColumnFamily1')
#session.set_keyspace('Cassandra_Test')

#################################################################################################################################################
# Using below cqlsh to create table and can be insert and select using datastax, can be use cassa-cli also, 
# using "get tweet['928141f2-156c-41dd-856c-0f59cdbc48c3'];" can get result
# [default@mykeyspace] get tweet['928141f2-156c-41dd-856c-0f59cdbc48c3'];
# => (name=, value=, timestamp=1401905311626000)
# => (name=message, value=68656c6c6f206a6f686e, timestamp=1401905311626000)
# => (name=userid, value=39323831343166322d313536632d343164642d383536632d306635396364626334386333, timestamp=1401905311626000)
# Returned 3 results.
# Elapsed time: 44 msec(s).
# INSERT INTO tweet (id, userId, message)  VALUES (928141f2-156c-41dd-856c-0f59cdbc48c3, '928141f2-156c-41dd-856c-0f59cdbc48c3', 'hello john'); #
#  1.创建键空间：                                                                                                                               #
# CREATE KEYSPACE mykeyspace                                                                                                                    #
# WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };                                                                  #
# 进入键空间：                                                                                                                                  #
# USE mykeyspace;                                                                                                                               #
# 2.创建表(列族)并插入数据：                                                                                                                    #
# CREATE TABLE tweet (                                                                                                                          #
#   id uuid PRIMARY KEY,                                                                                                                        #
#   userId text,                                                                                                                                #
#   message text,                                                                                                                               #
#   creationTime timestamp                                                                                                                      #
# );                                                                                                                                            #
# INSERT INTO user (id, userId, message)                                                                                                        #
#   VALUES (1743, '928141f2-156c-41dd-856c-0f59cdbc48c3', 'hello john');                                                                        #
# INSERT INTO user (id, userId, message, name)                                                                                                  #
#   VALUES (1744, '928141f2-156c-41dd-856c-0f59cdbc48c3', 'hello peter');                                                                       #
# INSERT INTO user (id, userId, message,  name)                                                                                                 #
#   VALUES (1744, '928141f2-156c-41dd-856c-0f59cdbc48c3', 'hello smith');                                                                       #
#################################################################################################################################################

session.set_keyspace('mykeyspace')   #success insert                                                                                          #
session.execute("INSERT INTO tweet (id, message, userid ) VALUES (%s, %s, %s)", [uuid.uuid1(), "42", "123456"]) #success insert               #

#or you can do this instead
#session.execute('USE Users_sp')
#session.set_keyspace('mykeyspace')
#session.execute('create table User')

rows = session.execute('SELECT * FROM tweet')
for row in rows:
    print row
count = session.execute('select count(*) from tweet')
print 'count : %r ' % count[0]
raw_input('debug')

#using %d is wrong
#session.execute( """ INSERT INTO users (name, credits, user_id) VALUES (%s, %d, %s) """ ("John O'Reilly", 42, uuid.uuid1()))
#cqlstat = """INSERT INTO users (name, credits, user_id) VALUES (%s, %d, %s)""" % ("\'John O''Reilly\'", 42, "2644bada-852c-11e3-89fb-e0b9a54a6d93")
#cqlstat = """ INSERT INTO users (name, credits, user_id) VALUES (%s, %s, %s) """ ("John O'Reilly", 42, uuid.uuid1())

#cqlstat = """ INSERT INTO users (name, credit) VALUES (%s, %s) """ ("John O'Reilly", 42)  #TypeError: 'str' object is not callable

#cqlstat = 'INSERT INTO users (name, credit) VALUES (%s, %s) ' % ("John O'Reilly", 42) #cassandra.protocol.SyntaxException: <ErrorMessage code=2000 [Syntax error in CQL query] message="line 1:60 mismatched character '<EOF>' expecting '''">

#print cqlstat
#session.execute(cqlstat )
#session.execute("INSERT INTO tbl_users (name, credits, user_id) VALUES (%s, %s, %s)", ["blah", "42", "123456"])   #cassandra.InvalidRequest: code=2200 [Invalid query] message="Missing mandatory PRIMARY KEY part key"

print 'insert into users (name, credits, user_id) values ("a", "b", "56")'
#session.execute('insert into users (name, credits, user_id) values ("a", "b", "56")')
#session.execute("INSERT INTO USERS (name, age) VALUES (%s, %d)", ("bob", 42))  # wrong

create_user_statement = session.prepare(
    "INSERT INTO users (username, email) VALUES (?, ?) IF NOT EXISTS")
create_user_statement.serial_consistency_level = ConsistencyLevel.SERIAL

new_username = 'testuser'
new_email = 'testemal.emal.com'

session.execute(create_user_statement, [new_username, new_email])

session.execute(                               
    """                                        
    INSERT INTO users (name, credits, user_id) 
    VALUES (%s, %s, %s)                        
    """                                        
    ("John O'Reilly", 42, uuid.uuid1())       
)                                              

#########################################################################
# session.execute(                                                      #
#     """                                                               #
#     INSERT INTO users (name, credits, user_id, username)              #
#     VALUES (%(name)s, %(credits)s, %(user_id)s, %(name)s)             #
#     """                                                               #
#     {'name': "John O'Reilly", 'credits': 42, 'user_id': uuid.uuid1()} #
# )                                                                     #
#########################################################################
#session.execute(string.escapeSingleQuotes(cqlstat) )

# there is two spaces, why can't be select, only can be select the new created one with command "create column family users" with cassandra-cli
rows = session.execute('SELECT * FROM Users')
for user_row in rows:
    print user_row
