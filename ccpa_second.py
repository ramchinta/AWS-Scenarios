import pymysql

def ccpa():
    MYSQL_HOST = "database-1.cszampg2p55a.us-east-1.rds.amazonaws.com"
    MYSQL_USERNAME = "admin"
    MYSQL_PASSWORD = "Lakshman4"
    MYSQL_DATABASE = "lakshman"
    column = []
    column2 = ['FUR-BO-3174', 'FUR-BO-3175', 'FUR-BO-3176', 'FUR-BO-3177', 'Office Supplies','FUR-BO-3409', 'FUR-BO-3615', 'Furniture','FUR-BO-3616', 'FUR-BO-3617', 'FUR-BO-3618']
    like = []


    mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,database=MYSQL_DATABASE)
    mysql_cur = mysql_conn.cursor()
    mysql_cur.execute("select max(userid) from lakshman.users")
    rows = mysql_cur.fetchall()
    print(rows)
    print(rows[0][0] + 1)

    for i in rows:
        print(rows[i][0]+1)
        for j in i:
            print('K')
            z= (j+1)
            print(z)
            #column.append(j)
    fullmatch = [B for B in column if B.lower() in (x.lower() for x in column2)]
    print(fullmatch)
    for i in fullmatch:
        print(i)
    column = set(column) - set(column2)
    print(list(column))
    for i in column:
        for j in column2:
            if j in i:
                like.append(i)

    print(like)



ccpa()