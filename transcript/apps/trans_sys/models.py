from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Degree(models.Model):
    degree_id = models.CharField(max_length=9, verbose_name='Degree ID', primary_key=True)
    degree = models.CharField(max_length=20,
                              choices=(('cs', 'COMPUTER SCIENCE'), ('mac', 'MASTER OF APPLIED COMPUTING')),
                              default='mac')

    class Meta:
        verbose_name = 'Degree'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.degree


class Semester(models.Model):
    semester_ID = models.CharField(primary_key=True, max_length=5, verbose_name='Semester ID')
    semester_Name = models.CharField(max_length=20, verbose_name='Semester Name')

    class Meta:
        verbose_name = 'Semester'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.semester_Name


class Student(AbstractUser):
    Address = models.CharField(max_length=50, null=True, blank=True)
    City = models.CharField(max_length=10, null=True, blank=True)
    Province = models.CharField(max_length=10, null=True, blank=True)
    Country = models.CharField(max_length=10, null=True, blank=True)
    Postal = models.CharField(max_length=10, null=True, blank=True)
    Citizenship = models.CharField(max_length=10, choices=(('citizen','CITIZEN'), ('temp-study','TEMPORARY STUDENT')))
    Gender = models.CharField(max_length=6, choices=(('male','MALE'),('female','FEMALE')))
    Phone = models.CharField(max_length=12, null=True, blank=True)
    GPA = models.IntegerField(null=True, blank=True)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Student Infomation'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Course(models.Model):
    Course_ID = models.CharField(verbose_name='Course ID', primary_key=True, max_length=6)
    Course_Name = models.CharField(verbose_name='Course Name', max_length=15)
    Course_Description =  models.CharField(verbose_name='Course Description', null=True, blank=True, max_length=100 )
    Course_Hour = models.IntegerField(null=True, blank=True, verbose_name='Course Hour')
    Degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    Semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Course Information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Course_Name

class Register(models.Model):
    student = models.ForeignKey(Student, verbose_name='Student', on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Grade = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Course Registration Information'
        verbose_name_plural = verbose_name







