from django.contrib import admin
from .models import UserModel   # 현재 폴더에서 models 파일의 UserModel 임포트

# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다