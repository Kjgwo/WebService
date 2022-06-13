import os.path
from turtle import mode
from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/notice_board/tag/{self.slug}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # unique=True 유일한 값을 가져야함
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # SlugField는 한글을 허용하지 않으나, allow=True를 설정하면 한글 사용 가능

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/notice_board/notice_list/category/{self.slug}'

    class Meta:
        verbose_name_plural: 'categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()

    hook_msg = models.TextField(blank=True)

    head_image = models.ImageField(upload_to='notice_board/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='notice_board/files/%Y/%m/%d/', blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/notice_board/notice_list/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

    def get_markdown_content(self):
        return markdown(self.content)


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'