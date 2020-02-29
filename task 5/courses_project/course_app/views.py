from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.response import Response
from rest_framework.decorators import api_view

from course_app import models
#from . import models

# Create your views here.

#@login_required(login_url='login')
def login(request):
    print(request.GET)
    # get_or_create
    #models.Teacher.objects.create_user('test', 'test@test.com', 'test')
    #tea = models.Teacher()
    #tea.save()
    #return redirect('post_detail')
    #return {'aaa':'aaaa'}

@api_view(['GET', 'POST'])
def signup(request):

    if request.method == 'POST':
        a = request.data

    else:
        a = request.data
        
    return Response(a)

#@permission_required('polls.add_choice', login_url='/login/')#raise_exception=True)
