from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets, filters

import django_filters
from django_filters.rest_framework import DjangoFilterBackend


# 사용자
from django.contrib.auth import authenticate, login
from .models import User
from django.contrib.auth.hashers import make_password

# 상품
from .models import Goods
from .serializers import GoodsSerializer

# 주문
from .models import Orders
from .serializers import OrdersSerializer


import pandas as pd
import random
import os
from django.conf import settings

import django_filters
from django_filters.rest_framework import DjangoFilterBackend




# 회원가입 API: 아이디, 이름, 비밀번호
@csrf_exempt
def signup_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            login_id = data.get('login_id')
            username = data.get('username')
            userpwd = data.get('userpwd')

            # 필드 확인
            if not login_id or not username or not userpwd:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # 중복 회원가입 방지
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
                                             'userpwd':user.userpwd,
                                             'username': user.username
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





# **CSV 파일 경로 설정 및 데이터 로드**
CSV_DIR = os.path.join(settings.BASE_DIR, 'pm/data/')
goods = pd.read_csv(os.path.join(CSV_DIR, 'goods.csv'), encoding='utf-8-sig')
goodsKeyword = pd.read_csv(os.path.join(CSV_DIR, 'goodsKeyword.csv'), encoding='utf-8-sig')
situation = pd.read_csv(os.path.join(CSV_DIR, 'situation.csv'), encoding='utf-8-sig')
situationCategory = pd.read_csv(os.path.join(CSV_DIR, 'situationCategory.csv'), encoding='utf-8-sig')
situationKeyword = pd.read_csv(os.path.join(CSV_DIR, 'situationKeyword.csv'), encoding='utf-8-sig')

# **CSV 데이터 병합 및 전처리**
goods = goods.merge(goodsKeyword[['ASIN', 'goodsKeyword']], on='ASIN', how='left')
goods['goodsKeyword'] = goods['goodsKeyword'].fillna('')

situation_data = situation.merge(situationCategory, on='situationCateKey', how='left')



# **추천 함수: 탕비실(식음료) 상품 포함/제외 처리**
def get_recommendations(goods_df, pantry_only=False, exclude_pantry=False, num_recommendations=12):
    if pantry_only:
        # category1이 '식음료'인 상품만 필터링
        filtered_goods = goods_df[goods_df['category1'] == '식음료']
    elif exclude_pantry:
        # category1이 '식음료'가 아닌 상품만 필터링
        filtered_goods = goods_df[goods_df['category1'] != '식음료']
    else:
        # 모든 상품 대상으로 추천
        filtered_goods = goods_df

    # 무작위 추천
    if filtered_goods.empty:
        return []

    recommendations = filtered_goods.sample(n=min(num_recommendations, len(filtered_goods)))

    return recommendations[[
        'category1', 'category2', 'goodsName', 'brand',
        'originalPrice', 'discountedPrice', 'ratingAvg',
        'ratingCount', 'goodsImg'
    ]].to_dict(orient='records')


# **상황 기반 추천 View (수정됨)**
def situation_based_recommendation_view(request, situation_key):
    try:
        print(f"Received request for situation_key: {situation_key}")

        # 상황 키 유효성 검사 및 데이터 가져오기
        situation_key = int(situation_key)
        situation_info = situation_data[situation_data['situationKey'] == situation_key]

        if situation_info.empty:
            return JsonResponse({'error': 'Invalid situation key'}, status=404)

        situation_info = situation_info.iloc[0]
        situation_category = f"{situation_info['situationCategory1']} > {situation_info['situationCategory2']}"
        # **추천 섹션 구분: 식음료 제외 섹션 / 식음료 전용 섹션**

        # 일반 상품 추천 (식음료 제외)
        general_recommendation_1 = get_recommendations(goods, exclude_pantry=True)
        general_recommendation_2 = get_recommendations(goods, exclude_pantry=True)

        # 탕비실 전용 상품 추천 (식음료만)
        pantry_recommendation_1 = get_recommendations(goods, pantry_only=True)
        pantry_recommendation_2 = get_recommendations(goods, pantry_only=True)

        # 프론트엔드로 전달할 응답 구성
        response = {
            'situation_category': situation_category,
            'headline1': situation_info['headline1'],
            'headline2': situation_info['headline2'],
            'general_recommendation_1': general_recommendation_1,
            'general_recommendation_2': general_recommendation_2,
            'pantry_recommendation_1': pantry_recommendation_1,
            'pantry_recommendation_2': pantry_recommendation_2,
        }

        return JsonResponse(response)

    except ValueError:
        return JsonResponse({'error': 'Invalid situation key format'}, status=400)
    except Exception as e:
        print(f"Error: {str(e)}")  # 로그 출력
        return JsonResponse({'error': str(e)}, status=500)