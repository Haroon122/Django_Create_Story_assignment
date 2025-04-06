from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='story_list'),
    path('create/', views.StoryCreateView.as_view(), name='story_create'),
    path('<int:pk>/', views.StoryDetailView.as_view(), name='story_detail'),
    path('<int:story_pk>/chapter/create/', views.ChapterCreateView.as_view(), name='chapter_create'),
    path('chapter/<int:pk>/', views.ChapterDetailView.as_view(), name='chapter_detail'),
    path('chapter/<int:pk>/vote/', views.vote_chapter, name='vote_chapter'),
    path('chapter/<int:pk>/approve/', views.approve_chapter, name='approve_chapter'),
    path('chapter/<int:pk>/reject/', views.reject_chapter, name='reject_chapter'),
] 