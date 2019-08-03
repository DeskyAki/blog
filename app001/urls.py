from django.urls import path, re_path
from app001 import views

urlpatterns = [
    re_path(r'/backend/add_article/', views.add_article),
    re_path(r'/comment/', views.comment),
    re_path(r'/comment_tree/(\d+)/', views.comment_tree),
    re_path(r'/up_down/', views.up_down),
    re_path(r'(\w+)/(tag|category|archive)/(.+)', views.home),
    re_path(r'(\w+)/article/(\d+)/$', views.article_detail),
    re_path(r'(\w+)', views.home),       # home （request,username)或者 re_path(r'?P<username>\w+)', views.home)
]