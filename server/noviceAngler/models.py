from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to="", blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()

class UserSubmission(models.Model):
   fish = models.CharField(max_length=20, blank=False)
   fishing = models.CharField(max_length=20, blank=False)
   locate = models.CharField(max_length=20, blank=False)
   hour = models.CharField(max_length=20, blank=False)
   month = models.CharField(max_length=20, blank=False)
