from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
  path("", views.staff_home_view, name="home"),
  path("customers/", views.unit_customers, name="unit_customers"),
  path("customer-details/<int:pk>/", views.customer_view, name="customer_detail"),
  path("purchase-description/<slug>/", views.purchase_description, name="purchase_description"),
  path("add-purchase/", views.add_customer_good , name="add_purchase"),
  path("add-new-customer/", views.add_new_customer , name="add_new_customer"),
  path("send-customer-message/", views.send_customer_message , name="send_customer_message"),
  path("customer-feedbacks/", views.customer_feedback, name="customer_feedbacks"),
  path("read-feedback/<int:pk>/", views.read_feedback, name="read_feedback")
]