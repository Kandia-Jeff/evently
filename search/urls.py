from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_events, name='search'),
    path('matched/', views.matched_events, name='matched'),
]