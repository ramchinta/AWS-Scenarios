import pymysql

def ccpa():
    MYSQL_HOST = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    MYSQL_USERNAME = "admin"
    MYSQL_PASSWORD = "Lakshman4"
    MYSQL_DATABASE = "ccpa"

    '''Connect to the mysql rds database'''
    mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,database=MYSQL_DATABASE)
    mysql_cur = mysql_conn.cursor()
    '''Query to get the column data from CCPA_SCHEMA_SET'''
    mysql_cur.execute("select ccpa_column from ccpa.ccpa_schema_set")
    rows = mysql_cur.fetchall()
    for i in rows:
        for j in i:
            print(j)
ccpa()