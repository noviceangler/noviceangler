from django.db import models
from django.contrib.auth.models import User

class Fish(models.Model):
    fish_name = models.CharField(max_length=32)
    float_fishing = models.TextField(blank=True, null=True)
    lure_fishing = models.TextField(blank=True, null=True)
    onetwo_fishing = models.TextField(blank=True, null=True)
    locations = models.TextField()
    notices = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d')
    season = models.CharField(max_length=32)
    
    def __str__(self):
        return self.fish_name
    
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
