from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls), # 관리자
    path('pm/', include('pm.urls')), # app명으로
]