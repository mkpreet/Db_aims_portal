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

def gradesheet(user_id):
    cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s",(user_id,))
    no_stu=cursor_my.fetchall()
    semester=0
    sem_gpa=0
    cnt=0
    cgpa=0
    cnt_cgpa=0
    
    print ("Student Name: ", no_stu[0][1] ,"          Student Roll No: " ,no_stu[0][0])
    cursor_my.execute("SELECT * FROM Graded_courses WHERE stu_id= %s ORDER BY sem",(user_id,))
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
    input("\nPress Enter to return to menu...")
    return

def calc_cgpa(user_id):
    cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s",(user_id,))
    no_stu=cursor_my.fetchall()
    semester=0
    sem_gpa=0
    cnt=0
    cgpa=0
    cnt_cgpa=0
    
    # print ("Student Name: ", no_stu[0][1] ,"          Student Roll No: " ,no_stu[0][0])
    cursor_my.execute("SELECT * FROM Graded_courses WHERE stu_id= %s ORDER BY sem",(user_id,))
    graded_courses= cursor_my.fetchall()
    no_courses=len(graded_courses)
    if(no_courses==0):
        # print("No courses found in database!")
        time.sleep(3)
        return
    for n in range(no_courses):
        if(semester!=graded_courses[n][3]):
            semester=graded_courses[n][3]
            if(cnt!=0 and sem_gpa!=0):
                # print("           SGPA",sem_gpa/cnt)
                # print("     ")
                sem_gpa=0
                cnt=0
            # print("           Semester: ",semester)
     
        

        cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id= %s",(graded_courses[n][0],))
        res=cursor_my.fetchall()
        if(graded_courses[n][2]!="-1"):
            cgpa=cgpa+float(graded_courses[n][2])
            sem_gpa=sem_gpa+float(graded_courses[n][2])
            cnt=cnt+1       
            # print(graded_courses[n][0],res[0][1],graded_courses[n][2])  
            cnt_cgpa=cnt_cgpa+1
        # else:
            # print(graded_courses[n][0],res[0][1],"W")
    # if(cnt!=0):
        # print("           SGPA:    ",sem_gpa/cnt)
    # else:
        # print("           SGPA:    ",sem_gpa)
    print("   ")
    cgpa=cgpa/cnt_cgpa
    print("          Your CGPA:    ",cgpa)
    time.sleep(5)
    return

