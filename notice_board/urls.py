from django.urls import path
from . import views


urlpatterns = [
    path('', views.notice_list),
    path('notice_list/', views.PostList.as_view()),
    path('notice_list/<int:pk>/', views.PostDetail.as_view()),
    path('notice_list/category/<str:slug>/', views.categories_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('notice_list/<int:pk>/addcomment/', views.addComment)

]

