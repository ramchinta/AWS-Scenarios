import pyodbc

server = 'database-1.cszampg2p55a.us-east-1.rds.amazonaws.com'
database = 'database-1'
username = 'admin'
password = 'Lakshman4'

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()

cursor.execute('''insert into lakshman.users values(5,'Naga','naga@gmail.com',95070);''')

cnxn.commit()

cursor.execute("SELECT * FROM lakshman.users;")

row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()