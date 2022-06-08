from django.urls import path
from . import views


urlpatterns = [
    path('all_list/', views.all_list),
    path('', views.landing),
]