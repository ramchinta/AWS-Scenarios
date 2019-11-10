import os
import pymysql
def createfile():
    MYSQL_HOST = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    MYSQL_USERNAME = "admin"
    MYSQL_PASSWORD = "Lakshman4"
    MYSQL_DATABASE = "lakshman"

    # Get data from Mysql
    mysql_table_name = 'adventureworks.salesorderdetail'
    mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,database=MYSQL_DATABASE)
    mysql_cur = mysql_conn.cursor()
    mysql_cur.execute('select * from %s ;' % mysql_table_name)
    #description = mysql_cur.description
    rows = mysql_cur.fetchall()
    #print("lakshman")
   # print(rows)
    #print(type(rows))
    f = open("C:\\Users\\Lakshman\\Documents\\testing.tsv", "w")
    f.truncate(0)
    for i in rows:
        for j in i:
            f.write(str(j) + '\t')
            #print(type(j))
        f.write('\n')
    f.close()

createfile()