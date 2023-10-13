import mysql.connector
import pandas as pd
import time
import os
import global_var


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  database="aims",
  autocommit=True
)

cursor_my = mydb.cursor()


def grade_particular_course(user_id):
    print("view grade of all student enrolled in a particular course")
    flag=0
    c_id=input("Enter the Course_ID for which you want student list with grades: ").upper()

    cursor_my.execute("SELECT * FROM Graded_courses WHERE course_id= %s", (c_id,))
    graded_course=cursor_my.fetchall()

    no_stu=len(graded_course)
    for g in range (no_stu):
        roll_no=graded_course[g][1]
        adm_yr=int(roll_no[-11:-7])
        finished_sem=int(graded_course[g][3])
        sem= ((global_var. ongoing_year)-adm_yr)*2+(global_var.ongoing_sem)
        # print(sem,finished_sem)
        if (sem-finished_sem)==0:
            cursor_my.execute("SELECT stu_id FROM Students WHERE stu_id=%s",(roll_no,))
            students=cursor_my.fetchall()
            
            flag=1
        
    if(flag==0):
        print("Students have not been graded in given ",c_id," in ongoing sem ",global_var.ongoing_sem)
    else:
        print("Name             Grade Point")
        for g in range(no_stu):
            print(students[0][0],graded_course[g][2])
   
    input("\nPress Enter to return to menu...")
    return

def offer_new_course(user_id):
    print("offer a new course(present in course catalog)\n")
    c_id=input("Enter the Course_ID that you want to offer: ").upper()
    cursor_my.execute("SELECT course_id,course_title FROM Course_catalog WHERE course_id= %s ",(c_id,))
    course_offer= cursor_my.fetchall()
    no_courses=len(course_offer)
    if(no_courses==0):
        print("\nCourse not present in course catalog. Please retry....")
        input("Press Enter to return to menu")
        return
    else:
        cursor_my.execute("SELECT course_id,fac_id FROM Faculty_offering WHERE course_id= %s ",(c_id,))
        course_offer= cursor_my.fetchall()
        no_courses=len(course_offer)
        if(no_courses>0):
            print("Course already offered!! \n                 Please try again...")
            input("Press Enter to return to menu")
            return

    print("Enter the minimum CGPA needed to register for the ",c_id," course:(Enter 0 if all can register)")
    cgpa_eligibility=input()
    if cgpa_eligibility=="0":
        cursor_my.execute("INSERT INTO Faculty_offering VALUES (%s,%s,%s)",(c_id,user_id,"0"))
    else:
        cursor_my.execute("INSERT INTO Faculty_offering VALUES (%s,%s,%s)",(c_id,user_id,cgpa_eligibility))
    print("Course successfully floated for current sem!")

    input("Press Enter to continue")
    return

def upload_grade_entry(user_id):
    print("Upload grade entries of student for offered course via .csv file ")
    c_id=input("Enter Course_id for which you want to upload grades of students ").upper()
    cursor_my.execute("SELECT course_id,course_title FROM Course_catalog WHERE course_id= %s ",(c_id,))
    course_offer= cursor_my.fetchall()
    no_courses=len(course_offer)
    if(no_courses==0):
        print("\nCourse not present in course catalog. Please retry....")
        
    else:
        cursor_my.execute("SELECT course_id,fac_id FROM Faculty_offering WHERE course_id= %s ",(c_id,))
        offer_course=cursor_my.fetchall()
        no_offer_course=len(offer_course)
        if(no_offer_course>0):
        
            cursor_my.execute("SELECT course_id,fac_id FROM Faculty_offering WHERE course_id= %s and fac_id=%s",(c_id,user_id,))
            offered_course= cursor_my.fetchall()
            no_offered_course=len(offered_course)
            if(no_offered_course==0):
                print("Course not offered by you... \n                 Please try again...")
                input("Press Enter to return to menu")
                return
            else:
                f_name=input("Enter the file name (.csv) present in working directory: ")
                location="/home/ashutosh/Prog/PGSL_Lab/A04/"+f_name
                file_present = os.path.isfile(location)
                if file_present==0:
                    print("File with given file name ",f_name," not present in current directory....\n")
                    time.sleep(4)
                    return
                else:
                    file_contents= pd.read_csv(f_name)
                    df_grades=pd.DataFrame(file_contents)
                    no_grades=len(df_grades)
                    for row in df_grades.itertuples():
                        # print(c_id,df_grades[r][0])
                        cursor_my.execute("SELECT * FROM Enrolled_students WHERE course_id=%s AND stu_id = %s",(c_id,row.Roll_no,))
                        enroll_stu = cursor_my.fetchall()
                        no_enroll_stu=len(enroll_stu)
                        # print(no_enroll_stu)
                        if no_enroll_stu>0:
                            cursor_my.execute("INSERT INTO Graded_courses VALUES(%s,%s,%s,%s)",(c_id,enroll_stu[0][1],row.Grade_point,enroll_stu[0][2]))
                            cursor_my.execute("DELETE FROM Enrolled_students WHERE stu_id=%s AND course_id = %s",(row.Roll_no,c_id,))
                        else:
                            print("Unable to upload grade of student ",row.Roll_no," as he/she has not enrolled for the course\n")
                    print("Grades Uploaded successfully!")
                    
        else:
            print("Course not offered in ongoing sem!! \n                 Please try again...")
    input("Press Enter to return to menu")
    return
    

