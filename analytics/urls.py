from django.urls import path
from . import views

urlpatterns = [
    path('organiser/', views.organiser_analytics_view, name='organiser_analytics'),
    path('admin/', views.admin_analytics_view, name='admin_analytics'),
]