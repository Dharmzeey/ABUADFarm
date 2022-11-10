from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
  path('', views.blog, name='blogs'),
  path('blog/<slug>/', views.blog_details, name='blog_details'),
  path('create-blog/', views.create_blog, name='create_blog'),
  path('update-blog/<slug>/', views.update_blog, name='update_blog'),
  path('delete-blog/<slug>/', views.delete_blog, name='delete_blog'),
]