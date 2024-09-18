# Serializer: 데이터 직렬화
# -- python 객체나 django에서 queryset 등 복잡한 객체들을 REST API에서 사용 가능하게 json 형태로 변환

from rest_framework import serializers
from .models import User, Goods

# 회원가입 API
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login_id', 'username', 'userpwd']

# 제품 정보 제공 API: 제품 데이터를 JSON 형식으로 직렬화
class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['goods_id', 'goodsname', 'category', 'brand', 'goodsdesc', 'goodsimg', 'price', 'discountprice']
