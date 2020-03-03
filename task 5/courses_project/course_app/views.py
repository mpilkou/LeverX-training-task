from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist

# for use
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from course_app import models
#from . import models

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
