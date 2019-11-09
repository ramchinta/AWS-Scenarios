import pymysql
from datetime import datetime

def ccpa():
    MYSQL_HOST = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    MYSQL_USERNAME = "admin"
    MYSQL_PASSWORD = "Lakshman4"
    MYSQL_DATABASE = "ccpa"

    try:
        '''Connect to the mysql rds database'''
        mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,database=MYSQL_DATABASE)
        mysql_cur = mysql_conn.cursor()
        '''Query to get the column data from CCPA_SCHEMA_SET'''
        mysql_cur.execute("insert into ccpa_pi_catalog (select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'N' as ccpa_for_del,b.ccpa_pi_pct,'Backend' as ccpa_user,current_date() as ccpa_date,1 as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on upper(a.ccpa_column) = upper('%'+b.ccpa_pi_alias+'%'))")
        mysql_cur.execute("insert into ccpa_pi_catalog(select '','',a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'N' as ccpa_pi,'N' as ccpa_for_del,0 as ccpa_pi_pct,'Backend' as ccpa_user,current_date() as ccpa_date,1 as ccpa_dataset from ccpa_schema_set as a left join ccpa_pi_catalog as b on b.ccpa_column is null and b.ccap_table)")
        f = open("C:\\Users\\Lakshman\\Documents\\ccpa_logs.txt", "a")
        f.write(str(datetime.now())+',Backend,Successful'+ '\n')
        f.close()

    except:
        f = open("C:\\Users\\Lakshman\\Documents\\ccpa_logs.txt", "a")
        f.write(str(datetime.now())+',Backend,Failed'+ '\n')
        f.close()

ccpa()