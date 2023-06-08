from django.urls import path
from . import views

app_name = 'noviceAngler'

urlpatterns = [
  path("", views.main_page, name="main_page"),
  path("point_recommendation/", views.point_recommendation, name="point_recommendation"),
  path("point_recommendation/question/", views.point_recommendation_question, name="point_recommendation_question"),
  path("point_recommendation/result/", views.point_recommendation_result, name="point_recommendation_result"),
  path("find_fish/", views.find_fish, name="find_fish"),
  path("fish_information/", views.fish_information, name="fish_information"),
]