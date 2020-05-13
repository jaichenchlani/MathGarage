import mysql.connector

mydb = mysql.connector.connect(
    host="35.232.6.247",
    user="root",
    passwd="password"
)

print(mydb)