from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Goods, Orders, Situation, User, SituationCategory, SituationKeyword

# admin 사이트에 DB 테이블 등록
admin.site.register(Goods)
admin.site.register(Orders)
admin.site.register(Situation)
admin.site.register(SituationCategory)
admin.site.register(SituationKeyword)

class CustomUserAdmin(BaseUserAdmin):
    model = User

    fieldsets = (
        # is_staff 필드 (일반 사용자 vs 관리자)
        # : Django의 사용자 모델에서 특정 사용자가 관리자 사이트에 접근할 수 있는지 여부를 나타내는 Boolean 필드

        # is_superuser 필드 (최상위 관리자 계정을 식별 -> 모든 권한 부여)
        # : Django의 사용자 모델에서 특정 사용자가 모든 권한을 가지는지를 나타내는 Boolean 필드

        (None, {'fields': ('login_id', 'username', 'password')}),
        (_('Personal info'), {'fields': ('date_joined', 'last_login')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login_id', 'username', 'password1', 'password2'),
        }),
    )

    list_display = ('login_id', 'username', 'is_staff', 'is_superuser') # 4가지 시각화
    search_fields = ('login_id', 'username') # 아이디와 사용자명 서치
    ordering = ('login_id',) # 아이디 기본 정렬

admin.site.register(User, CustomUserAdmin)