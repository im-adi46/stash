from django.contrib import admin
from django.urls import path
from app1.views import *

urlpatterns = [
    path('',signin,name='signin'),
    path('signout/',signout,name='signout'),
    path('signup/',signup,name='signup'),
    path('verify_otp/<int:user_id>/',verify_otp, name='verify_otp'),
    path('calci/',calci,name='calci'),
    path('home/',home,name='home'),
    path("fetch-users/", fetch_users_by_operation, name="fetch_users"),
]
