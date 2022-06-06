from django.shortcuts import render

# Create your views here.
from notice_board.models import Category, Post


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )


def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {
                      'recent_posts': recent_posts,
                      'categories': Category.objects.all(),
                      'count_posts_without_category': Post.objects.filter(category=None).count(),

                  })