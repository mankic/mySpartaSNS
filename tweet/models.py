# tweet/models.py
from django.db import models
from user.models import UserModel   # user 폴더에서 models 파일의 UserModel 사용
from taggit.managers import TaggableManager


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    # ForeignKey : 다른 데이터베이스에서 가져옴
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
