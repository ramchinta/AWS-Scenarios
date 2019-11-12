import boto3
import pandas as pd
import pymysql
import numpy as np
import io

def import_schema():
    bucket = "axlpoc2"
    file_name = "CS_2018-01-18/Vertica-HIVE-USAS.csv"
    input = []
    mysql_host = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    mysql_username = "admin"
    mysql_password = "Lakshman4"
    mysql_database = "ccpa"
    s3 = boto3.client('s3')

    mysql_conn = pymysql.connect(host=mysql_host, port=3306, user=mysql_username, password=mysql_password,database=mysql_database)
    mysql_cur = mysql_conn.cursor()
    mysql_cur.execute('drop table if exists ccpa_schema_set_tmp;')
    mysql_cur.execute('create table ccpa_schema_set_tmp (ccpa_system char(50),ccpa_schema char(50),ccpa_table char(50),ccpa_column char(50))')


    obj = s3.get_object(Bucket= bucket, Key= file_name)

    initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word
    #initial_df = pd.read_excel(obj['Body'])  # 'Body' is a key word
    print('ok')

    for col in initial_df.values:
        input.append(col)
    print(input)
    for i in input:
        value = '"' + '","'.join(i) + '"'
        print(value)
        mysql_cur.execute("insert into ccpa_schema_set_tmp (ccpa_system,ccpa_schema,ccpa_table,ccpa_column)values("+value+")")
    print('Done inserting to temp')
    mysql_cur.execute("insert into ccpa_schema_set(ccpa_system,ccpa_schema,ccpa_table,ccpa_column)(select a.ccpa_system,a.ccpa_schema,a.ccpa_table,a.ccpa_column from ccpa_schema_set_tmp a left join ccpa_schema_set b on a.ccpa_system = b.ccpa_system and a.ccpa_schema = b.ccpa_schema and a.ccpa_table = b.ccpa_table and a.ccpa_column = b.ccpa_column where b.ccpa_system is null and b.ccpa_schema is null and b.ccpa_table is null and b.ccpa_column is null )")
    mysql_cur.execute("drop table ccpa_schema_set_tmp")
    mysql_conn.commit()
import_schema()

