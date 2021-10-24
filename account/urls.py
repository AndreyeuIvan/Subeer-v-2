from django.contrib import admin
from django.urls import path, include, re_path
from subeer import views
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    #registration 
    #re_path(r'^accounts/', include('registration.backends.simple.urls')),
    #re_path(r'^accounts/register/', views.My.as_view(), name='registration_register'),
    re_path(r'^register/', views.register, name='register'),
    re_path(r'^login/', views.user_login, name='login'),
    #re_path(r'restricted/', views.restricted, name='restricted'),
    re_path(r'^logout/$', views.user_logout, name='logout'),
    ]