from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .forms import CommentForm
from .models import Post, Category, Tag


def addComment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())

    else:
        raise PermissionDenied


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_msg', 'content', 'head_image', 'attached_file', 'category', 'tags']

    template_name = "notice_board/post_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_msg', 'content', 'head_image', 'attached_file', 'category', 'tags']

    def test_func(self):
        return self.request.user.is_authenticated

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/notice_board/')


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


def categories_page(request, slug):
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'categories': Category.objects.all(),
        'count_posts_without_category': Post.objects.filter(category=None).count(),
        'category': category,
        'post_list': post_list
    }

    return render(request, 'notice_board/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'categories': Category.objects.all(),
        'count_posts_without_category': Post.objects.filter(category=None).count(),
        'tag': tag,
        'post_list': post_list
    }
    return render(request, 'notice_board/post_list.html', context)


def notice_list(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'notice_board/notice_list.html',
        {
            'posts': posts,
            'categories': Category.objects.all(),
            'count_posts_without_category': Post.objects.filter(category=None).count()
        }
    )
