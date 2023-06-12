from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from .image_classify import load_model, image_processing, resize_image
from .models import Fish, Article, Comment, UserSubmission
from .forms import ArticleForm, CommentForm
from PIL import Image
import numpy as np
import pandas as pd
import os
import tensorflow as tf

def main_page(request, *args, **kwargs):
    return render(request, 'noviceAngler/main_page.html')

def point_recommendation(request, *args, **kwargs):
    return render(request, 'noviceAngler/point_recommendation.html')

# 낚시 포인트 추천 질문
def point_recommendation_question(request, *args, **kwargs):
    if request.method == 'POST':
        preferred_fish = request.POST.get('fish')
        preferred_fishing = request.POST.get('fishing')
        preferred_locate = request.POST.get('locate')
        preferred_hour = request.POST.get('hour')
        preferred_month = request.POST.get('month')
        
        submission = UserSubmission(fish=preferred_fish, locate=preferred_locate, fishing=preferred_fishing, hour=preferred_hour, month=preferred_month)
        submission.save()
        
        request.session['submission_id'] = submission.id
        return redirect('noviceAngler:point_recommendation_result')
    return render(request, 'noviceAngler/point_recommendation_question.html')

# 낚시 포인트 추천 코드
def find_recommendation_point(preferred_fish, preferred_fishing, preferred_locate, preferred_month, preferred_hour):
    file_path = os.path.join(settings.BASE_DIR, 'static', '포인트_추천_데이터.xlsx')
    blog_data = pd.read_excel(file_path)
    matched_points = []

    for index, row in blog_data.iterrows():
        frequency = 0
        if row['fish'] == preferred_fish:
            frequency += 1
        elif row['fishing'] == preferred_fishing:
            frequency += 1
        elif row['locate'] == preferred_locate:
            frequency += 1
        elif row['month'] == preferred_month:
            frequency += 1
        elif row['hour'] == preferred_hour:
            frequency += 1

        matched_points.append((row['point'], frequency))
    print(matched_points)

    if matched_points:
        max_frequency = max(matched_points, key=lambda x: x[1])[1]
        highest_frequency_points = [point[0] for point in matched_points if point[1] == max_frequency]

        priority = ['fish', 'locate', 'fishing', 'month', 'hour']
        recommended_point = None

        for point in highest_frequency_points:
            recommend = True
            for attr in priority:
                if row[attr] != eval(f"preferred_{attr}") and eval(f"preferred_{attr}") != '':
                    recommend = False
                    break
                if recommend:
                    recommended_point = point
                    break
        
        print(recommended_point)
        return recommended_point
    else:
        return None

# 낚시 포인트 추천 결과
def point_recommendation_result(request, *args, **kwargs):
    submission_id = request.session.get('submission_id')
    submission = UserSubmission.objects.get(id=submission_id) if submission_id else None
    fish_mapping = {
        'hairtail': '갈치',
        'mackerel': '고등어',
        'mullet': '숭어',
        'red_snapper': '참돔',
        'rockfish': '우럭',
        'flatfish': '광어',
        'no_matter': '상관없음',
    }
    locate_mapping = {
        'south_west': '남해서부',
        'south_central': '남해중부',
        'south_east': '남해동부',
        'east_south': '동해남부',
        'east_north': '동해북부',
        'west_north': '서해북부',
        'west_south': '서해남부',
        'no_matter': '상관없음',
    }
    hour_mapping = {
        '6to12': '오전6시~정오12시',
        '12to18': '정오12시~오후18시',
        '18to21': '오후18시~자정12시',
        '0to6': '자정12시~오전6시',
        'no_matter': '상관없음',
    }
    month_mapping = {
        '1': '1월',
        '2': '2월',
        '3': '3월',
        '4': '4월',
        '5': '5월',
        '6': '6월',
        '7': '7월',
        '8': '8월',
        '9': '9월',
        '10': '10월',
        '11': '11월',
        '12': '12월',
        'no_matter': '상관없음',
    }
    fishing_mapping = {
        'float': '찌낚시',
        'one-two': '원투낚시',
        'lure': '루어낚시',
        'boat': '선상낚시',
        'no_matter': '상관없음',
    }

    preferred_fish = fish_mapping.get(submission.fish, submission.fish)
    preferred_locate = locate_mapping.get(submission.locate, submission.locate)
    preferred_hour = hour_mapping.get(submission.hour, submission.hour)
    preferred_month = month_mapping.get(submission.month, submission.month)
    preferred_fishing = fishing_mapping.get(submission.fishing, submission.fishing)

    recommended_point = find_recommendation_point(preferred_fish, preferred_fishing, preferred_locate, preferred_hour, preferred_month)
    
    context = {
        'submission':submission, 
        'preferred_fish':preferred_fish,
        'preferred_locate': preferred_locate,
        'preferred_hour': preferred_hour,
        'preferred_month': preferred_month,
        'preferred_fishing': preferred_fishing,
        'recommended_point': recommended_point,
        }
    return render(request, 'noviceAngler/point_recommendation_result.html', context)

