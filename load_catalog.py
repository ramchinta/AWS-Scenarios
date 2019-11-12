import pymysql
import boto3
import json
from datetime import datetime

def ccpa():
    mysql_host = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"#"axlmysql1.c6qb7wtolxea.us-east-1.rds.amazonaws.com"
    mysql_username = "admin"#"lakshman"
    mysql_password = "Lakshman4"#"Axelaar123"
    mysql_database = "ccpa"
    column = set()
    alias = set()
    print(datetime.now())
    mysql_conn = pymysql.connect(host=mysql_host, port=3306, user=mysql_username, password=mysql_password,database=mysql_database)
    mysql_cur = mysql_conn.cursor()
    mysql_cur.execute("select (select max(ccpa_dataset) from ccpa_pi_catalog)")
    data = mysql_cur.fetchall()
    x=(data[0][0] )
    ccpa_dataset = (str(1) if x is None else str(x+1) )
    print(ccpa_dataset)
    mysql_cur.execute("select ccpa_column from (select ccpa_system,ccpa_schema,ccpa_table,ccpa_column from ccpa_schema_set union all select ccpa_system,ccpa_schema,ccpa_table,ccpa_column from ccpa_pi_catalog)tbl group by ccpa_system,ccpa_schema,ccpa_table,ccpa_column having count(*) =1")
    data = mysql_cur.fetchall()
    for row in data:
        for col in row:
            column.add(col)
    mysql_cur.execute("select ccpa_pi_alias from ccpa_pi_keyset")
    data = mysql_cur.fetchall()
    for row in data:
        for col in row:
            alias.add(col)
    fullmatch = [B for B in column if B.lower() in (x.lower() for x in alias)]
    fullmatch = set(fullmatch)
    print(len(fullmatch))
    for i in fullmatch:
        mysql_cur.execute("insert into ccpa_pi_catalog (ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_pi,ccpa_exempt_del,ccpa_pi_pct,ccpa_userid,ccpa_ins_date,ccpa_dataset)(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system,a.ccpa_schema,a.ccpa_table,a.ccpa_column,'Y' as ccpa_pi,'Y' as ccpa_exempt_del,(100+b.ccpa_pi_pct)/2,15 as ccpa_userid,current_date as ccpa_ins_date,"+ccpa_dataset+" as ccpa_dataset from ccpa_schema_set a inner join ccpa_pi_keyset b on a.ccpa_column = '"+i+"' and b.ccpa_pi_alias = '"+i+"')")

    column = set(column) - set(fullmatch)
    alias = set(alias) - set(fullmatch)
    for j in column:
        for i in alias:
            if j.lower() in i.lower():
                mysql_cur.execute("insert into ccpa_pi_catalog(ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_Pi,ccpa_exempt_del,ccpa_pi_pct,ccpa_userid,ccpa_ins_date,ccpa_dataset)(select b.ccpa_category,b.ccpa_pi_name,a.ccpa_system ,a.ccpa_schema,a.ccpa_table ,a.ccpa_column,'Y' as ccpa_pi,'Y' as ccpa_for_del,round((b.ccpa_pi_pct + 75)/2),1 as ccpa_userid,current_date() as ccpa_date," + ccpa_dataset + " as ccpa_dataset from ccpa_schema_set as a inner join ccpa_pi_keyset as b on a.ccpa_column = '" + j + "' and b.ccpa_pi_alias = '" + i + "')")
                break
            else:
                continue
    mysql_cur.execute("insert into ccpa_pi_catalog (ccpa_category,ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,ccpa_Pi,ccpa_exempt_del,ccpa_pi_pct,ccpa_userid,ccpa_ins_date,ccpa_dataset)(select ''as ccpa_category,''ccpa_pi_name,ccpa_system,ccpa_schema,ccpa_table,ccpa_column,'N' as ccpa_pi,'N' as ccpa_exempt_del,0 as ccpa_pi_pct,15 as ccpa_userid,current_date as ccpa_ins_date,"+ccpa_dataset+" as ccpa_dataset from ( select ccpa_system,ccpa_schema,ccpa_table,ccpa_column from ccpa_schema_set union all select ccpa_system,ccpa_schema,ccpa_table,ccpa_column from ccpa_pi_catalog)tbl group by ccpa_system,ccpa_schema,ccpa_table,ccpa_column having count(*) =1)")

    mysql_conn.commit()


ccpa()
