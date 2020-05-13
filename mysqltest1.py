import mysql.connector

db_host="35.232.6.247"
db_localhost="127.0.0.1"
db_user = "root"
db_pass = "password"
db_name = "mathgarage-prod"
cloud_sql_connection_name = "mathgarage:us-central1:mathgarage-prod"


mydb = mysql.connector.connect(
    host=db_host,
    db=db_name,
    user=db_user,
    passwd=db_pass
)

print(mydb)