def reg_course(user_id):
    student_user_id=user_id
    flag_present=0
    print("FLoated courses in ongoing semester are: ")
    cursor_my.execute("SELECT * FROM Faculty_offering")
    offered_course=cursor_my.fetchall()
    no_offer_course=len(offered_course)
    for f in offered_course:
        
        print(f,"\n")
    print("           ")
    course_to_enroll=input("Enter Course_ID which you want to enroll/register: ")
    cursor_my.execute("SELECT * FROM Faculty_offering WHERE course_id=%s",(course_to_enroll,))
    enroll_course=cursor_my.fetchall()
    if(len(enroll_course)==0):
        print("Course not offered.... Please retry...")
        input("Press Enter to go to menu...")
        return
    else:
        flag_present=1
    cursor_my.execute("SELECT * FROM Graded_courses WHERE stu_id=%s",(student_user_id,))
    graded_courses=cursor_my.fetchall()
    no_of_courses=len(graded_courses)
    cnt=0
    credits_enrolled_currently=0
    credits_completed=0
    semester=0
    credits_left=16
    cursor_my.execute("SELECT * FROM Enrolled_students WHERE stu_id=%s",(student_user_id,))
    enroll_courses=cursor_my.fetchall()
    no_enroll_courses=len(enroll_courses)
    for e in range(no_enroll_courses):
        cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id=%s",(enroll_courses[e][0],))
        course_det= cursor_my.fetchall()
        no_of_courses=len(course_det)
        credits_enrolled_currently=credits_enrolled_currently+int(course_det[0][6],)
    print("You have Enrolled for ",credits_enrolled_currently," credits")

    for c in range(no_enroll_courses):
        if(float(enroll_courses[c][2])>=4 ):
            if(float(enroll_courses[c][2])<=10):

                cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id=%s",(enroll_courses[c][0],))
                res_courses=cursor_my.fetchall()
                semester=int(graded_courses[c][3])
                credits_completed=credits_completed+float(res_courses[0][6])
                cnt=cnt+1
    if(semester!=0):
        print("Completed credits till now: ",credits_completed)
        credits_left=((credits_completed/semester)*(125/100))-credits_enrolled_currently
        print("Credits left to enroll a course ",credits_left)
        if(credits_left<0):
            time.sleep(5)
            return
  

    flag_comp_pre_req=0
    #check_pre_req
    requisite=0
    cursor_my.execute("SELECT * FROM Course_pre_req WHERE course_id =%s",(course_to_enroll,))
    pre_req=cursor_my.fetchall()
    no_pre_req=len(pre_req)
    for p in range(no_pre_req):
        cursor_my.execute("SELECT * FROM Graded_courses WHERE course_id=%s and stu_id=%s and points!=%s and points!=%s",(pre_req[p][1],student_user_id,"0","-1",))
        grade_course=cursor_my.fetchall()
        no_grade_course=len(grade_course)
        if(no_grade_course!=0):
            requisite=requisite+1
    if(requisite==no_pre_req):
        flag_comp_pre_req=1

    cursor_my.execute("SELECT * FROM Enrolled_students WHERE course_id=%s and stu_id=%s",(course_to_enroll,student_user_id,))
    result= cursor_my.fetchall()
    no_res=len(result)
    if(flag_present==1):
        if(no_res==0):
            if(semester==0):   #new student
                cursor_my.execute("INSERT INTO Enrolled_students VALUES (%s,%s,%s)",(course_to_enroll,student_user_id,str(semester+1),))
                print("Course ",course_to_enroll," registered successfully!")
                time.sleep(4)
                return
        else:
            print("You are already enrolled for the ... Cannot register again... \n           Taking to menu...")
            time.sleep(4)
            return
    if(flag_present==1):        #course present in catalog
        if(flag_comp_pre_req==1):              #course pre req completed
            if(no_res==0):                    # course not already registered
                
                #calculate_CGPA
                cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s",(user_id,))
                no_stu=cursor_my.fetchall()
                semester=0
                sem_gpa=0
                cnt=0
                cgpa=0
                cnt_cgpa=0
                
                # print ("Student Name: ", no_stu[0][1] ,"          Student Roll No: " ,no_stu[0][0])
                cursor_my.execute("SELECT * FROM Graded_courses WHERE stu_id= %s ORDER BY sem",(user_id,))
                graded_courses= cursor_my.fetchall()
                no_courses=len(graded_courses)
                if(no_courses==0):
                    # print("No courses found in database!")
                    time.sleep(3)
                    return
                for n in range(no_courses):
                    if(semester!=graded_courses[n][3]):
                        semester=graded_courses[n][3]
                        if(cnt!=0 and sem_gpa!=0):
                            # print("           SGPA",sem_gpa/cnt)
                            # print("     ")
                            sem_gpa=0
                            cnt=0
                        # print("           Semester: ",semester)
                        
                  
                    

                    cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id= %s",(graded_courses[n][0],))
                    res=cursor_my.fetchall()
                    if(graded_courses[n][2]!="-1"):
                        cgpa=cgpa+float(graded_courses[n][2])
                        sem_gpa=sem_gpa+float(graded_courses[n][2])
                        cnt=cnt+1       
                        # print(graded_courses[n][0],res[0][1],graded_courses[n][2])  
                        cnt_cgpa=cnt_cgpa+1
                    # else:
                        # print(graded_courses[n][0],res[0][1],"W")
                # if(cnt!=0):
                    # print("           SGPA:    ",sem_gpa/cnt)
                # else:
                    # print("           SGPA:    ",sem_gpa)
                print("   ")
                cgpa=cgpa/cnt_cgpa
                print("    ")
                cursor_my.execute("SELECT * FROM Faculty_offering WHERE course_id=%s",(course_to_enroll,))
                o=cursor_my.fetchall()
                if( cgpa >= float(o[0][2])):
                    cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id=%s",(course_to_enroll,))
                    c=cursor_my.fetchall()
                    if(credits_left-float(c[0][6])<0):
                        print("You are not allowed to add more courses...\n Credit limit reached...\n Please Deregister a course to add new courses\n")
                        time.sleep(4)
                        return
                    else:
                        cursor_my.execute("INSERT INTO Enrolled_students VALUES (%s,%s,%s)",(course_to_enroll,student_user_id,str(semester+1),))
                        print("Course ",course_to_enroll," registered successfully")
                        time.sleep(4)
                        return
                    
                else:
                    print("CGPA Eligibility criteria not fulfilled...\n                       Required CGPA: ")
                    print(o[0][2])
                    time.sleep(4)
                    return
             
            else:
                print("You are already enrolled for the ... Cannot register again... \n           Taking to menu...")
                time.sleep(4)
                return
        else:
            print("Course Pre-requisite criteria not fulfilled \n Cannot register...\n          Taking to menu...")
            time.sleep(4)
            return

    time.sleep(5)
    return

def dereg_course(user_id):
    print("Your enrolled courses are:\n")
    cursor_my.execute("SELECT course_id FROM Enrolled_students WHERE stu_id = %s",(user_id,))
    id=cursor_my.fetchall()
    for d in id:
        print(d)
    print("Enter Course_ID that you want to deregister")
    c_id=input()
    cursor_my.execute("SELECT * FROM Enrolled_students WHERE course_id =%s and stu_id =%s",(c_id,user_id,))
    e=cursor_my.fetchall()
    no_e=len(e)
    if(no_e!=0):
        cursor_my.execute("INSERT INTO Graded_courses VALUES(%s,%s,%s,%s)",(e[0][0],e[0][1],"-1",e[0][2],))
        cursor_my.execute("DELETE FROM Enrolled_students WHERE course_id=%s and stu_id=%s",(c_id,user_id,))
        print("Course deregister Success.\n                    Course ",c_id," withdrawn")
    else:
        print("Not enrolled in this course...")
    input("Press Enter to return to menu")
    return

   