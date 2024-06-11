
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User


# 간단한 인덱스 뷰
def index(request):
    return JsonResponse({'message': 'Welcome to the API'})


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