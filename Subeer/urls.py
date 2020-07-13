"""Subeer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from subeer import views
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('userapi/', include('api.urls')),
    #path('rest_api/',views.rest, name='rest'),
    path('category/new/',views.category_new, name='category-new'),
    path('category/<int:pk>', views.category_show, name='category-show'),
    path('category/<int:pk>/edit',views.category_edit, name='category-edit'),
    path('',views.serial_list, name='main'),
    path('list/',views.serial_list, name='list'),
    path('search/', views.search_serial,name='search'),
    path('popular/', views.rating, name='popular'),
    path('new_episodes/', views.new_episodes, name='new_episodes'),
    path('new_serials/',views.new_serials,name='new_serials'),
    path('form/',views.category_new, name='add_category'),
    path('new/', views.serial_new, name='serial_new'),
    #path('/<int: pk>/edit/',views.serial_edit, name='serial_edit'),
    path('<slug:slug>/', views.SerialDetailView.as_view(),name='details'),


    #path('<slug:slug>/<int:pk_season>/<int:pk_episode', viewsEpisodeDetailView.as_view, name='episode'),
]
