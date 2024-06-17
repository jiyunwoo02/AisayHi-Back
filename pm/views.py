from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from .models import User

# 회원가입 API: 아이디, 이름, 비밀번호
@csrf_exempt
def signup_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            login_id = data.get('login_id')
            username = data.get('username')
            userpwd = data.get('userpwd')

            if not login_id or not username or not userpwd:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # 사용자가 이미 존재하는지 확인해 중복 회원가입 방지
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

            user = authenticate(request, login_id=login_id, password=userpwd)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful',
                                     'user': {
                                         # 로그인 성공시 프론트에 넘길 객체
                                         'login_id': user.login_id,
                                     },
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)
