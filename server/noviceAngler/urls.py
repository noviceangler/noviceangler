from django.urls import path
from . import views

app_name = 'noviceAngler'

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path('community/<int:article_id>/', views.detail, name='detail'),
    path('community/', views.community, name="community"),
    path('community/comment/create/<int:article_id>/', views.comment_create, name='comment_create'),
    path('community/article/create/', views.article_create, name="article_create"),
    path('community/article/modify/<int:article_id>/', views.article_modify, name='article_modify'),
    path('community/article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('community/comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('community/comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('point_recommendation/', views.point_recommendation, name='point_recommendation'),
    path("point_recommendation/question/", views.point_recommendation_question, name="point_recommendation_question"),
    path("point_recommendation/result/", views.point_recommendation_result, name="point_recommendation_result"),
    path("fish_information/", views.fish_information, name="fish_information"),
]