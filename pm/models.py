# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

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


class UserManager(BaseUserManager):
    def create_user(self, login_id, username, userpwd, **extra_fields):
        if not login_id:
            raise ValueError('The Login ID must be set')
        user = self.model(login_id=login_id, username=username, **extra_fields)
        user.userpwd = make_password(userpwd)
        user.set_password(userpwd)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, username, userpwd, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(login_id, username, userpwd, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    login_id = models.CharField(unique=True, max_length=50)
    username = models.CharField(max_length=20)
    userpwd = models.CharField(max_length=128)

    # Required fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.userpwd = make_password(self.userpwd) # 비밀번호 해시화
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.userpwd)

    class Meta:
        managed = True
        db_table = 'user'

    # Add password field with a default value
    password = models.CharField(max_length=128, default=make_password('default_password'))