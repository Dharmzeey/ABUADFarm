from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
  path('', views.news, name='news'),
  path('news-details/<slug>/', views.news_details, name='news_details'),
  path('create-news/', views.create_news, name='create_news'),
  path('update-news/<slug>/', views.update_news, name='update_news'),
  path('delete-news/<slug>/', views.delete_news, name='delete_news'),
]