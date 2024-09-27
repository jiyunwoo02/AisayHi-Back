from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets, filters

import django_filters
from django_filters.rest_framework import DjangoFilterBackend


# 사용자
from django.contrib.auth import authenticate, login
from .models import User

# 상품
from .models import Goods
from .serializers import GoodsSerializer

# 주문
from .models import Orders
from .serializers import OrdersSerializer

# 회원가입 API: 아이디, 이름, 비밀번호
@csrf_exempt
def signup_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            login_id = data.get('login_id')
            username = data.get('username')
            userpwd = data.get('userpwd')

            # 아이디, 사용자명, 비밀번호 중 하나라도 입력하지 않으면 -> 에러
            if not login_id or not username or not userpwd:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # 사용자가 이미 존재하는지 확인 -> 중복 회원가입 방지
            if User.objects.filter(login_id=login_id).exists():
                return JsonResponse({'error': 'User already exists'}, status=400)

            user = User(
                login_id=login_id,
                username=username,
                userpwd=userpwd
            )
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

# 로그인 API: 아이디, 비밀번호
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            login_id = data.get('login_id')
            userpwd = data.get('userpwd')

            if not login_id or not userpwd:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # 사용자 인증 - 아이디, 비밀번호
            user = authenticate(request, login_id=login_id, password=userpwd)

            # 사용자가 존재한다면
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful',
                                     'user': {
                                         # 로그인 성공시 프론트에 넘길 객체: 로그인하면 해당 사용자 정보로 사이트 이용
                                         'login_id': user.login_id,
                                     },
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

# 제품 관련 API: 모든 필드 사용 (등록/제거/조회/갱신)
# -- 제품 데이터에 대한 CRUD 및 검색/필터링/정렬 기능 제공
class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # 필터링/검색/정렬 백엔드 설정
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 필터링 필드 설정
    filterset_fields = ['category1', 'brand']

    # 검색 필드 설정
    search_fields = ['goodsName', 'goodsDesc']

    # 정렬 필드 설정
    ordering_fields = ['originalPrice', 'discountedPrice']

# 주문등록 API: 모든 필드 사용
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer