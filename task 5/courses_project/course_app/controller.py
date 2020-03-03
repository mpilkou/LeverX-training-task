
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


# Courses
# C
#@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')

def create_courses(request):
    
    try:
        course = models.Course.objects.get(name=request.data.get('name'))
        return Response({'message':'course already exists'})

    except ObjectDoesNotExist:
        '''expected error (not exist)'''
        teacher = models.Teacher.objects.get(id=request.user.teacher.id)
        course = models.Course(name = request.data.get('name'))
        course.name = request.data.get('name')
        course.save()
        course.teachers.set([teacher])
        course.save()

    print(request.user.teacher)
        
    return Response({'message':'sucess'})

# R
@login_required(login_url='/api/login')
def select_all_courses(request):
    ansver = serializers.serialize('json', models.Course.objects.all())
    response = Response(ansver)
    return response