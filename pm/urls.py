from django.urls import path
from .views import signup_api
from .views import login_api
from .views import GoodsList, GoodsDetail


urlpatterns = [
    path('signup/', signup_api, name='signup'), # 회원가입
    path('login/', login_api, name='login'), # 로그인
    path('goods/', GoodsList.as_view(), name='goods-list'),  # 전체 제품 목록
    path('goods/<int:goods_id>/', GoodsDetail.as_view(), name='goods-detail'),  # 개별 제품 상세
]
