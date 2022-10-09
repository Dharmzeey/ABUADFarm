from django.urls import path
from . import views


app_name = "administrator"

urlpatterns = [
  path("", views.home, name="home"),
  path("sales/", views.sales, name="sales"),
  path('login/', views.admin_login, name="login"),
  path('logout/', views.admin_logout, name="logout"),
  path('customers/', views.all_customers, name="customers"),
  path('customer/<int:pk>', views.customer_detail, name="customer_detail"),
  path("purchase-description/<slug>/", views.purchase_description, name="purchase_description"),
  path("feedbacks", views.feedbacks, name='feedbacks'),
  
  # HERE ARE THE URL THAT WILL BE ACCESSED WITH AJAX
  path("customer-chart/", views.customer_chart, name="customer_chart"),
  path("home-chart", views.home_chart, name="home_chart")
  
]
