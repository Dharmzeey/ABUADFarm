from django.urls import path
from . import views


app_name = "administrator"

urlpatterns = [
  path("", views.admin_view, name="home"),
  path('login/', views.admin_login, name="login"),
  path('logout/', views.admin_logout, name="logout"),
  path('customers/', views.all_customers, name="customers"),
  path('customer/<int:pk>', views.customer_detail, name="customer_detail"),
  path("purchase-description/<int:pk>/", views.purchase_description, name="purchase_description"),
  
]
