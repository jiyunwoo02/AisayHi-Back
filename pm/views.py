from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets, filters


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


from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend


# 추천
import os
import pandas as pd
import ast
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



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


# 추천

# CSV 파일 경로 설정
CSV_DIR = os.path.join(settings.BASE_DIR, 'pm/data/')

# CSV 데이터 로드
goods = pd.read_csv(os.path.join(CSV_DIR, 'goods.csv'), encoding='utf-8-sig')
goodsKeyword = pd.read_csv(os.path.join(CSV_DIR, 'goodsKeyword.csv'), encoding='utf-8-sig')
situation = pd.read_csv(os.path.join(CSV_DIR, 'situation.csv'), encoding='utf-8-sig')
situationCategory = pd.read_csv(os.path.join(CSV_DIR, 'situationCategory.csv'), encoding='utf-8-sig')
situationKeyword = pd.read_csv(os.path.join(CSV_DIR, 'situationKeyword.csv'), encoding='utf-8-sig')

# ASIN 기준으로 goods와 goodsKeyword 병합
merged_data = pd.merge(goods, goodsKeyword[['ASIN', 'goodsKeyword']], on='ASIN', how='left')

# 안전한 키워드 처리 함수
def safe_literal_eval(value):
    try:
        return ' '.join(ast.literal_eval(value)) if pd.notna(value) else ''
    except (ValueError, SyntaxError):
        return str(value)

merged_data['keyword_str'] = merged_data['goodsKeyword'].apply(safe_literal_eval)

# TF-IDF 벡터화
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(merged_data['keyword_str'])

# 섹션 정의와 상황 키 매핑
SECTIONS = [
    {"name": "일반 섹션 1", "categories": ['사무용품', '사무실 꾸미기', '직장 생활'], "situationKeys": [17, 18, 19]},
    {"name": "일반 섹션 2", "categories": ['사무용품', '사무실 꾸미기', '직장 생활'], "situationKeys": [20, 21, 22]},
    {"name": "탕비실 섹션 3", "categories": ['식음료', '탕비실'], "situationKeys": [1, 2, 3]},
    {"name": "탕비실 섹션 4", "categories": ['식음료', '탕비실'], "situationKeys": [4, 5, 6]}
]

# 상황 키를 통해 헤드라인과 키워드를 추출
def get_situation_data(situation_key):
    try:
        row = situation[situation['situationKey'] == situation_key].iloc[0]
        keywords = situationKeyword[situationKeyword['situationKey'] == situation_key]['situationKeyword'].tolist()
        return {
            'headline1': row['headline1'],
            'headline2': row['headline2'],
            'mainKeyword': row['mainKeyword'],
            'keywords': keywords
        }
    except IndexError:
        return None

# 섹션에 맞는 추천을 생성
def generate_section_recommendation(section, used_goods):
    categories = [c.strip().lower() for c in section['categories']]
    situation_keys = section['situationKeys']

    for _ in range(10):  # 최대 10회 시도
        situation_key = random.choice(situation_keys)
        situation_data = get_situation_data(situation_key)

        if not situation_data:
            continue

        # 사용된 상품 제외한 데이터 필터링
        filtered_data = merged_data[
            merged_data['category1'].str.strip().str.lower().isin(categories) &
            (~merged_data['goodsKey'].isin(used_goods))
        ]

        recommendations = recommend_products(filtered_data, used_goods)

        if len(recommendations) == 12:
            # 추천된 상품의 goodsKey를 기록
            used_goods.update([item['goodsKey'] for item in recommendations])

            return {
                'section': section["name"],
                'headline1': situation_data['headline1'],
                'headline2': situation_data['headline2'],
                'mainKeyword': situation_data['mainKeyword'],
                'recommendations': recommendations
            }

    return None

def recommend_products(data, used_goods, num_recommendations=12):
    if data.empty:
        return []

    index = random.choice(data.index)
    cosine_sim = cosine_similarity(tfidf_matrix[index], tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[::-1][1:num_recommendations + 1]

    # 중복되지 않는 상품만 선택
    similar_indices = [i for i in similar_indices if i in data.index and data.loc[i, 'goodsKey'] not in used_goods]

    # 추천 개수 부족 시 추가 상품 선택
    if len(similar_indices) < num_recommendations:
        additional_indices = list(data.index.difference(similar_indices))
        random.shuffle(additional_indices)
        similar_indices += additional_indices[:num_recommendations - len(similar_indices)]

    recommendations = data.loc[similar_indices][[
        'goodsKey', 'ASIN', 'goodsName', 'originalPrice', 'goodsImg'
    ]].copy()

    recommendations['similarity'] = cosine_sim[similar_indices]

    # DataFrame을 리스트로 변환하여 반환
    return recommendations.to_dict(orient='records')

def recommend(request):
    recommendations = []
    used_goods = set()

    for section in SECTIONS:
        section_recommendation = generate_section_recommendation(section, used_goods)

        if section_recommendation:
            recommendations.append(section_recommendation)

    if not recommendations:
        return JsonResponse({'error': 'No recommendations available'}, status=404)

    return JsonResponse({'recommendations': recommendations})