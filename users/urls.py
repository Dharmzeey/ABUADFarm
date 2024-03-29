from django.urls import path
from . import views


urlpatterns = [
    path("u/", views.profile_update_view, name="profile_view"),
    path("ajax/load-data/", views.load_data, name="ajax_load_data"),
    
    path("dashboard/", views.dashboard, name="dashboard"),
    path("messages/", views.user_messages, name="messages"),
    path("read-message/", views.read_message, name="read_message"),
    path("notifications/", views.notifications, name="notifications"),
    path("purchase-description/<slug>/", views.purchase_description, name="purchase_description"),
    # URL FOR CHART
    path("chart/", views.chart, name="chart"),
]
