from django.urls import path
from . import views


app_name = "administrator"

urlpatterns = [
  path("", views.admin_view, name="home"),
  path('login/', views.admin_login, name="login"),
  path('logout/', views.admin_logout, name="logout"),
  
  # STAFF
  path("staff/", views.staff_home_view, name="staff-home"),
  path("customers/", views.unit_customers, name="unit-customers"),
  path("customer-details/<int:pk>/", views.customer_view, name="customer-detail"),
  path("add-purchase/", views.add_customer_good , name="add-purchase"),
  path("add-new-customer/", views.add_new_customer , name="add-new-customer"),
]
