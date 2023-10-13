import mysql.connector
import hashlib
import pandas as pd

salt = b'32'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  database="aims",
  autocommit=True
)
cursor_my = mydb.cursor()

# Acad_Name	Acad_ID	Acad_EmailID
# Fac_ID	Fac_Name	Fac_Email




data_stu = pd.read_csv("student_records.csv")

df_stu=pd.DataFrame(data_stu)

for row in df_stu.itertuples():
  query="INSERT INTO Students VALUES('"+str(row.Roll_No)+"','"+str(row.Stu_Name)+"','"+str(row.Stu_Email)+"','"+str(row.DOB)+"','"+str(row.CGPA)+"','"+str(row.Sem)+"','"+str(row.Year)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Students")
for a in cursor_my:
  print(a)

data_acad = pd.read_csv("acad_records.csv")

df_acad=pd.DataFrame(data_acad)
#print(mydb)

for row in df_acad.itertuples():
  query="INSERT INTO Academics VALUES('"+str(row.Acad_ID)+"','"+str(row.Acad_Name)+"','"+str(row.Acad_EmailID)+"','"+str(row.Acad_DOB)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Academics")
for a in cursor_my:
  print(a)

data_fac = pd.read_csv("faculty_records.csv")

df_fac=pd.DataFrame(data_fac)
#print(mydb)

for row in df_fac.itertuples():
  query="INSERT INTO Faculty VALUES('"+str(row.Fac_ID)+"','"+str(row.Fac_Name)+"','"+str(row.Fac_Email)+"','"+str(row.Fac_Dob)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Faculty")
for a in cursor_my:
  print(a)

data_login = pd.read_csv("login_info.csv")

df_login=pd.DataFrame(data_login)
#print(mydb)

for row in df_login.itertuples():
  query="INSERT INTO Login VALUES('"+str(row.User_ID)+"','"+str(row.Password)+"','"+str(row.User_Type)+"','"+str(row.DOB)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Login")
for a in cursor_my:
  print(a)

data_course = pd.read_csv("course_catalog.csv")

df_course=pd.DataFrame(data_course)
#print(mydb)

for row in df_course.itertuples():
  query="INSERT INTO Course_catalog VALUES('"+str(row.Course_ID)+"','"+str(row.Course_Title)+"','"+str(row.L)+"','"+str(row.T)+"','"+str(row.P)+"','"+str(row.S)+"','"+str(row.C)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Course_catalog")
for a in cursor_my:
  print(a)

data_pre_req = pd.read_csv("course_pre_req.csv")

df_pre_req=pd.DataFrame(data_pre_req)
#print(mydb)

for row in df_pre_req.itertuples():
  query="INSERT INTO Course_pre_req VALUES('"+str(row.Course_ID)+"','"+str(row.Course_Pre_Req)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Course_pre_req")
for a in cursor_my:
  print(a)

data_graded_courses = pd.read_csv("graded_courses.csv")

df_gc=pd.DataFrame(data_graded_courses)
#print(mydb)

for row in df_gc.itertuples():
  query="INSERT INTO Graded_courses VALUES('"+str(row.Course_ID)+"','"+str(row.Student_ID)+"','"+str(row.Points)+"','"+str(row.Sem)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Graded_courses")
for a in cursor_my:
  print(a)

data_es = pd.read_csv("enrolled_students.csv")

df_es=pd.DataFrame(data_es)
#print(mydb)

for row in df_es.itertuples():
  query="INSERT INTO Enrolled_students VALUES('"+str(row.Course_ID)+"','"+str(row.Student_ID)+"','"+str(row.Sem)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Enrolled_students")
for a in cursor_my:
  print(a)

data_of = pd.read_csv("faculty_offering.csv")

df_of=pd.DataFrame(data_of)
#print(mydb)

for row in df_of.itertuples():
  query="INSERT INTO Faculty_offering VALUES('"+str(row.Course_ID)+"','"+str(row.Fac_ID)+"','"+str(row.CGPA_eligibility)+"')"
  print(query)
  cursor_my.execute(query)

cursor_my.execute("select * from Faculty_offering")
for a in cursor_my:
  print(a)






cursor_my.execute("show tables")
for a in cursor_my:
  print(a)


cursor_my.execute("SELECT id, DOB FROM Login")
result=cursor_my.fetchall()
for val in result:
  id_ = val[0]
  pass_word = val[1]
  pass_word = pass_word.encode()
  hashed_pass = hashlib.sha256(pass_word).hexdigest()
 
  
  sql = "UPDATE Login SET password = %s WHERE id = %s"
  cursor_my.execute(sql,(hashed_pass, id_,))


cursor_my.execute("select * from Login")
for a in cursor_my:
  print(a)




