from django.urls import path
from . import views


urlpatterns = [
    path("u/", views.profile_update_view, name="profile_view"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("messages/", views.user_messages, name="messages"),
    path("read-message/", views.read_message, name="read_message"),
    path("chart/", views.chart, name="chart"),
]
