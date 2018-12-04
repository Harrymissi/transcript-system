from django.shortcuts import render,redirect
from  django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate,login
from django.views.generic.base import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .models import Student, Semester, Course, Register, Degree
from .forms import ChangeForm
# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Student.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def user_login(request):
    if request.method=='POST':
        user_name=request.POST.get("username","")    # 取不到时候为空  username和password是前端页面账号名密码的name
        user_psw = request.POST.get("password", "")

        user=authenticate(username=user_name,password=user_psw)    #成功返回user对象,失败返回null

        if user is not None:        # 如果不是null说明验证成功

            student = Student.objects.get(username=user_name)

            login(request,user)

            return render(request,"usercenter-info.html",{
                "student": student,
                "current_page": 'info'
            })
            #登陆成功跳回首页
        else:
            return render(request,"login.html",{"msg":"username or password is wrong"})

    elif request.method=="GET":
        return render(request,"login.html",{})

def user_info(request):
    if request.method == "GET":
      stu_id = request.user.id
      student = Student.objects.get(id = int(stu_id))
      current_page = "info"
      return render(request,"usercenter-info.html",{
        "student":student,
        "current_page":current_page
    })

def user_course(request):
    if request.method=="GET":
        stu_id = request.user.id
        student = Student.objects.get(id=int(stu_id))
        courses = Register.objects.filter(student = student)

        return render(request,"usercenter-mycourse.html",{
            "courses" : courses,
            "current_page": "course"
        })

totalGPA = [0,0,0]  # summer, fall, winter
totalHour = [0,0,0]
i = 0

def user_GPA(request):
    if request.method=="GET":
        stu_id = request.user.id
        student = Student.objects.get(id=int(stu_id))
        regesterd_courses = Register.objects.filter(student=student)

        for course in regesterd_courses:
            i = semsterGPA(course.Course.Semester.semester_Name)
            if course.Grade >= 90:
                totalGPA[i] += 4 *course.Course.Course_Hour
            elif course.Grade >= 80 and course.Grade <90:
                totalGPA[i] += 3 *course.Course.Course_Hour
            elif course.Grade >= 70 and course.Grade <80:
                totalGPA[i] += 2 *course.Course.Course_Hour
            elif course.Grade >= 50 and course.Grade < 70:
                totalGPA[i] += 1 *course.Course.Course_Hour
            else:
                totalGPA[i] += 0
            totalHour[i] += course.Course.Course_Hour

        stu_GPA = (totalGPA[0]+totalGPA[1]+totalGPA[2]) / (totalHour[0]+totalHour[1]+totalHour[2])
        summer_GPA = totalGPA[0] / totalHour[0]
        fall_GPA = totalGPA[1] / totalHour[1]
        winter_GPA = totalGPA[2] / totalHour[2]

        return render(request, 'usercenter-gpa.html', {
            'total_GPA': round(stu_GPA,2),
            'summer_GPA': summer_GPA,
            'fall_GPA': fall_GPA,
            'winter_GPA': winter_GPA,
            'current_page': 'gpa'
        })

def semsterGPA(semester):
    if semester == 'Summer':
        return 0
    elif semester == 'Fall':
        return 1
    elif semester == 'Winter':
        return 2


def user_transcript(request):
    if request.method=="GET":
        stu_id = request.user.id
        student = Student.objects.get(id=int(stu_id))
        regesterd_courses = Register.objects.filter(student=student)

        summerCourse = []
        fallCourse = []
        winterCourse = []

        for course in regesterd_courses:
            if course.Course.Semester.semester_Name == 'Summer':
                summerCourse.append(course)
            elif course.Course.Semester.semester_Name == 'Fall':
                fallCourse.append(course)
            else:
                winterCourse.append(course)

        summerGPA = totalGPA[0] / totalHour[0]
        fallGPA = (totalGPA[0] + totalGPA[1]) / (totalHour[0] + totalHour[1])
        winterGPA = (totalGPA[0] + totalGPA[1] + totalGPA[2]) / (totalHour[0] + totalHour[1] + totalHour[2])

        return render(request, 'transcript.html', {
            'summerGPA': round(summerGPA, 2),
            'fallGPA': round(fallGPA,2),
            'winterGPA': round(winterGPA,2),
            'student': student,
            'summer_courses': summerCourse,
            'fall_courses': fallCourse,
            'winter_courses': winterCourse,
            'summer_agpa': totalGPA[0] / totalHour[0],
            'fall_agpa': totalGPA[1] / totalHour[1],
            'winter_agpa': totalGPA[2] / totalHour[2]
        })

def changeProfile(request):
    if request.method == "POST":
        user_address = request.POST.get("address","")
        user_email = request.POST.get("email","")

        student = Student.objects.get(id = int(request.user.id))
        student.email = user_email
        student.Address = user_address
        student.save()

        return render(request, 'usercenter-info.html')

    if request.method == "GET":
        stu_id = request.user.id
        student = Student.objects.get(id=int(stu_id))
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "student": student,
            "current_page": current_page
        })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'forget_psw.html', {
        'form': form
    })

# def regester_courses(request):
#     if request.method == 'POST':
#         user = Student.objects.get(id = request.user.id)
#         semester = request.POST.get("type1", "")
#         semester_obj = Semester.objects.get(semester_Name= semester)
#         degree_obj = Degree.objects.get(degree_id=user.degree.degree_id)
#
#         unregestered_courses = Course.objects.filter(Semester=semester_obj).filter(Degree=degree_obj).exclude(register__student=request.user)  # 学生没有注册的课程
#
#         return render(request, 'usercenter-register_courseList.html', {
#             "courses": unregestered_courses,
#             "current_page": "course_register"
#         })
#     else:
#         return render(request, 'usercenter-register_semester.html', {
#             "current_page": "course_register"
#         })
#
#
# def self_register(request):
#     if request.method == 'POST':
#         user = Student.objects.get(id=request.user.id)
#         course_name =  request.POST.get("course", "")
#         course_obj = Course.objects.get(Course_Name=course_name)
#
#         regestering_course = Register()
#         regestering_course.Course = course_obj
#         regestering_course.student = user
#         regestering_course.save()
#
#
#         semester = request.POST.get("type1", "")
#         semester_obj = Semester.objects.get(semester_Name=semester)
#         degree_obj = Degree.objects.get(degree_id=user.degree.degree_id)
#
#         unregestered_courses = Course.objects.filter(Semester=semester_obj).filter(Degree=degree_obj).exclude(
#             register__student=request.user)
#
#         return render(request, 'usercenter-register_courseList.html', {
#             "courses": unregestered_courses,
#             "current_page": "course_register"
#         })
#
#     else:
#         return render(request, 'usercenter-register_courseList.html', {
#             "current_page": "course_register"
#         })
