from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.FeedView.as_view(), name='api-feed'),
]
