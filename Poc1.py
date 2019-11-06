import pymysql
import csv

def createfile():
    MYSQL_HOST = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    MYSQL_USERNAME = "admin"
    MYSQL_PASSWORD = "Lakshman4"
    MYSQL_DATABASE = "lakshman"
    lt=[]

    with open('C:\\Users\\Lakshman\\Downloads\\Products_2016-full.csv', 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        fulllist = list(readCSV)
        for row in range(1,len(fulllist)):
            lt.append(fulllist[row])

    mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,database=MYSQL_DATABASE)
    mysql_cur = mysql_conn.cursor()

    for i in lt:
        TF =next((True for j in i if "'" in j),False)
        if (TF == True):
        #if "'" in i:
            values = '"'+'","'.join(i)+'"'
            print(values)
            mysql_cur.execute('insert into lakshman.poc1 values('+values+')')
        else:
            values = "'" + "','".join(i) + "'"
            print(values)
            mysql_cur.execute('insert into lakshman.poc1 values(' + values + ')')
        mysql_conn.commit()

createfile()
