from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Goods, Orders, Situation, User, Detail

# Register your models here
admin.site.register(Goods)
admin.site.register(Orders)
admin.site.register(Situation)
admin.site.register(Detail)

class CustomUserAdmin(BaseUserAdmin):
    model = User

    fieldsets = (
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
    list_display = ('login_id', 'username', 'is_staff', 'is_superuser')
    search_fields = ('login_id', 'username')
    ordering = ('login_id',)

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
