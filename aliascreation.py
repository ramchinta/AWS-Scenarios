import csv
import pymysql

def createfile():
    MYSQL_HOST = "axlmysql1.c6qb7wtolxea.us-east-1.rds.amazonaws.com"
    MYSQL_USERNAME = "lakshman"
    MYSQL_PASSWORD = "Axelaar123"
    MYSQL_DATABASE = "ccpa"
    input = []
    output = []
    o_pct = [100, 80, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25]
    existing =[]

    mysql_conn = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USERNAME, password=MYSQL_PASSWORD,
                                 database=MYSQL_DATABASE)
    mysql_cur = mysql_conn.cursor()

    mysql_cur.execute("select ccpa_pi_alias from ccpa.ccpa_pi_keyset")

    data = mysql_cur.fetchall()
    for row in data:
        for col in row:
            existing.append(col)


    with open('C:\\Users\\sanat\\OneDrive\\Desktop\\CCPA_Alias\\sheet1.csv', 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        fulllist = list(readCSV)
        for row in range(1, len(fulllist)):
            input.append(fulllist[row])
            a = fulllist[row][0]
            b = fulllist[row][1]
            category = fulllist[row][2]
            i = a+b
            if b == "":
                output.append(a)
                output.append(a[0:3]+a[-1])
                output.append(a[0:3])
                #f = open("C:\\Users\\sanat\\OneDrive\\Desktop\\CCPA_Alias\\ testing.csv", "a")
                print(output)
                dup = []
                for i in output:
                    for j in existing:
                        if i.lower() == j.lower():
                            dup.append(i)
                output = list(set(output) - set(output1))

                for j in range(len(output)):
                    z = (category + ',' + i + ',' + output[j] + ',' + str(o_pct[j]))
                    print(z)
                    value = z.split(',')
                    val = '"' + '","'.join(value) + '"'
                    print(val)
                    mysql_cur.execute('insert into ccpa_pi_keyset (ccpa_category,ccpa_pi_name,ccpa_pi_alias,ccpa_pi_pct) values ('+val+')')
                mysql_conn.commit()
                output.clear()
            else:
                output.append(a + b)
                output.append(a +'_'+ b)
                output.append(a +'-'+ b)
                output.append(a+b[0:3])
                output.append(a + "_" +b[0:3])
                output.append(a + "-" + b[0:3])
                output.append(a[0:3]+ b)
                output.append(a[0:3] +"_"+ b)
                output.append(a[0:3] +"-"+ b)
                output.append(a[0:3]+b[0:3])
                output.append(a[0:3]+"_"+b[0:3])
                output.append(a[0:3]+"-"+b[0:3])
                #f = open("C:\\Users\\sanat\\OneDrive\\Desktop\\CCPA_Alias\\ testing.csv", "a")
                dup = []
                for i in output:
                    for j in existing:
                        if i.lower() == j.lower():
                            dup.append(i)
                output = list(set(output) - set(output1))
                for j in range(len(output)):
                    #z = (i+','+output[j]+','+category+','+str(o_pct[j]))
                    print (category)
                    print(i)
                    print(output[j])
                    print(o_pct[j])
                    z=(category+','+i+','+output[j]+','+str(o_pct[j]))
                    value=z.split(',')
                    val = '"' + '","'.join(value) + '"'
                    print(val)
                    mysql_cur.execute('insert into ccpa_pi_keyset (ccpa_category,ccpa_pi_name,ccpa_pi_alias,ccpa_pi_pct) values(' +val+ ')')
                mysql_conn.commit()
                output.clear()
createfile()