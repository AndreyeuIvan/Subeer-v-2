from django.contrib import admin
from django.urls import path, include, re_path
from subeer import views
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('userapi/', include('api.urls')),
    #path('rest_api/',views.rest, name='rest'),
    # category form
    path('category/new/',views.category_new, name='category-new'),
    path('category/<int:pk>', views.category_show, name='category-show'),
    path('category/<int:pk>/edit',views.category_edit, name='category-edit'),

    #serial form
    path('serial/new/',views.serial_new, name='serial-new'),
    path('serial/<int:pk>/', views.serial_show, name='serial-list'),
    path('serial/<int:pk>/edit/',views.serial_edit, name='serial-edit'),

    #registration 
    #re_path(r'^accounts/', include('registration.backends.simple.urls')),
    #re_path(r'^accounts/register/', views.My.as_view(), name='registration_register'),
    re_path(r'^register/', views.register, name='register'),
    re_path(r'^login/', views.user_login, name='login'),
    #re_path(r'restricted/', views.restricted, name='restricted'),
    re_path(r'^logout/$', views.user_logout, name='logout'),

    path('',views.serial_list, name='main'),
    path('list/',views.serial_list, name='list'),
    path('search/', views.search_serial,name='search'),
    path('popular/', views.rating, name='popular'),
    path('new_episodes/', views.new_episodes, name='new_episodes'),
    path('new_serials/',views.new_serials,name='new_serials'),
    path('form/',views.category_new, name='add_category'),
    path('new/', views.serial_new, name='serial_new'),
    #path('/<int: pk>/edit/',views.serial_edit, name='serial_edit'),
    #path('<slug:slug>/', views.get_serial, name='details'),



    #path('<slug:slug>/<int:pk_season>/<int:pk_episode', viewsEpisodeDetailView.as_view, name='episode'),
]
