from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
# from django.contrib.auth import authenticate, login

# 간단한 인덱스 뷰
def index(request):
    return JsonResponse({'message': 'Welcome to the API'})

# 회원가입 API - 아이디, 이름, 비밀번호
    # 2024.06.14
    # 중복 사용자 처리 대해서 논의 필요
    # 그 외 정상 장독 확인 완료
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            login_id = data.get('login_id')
            username = data.get('username')
            userpwd = data.get('userpwd')

            if not login_id or not username or not userpwd:
                return JsonResponse({'error': 'Missing fields'}, status=400)

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

# 로그인 API - 아이디, 비밀번호