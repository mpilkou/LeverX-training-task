from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
# base.User
# AbstractUser
#hasattr(user, 'myspecialuser')
class Teacher(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    class Meta:
        permissions = [
            ("custom_teach_permissions", "my custom permisions for teachers"),
        ]

class Student(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    class Meta:
        permissions = [
            ("custom_stud_permissions", "my custom permisions for students"),
        ]

class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    teachers = models.ManyToManyField(Teacher)
    students = models.ManyToManyField(Student)

class Lection(models.Model):

    title = models.CharField(max_length=80, blank=False)
    presentation = models.TextField(blank=False)


    course = models.ForeignKey(Course, on_delete = models.PROTECT)

class Homework(models.Model):
    txt = models.CharField(max_length=200, blank=False)
    comment = models.CharField(max_length=40, blank=True)
    mark = models.DecimalField(max_digits=3, decimal_places=0, blank=True)

    lection = models.ForeignKey(Lection, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)

