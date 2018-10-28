from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('send_email/', views.send_email),
    path('send_notification/', views.send_notification),
    path('register/', views.register),
    path('login/', views.login),
	path('user_info/', views.user_info),
	path('<int:identifier>/solicitude/', views.solicitude_list),
	path('<int:identifier>/solicitude/<int:pk_solicitude>/', views.solicitude_detail),
]
