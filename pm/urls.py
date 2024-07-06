from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import signup_api
from .views import login_api
from .views import GoodsViewSet

router = DefaultRouter()
router.register(r'goods', GoodsViewSet)

urlpatterns = [
    path('signup/', signup_api, name='signup'), # 회원가입
    path('login/', login_api, name='login'), # 로그인
    path('', include(router.urls)), # 제품등록
]
