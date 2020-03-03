
# for use
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# all models
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ObjectDoesNotExist
from course_app import models

# work on data 
from django.core import serializers

def make_set_of_teachers(teachers):
    
    teachers_set = set(teachers)
    teachers = []

    for teacher_name in teachers_set:
        teachers.append(User.objects.get(username=teacher_name).teacher)

    return teachers

def make_set_of_students(students):
    
    students_set = set(students)
    students = []

    for student_name in students_set:
        students.append(User.objects.get(username=student_name).student)
        
    return students

# Courses
# C
#@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')

def create_course(request):
    try:
        course = models.Course.objects.get(name=request.data.get('name'))
        return Response({'message':'course already exists'})
    except ObjectDoesNotExist:
        '''expected error (not exist)'''
        pass

    teacher = models.Teacher.objects.get(id=request.user.teacher.id)
    course = models.Course()
    course.name = request.data.get('name')
    course.save()

    teachers = request.data.get('teachers')
    students = request.data.get('students')

    if teachers is None or teachers == []:
        teachers = [teacher]
    else:
        teachers = make_set_of_teachers(teachers)

    if students is None or students == []:
        students = []
    else:
        students = make_set_of_students(students)

    course.teachers.set(teachers)
    course.students.set(students)
    course.save()
        
    return Response({'message':'sucess'})

# R
@login_required(login_url='/api/login')
def select_all_courses(request):
    ansver = serializers.serialize('json', models.Course.objects.all())
    response = Response(ansver)
    return response

# U
def update_course(request):
    course = None
    try:
        course = models.Course.objects.get(name=request.data.get('name'))
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    teachers = request.data.get('teachers')
    students = request.data.get('students')

    if not( teachers is None or teachers == []):
        teachers = make_set_of_teachers(teachers)
        course.teachers.set(teachers)

    if not( students is None or students == []):
        students = make_set_of_students(students)
        course.students.set(students)

    course.save()

    return Response({'message':'sucess'})

# D
def delete_course(request):
    course = None
    try:
        course = models.Course.objects.get(name=request.data.get('name'))
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    course.delete()

    return Response({'message':'sucess'})
