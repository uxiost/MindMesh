# urls.py
from django.urls import path
from .views import ai_profile, post_message, follow_ai, ai_feed

app_name = 'ai_models'

urlpatterns = [
    path('ai/<int:ai_id>/', ai_profile, name='ai_profile'),
    path('ai/<int:ai_id>/post', post_message, name='post_message'),
    path('ai/<int:ai_id>/follow', follow_ai, name='follow_ai'),
    path('', ai_feed, name='ai_feed'),
]
