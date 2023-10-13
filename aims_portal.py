import mysql.connector
from getpass import getpass
import hashlib
import os
import time
import datetime
import academic
import faculty_functions
import student_functions
import global_var
salt = b'32'


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  database="aims",
  autocommit=True
)

cursor_my = mydb.cursor()




def welcome_screen():
    """
    Function to display the login screen
    """
    os.system("clear")
    print("""Welcome to AIMS portal 

Please login to continue

1: Student 
2: Faculty 
3: Academics
4: Exit
""")
    print("current sem:",global_var. ongoing_sem,"   YEAR: ",global_var.ongoing_year)

    user_type = input()

    # user_type = 3
    # username = "ad # print(results)
    # cursor_my.execute("select * from Login")
    # for a in cursor_my:
    #     print(a)min"
    # password = "password"

    if user_type not in ["1","2","3","4"]:
        print("No such user type. Please try again")
        time.sleep(3)
        welcome_screen()
    if (user_type=="4"):
        exit()
        # return


    if(user_type=="1"):
        user_type='S'
    if(user_type=="2"):
        user_type='F'
    if(user_type=="3"):
        user_type='A'

    username = input("Username: ")
    password = getpass()

    success,user_id = login(user_type,username,password)
    
    if success:
        if user_type == "A":
            academics(user_id)
        elif user_type == "F":
            faculty(user_id)
        elif user_type == "S":
            student(user_id)
    else:
        print("Login denied. Please try again")
        time.sleep(3)
        welcome_screen()



def logout(user_id):
    sql = "DELETE FROM Session WHERE id =  %s"
    val = (user_id,)

    cursor_my.execute(sql,val)
    # mydb.commit()
    welcome_screen()
            
def login(user_type,username,password):
    """
Function to authenticate username and password.
"""
    # print(username)
    

    sql = "SELECT id,password,user_type FROM Login WHERE id = %s and user_type= %s"
    # val = (username,user_type)
    cursor_my.execute(sql, (username,user_type,  ))
    
    results = cursor_my.fetchall()
    # print(results)
    # cursor_my.execute("select * from Login")
    # for a in cursor_my:
    #     print(a)

    if len(results) == 0:
        print("No such user present in database")
        return False,None
    
    if len(results) == 1:
        password = password.encode()
        hashed_pass = hashlib.sha256(password).hexdigest()
 
        
        if results[0][1] == str(hashed_pass):
            cursor_my.execute("SELECT * FROM Session where id=%s",(username,))
            res=cursor_my.fetchall()
            if(len(res)!=0):
                print("User already logged in... Try after 3 min..\n")
                return False,None
            
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            sql = "INSERT INTO Session (id, time,user_type) VALUES (%s,%s,%s)"
            val = (results[0][0],timestamp,user_type)

            cursor_my.execute(sql,val)
            
            print("Login successful")
            time.sleep(1)
            
            return True,results[0][0]
        else:
            print("Login Denied: Wrong password")
            return False,None
    else:
        print("Multiple users present. Contact Admin")
        return False,None

    
def academics(user_id):
    """
    Function that displays home screen for academic users
"""
    os.system("clear")
    print(""" Welcome Academics office user

1. Create a new course.
2. View transcript of a student.
3. Generate transcript of a student(.txt).
4. Logout.
5. Exit.
""")

    choice=input()

    if choice == "1":
        academic.new_course(user_id)
    
    if choice == "2":
        academic.view_transcript(user_id)
    
    if choice == "3":
        academic.generate_transcript(user_id)
    
    if choice == "4":
        logout(user_id)
        welcome_screen()
    
    if choice == "5":
        exit()
        

    if choice not in ["1","2","3","4","5"]:
        print("Wrong choice!!!")
        time.sleep(3)
    academics(user_id)




def student(user_id):
    """
Function that displays home screen for student users
"""
    os.system("clear")
    print(""" Welcome Student!

1. View my gradesheet.
2. Compute CGPA.
3. Register a course.
4. Deregister a course.
5. Logout.
6. Exit.
    """)

    choice = input()
    
    if choice == "1":
        student_functions.gradesheet(user_id)
    
    if choice == "2":
        student_functions.calc_cgpa(user_id)
    
    if choice == "3":
        student_functions.reg_course(user_id)
    
    if choice == "4":
        student_functions.dereg_course(user_id)
    
    if choice == "5":
        logout(user_id)
        welcome_screen()
    
    if choice == "6":
        exit()

    if choice not in ["1","2","3","4","5","6"]:
        print("Wrong choice!!!")
        time.sleep(3)
    student(user_id)



def faculty(user_id):
    """
Function that displays home screen for faculty users
"""
    os.system("clear")
    print(""" Welcome Faculty user

1. View Grade of all student(current sem).
2. Offer a new course.
3. Upload Grade entry via .CSV file.
4. View all Offered course.
5. View Student list for a course.
6. View grades of a student(transcript)
7. Logout.
8. Exit
""")

    choice = input()

    if choice == "1":
        faculty_functions.grade_particular_course(user_id)
    
    if choice == "2":
        faculty_functions.offer_new_course(user_id)
    
    if choice == "3":
        faculty_functions.upload_grade_entry(user_id)
    
    if choice == "4":
        faculty_functions.offered_courses(user_id)

    if choice == "5":
        faculty_functions.student_enrolled_particular_course(user_id)
        
    if choice == "6":
        faculty_functions.grade_student_transcript(user_id)
    
    if choice == "7":
        logout(user_id)
        faculty_functions.welcome_screen()
    
    if choice == "8":
        exit()

    if choice not in ["1","2","3","4","5","6","7"]:
        print("Wrong choice!!!")
        time.sleep(3)
    faculty(user_id)

os.system("nohup python3 -u /home/ashutosh/Prog/PGSL_Lab/A04/run_in_background.py output.log &")
os.system("clear")

welcome_screen()