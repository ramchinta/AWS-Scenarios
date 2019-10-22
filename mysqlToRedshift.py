#userName = admin
#Pwd = Lakshman4

import psycopg2
import pymysql

MYSQL_HOST = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
MYSQL_USERNAME = "admin"
MYSQL_PASSWORD = "Lakshman4"
MYSQL_DATABASE = "lakshman"

# Get data from Mysql
mysql_table_name = 'lakshman.users'
mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,database=MYSQL_DATABASE)
mysql_cur = mysql_conn.cursor()
mysql_cur.execute('select * from %s;' % mysql_table_name)
description = mysql_cur.description
rows = mysql_cur.fetchall()
print(rows)
'''
# Insert data into Redshift
redshift_table_name = 'some_table_2'
redshift_conn = psycopg2.connect(host=REDSHIFT_HOST, port=3306, user=REDSHIFT_USERNAME, password=REDSHIFT_PASSWORD,database=REDSHIFT_DATABASE)
redshift_cur = redshift_conn.cursor()
insert_template = 'insert into %s (%s) values %s;'
column_names = ', '.join([x[0] for x in description])
values = ', '.join(['(' + ','.join(map(str, x)) + ')' for x in rows])

redshift_cur.execute(insert_template % (redshift_table_name, column_names, values))
'''