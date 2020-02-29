from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

@login_required(login_url='/login/')
def get_courses(request):
    pass

#@permission_required('polls.add_choice', login_url='/login/')#raise_exception=True)
