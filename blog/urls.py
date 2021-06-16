from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/item/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/item/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/item/<slug:slug>/publish/', views.post_publish, name='post_publish'),
    path('post/item/<slug:slug>/unpublish/', views.post_unpublish, name='post_unpublish'),
    path('post/item/<slug:slug>/remove/', views.post_remove, name='post_remove'),
    path('post/draft-list/', views.post_draft_list, name='post_draft_list'),
]
