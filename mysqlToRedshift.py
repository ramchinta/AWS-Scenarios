#userName = admin
#Pwd = Lakshman4

import psycopg2
import pymysql
def readmysql():
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
    print(type(rows))
    '''print(description)
    for x in description:
        print(x[0])
        
    # Insert data into Redshift
    redshift_table_name = 'lakshman.users'
    REDSHIFT_HOST = 'redshift-cluster-1.cfnzlezppkcj.us-east-1.redshift.amazonaws.com'
    REDSHIFT_USERNAME = 'awsuser'
    REDSHIFT_PASSWORD = 'Lakshman4'
    REDSHIFT_DATABASE = 'lakshman'
    #conn_string = "dbname='userbhv' port='5439' user='lakshman' password='AxlCs*123*' host='axlpoc2rs.cphm5aouzbjy.us-east-1.redshift.amazonaws.com'"
    redshift_conn = psycopg2.connect(host=REDSHIFT_HOST, port=5439, user=REDSHIFT_USERNAME, password=REDSHIFT_PASSWORD,database=REDSHIFT_DATABASE)
    redshift_cur = redshift_conn.cursor()
    column_names = ', '.join([x[0] for x in description])
    values = ', '.join(['(' + ','.join(map(str, x)) + ')' for x[0] in rows])
    print(values)
    insert_template = 'insert into ' + redshift_table_name +'  values ' + values + ';'

    redshift_cur.execute(insert_template)

readmysql()