
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

def remove_same_in_list(some_list):
    items_set = set(some_list)
    items_list = []

    for name in items_set:
        items_list.append(models.Teacher.objects.get(name=name))

    return items_list


# Courses
# C
#@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')

def create_courses(request):
    try:
        course = models.Course.objects.get(name=request.data.get('name'))
        return Response({'message':'course already exists'})
    except ObjectDoesNotExist:
        '''expected error (not exist)'''
        pass

    teacher = models.Teacher.objects.get(id=request.user.teacher.id)
    course = models.Course.objects.create(name = request.data.get('name'))
    teachers = request.data.get('teachers')
    students = request.data.get('students')
    
    if teachers is None:
        teachers = [teacher]
    else:
        teachers = remove_same_in_list(teachers)
    
    course.teachers.set(teachers)

    course.students.set([students] if students is None else remove_same_in_list(students))
    course.save()

    return Response({'message':'sucess'})

# R
@login_required(login_url='/api/login')
def select_all_courses(request):
    ansver = serializers.serialize('json', models.Course.objects.all())
    response = Response(ansver)
    return response