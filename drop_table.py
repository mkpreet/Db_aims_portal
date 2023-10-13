import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  database="aims",
  autocommit=True
)
cursor_my = mydb.cursor()

cursor_my.execute("DROP TABLE Graded_courses")
cursor_my.execute("DROP TABLE Enrolled_students")
cursor_my.execute("DROP TABLE Faculty_offering")
cursor_my.execute("DROP TABLE Students")
cursor_my.execute("DROP TABLE Academics")
cursor_my.execute("DROP TABLE CGPA_constraint")
cursor_my.execute("DROP TABLE Session")
cursor_my.execute("DROP TABLE Login")
cursor_my.execute("DROP TABLE Course_pre_req")
cursor_my.execute("DROP TABLE Course_catalog")
cursor_my.execute("DROP TABLE Faculty")

