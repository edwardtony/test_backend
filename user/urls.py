from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'users'
urlpatterns = [
    path('update_fcm_token/', views.update_fcm_token),
    path('send_email/', views.send_email),
    path('send_massive_notification/', views.send_massive_notification, name="send_massive_notification"),
    path('register/', views.register, name="register"),
    path('login/', views.login),
    path('logout/', views.logout, name="logout"),
	path('user_info/', views.user_info),
	path('upload_image/', views.upload_image),
	path('forgotten_password/', views.forgotten_password),
	path('<int:identifier>/donate/', views.donate),
	path('<int:identifier>/solicitude/', views.solicitude_list),
	path('<int:identifier>/solicitude/<int:pk_solicitude>/', views.solicitude_detail),
	path('<int:identifier>/solicitude/<int:pk_solicitude>/item/<int:pk_item>/', views.update_item),

    path('excel/', views.export_excel, name="excel"),


    path('index/',  views.index, name='index'),
    path('reset_password/',  views.reset_password, name='reset_password'),
    path('home/',  views.home, name='home'),
    path('detail/<int:pk_solicitude>/',  views.detail, name='detail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
