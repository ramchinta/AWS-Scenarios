import pymysql
import boto3
import json
from datetime import datetime

def ccpa():
    mysql_host = "axlmysql1.c6qb7wtolxea.us-east-1.rds.amazonaws.com"
    mysql_username = "lakshman"
    mysql_password = "Axelaar123"
    mysql_database = "ccpa"
    column = []
    likecolumn =[]
    alias = []
    print(datetime.now())


    try:
        '''Connect to the mysql rds database'''
        mysql_conn = pymysql.connect(host=mysql_host, port=3306, user=mysql_username, password=mysql_password,database=mysql_database)
        mysql_cur = mysql_conn.cursor()
        '''Build dataset number'''
        mysql_cur.execute("select (select max(ccpa_dataset) from ccpa_pi_catalog)")
        data = mysql_cur.fetchall()
        ccpa_dataset = str(1)#str((data[0][0] + 1))
        print(data)
        print(datetime.now())
        '''Build list of column names'''
        mysql_cur.execute("select ccpa_column from ccpa.ccpa_schema_set")
        data = mysql_cur.fetchall()
        print(data)
        print(datetime.now())
        for row in data:
            for col in row:
                column.append(col)
        print('data')
        print(datetime.now())
        '''Build list of alias names'''
        mysql_cur.execute("select ccpa_pi_alias from ccpa.ccpa_pi_keyset")
        data = mysql_cur.fetchall()
        for row in data:
            for col in row:
                alias.append(col)
        print('data22')
        print(datetime.now())
        '''100% match columns'''
        #fullmatch = [B for B in column if B.lower() == (x.lower() for x in alias)]
        fullmatch = [B for B in column if B.lower() in (x.lower() for x in alias)]
        fullmatch = set(fullmatch)
        print(datetime.now())
        '''Insert 100% match columns'''
        for i in fullmatch:
            mysql_cur.execute("insert into ccpa_pi_catalog(ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_Pi,ccpa_exempt_del,ccpa_pi_pct,ccpa_userid,ccpa_ins_date,ccpa_dataset)(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'N' as ccpa_for_del,(b.ccpa_pi_pct + 100)/2,1 as ccpa_userid,current_date() as ccpa_date,"+ ccpa_dataset+" as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on a.ccpa_column = '"+i+"' and b.ccpa_pi_alias = '"+i+"')")
            print("Yes")
        mysql_conn.commit()
        print(datetime.now())
        column = set(column) - set(alias)
        print(datetime.now())
        '''Generate Like columns'''
        for i in column:
            for j in alias:
                if j.lower() in i.lower():
                    likecolumn.append(i)
        likecolumn = set(likecolumn)
        print(datetime.now())
        print(likecolumn)
        '''Insert like columns'''
        for j in likecolumn:
            mysql_cur.execute("insert into ccpa_pi_catalog(ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_Pi,ccpa_exempt_del,ccpa_pi_pct,ccpa_userid,ccpa_ins_date,ccpa_dataset)(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'N' as ccpa_for_del,(b.ccpa_pi_pct + 75)/2,1 as ccpa_userid,current_date() as ccpa_date,"+ ccpa_dataset+" as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on a.ccpa_column = '"+j+"' and b.ccpa_pi_alias = '"+j+"')")
            print('Yes2')
        print(datetime.now())
        mysql_conn.commit()
        mysql_cur.execute("insert into ccpa_pi_catalog (ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_Pi,ccpa_exempt_del,ccpa_pi_pct,ccpa_userid,ccpa_ins_date,ccpa_dataset)(select ''as ccpa_category,'' as ccpa_pi_name ,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'N' as ccpa_pi,'N' as ccpa_for_del,0 as ccpa_pi_pct,1 as ccpa_userid,current_date() as ccpa_ins_date,"+ccpa_dataset+ " as ccpa_dataset from ccpa.ccpa_schema_set as a left join ccpa.ccpa_pi_catalog as b on a.ccpa_system = b.ccpa_system and a.ccpa_schema = b.ccpa_schema and a.ccpa_table = b.ccpa_table and a.ccpa_column = b.ccpa_column WHERE b.ccpa_system is null and b.ccpa_schema is null and b.ccpa_table is null and b.ccpa_column is null)")
        mysql_conn.commit()
        print(datetime.now())
        print("Yes3")
        '''Write the log file to s3 : Successful'''
        s3 = boto3.resource('s3')
        obj = s3.Object('axelaardev.com', 'logs/ccpa_pi_catalog/'+str(datetime.now()))
        data= str(datetime.now())+',Backend,Successful'
        obj.put(Body=json.dumps(data))


    except:
        mysql_cur.execute("insert into ccpa_pi_catalog(ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_Pi,ccpa_for_del,ccpa_pi_pct,ccpa_user,ccpa_date,ccpa_dataset)(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'N' as ccpa_for_del,avg(b.ccpa_pi_pct + 100),'Backend' as ccpa_user,current_date() as ccpa_date," + ccpa_dataset + " as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on a.ccpa_column = '" + i + "' and b.ccpa_pi_alias = '" + i + "'))")
        '''Write the log file to s3: Failed'''
        s3 = boto3.resource('s3')
        obj = s3.Object('axelaardev.com', 'logs/ccpa_pi_catalog/'+str(datetime.now()))
        data= str(datetime.now())+',Backend,Failed'
        obj.put(Body=json.dumps(data))

ccpa()