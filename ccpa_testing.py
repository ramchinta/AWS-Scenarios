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
        mysql_cur.execute("select ccpa_column from ccpa.ccpa_schema_set")
        data = mysql_cur.fetchall()
        print(data)
        print(datetime.now())
        for row in data:
            for col in row:
                column.append(col)
        print(len(column))
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
        fullmatch = [B for B in column if B.lower() == (x.lower() for x in alias)]
        print(len(fullmatch))
        fullmatch = set(fullmatch)
        print(len(fullmatch))
        column = set(column) - set(fullmatch)
        print(datetime.now())
        '''Generate Like columns'''
        for i in column:
            for j in alias:
                if j.lower() in i.lower():
                    likecolumn.append(i)
        print(len(likecolumn))
        likecolumn = set(likecolumn)
        print(len(alias))
        print(len(likecolumn))
    except:
        print("something wrong")
ccpa()