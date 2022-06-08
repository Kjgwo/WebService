from django.shortcuts import render

# Create your views here.
from notice_board.models import Category, Post


def all_list(request):
    recent_posts = Post.objects.order_by('-pk')[:15]
    return render(
        request,
        'single_pages/all_list.html',
        {
            'recent_posts': recent_posts,
        }
    )


def landing(request):
    return render(request, 'single_pages/landing.html',
                  {
                      'categories': Category.objects.all(),
                      'count_posts_without_category': Post.objects.filter(category=None).count(),

                  })