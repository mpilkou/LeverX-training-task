from django.shortcuts import render

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
from course_app import models, controller

# work on data 
from django.core import serializers

# Create your views here.

@api_view(['GET'])
@login_required(login_url='/api/login')
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def test(request):
    res = Response({'test':'test'})
    #print(us.permission)
    #res.user = request.user
    return res

@api_view(['GET','POST'])
def api_logout(request):
    logout(request)

    response = Response({'message':'you logged out'})
    response.delete_cookie('csrftoken')
    #response.delete_cookie('sessionid')
    return response


@api_view(['POST'])
def api_login(request):

    user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))

    if user is None:
        return Response({'message':'user not exists'})

    if not user.check_password(request.data.get('password')):
        return Response({'message':'incorrect password'})
    
    login(request, user)
    res = Response({'message':'sucsess'})
    return res


@api_view(['POST'])
def api_signup(request):

    user = None
    try:
        user = User.objects.get(username=request.data.get('username'))
        return Response({'message':'user already exists'})
    except ObjectDoesNotExist:
        '''expected error (user not exist)'''
        pass
        

    role = None
    perm = None
    if request.data.get('is_teacher'):
        role = models.Teacher()
        perm = Permission.objects.get(name='my custom permisions for teachers')
    else:
        perm = Permission.objects.get(name='my custom permisions for students')
        role = models.Student()

    user = User(username=request.data.get('username'), password=request.data.get('password'))
    user.set_password(user.password)
    user.save()
    user.user_permissions.add(perm)
    user.save()
    role.user = user
    role.save()

    login(request, authenticate(request, username=request.data.get('username'), password=request.data.get('password')))
    res = Response({'message':'sucsess'})
    return res

#@permission_required('polls.add_choice', login_url='/login/')#raise_exception=True)




#####################
#                   #
#   CRUD            #
#                   #
#####################

# Course

@api_view(['GET','POST','PUT','DELETE'])
@login_required(login_url='/api/login')
def course(request):
    authenticate(request, username=request.user)
    if request.method == 'GET':
        return controller.select_all_courses(request)
    elif request.method == 'POST':        
        return controller.create_course(request)
    elif request.method == 'PUT':        
        return controller.update_course(request)
    elif request.method == 'DELETE':        
        return controller.delete_course(request)
    else:
        return Response({'error':'not found'})

@api_view(['GET','POST','PUT','DELETE'])
@login_required(login_url='/api/login')
def lections(request, course_id):
    if request.method == 'GET':
        return controller.select_all_lections_by_course(request, course_id)
    elif request.method == 'POST':        
        return controller.create_lection(request, course_id)
    elif request.method == 'PUT':        
        return controller.update_lection(request, course_id)
    elif request.method == 'DELETE':        
        return controller.delete_lection(request, course_id)
    else:
        return Response({'error':'not found'})

#@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')