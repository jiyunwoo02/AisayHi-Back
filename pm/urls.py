from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import signup_api
from .views import login_api
from .views import GoodsViewSet, OrdersViewSet

# DefaultRouter는 ViewSet와 함께 사용되어 URL 패턴 자동 생성 및 관리
router = DefaultRouter() # DefaultRouter 인스턴스 생성

# register() 메서드: ViewSet을 라우터에 등록, 두 개의 주요 인자 받는다!
# prefix: URL의 접두사로 사용될 문자열
# viewset: 등록할 ViewSet 클래스
router.register(r'goods', GoodsViewSet)
router.register(r'orders', OrdersViewSet)

urlpatterns = [
    path('signup/', signup_api, name='signup'), # 회원가입
    path('login/', login_api, name='login'), # 로그인
    path('', include(router.urls)), # 제품 관련, 주문 등록
]
