from django.contrib import admin
from .models import Article
from .models import Comment, Fish

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Fish)
