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

def find_fish_page(request, *args, **kwargs):
  return render(request, 'noviceAngler/find_fish.html')

def find_fish(request):
  if request.method == "POST":
    user_image = request.FILES['photo']
    print(user_image)
    return redirect("/")
  return render(request, "noviceAngler/point_recommendation_result.html")

  
  
  
  
# def point_result(request, *args, **kwargs):
  if request.method == "POST":
    match_form = MatchRegisterForm(request.POST, request.FILES)
    if match_form.is_valid() and request.recaptcha_is_valid:
      match = match_form.save(commit=False)
      match.host_id = request.user
      match.save()
      # 만들어진 페이지로 이동
      return redirect("matchingMatch:match_detail", pk=match.pk)
    else:
      print(match_form.errors)
      stadium_name = Stadium.objects.order_by('stadium_name')
      stadium_name_list = stadium_name
      context = {"match_form": match_form, "stadium_name": stadium_name,
                  "stadium_name_list": stadium_name_list, }
      return render(request, "matchingMatch/match_register.html", context=context)