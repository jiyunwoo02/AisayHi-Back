from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Goods(models.Model):
    goodsKey = models.AutoField(primary_key=True)  # Auto-increment primary key
    ratingCount = models.FloatField(null=True)
    goodsImg = models.CharField(max_length=500)
    ASIN = models.CharField(unique=True, max_length=30)  # Not null
    goodsName = models.CharField(max_length=300)  # Not null
    brand = models.CharField(max_length=50, blank=True, null=True)  # Nullable
    originalPrice = models.IntegerField()  # Not null
    discountedPrice = models.IntegerField()  # Not null
    ratingAvg = models.FloatField(blank=True, null=True) # Nullable
    goodsInfo = models.TextField(blank=True, null=True)  # Nullable
    goodsDesc = models.TextField(blank=True, null=True)  # Nullable
    category1 = models.CharField(max_length=30)
    category2 = models.CharField(max_length=30)
    category3 = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'goods'



class Orders(models.Model):
    orderKey = models.AutoField(primary_key=True)
    userKey = models.IntegerField()
    totalPrice = models.PositiveIntegerField()  # 총 가격
    rdate = models.DateField()  # 주문 날짜
    orderDetKey = models.IntegerField()  # 주문 세부 정보 키
    goodsKey = models.ForeignKey(Goods, on_delete=models.CASCADE, db_column='goodsKey')  # 상품 외래 키
    price = models.PositiveIntegerField()  # 개별 가격
    cnt = models.PositiveIntegerField()  # 수량

    class Meta:
        managed = False
        db_table = 'orders'


class SituationCategory(models.Model):
    situationCateKey = models.AutoField(primary_key=True)  # 카테고리 키
    situationCategory1 = models.CharField(max_length=30)  # 카테고리 1
    situationCategory2 = models.CharField(max_length=30)  # 카테고리 2
    situationCategory3 = models.CharField(max_length=30)  # 카테고리 3

    class Meta:
        managed = False
        db_table = 'situationCategory'


class Situation(models.Model):
    situationKey = models.AutoField(primary_key=True)
    situationCateKey = models.ForeignKey(SituationCategory, on_delete=models.CASCADE, db_column='situationCateKey')  # 상황 카테고리 외래 키
    headline1 = models.CharField(max_length=50)
    headline2 = models.CharField(max_length=50)
    mainKeyword = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'situation'


class SituationKeyword(models.Model):
    situationKwKey = models.AutoField(primary_key=True)  # 키워드 키
    situationKey = models.ForeignKey(Situation, on_delete=models.CASCADE, db_column='SituationKeyword')  # 상황 외래키
    situationKeyword = models.CharField(max_length=30)  # 키워드

    class Meta:
        managed = False
        db_table = 'situationKeyword'

class goodsKeyword(models.Model):
    goodsKwKey = models.AutoField(primary_key=True)
    ASIN = models.ForeignKey(Goods, on_delete=models.CASCADE, db_column='ASIN')
    goodsKeyword = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'goodsKeyword'


# UserManager 클래스: 사용자 생성 및 슈퍼유저 생성을 위한 메서드 정의
class UserManager(BaseUserManager):
    # 일반 사용자 생성 메서드
    def create_user(self, login_id, username, userpwd, **extra_fields):
        if not login_id:
            raise ValueError('The Login ID must be set')  # 로그인 ID가 없으면 - 에러 발생
        user = self.model(login_id=login_id, username=username, **extra_fields)  # 사용자 인스턴스 생성
        user.userpwd = make_password(userpwd)  # 비밀번호 해시화
        user.save(using=self._db)  # 데이터베이스에 저장
        return user

    # 슈퍼유저 생성 메서드
    def create_superuser(self, login_id, username, userpwd, **extra_fields):
        extra_fields.setdefault('is_superuser', True)  # 기본 값으로 is_superuser를 True로 설정
        extra_fields.setdefault('is_staff', True)  # 기본 값으로 is_staff를 True로 설정

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')  # is_superuser가 True가 아니면 - 에러 발생
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')  # is_staff가 True가 아니면 - 에러 발생

        return self.create_user(login_id, username, userpwd, **extra_fields)  # 일반 사용자 생성 메서드 호출

# User 클래스: 사용자 모델 정의
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    login_id = models.CharField(unique=True, max_length=50)
    username = models.CharField(max_length=20)
    userpwd = models.CharField(max_length=128)

    # 필수 필드들
    is_staff = models.BooleanField(default=False)  # 직원 여부 필드
    is_active = models.BooleanField(default=True)  # 활성 사용자 여부 필드
    date_joined = models.DateTimeField(default=timezone.now)  # 가입 날짜 필드

    # 그룹과의 관계 설정, 충돌을 피하기 위해 related_name과 related_query_name 설정
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set', # ForeignKey 조회 관련 문제 해결!
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    USERNAME_FIELD = 'login_id'  # 사용자 모델에서 유일한 식별자로 사용할 필드
    REQUIRED_FIELDS = ['username']  # 사용자 생성 시 반드시 필요한 필드

    objects = UserManager()  # UserManager를 사용자 모델의 매니저로 설정

    # 사용자 인스턴스 저장 메서드 오버라이드
    # Override: 부모 클래스가 정의한 함수를 덮어씌워 다시 정의하여 사용
    def save(self, *args, **kwargs):
        if not self.pk:
            self.userpwd = make_password(self.userpwd)  # 비밀번호 해시화
        super().save(*args, **kwargs)  # 부모 클래스의 save 메서드 호출

    # 비밀번호 확인 메서드
    def check_password(self, raw_password):
        return check_password(raw_password, self.userpwd)  # 비밀번호 일치 여부 확인

    class Meta:
        managed = False
        db_table = 'user'
