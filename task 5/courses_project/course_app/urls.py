from django.urls import path
from . import views

# login
urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),

    
]
