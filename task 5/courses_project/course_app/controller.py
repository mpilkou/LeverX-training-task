
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

#################
#
#   Courses
#
#################
# C
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
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
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
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
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def delete_course(request):
    course = None
    try:
        course = models.Course.objects.get(name=request.data.get('name'))
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    course.delete()

    return Response({'message':'sucess'})

# CUSTOM COURSE

# select students on course
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def show_students_on_course(request, course_id):
    current_course = None
    try:
        teacher_id = request.user.teacher.id
        current_course = models.Course.objects.get(id = course_id)
        is_course_teacher = list(current_course.teachers.filter(id = teacher_id))

        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    ansver = serializers.serialize('json', current_course.students.all())

    response = Response(ansver)
    return response
    

# add student to course
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def add_student_to_course(request, course_id):
    current_course = None
    try:
        teacher_id = request.user.teacher.id
        current_course = models.Course.objects.get(id = course_id)
        is_course_teacher = list(current_course.teachers.filter(id = teacher_id))

        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    
    student = None

    try:
        student_name = request.data.get('name')
        student = User.objects.get(username = student_name).student
        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'student not exist'})

    current_course.students.add(student)

    return Response({'message':'sucess'})

# delete student to course
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def delete_student_from_course(request, course_id):

    current_course = None
    try:
        teacher_id = request.user.teacher.id
        current_course = models.Course.objects.get(id = course_id)
        is_course_teacher = list(current_course.teachers.filter(id = teacher_id))

        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    
    student = None

    try:
        student_name = request.data.get('name')
        student = User.objects.get(username = student_name).student
        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'student not exist'})

    current_course.students.remove(student)

    return Response({'message':'sucess'})

#################
#
#   Lections
#
#################

@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def create_lection(request, course_id):
    current_course = None
    try:
        teacher_id = request.user.teacher.id
        current_course = models.Course.objects.get(id = course_id)
        is_course_teacher = list(current_course.teachers.filter(id = teacher_id))
        
        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    title = request.data.get('title')
    presentation = request.data.get('presentation')

    if title is None:
        Response({'message':'set title'})
    
    if presentation is None:
        Response({'message':'set presentation text'})

    lection = models.Lection()
    lection.title = title
    lection.presentation = presentation
    lection.course = current_course
    lection.save()
    
        
    return Response({'message':'sucess'})

# R
@login_required(login_url='/api/login')
def select_all_lections_by_course(request, course_id):
    print(request.user)
    ansver = serializers.serialize('json', models.Lection.objects.filter(course_id = course_id))
    response = Response(ansver)
    return response

# U
@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def update_lection(request, course_id):

    current_course = None
    try:
        teacher_id = request.user.teacher.id
        current_course = models.Course.objects.get(id = course_id)
        is_course_teacher = list(current_course.teachers.filter(id = teacher_id))
        
        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    current_lection = None
    try:
        lections = models.Lection.objects.filter(course = current_course)
        current_lection = lections.get(title = request.data.get('title'))
    except ObjectDoesNotExist:
        return Response({'message':'lection not exist'})

    presentation = request.data.get('presentation') if request.data.get('presentation') else lection.presentation

    current_lection.presentation = presentation
    current_lection.save()

    return Response({'message':'sucess'})

@permission_required('course_app.custom_teach_permissions', login_url='/api/login/')
def delete_lection(request, course_id):

    current_course = None
    try:
        teacher_id = request.user.teacher.id
        current_course = models.Course.objects.get(id = course_id)
        is_course_teacher = list(current_course.teachers.filter(id = teacher_id))
        
        if is_course_teacher == []:
            return Response({'message':'you not teacher of this course'})
    except ObjectDoesNotExist:
        return Response({'message':'course not exist'})

    current_lection = None
    try:
        lections = models.Lection.objects.filter(course = current_course)
        current_lection = lections.get(title = request.data.get('title'))
    except ObjectDoesNotExist:
        return Response({'message':'lection not exist'})

    current_lection.delete()

    return Response({'message':'sucess'})

#################
#
#   homework
#
#################
