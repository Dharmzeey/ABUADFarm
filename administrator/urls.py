from django.urls import path
from . import views


app_name = "administrator"

urlpatterns = [
  path("", views.admin_view, name="home"),
  path('login/', views.admin_login, name="login"),
  path('logout/', views.admin_logout, name="logout"),
]
