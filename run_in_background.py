#!/user/bin/env python3



import mysql.connector
import time


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  database="aims",
  autocommit=True
)

cursor_my = mydb.cursor()
iterator=1

while iterator:
    time.sleep(180)                           #for evaluation taking 3 mins as auto logout time
    cursor_my.execute("DELETE FROM Session")

    print("All Session entry deleted")
    iterator=iterator+1