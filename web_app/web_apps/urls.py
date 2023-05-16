"""url patterns for web_apps app"""

from django.urls import path
from . import views

app_name = "web_apps"
urlpatterns = [
    # homepage
    path("", views.index, name="index"),
    path("topics/", views.topics, name="topics"),
    path("topics/<int:topic_id>/", views.topic, name="topic")

]
