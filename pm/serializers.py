from rest_framework import serializers
from .models import User

# 회원가입 API 생성에 필요
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login_id', 'username', 'userpwd']
