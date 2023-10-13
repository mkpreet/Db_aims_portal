import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  
  autocommit=True
)

cursor_my = mydb.cursor()


# cursor_my = mydb.cursor()
cursor_my.execute("USE aims")
#print(mydb)

cursor_my.execute("CREATE TABLE Students(stu_id varchar(20) ,stu_name varchar(30),stu_email varchar(30),stu_dob varchar(15),stu_cgpa varchar(10),sem varchar(10),admission_year varchar(10), PRIMARY KEY(stu_id));")
cursor_my.execute("desc Students")
for a in cursor_my:
  print(a)


# #Name	Acad_id	Acad_Email

cursor_my.execute("CREATE TABLE Academics(acad_id varchar(20),acad_name varchar(30),acad_email varchar(30),acad_dob varchar(20),PRIMARY KEY(acad_id));")
cursor_my.execute("desc Academics")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Course_catalog(course_id varchar(12),course_title varchar(100),l varchar(2),t varchar(2),p varchar(2),s varchar(2),c varchar(2),PRIMARY KEY(course_id));")
cursor_my.execute("desc Course_catalog")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Faculty(fac_id varchar(20),fac_name varchar(30),fac_email varchar(30),fac_dob varchar(20),PRIMARY KEY(fac_id));")
cursor_my.execute("desc Faculty")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE CGPA_constraint(fac_id varchar(20),course_id varchar(30),CGPA varchar(5),PRIMARY KEY(course_id),FOREIGN KEY (fac_id) REFERENCES Faculty(fac_id));")
cursor_my.execute("desc CGPA_constraint")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Login(id varchar(20),password varchar(500),user_type varchar(5),DOB varchar(12),PRIMARY KEY(id));")
cursor_my.execute("desc Login")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Course_pre_req(course_id varchar(12),course_pre_req varchar(20),FOREIGN KEY (course_id) REFERENCES Course_catalog(course_id));")
cursor_my.execute("desc Course_pre_req")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Session(id varchar(20),time varchar(30),user_type varchar(5),PRIMARY KEY(id));")
cursor_my.execute("desc Session")
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Faculty_offering(course_id varchar(12),fac_id varchar(20),CGPA varchar(12),FOREIGN KEY (course_id) REFERENCES Course_catalog(course_id),FOREIGN KEY (fac_id) REFERENCES Faculty(fac_id));")
cursor_my.execute("desc Faculty_offering")                                          #
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Graded_courses(course_id varchar(10),stu_id varchar(20),points varchar(5),sem varchar(5),FOREIGN KEY (course_id) REFERENCES Course_catalog(course_id),FOREIGN KEY (stu_id) REFERENCES Students(stu_id));")
cursor_my.execute("desc Graded_courses")                                      #,credits_earned varchar(5)
for a in cursor_my:
  print(a)

cursor_my.execute("CREATE TABLE Enrolled_students(course_id varchar(10),stu_id varchar(20),sem varchar(5),FOREIGN KEY (course_id) REFERENCES Course_catalog(course_id),FOREIGN KEY (stu_id) REFERENCES Students(stu_id));")
cursor_my.execute("desc Enrolled_students")
for a in cursor_my:
  print(a)





