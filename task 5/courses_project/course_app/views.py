from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from course_app import models
#from . import models

# Create your views here.

@api_view(['GET'])
#@login_required(login_url='/api/login')
#@permission_required('teacher.my_teacher', raise_exception=True)
@permission_required('course_app.custom_permissions', raise_exception=True)
def test(request):
    us = User.objects.get(username='test')
    #t = models.Teacher.objects.get(id = 1)
    from django.shortcuts import get_object_or_404

    #user = get_object_or_404(User, pk=request.user.id)
    #permission = Permission.objects.get(name='teacher permisions')
    #user.user_permissions.add(permission)
    #user = get_object_or_404(User, pk=user_id)

    #perm = Permission.objects.get(name='my teacher permisions')
    #print('perm')
    #print(perm)
    #request.user.user_permissions.add(perm)
    #us.user_permissions.add(perm)
    #us.save()

    print([Permission.objects.all()])
    #ct = ContentType.objects.get(app_label='auth', model='user')
    #perm, created = Permission.objects.get_or_create(codename='can_view', name='Can View Users', content_type=ct)
    #post_syncdb.connect(add_user_permissions, sender=auth_models)
    
    #request.user.user_permissions.set([perm])

    #print(request.user.user_permissions)
    print(us.user_permissions)
    print(request.auth)
    print('aaa')
    
    print(us.has_perm('view_homework'))
    print(us.has_perm('course_app.view_homework'))
    
    print(us.has_perm('custom_permissions'))

    print(us.has_perm('course_app.custom_permissions'))

    print(us.has_perm('teacher'))
    print(us.has_perm('teacher permisions'))
    print(us.has_perm('teacher.my_teacher'))
    print(us.has_perm('teacher.my teacher permisions'))
    print(request.user.has_perm('teacher'))
    print(request.user.has_perm('teacher permisions'))

    
    res = Response({'a':'a'})
    
    #print(us.permission)
    
    res.user = request.user
    return res

@api_view(['GET','POST'])
def api_logout(request):
    logout(request)
    #print(request.user.permissions)

    response = Response({'message':'you logged out'})
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response


@api_view(['POST'])
def api_login(request):

    # don't work
    #print()
    #perm = Permission.objects.get(name='teacher permisions')
    #print(type(perm))


    user = User.objects.get(username=request.data.get('username'))

    if user is None:
        return Response({'message':'user not exists'})

    if not user.check_password(request.data.get('password')):
        return Response({'message':'incorrect password'})

    #try:
    #    user.teacher
    #except ObjectDoesNotExist:
    #    return Response({'message':'incorrect role'})

    #try:
    #    user.student
    #except ObjectDoesNotExist:
    #    return Response({'message':'incorrect role'})

    from django.contrib.auth import get_user_model
    per = Permission.objects.get(name='my custom permisions')

    #user.save()
    u = get_user_model().objects.get(username=request.data.get('username'))
    u.user_permissions.add(per)
    u.save()
    print(u.user_permissions)
    user = u
    
    #print(a)
    login(request, authenticate(request, username=request.data.get('username'), password=request.data.get('password')))
    res = Response({'message':'sucsess', 'check': user.has_perm('teacher permisions'),'check1': user.has_perm('teacher')})
    return res


@api_view(['POST'])
def api_signup(request):

    user = None
    try:
        user = User.objects.get(username=request.data.get('username'))
        return Response({'message':'user already exists'})
    except:
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

    
    user = User(username = request.data.get('username'), password = request.data.get('password'))
    user.set_password(user.password)
    user.save()
    user.user_permissions.add(perm)
    #user.user_permissions.add(perm)
    user.save()
    role.user = user
    role.save()

    user = User.objects.get(username=user.username)

    #print(user.user_permissions)
    #print(user.user_permissions.add(perm))

    # WORK ++
    #print(user.user_permissions.set([perm]))

    login(request, authenticate(request, username=request.data.get('username'), password=request.data.get('password')))
    res = Response({'message':'sucsess'})

    return res

#@permission_required('polls.add_choice', login_url='/login/')#raise_exception=True)
