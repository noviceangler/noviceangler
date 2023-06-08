from django.db import models

class Fish(models.Model):
    fish_name = models.CharField(max_length=32)
    description = models.TextField()
    information = models.TextField()
    habitat = models.TextField()
    notice = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d')
    season = models.CharField(max_length=32)