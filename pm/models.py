# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# MySQL DB와 연동하여 생성
# python manage.py inspectdb > models.py 와 추가 작성 코드

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


class Detail(models.Model):
    situation = models.ForeignKey('Situation', models.DO_NOTHING)
    detail = models.CharField(max_length=150)
    detail_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'detail'



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
    goods_id = models.AutoField(primary_key=True)
    goodsname = models.CharField(db_column='goodsName', max_length=30)
    category = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    goodsdesc = models.CharField(db_column='goodsDesc', max_length=150, blank=True, null=True)
    goodsimg = models.TextField(db_column='goodsImg', blank=True, null=True)
    price = models.IntegerField()
    discountprice = models.IntegerField(db_column='discountPrice', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods'


class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    # ForeignKey로 연결된 외래 키 필드는 해당 객체로 자동 변환된다
    # -- 따라서 user_id라는 이름 대신에 user라는 필드명으로 변환
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item_id = models.IntegerField()
    itemcnt = models.IntegerField(db_column='itemCnt')
    itemprice = models.IntegerField(db_column='itemPrice')
    totalprice = models.IntegerField(db_column='totalPrice')

    class Meta:
        managed = False
        db_table = 'orders'


class Situation(models.Model):
    situation_id = models.AutoField(primary_key=True)
    situationcategory = models.CharField(db_column='situationCategory', max_length=50)
    situation = models.CharField(max_length=30)
    keyword = models.CharField(max_length=30)
    headline = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'situation'

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
        managed = True
        db_table = 'user'

    # 기본 값으로 비밀번호 필드 추가
    password = models.CharField(max_length=128, default=make_password('default_password'))