def fish_information(request, pk, *args, **kwargs):
    fish = Fish.objects.get(id=pk)
    return render(request, 'noviceAngler/fish_information.html', {'fish': fish})

def find_fish_page(request, *args, **kwargs):
    return render(request, 'noviceAngler/find_fish.html')
# def find_fish(request):
#     predicted_class = None
#     print(request.method, request.FILES['photo'])
#     if request.method == "POST" and request.FILES['photo']:
#         model = load_model()
#         uploaded_image = request.FILES['photo']
#         img = Image.open(uploaded_image)
#         img = img.resize((100, 100))
#         img = np.array(img)
#         img = img / 255.0
#         img = np.expand_dims(img, axis=0)
#         prediction = model.predict(img)
#         predicted_class_index = np.argmax(prediction)
#         fish_classes = ['갈치', '고등어', '숭어', '광어', '우럭', '참돔']
#         predicted_class = fish_classes[predicted_class_index]
#     return render(request, "noviceAngler/fish_information.html", {'fish': predicted_class})
        
def find_fish(request):
    if request.method == 'POST':
        fish = Fish.objects.get(fish_name='고등어')
        return render(request, "noviceAngler/fish_information.html", {'fish': fish})

# 게시판
def community(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    article_list = Article.objects.order_by('-create_date')
    if kw:
        article_list = article_list.filter(
            Q(subject__icontains=kw) | 
            Q(content__icontains=kw) |  
            Q(comment__content__icontains=kw) |  
            Q(author__username__icontains=kw) | 
            Q(comment__author__username__icontains=kw) 
        ).distinct()
    paginator = Paginator(article_list, 10)
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj}
    return render(request, 'noviceAngler/article_list.html', context)

# 게시물 상세
def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'noviceAngler/article_detail.html', context)

# 댓글 추가 (로그인 필요)
@login_required(login_url='common:login')
def comment_create(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.article = article
            comment.save()
            return redirect('noviceAngler:detail', article_id=article.id)
    else:
        form = CommentForm()
    context = {'article': article, 'form': form}
    return render(request, 'noviceAngler/article_detail.html', context)

# 댓글 수정 (로그인 필요)
@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('noviceAngler:detail', article_id=comment.article.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('noviceAngler:detail', article_id=comment.article.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'noviceAngler/comment_form.html', context)

# 댓글 삭제 (로그인 필요)
@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('noviceAngler:detail', article_id=comment.article.id)

# 게시글 추가 (로그인 필요)
@login_required(login_url='common:login')
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.create_date = timezone.now()
            article.save()
            return redirect('noviceAngler:community')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'noviceAngler/article_form.html', context)

# 게시글 수정 (로그인 필요)
@login_required(login_url='common:login')
def article_modify(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('noviceAngler:detail', article_id=article.id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.modify_date = timezone.now() 
            article.save()
            return redirect('noviceAngler:detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form, 'article':article}
    return render(request, 'noviceAngler/article_form.html', context)

# 게시글 삭제 (로그인 필요)
@login_required(login_url='common:login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('noviceAngler:detail', article_id=article.id)
    article.delete()
    return redirect('noviceAngler:community')

