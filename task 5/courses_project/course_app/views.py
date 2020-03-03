from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 

from course_app import models
#from . import models

# Create your views here.

@api_view(['GET'])
@login_required(login_url='/api/login')
def test(request):
    return Response({'a':'a'})

@api_view(['GET','POST'])
def api_logout(request):
    logout(request)
    
    response = Response({'message':'you logged out'})
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response


@api_view(['POST'])
def api_login(request):
    user = User.objects.get(username=request.data.get('username'))

    if user is None:
        return Response({'message':'user not exists'})

    if not request.data.get('password') == user.password:
        return Response({'message':'incorrect password'})

    cookie = None

    if request.data.get('is_teacher'):
        try:
            user.teacher
        except ObjectDoesNotExist:
            return Response({'message':'incorrect role'})

        cookie = True
    elif not request.data.get('is_teacher'):
        try:
            user.student
        except ObjectDoesNotExist:
            return Response({'message':'incorrect role'})

        cookie = False
    else:
        return Response({'message':'role not used'})    
    
    if cookie == None:
        return Response({'message':'cookie error'})

    login(request, user)
    res = Response({'message':'sucsess'})
    res.set_cookie('is_teacher', cookie)
    return res


@api_view(['POST'])
def api_signup(request):

    if request.method == 'POST':
        a = request.data

    a = models.Teacher.objects.all()

    #from django.contrib.auth.models import User

    #u = User(username = 'test', email = 'test@test.com', password = 'test')
    #u.save()
    #t = models.Teacher()
    #t.user = u
    #t.save()
    print(list(a))

    return Response({'type':'{}'.format(type(a))})

#@permission_required('polls.add_choice', login_url='/login/')#raise_exception=True)
