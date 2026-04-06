import mysql.connector as mysql

connection = mysql.connect(host="localhost", user="root", password="system")
cursor = connection.cursor()
cursor.execute("use dramas;")
while True:
    drama_name = input("enter drama_name to enter : ")
    date=2
    if drama_name  == 'fuck off':break
    else: 
        cursor.execute('UPDATE user_table SET `timestamp` = %s where drama_name=%s;',("2025-09-"+str(date),drama_name))
        date+=1
connection.commit()
cursor.close()
connection.close()