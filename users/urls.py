from django.urls import path
from . import views


urlpatterns = [
    path("u/", views.profile_update_view, name="profile-view"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("messages/", views.messages, name="messages"),
    path("read-message/", views.read_message, name="read-message"),
    path("chart/", views.chart, name="chart"),
]
