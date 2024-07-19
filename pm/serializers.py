from rest_framework import serializers
from .models import User
from .models import Goods
from .models import Orders

# Serializer: 데이터 직렬화
# -- python 객체나 django에서 queryset 등 복잡한 객체들을 REST API에서 사용 가능하게 json 형태로 변환

# 회원가입 API
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login_id', 'username', 'userpwd']

# 제품 관련 API (등록/제거/조회/갱신)
class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'

# 주문등록 API
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'