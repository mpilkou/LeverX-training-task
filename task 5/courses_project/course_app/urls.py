from django.urls import path
from . import views

# login
urlpatterns = [
    path('login', views.api_login),
    path('signup', views.api_signup),
    path('logout', views.api_logout),

    # course
    path('course', views.crud_course),
    path('course/<int:course_id>/students', views.course_edit_student),
    path('course/<int:course_id>', views.crud_lections),
    #path('lection/<int:lections_id>', views.lections_homework),

    path('test', views.test),

    
]
