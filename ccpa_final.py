import pymysql
import boto3
import json
from datetime import datetime

def ccpa():
    mysql_host = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    mysql_username = "admin"
    mysql_password = "Lakshman4"
    mysql_database = "ccpa"
    column = []
    likecolumn =[]
    alias = []


    try:
        '''Connect to the mysql rds database'''
        mysql_conn = pymysql.connect(host=mysql_host, port=3306, user=mysql_username, password=mysql_password,database=mysql_database)
        mysql_cur = mysql_conn.cursor()
        mysql_cur.execute("select ccpa_column from ccpa.ccpa_schema_set")
        data = mysql_cur.fetchall()
        for row in data:
            for col in row:
                column.append(col)

        mysql_cur.execute("select ccpa_pi_alias from ccpa.ccpa_pi_keyset")
        data = mysql_cur.fetchall()
        for row in data:
            for col in row:
                alias.append(col)
        '''100% match columns'''
        fullmatch = [B for B in column if B.lower() in (x.lower() for x in alias)]
        '''Insert 100% match columns'''
        for i in fullmatch:
            mysql_cur.execute("insert into ccpa_pi_catalog(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'N' as ccpa_for_del,avg(b.ccpa_pi_pct + 100),'Backend' as ccpa_user,current_date() as ccpa_date,(select max(ccpa_dataset) from ccpa_pi_catalog)+1 as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on a.ccpa_column = '"+i+"' and b.ccpa_pi_alias = '"+i+"'))")
        column = set(column) - set(alias)
        '''Generate Like columns'''
        for i in column:
            for j in alias:
                if j.lower() in i.lower():
                    likecolumn.append(i)
        '''Insert like columns'''
        for j in likecolumn:
            mysql_cur.execute("insert into ccpa_pi_catalog(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'N' as ccpa_for_del,avg(b.ccpa_pi_pct + 75),'Backend' as ccpa_user,current_date() as ccpa_date,(select max(ccpa_dataset) from ccpa_pi_catalog)+1 as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on a.ccpa_column = '"+j+"' and b.ccpa_pi_alias = '"+j+"'))")
        mysql_cur.execute("insert into ccpa_pi_catalog(ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccap_table,ccpa_column,ccpa_Pi,ccpa_for_del,ccpa_pi_pct,ccpa_user,ccpa_date,ccpa_dataset)(select ''as ccpa_category,'' as ccpa_pi_name ,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'N' as ccpa_pi,'N' as ccpa_for_del,0 as ccpa_pi_pct,'Backend' as ccpa_user,current_date() as ccpa_date,1 as ccpa_dataset from ccpa_schema_set as a left join ccpa_pi_catalog as b on b.ccpa_column is null and b.ccap_table is null)")
        '''Write the log file to s3 : Successful'''
        s3 = boto3.resource('s3')
        obj = s3.Object('axelaardev.com', 'logs/ccpa_pi_catalog/'+str(datetime.now()))
        data= str(datetime.now())+',Backend,Successful'+ '\n'
        obj.put(Body=json.dumps(data))
        print("Y")


    except:
        '''Write the log file to s3: Failed'''
        s3 = boto3.resource('s3')
        obj = s3.Object('axelaardev.com', 'logs/ccpa_pi_catalog/'+str(datetime.now()))
        data= str(datetime.now())+',Backend,Failed'+ '\n'
        obj.put(Body=json.dumps(data))

ccpa()