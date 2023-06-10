from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# 게시판
def index(request):
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

# 댓글 수정
@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('noviceAngler:detail', question_id=comment.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('noviceAngler:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'noviceAngler/comment_form.html', context)

# 댓글 삭제
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
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.create_date = timezone.now()
            article.save()
            return redirect('noviceAngler:index')
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
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.modify_date = timezone.now() 
            article.save()
            return redirect('noviceAngler:detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    context = {'form': form}
    return render(request, 'noviceAngler/article_form.html', context)

# 게시글 삭제 (로그인 필요)
@login_required(login_url='common:login')
def article_delete(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user != article.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('noviceAngler:detail', article_id=article.id)
    article.delete()
    return redirect('noviceAngler:index')