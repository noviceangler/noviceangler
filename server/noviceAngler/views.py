from django.shortcuts import render

# Create your views here.


def main_page(request, *args, **kwargs):
  return render(request, 'noviceAngler/main_page.html')
  
def point_recommendation(request, *args, **kwargs):
  return render(request, 'noviceAngler/point_recommendation.html')
  
def point_recommendation_question(request, *args, **kwargs):
  return render(request, 'noviceAngler/point_recommendation_question.html')
  
def point_recommendation_result(request, *args, **kwargs):
  return render(request, 'noviceAngler/point_recommendation_result.html')
  
def fish_information(request, *args, **kwargs):
  return render(request, 'noviceAngler/fish_information.html')
  