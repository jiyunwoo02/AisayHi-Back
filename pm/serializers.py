from rest_framework import serializers
from .models import User

# 회원가입 API 생성에 필요
# Serializer: 데이터 직렬화
# -- python 객체나 django에서 queryset 등 복잡한 객체들을 REST API에서 사용 가능하게 json 형태로 변환
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login_id', 'username', 'userpwd']
