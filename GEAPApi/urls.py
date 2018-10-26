
from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls', namespace='users')),
]
