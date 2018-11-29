from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'users'
urlpatterns = [
    path('send_email/', views.send_email),
    path('register/', views.register),
    path('login/', views.login),
	path('user_info/', views.user_info),
	path('upload_image/', views.upload_image),
	path('forgotten_password/', views.forgotten_password),
	path('<int:identifier>/donate/', views.donate),
	path('<int:identifier>/solicitude/', views.solicitude_list),
	path('<int:identifier>/solicitude/<int:pk_solicitude>/', views.solicitude_detail),

    path('excel/', views.export_excel),


    path('login/',  views.login, name='login'),
    path('home/',  views.home, name='home'),
    path('detail/<int:pk_solicitude>/',  views.detail, name='detail'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
