from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from course_app import models
#from . import models

# Create your views here.

#@login_required(login_url='login')
def login(request):
    pass
    # get_or_create
    #models.Teacher.objects.create_user('test', 'test@test.com', 'test')
    #return redirect('post_detail')
    #return {'aaa':'aaaa'}

def signup(reqest):
    pass

#@permission_required('polls.add_choice', login_url='/login/')#raise_exception=True)
