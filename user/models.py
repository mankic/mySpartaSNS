#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser  # 장고에서 제공하는 기본 유저 모델. auth_user 테이블과 연결
from django.conf import settings

# Create your models here.
class UserModel(AbstractUser):      # 상속
    class Meta:     # db table의 이름을 정해준다.(정보를 넣어준다)
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')  # 기본 모델에는 bio 없어서 추가해줌
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')
