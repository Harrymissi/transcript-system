import xadmin
from xadmin import views
from .models import Student, Semester, Course, Register, Degree
# Register your models here.

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    site_title = "Transcript System"  # 修改左上角名称和底角名称
    site_footer = "Developed by Zhen Zhu "
    menu_style = "accordion"

xadmin.site.register(views.CommAdminView, GlobalSettings)

class StudentAdmin(object):
    search_fields = ['Address', 'GPA', 'Gender', 'Citizenship']
    list_filter = ['Address', 'GPA', 'Gender', 'Citizenship']
    list_display = ['username', 'Address', 'GPA', 'Gender', 'Citizenship']

#xadmin.site.register(Student, StudentAdmin)


class SemesterAdmin(object):
    search_fields = ['semester_ID', 'semester_Name']
    list_filter = ['semester_ID', 'semester_Name']
    list_display = ['semester_ID', 'semester_Name']


xadmin.site.register(Semester, SemesterAdmin)

class CourseAdmin(object):
    search_fields = ['Course_ID', 'Course_Name', 'Course_Hour', 'Degree']
    list_filter = ['Course_ID', 'Course_Name', 'Course_Hour', 'Degree', 'Course_Description']
    list_display = ['Course_ID', 'Course_Name', 'Course_Hour', 'Degree']

xadmin.site.register(Course, CourseAdmin)

class RegisterAdmin(object):
    search_fields = ['student', 'Course', 'Grade']
    list_filter = ['student', 'Course', 'Grade']
    list_display = ['student', 'Course', 'Grade']

xadmin.site.register(Register, RegisterAdmin)

class DegreeAdmin(object):
    search_fields = ['degree_id', 'degree']
    list_filter = ['degree_id', 'degree']
    list_display = ['degree_id', 'degree']

xadmin.site.register(Degree, DegreeAdmin)
