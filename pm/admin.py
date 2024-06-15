from django.contrib import admin
from .models import Goods, Orders, Situation, User, Detail
from .models import DjangoAdminLog

admin.site.register(Goods)
admin.site.register(Orders)
admin.site.register(Situation)
admin.site.register(Detail)
admin.site.register(User)
admin.site.register(DjangoAdminLog)
