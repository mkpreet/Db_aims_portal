import mysql.connector
import time
# import aims_portal
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="strongpassword",
  database="aims",
  autocommit=True
)

cursor_my = mydb.cursor()


def new_course(user_id):
    # cursor_my.execute("DELETE FROM Course_pre_req where course_id= %s",("2",))
    # cursor_my.execute("DELETE FROM Course_pre_req where course_id= %s",("CS556",))
    # cursor_my.execute("DELETE FROM Course_catalog where course_id=%s",("2",))
    # cursor_my.execute("DELETE FROM Course_catalog where course_id=%s",("CS556",))
    if(user_id!="staffdeanoffice"):
        print("          You are not a valid user to create a course...\n Access denied..\n Course can only be added by 'staffdeanoffice'\n")
        input("Press Enter to continue...")
        return
    print("Enter Course_ID (to be added in Course catalog)")
    C_id=input()
    C_id= C_id.upper()
    cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id=%s",(C_id,))
    c=cursor_my.fetchall()
    if(len(c)!=0):
        print("Course already present in catalog... Please retry...")
        time.sleep(4)
        return

    print("Enter Course_Title ")
    C_title=input()
    print("Enter L T P S C (one by one)")
    L=input()
    T=input()
    P=input()
    S=input()
    C=input()
    cursor_my.execute("INSERT INTO Course_catalog VALUES (%s,%s,%s,%s,%s,%s,%s)",(C_id,C_title,L,T,P,S,C,))
    print("Enter number of pre-requisite courses (0/1/2)")
    C_pre_req=int(input())
    if(C_pre_req>2):
        print("More than 2 pre req not allowed! Moving to menu...")
        cursor_my.execute("DELETE FROM Course_catalog where course_id= %s",(C_id,))
        time.sleep(3)
        return

    if(C_pre_req>0):
        for i in range(C_pre_req):
            print("Enter Course_ID (to be added as Pre-requisite)")
            C_pre_req_id=input()
            C_pre_req_id= C_pre_req_id.upper()
            cursor_my.execute("select * from Course_catalog where course_id=%s",(C_pre_req_id,))
            results=cursor_my.fetchall()
            if len(results) == 0:
                print("No such course present to set as pre req. Deleting the added course...")
                cursor_my.execute("DELETE FROM Course_pre_req where course_id= %s",(C_id,))
                cursor_my.execute("DELETE FROM Course_catalog where course_id= %s",(C_id,))
                time.sleep(3)
                return
            if len(results)!= 0:
                cursor_my.execute("INSERT INTO Course_pre_req VALUES (%s,%s)",(C_id,C_pre_req_id, ))
    if (C_pre_req==0):
        Course_pre_req="Nil"
        cursor_my.execute("INSERT INTO Course_pre_req (course_id,course_pre_req) VALUES (%s,%s)",(C_id,Course_pre_req,))
    
    print("Course added successfully!")
      
    time.sleep(5)
            
    return

def view_transcript(user_id):
    print(":                                  View transcript")
    roll_no = input("Enter the Roll No of student for transcript to be generated: ").upper()
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

def generate_transcript(user_id):   # download .txt file for a particular student's transcript
    print(":                                  View transcript")
    roll_no = input("Enter the Roll No of student for transcript to be generated: ").upper()
    cursor_my.execute("SELECT * FROM Students WHERE stu_id= %s",(roll_no,))
    no_stu=cursor_my.fetchall()
    if len(no_stu)==0:
        print("Incorrect Student Roll no... Taking to main menu")
        time.sleep(3)
        return
    if len(no_stu)==1:
        file=open(roll_no+"_transcript.txt","w")
        semester=-1
        sem_gpa=0
        cnt=0
        cgpa=0
        cnt_cgpa=0
        
        l= "Student Name: "+ str(no_stu[0][1]) +"          Student Roll No: " + str(no_stu[0][0])+"\n"
        file.write(l)
        cursor_my.execute("SELECT * FROM Graded_courses WHERE stu_id= %s ORDER BY sem",(roll_no,))
        graded_courses= cursor_my.fetchall()
        no_courses=len(graded_courses)
        if(no_courses==0):
            l="No courses found in database!"
            print("no courses found!")
            file.write(l)
            time.sleep(3)
            return
        for n in range(no_courses):
            if(semester!=graded_courses[n][3]):
                semester=graded_courses[n][3]
                if(sem_gpa!=0):
                    l="           SGPA:  "+ str(sem_gpa/cnt)+"\n"
                    # print(l)
                    file.write(l)
                    
                    sem_gpa=0
                    cnt=0
                l="           Semester: "+str(semester)+"\n"
                file.write(l)
                
    

            cursor_my.execute("SELECT * FROM Course_catalog WHERE course_id= %s",(graded_courses[n][0],))
            res=cursor_my.fetchall()
            if(graded_courses[n][2]!="-1"):
                cgpa=cgpa+float(graded_courses[n][2])
                sem_gpa=sem_gpa+float(graded_courses[n][2])
                cnt=cnt+1       
                l=graded_courses[n][0]+" "+res[0][1]+" "+graded_courses[n][2]+"\n"
                file.write(l)  
                cnt_cgpa=cnt_cgpa+1
            else:
                l=graded_courses[n][0]+" "+res[0][1]+" W"+"\n"
                file.write(l)     
        if(cnt!=0):
            l="           SGPA:    "+str(sem_gpa/cnt)+"\n"
            file.write(l)
        else:
            l="           SGPA:    "+str(sem_gpa)+"\n"
            file.write(l)
        if(cnt_cgpa!=0):
            l="           CGPA:    "+str(cgpa/cnt_cgpa)+"\n"
            file.write(l)
        else:
            l="           CGPA:    "+str(cgpa)+"\n"
            file.write(l)

    print("           ")
    print("Transcript generated")
    path=os.path.abspath(roll_no+"_transcript.txt")
    print("File is present at directory: ",path)
    file.close()
    input("Press Enter to return back...")
    return


