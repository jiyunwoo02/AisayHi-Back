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





import os
import pandas as pd
import ast
import random
from django.conf import settings
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CSV 파일 경로 설정
CSV_DIR = os.path.join(settings.BASE_DIR, 'pm/data/')

# CSV 데이터 로드
goods = pd.read_csv(os.path.join(CSV_DIR, 'goods.csv'), encoding='utf-8-sig')
goodsKeyword = pd.read_csv(os.path.join(CSV_DIR, 'goodsKeyword.csv'), encoding='utf-8-sig')
situation = pd.read_csv(os.path.join(CSV_DIR, 'situation.csv'), encoding='utf-8-sig')
situationCategory = pd.read_csv(os.path.join(CSV_DIR, 'situationCategory.csv'), encoding='utf-8-sig')
situationKeyword = pd.read_csv(os.path.join(CSV_DIR, 'situationKeyword.csv'), encoding='utf-8-sig')

# ASIN을 기준으로 goods와 goodsKeyword 병합
merged_data = pd.merge(goods, goodsKeyword[['ASIN', 'goodsKeyword']], on='ASIN', how='left')

# 안전한 키워드 변환 함수
def safe_literal_eval(value):
    try:
        return ' '.join(ast.literal_eval(value)) if pd.notna(value) else ''
    except (ValueError, SyntaxError):
        return str(value)

# 'goodsKeyword' 열 처리
merged_data['keyword_str'] = merged_data['goodsKeyword'].apply(safe_literal_eval)

# TF-IDF 벡터화
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(merged_data['keyword_str'])

# 추천 섹션 목록 정의
SECTIONS = [
    {"name": "일반 추천", "categories": ["식음료"], "exclude": True},
    {"name": "일반 추천 2", "categories": ["식음료"], "exclude": True},
    {"name": "탕비실 추천", "categories": ["식음료"], "exclude": False},
    {"name": "탕비실 추천 2", "categories": ["식음료"], "exclude": False},
]

# 상황과 카테고리를 매핑하는 함수
def get_situation_with_category(situation_key):
    situation_row = situation[situation['situationKey'] == situation_key].iloc[0]
    category_row = situationCategory[situationCategory['situationCateKey'] == situation_row['situationCatekey']].iloc[0]

    return {
        'headline1': situation_row['headline1'],
        'headline2': situation_row['headline2'],
        'mainKeyword': situation_row['mainKeyword'],
        'categories': [category_row['situationCategory1'], category_row['situationCategory2']]
    }

# 유사 상품 추천 함수 정의 (12개 추천)
def recommend_products(data, index, num_recommendations=12, category_filter=None):
    cosine_sim = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[::-1][1:num_recommendations + 1]

    if category_filter:
        similar_indices = [
            i for i in similar_indices if data.iloc[i]['category1'] in category_filter
        ]

    recommendations = data.iloc[similar_indices][[
        'goodsKey', 'ASIN', 'goodsName', 'originalPrice',
        'goodsInfo', 'goodsDesc', 'goodsImg'
    ]].copy()
    recommendations['similarity'] = cosine_sim[similar_indices]
    return recommendations

# 섹션별 추천 생성 함수
def generate_section_recommendation(section):
    categories = section["categories"]
    exclude = section["exclude"]

    # 랜덤 인덱스 선택 및 상황 데이터 가져오기
    situation_key = random.choice(situation['situationKey'].unique())
    situation_data = get_situation_with_category(situation_key)

    # 카테고리 필터링 설정
    category_filter = categories if not exclude else merged_data['category1'].unique().tolist()
    if exclude:
        category_filter = [c for c in category_filter if c not in categories]

    # 추천 생성
    index = random.randint(0, len(merged_data) - 1)
    recommendations = recommend_products(merged_data, index, 12, category_filter)

    return {
        'section': section["name"],
        'headline1': situation_data['headline1'],
        'headline2': situation_data['headline2'],
        'mainKeyword': situation_data['mainKeyword'],
        'recommendations': recommendations.to_dict(orient='records')
    }

# 추천 API
def recommend(request):
    # 4개의 섹션에 대해 각각 추천 생성
    recommendations = []
    used_indices = set()  # 중복 방지를 위한 인덱스 추적

    for section in SECTIONS:
        while True:
            section_recommendation = generate_section_recommendation(section)

            # 추천이 비어있지 않고, 인덱스가 중복되지 않으면 추가
            if section_recommendation["recommendations"]:
                index = section_recommendation["recommendations"][0]['goodsKey']
                if index not in used_indices:
                    used_indices.add(index)
                    recommendations.append(section_recommendation)
                    break

    # JSON 응답 반환
    return JsonResponse({
        'recommendations': recommendations
    })