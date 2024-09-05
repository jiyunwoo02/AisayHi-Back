from django.urls import path
from .views import signup_api
from .views import login_api


urlpatterns = [
    path('signup/', signup_api, name='signup'), # 회원가입
    path('login/', login_api, name='login'), # 로그인
]