def offered_courses(user_id):
    print("View all offered courses in the current semester")
    cursor_my.execute("SELECT course_id,fac_id,CGPA FROM Faculty_offering")
    course_offer= cursor_my.fetchall()
    no_courses=len(course_offer)
    if(no_courses==0):
        print("\nCurrently no courses are offered...")
        
    else:
        print("Course_id     Course_Title               L T P S C Offered_by CGPA_Eligibility")
        for c in range(no_courses):
            cursor_my.execute("SELECT course_id,course_title,l,t,p,s,c FROM Course_catalog WHERE course_id= %s ",(course_offer[c][0],))
            course_details= cursor_my.fetchall()
            no_courses_det=len(course_details)
            for d in range(no_courses_det):
                print(course_details[d][0],course_details[d][1],course_details[d][2],course_details[d][3],course_details[d][4],course_details[d][5],course_details[d][6],course_offer[c][1],course_offer[c][2])
    
    input("Press Enter to return to menu")
    return

def student_enrolled_particular_course(user_id):
    print("View list of students enrolled in a particular course")
    c_id=input("Enter the Course_ID for which you want student list: ").upper()
    cursor_my.execute("SELECT * FROM Enrolled_students WHERE Course_id=%s ",(c_id,))
    student_enrolled=cursor_my.fetchall()
    no_stu=len(student_enrolled)
    print("\nRoll no       Student Name\n")
    for s in range (no_stu):
        cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s", (student_enrolled[s][1],))
        list_students=cursor_my.fetchall()
        print(list_students[0][0],list_students[0][1])

    time.sleep(3)
    return

def grade_student_transcript(user_id):
    print(":                                  View grade of a student")
    roll_no = input("Enter the Roll No of student for transcript to be generated: ").upper()
    cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s",(roll_no,))
    no_stu=cursor_my.fetchall()
    if len(no_stu)==0:
        print("Incorrect Student Roll no... Taking to main menu")
        time.sleep(3)
        return
    if len(no_stu)==1:
        cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s",(roll_no,))
    no_stu=cursor_my.fetchall()
    if len(no_stu)==0:
        print("Incorrect Student Roll no... Taking to main menu")
        time.sleep(3)
        return
    if len(no_stu)==1:
        semester=0
        sem_gpa=0
        cnt=0
        cgpa=0
        cnt_cgpa=0
        
        print ("Student Name: ", no_stu[0][1] ,"          Student Roll No: " ,no_stu[0][0])
        cursor_my.execute("SELECT * FROM Graded_courses WHERE stu_id= %s ORDER BY sem",(roll_no,))
        graded_courses= cursor_my.fetchall()
        no_courses=len(graded_courses)
        if(no_courses==0):
            print("No courses found in database!")
            time.sleep(3)
            return
        for n in range(no_courses):
            if(semester!=graded_courses[n][3]):
                semester=graded_courses[n][3]
                if(cnt!=0 and sem_gpa!=0):
                    print("           SGPA",sem_gpa/cnt)
                    print("     ")
                    sem_gpa=0
                    cnt=0
                print("           Semester: ",semester)
                
            # if(semester==graded_courses[n][3]):
            #     total_points=total_points+graded_courses[n][2]
            

            cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id= %s",(graded_courses[n][0],))
            res=cursor_my.fetchall()
            if(graded_courses[n][2]!="-1"):
                cgpa=cgpa+float(graded_courses[n][2])
                sem_gpa=sem_gpa+float(graded_courses[n][2])
                cnt=cnt+1       
                print(graded_courses[n][0],res[0][1],graded_courses[n][2])  
                cnt_cgpa=cnt_cgpa+1
            else:
                print(graded_courses[n][0],res[0][1],"W")
        if(cnt!=0):
            print("           SGPA:    ",sem_gpa/cnt)
        else:
            print("           SGPA:    ",sem_gpa)
        print("   ")
        cgpa=cgpa/cnt_cgpa
        print("          Your CGPA:    ",cgpa)

    print("           ")
    input("Press Enter to continue...")
    return
